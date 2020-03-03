'''
Setup all the api routes in add_routes(api) method.
'''
from flask_restful import Api
from .controllers.jwt_test import JWTTest

API_V1_PREFIX = '/api/v1.0'
API_PREFIX = API_V1_PREFIX


def add_routes(api: Api):
    '''
    Sets up all the api routes.
    '''
    api.add_resource(JWTTest, API_PREFIX + '/test')
