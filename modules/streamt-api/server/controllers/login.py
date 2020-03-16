'''
Api endpoints handling live streams.
'''
import logging

from flask import request, g
from flask_restful import Resource

from streamt_core.account_management import AccountManager
from streamt_web import responses

from .. import jwt, db

logger = logging.getLogger(__name__)

account_manager: AccountManager = AccountManager(db.session)


class LoginController(Resource):

    @jwt.requires_auth
    def get(self):
        ret = account_manager.get_user(g.user)
        return responses.success(ret, 200)

    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        user = account_manager.authenticate_user(email, password)
        jwt_token = jwt.encode_jwt(user.login_id)
        cookie_name = jwt.jwt_cookie_name
        ret = {'token': jwt_token}
        return responses.success(ret, 200, {
            'Set-Cookie': f'{cookie_name}={jwt_token}'
        })

    @jwt.requires_auth
    def delete(self):
        '''Sets empty cookie (to simulate logging out)'''
        ret = 'Successfully logged out.'
        cookie_name = jwt.jwt_cookie_name
        return responses.success(ret, 200, {
            'Set-Cookie': f'{cookie_name}=\'\''''
        })


class SignupController(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        first_name = post_data.get('first_name')
        last_name = post_data.get('last_name')
        user = account_manager.create_new_user(
            email, password, first_name, last_name)
        jwt_token = jwt.encode_jwt(user.login_id)
        cookie_name = jwt.jwt_cookie_name
        ret = {'token': jwt_token}
        return responses.success(ret, 201, {
            'Set-Cookie': f'{cookie_name}={jwt_token}'
        })
