'''
This package contains the Flask REST Api for the Stream API module.
'''

from streamt_db.user import User
from streamt_web import flask_setup, jwt_auth

app = flask_setup.create_app(__name__)
db = flask_setup.create_db(app)
api = flask_setup.create_api(app)
jwt = flask_setup.create_jwt(app)
jwt.load_user = jwt_auth.JWTManager.default_load_user_fn(db.session, User)

# Ugly dependency, but since routes import controller classes
# the api and app objects needs to be available when importing routes
# Attach routes to the Flask-RESTful Resource objects found at controllers/*
from . import routes  # noqa
routes.add_routes(api)
