from flask import request, g
from flask_restful import Resource

from streamt_core.highlight_management import HighlightManager
from streamt_web import responses

from .. import jwt, db

highlight_manager: HighlightManager = HighlightManager(db.session)


class HighlightListController(Resource):
    '''/hightlights API resource'''

    @jwt.requires_auth
    def get(self):
        return responses.success(highlight_manager.get_user_highlights(g.user))

    @jwt.requires_auth
    def post(self):
        post_data = request.get_json()
        name = post_data.get('name')
        new_highlight = highlight_manager.create_highlight(g.user, name=name)
        return responses.success(new_highlight, 204)


class HighlightController(Resource):
    '''/higlights/<id> API resource'''

    @jwt.requires_auth
    def get(self, id):
        highlight = highlight_manager.get_user_highlight(g.user, id)
        if highlight:
            return responses.success(highlight)
        return responses.client_error('Highlight can not be found.', 404)

    @jwt.requires_auth
    def put(self, id):
        pass

    @jwt.requires_auth
    def delete(self, id):
        pass
