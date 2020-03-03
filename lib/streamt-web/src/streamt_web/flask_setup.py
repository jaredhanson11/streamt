'''
Setup Flask objects.
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from streamt_web.jwt_auth import JWTManager

from .controllers import heartbeat


def create_app(name) -> Flask:
    '''Initiliaze Flask app object with configs'''
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG')
    return app


def create_db(app) -> SQLAlchemy:
    '''Initialize Flask-SQLAlchemy db object'''
    db = SQLAlchemy(app)
    return db


def create_api(app) -> Api:
    '''
    Initialize Flask-RESTful api object
    Adds common controllers to api object.
    '''
    api = Api(app)
    api.add_resource(heartbeat.HeartbeatController, '/hb')
    return api


def create_jwt(app) -> JWTManager:
    '''
    Initialized JWTManager object from Flask-JWT-Extended.
    '''
    jwt = JWTManager(app)
    return jwt
