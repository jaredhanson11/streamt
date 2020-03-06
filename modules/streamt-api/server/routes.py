'''
Setup all the api routes in add_routes(api) method.
'''
from flask_restful import Api
from .controllers.jwt_test import JWTTest
from .controllers.stream import StreamStopController, StreamStartController

API_V1_PREFIX = '/api/v1.0'


def v1_url(path: str) -> str:
    '''Generate full path for v1 url'''
    return API_V1_PREFIX + path


def add_routes(api: Api):
    '''
    Sets up all the api routes.
    '''
    api.add_resource(JWTTest, v1_url('/test'))
    api.add_resource(StreamStartController, v1_url('/stream/publish'))
    api.add_resource(StreamStopController, v1_url('/stream/publish-done'))
