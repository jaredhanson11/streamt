'''
Api endpoints handling home page info.
'''
import logging

from flask import request, g
from flask_restful import Resource

from streamt_core.account_management import AccountManager
from streamt_core.stream_management import StreamManager
from streamt_core.clip_management import ClipManager
from streamt_core.highlight_management import HighlightManager
from streamt_web import responses

from .. import jwt, db

logger = logging.getLogger(__name__)

account_manager: AccountManager = AccountManager(db.session)
stream_manager: StreamManager = StreamManager(db.session)
clip_manager: ClipManager = ClipManager(db.session)
highlight_manager: HighlightManager = HighlightManager(db.session)


class HomeController(Resource):
    @jwt.requires_auth
    def get(self):
        user = account_manager.get_user(g.user)
        streams = stream_manager.get_user_streams(g.user)
        clips = clip_manager.get_user_clips(g.user)
        highlights = highlight_manager.get_user_highlights(g.user)
        ret = {
            'highlights': highlights,
            'streams': streams,
            'clips': clips,
            'user': user
        }
        return responses.success(ret, 200)
