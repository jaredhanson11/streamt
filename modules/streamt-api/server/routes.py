'''
Setup all the api routes in add_routes(api) method.
'''
from flask_restful import Api
from .controllers.jwt_test import JWTTest
from .controllers.stream import StreamListController, StreamController, \
    StreamStopController, StreamStartController
from .controllers.clip import ClipListController, ClipController
from .controllers.highlight import HighlightListController, HighlightController
from .controllers.login import LoginController, SignupController
from .controllers.home import HomeController

API_V1_PREFIX = '/api/v1.0'


def v1_url(path: str) -> str:
    '''Generate full path for v1 url'''
    return API_V1_PREFIX + path


def add_routes(api: Api):
    '''
    Sets up all the api routes.
    '''
    api.add_resource(JWTTest, v1_url('/test'))

    # Login/Signup
    api.add_resource(LoginController, v1_url('/login'))
    api.add_resource(SignupController, v1_url('/signup'))

    # Home
    api.add_resource(HomeController, v1_url('/home'))

    # Streams
    api.add_resource(StreamListController, v1_url('/streams'))
    api.add_resource(StreamController, v1_url('/streams/<int:id>'))
    api.add_resource(StreamStartController, v1_url('/stream/publish'))
    api.add_resource(StreamStopController, v1_url('/stream/publish-done'))

    # Clips
    api.add_resource(ClipListController, v1_url('/clips'))
    api.add_resource(ClipController, v1_url('/clips/<int:id>'))

    # Highlights
    api.add_resource(HighlightListController, v1_url('/highlights'))
    api.add_resource(HighlightController, v1_url('/highlights/<int:id>'))
