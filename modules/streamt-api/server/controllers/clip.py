from flask import request, g
from flask_restful import Resource

from streamt_core.clip_management import ClipManager
from streamt_web import responses

from .. import jwt, db

clip_manager: ClipManager = ClipManager(db.session)


class ClipListController(Resource):
    '''/clips API resource'''

    @jwt.requires_auth
    def get(self):
        ret = clip_manager.get_user_clips(g.user)
        return responses.success(ret)

    @jwt.requires_auth
    def post(self):
        post_data = request.get_json()
        stream_id = post_data.get('stream_id')
        name = post_data.get('name')
        start = float(post_data.get('start'))
        end = float(post_data.get('end'))
        ret = clip_manager.create_clip(
            stream_id=stream_id, name=name, start=start, end=end)
        return responses.success(ret, 201)


class ClipController(Resource):
    '''/clips/<id> API resource'''

    @jwt.requires_auth
    def get(self, id):
        clip_json = clip_manager.get_user_clip(g.user, id)
        if clip_json:
            return responses.success(clip_json, 200)
        return responses.client_error('Clip can not be found.', 404)

    @jwt.requires_auth
    def put(self, id):
        pass

    @jwt.requires_auth
    def delete(self, id):
        pass
