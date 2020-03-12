import logging
from typing import Optional, List
from datetime import datetime

from streamt_db.user import User
from streamt_db.stream import Stream, Highlight, ClipToHighlight, Clip

logger = logging.getLogger(__name__)


class HighlightManager:
    '''
    Manages business logic for all things stream related.
    '''
    session = None  # DB session

    def __init__(self, db_session):
        self.session = db_session

    def get_user_highlight(self, user: User, highlight_id: int) \
            -> Optional[dict]:
        '''Get highlight object'''
        highlight = list(filter(lambda hilite: hilite.id ==
                                highlight_id, user.highlights))
        if highlight:
            return self._get_highlight_model(highlight[0])
        return None

    def get_user_highlights(self, user: User) -> List[dict]:
        '''
        Get all highlights for a user
        User has Stream(s)
        Stream has Clip(s)
        Highlight has Clip(s)
        '''
        highlights = list(map(lambda hilite: self._get_highlight_model(
            hilite), user.highlights))
        return highlights

    def create_highlight(self, user: User, title=None) -> Highlight:
        '''
        Create a new highlight, for the user.
        '''
        if title is None:
            created_time = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
            title = f'Highlight created {created_time}'
        new_highlight = Highlight(title=title, owner=user)
        self.session.add(new_highlight)
        self.session.commit()
        logger.info('User[id=%d] created new Highlight[id=%d]',
                    user.id, new_highlight.id)
        return new_highlight

    def update_highlight_clips(self, highlight_id: int, clips: List[Clip]):
        '''Update the list of clips that make up a highlight.'''
        self.session.query(ClipToHighlight).filter_by(
            highlight_id=highlight_id).delete()
        for idx, clip in enumerate(clips):
            h_2_c = ClipToHighlight(
                highlight_id=highlight_id, clip=clip, clip_rank=idx)
            self.session.add(h_2_c)
        self.session.commit()

    def _get_highlight_model(self, highlight: Highlight):
        '''Return API safe model for Highlight object'''
        ret: dict = {}
        ret['id'] = highlight.id
        ret['title'] = highlight.title
        ret['created_at'] = int(highlight.created_at.timestamp()) if \
            highlight.created_at else None
        ret['clips'] = list(map(lambda c_2_h: c_2_h.clip_id, highlight.clips))
        return ret
