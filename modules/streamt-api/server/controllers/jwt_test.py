from flask import request, g
from flask_restful import Resource

from streamt_web import responses
from streamt_core.account_management import AccountManager

from .. import jwt, db


class JWTTest(Resource):
    account_manager = AccountManager(db.session)

    def post(self):
        '''Login'''
        user = self.account_manager.authenticate_user(
            'jred0011@gmail.com', 'test_pw')
        jwt_token = jwt.encode_jwt(user.login_id)
        return responses.success({'token': jwt_token})

    @jwt.requires_auth
    def get(self):
        return responses.success({'id': g.user.id})
