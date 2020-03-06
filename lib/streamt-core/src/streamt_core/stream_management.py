import logging
from typing import Optional
from datetime import datetime

from streamt_db.user import User
from streamt_db.stream import Stream

logger = logging.getLogger(__name__)


class StreamManager:
    '''
    Manages business logic for all things stream related.
    '''
    session = None  # DB session

    def __init__(self, db_session):
        self.session = db_session

    def start_stream(self, stream_key) -> Optional[Stream]:
        '''
        Return newly created stream record, or none if shouldn't create new
            stream.
        Can return None for multiple reasons, i.e. stream already live, no user
            associated with the stream_key, etc.
        '''
        user = self.session.query(User).filter_by(stream_key=stream_key)\
            .one_or_none()
        if user:
            logger.debug('User:%d attempting to start stream.', user.id)
            live = [self._is_stream_live(stream) for stream in user.streams]
            if sum(live) > 0:
                # This user already has a live stream
                logger.info('User:%d is already live, can\'t start another \
                            stream.', user.id)
                return None
            else:
                start = datetime.utcnow()
                start_time = start.strftime("%Y%m-%d_%H:%M:%S")
                name = f'Stream starting {start}'
                new_stream = Stream(
                    name=name,
                    created_at=start,
                    user=user
                )
                self.session.add(new_stream)
                self.session.commit()
                logger.info('User:%d starting new stream named:%s.',
                            user.id, user.name)
                return new_stream

    def end_stream(self, stream_id) -> None:
        '''End stream with stream_id'''
        logger.debug('Attempting to stop Stream:%s', stream_id)
        stream: Stream = self.session.query(Stream).get(stream_id)
        if stream and stream.ended_at is None:
            stream.ended_at = datetime.utcnow()
            self.session.add(stream)
            self.session.commit()
            logger.info('Stopped Stream:%s', stream_id)
        elif stream and stream.ended_at is not None:
            logger.warning('Attempted to stop Stream:%s, but it was already \
                stopped.', stream_id)
        else:
            logger.info('Stream:%s does not exist, can\'t stop it', stream_id)

    def _is_stream_live(self, stream: Stream):
        '''Return if stream has been started, and is still live'''
        return stream.ended_at is not None
