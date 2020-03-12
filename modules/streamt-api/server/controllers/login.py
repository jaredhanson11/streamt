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
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        user = account_manager.authenticate_user(email, password)
        jwt_token = jwt.encode_jwt(user.login_id)
        ret = {'token': jwt_token}
        return responses.success(ret, 200)


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
        ret = {'token': jwt_token}
        return responses.success(ret, 201)
