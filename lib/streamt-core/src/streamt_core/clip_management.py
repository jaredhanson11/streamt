import logging
from typing import Optional, List
from datetime import datetime

from streamt_db.user import User
from streamt_db.stream import Clip

logger = logging.getLogger(__name__)


class ClipManager:
    '''
    Manages business logic for all things stream related.
    '''
    session = None  # DB session

    def __init__(self, db_session):
        self.session = db_session

    def create_clip(self, stream_id: int, name: Optional[str], start: float,
                    end: float) -> Clip:
        '''
        Create a clip for a stream.
        TODO ensure user owns the stream to create the clip
        '''
        if name is None:
            created_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            name = f'Clip created {created_time}'
        new_clip = Clip(name=name, start=start, end=end, stream_id=stream_id)
        self.session.add(new_clip)
        self.session.commit()
        return new_clip

    def update_clip(self, clip_id: int, name: Optional[str], start: float,
                    end: float) -> Clip:
        '''
        Update clip with new values.
        TODO ensure user can edit it
        '''
        clip = self.session.query(Clip).get(clip_id)
        if clip:
            clip.name = name
            clip.start = start
            clip.end = end
            self.session.add(clip)
            self.session.commit()
            return clip
        return None

    def get_user_clip(self, user: User, clip_id: int) -> Optional[dict]:
        '''
        Get clip for user, or none if clip doesn't exist or user doesn't have
        permission to view clip
        '''
        clip = self.session.query(Clip).get(clip_id)
        if clip and clip.stream.user_id == user.id:
            return self._get_clip_model(clip)
        return None

    def get_user_clips(self, user: User) -> List[dict]:
        '''
        Get all clips for a user
        '''
        clips = []
        for stream in user.streams:
            clips.extend(stream.clips)
        return list(map(lambda clip: self._get_clip_model(clip), clips))

    def _get_clip_model(self, clip: Clip):
        '''Return API safe model for Clip object'''
        ret: dict = {}
        ret['id'] = clip.id
        ret['name'] = clip.name
        ret['created_at'] = int(clip.created_at.timestamp()) if \
            clip.created_at else None
        ret['start'] = int(clip.start) if clip.start is not None else None
        ret['end'] = int(clip.end) if clip.end is not None else None
        ret['stream_id'] = int(clip.stream_id)
        return ret
