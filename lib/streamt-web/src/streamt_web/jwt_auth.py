'''
JWT related tasks.
'''
import logging
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import request, g
import jwt

from . import responses

logger = logging.getLogger(__name__)


class JWTManager:
    '''
    JWTManager is custom solution for managing authentication to api.

    Override the load_user and expire_token functions for login/logout to
    function properly.
    '''
    secret_key = None
    jwt_lifespan = None  # num minutes token is valid for after being issued
    jwt_freshspan = None  # num minutes token is "fresh"
    jwt_algorithm = 'HS256'

    def __init__(self, app):
        secret_key = app.config.get('SECRET_KEY')
        jwt_lifespan = app.config.get('JWT_LIFESPAN', -1)
        jwt_freshspan = app.config.get('JWT_FRESHSPAN', 5)
        assert secret_key is not None
        self.secret_key = secret_key
        self.jwt_lifespan = int(jwt_lifespan)
        self.jwt_freshspan = int(jwt_freshspan)

    def load_user(self, id: str) -> object:
        '''Implement this function to enable JWT protected endpoints'''
        pass

    @staticmethod
    def default_load_user_fn(session, user_model):
        '''
        Default load user fn. Requires SQLalchemy session and a user model with
        the unique column 'login_id'.
        '''
        def load_user(id):
            return session.query(user_model)\
                .filter_by(login_id=id).one_or_none()
        return load_user

    def expire_token(self, id: str) -> None:
        '''Implement this function to invalidate JWT token'''
        pass

    def requires_auth(self, f):
        '''
        Requires non-expired JWT token in the 'X-JWT-TOKEN' header.
        Token must correspond to a valid user, defined by load_user function.
        '''
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get('X-JWT-TOKEN', None)
            jwt_data = self._decode_jwt(token) if token else None
            jwt_id = jwt_data.get('id') if jwt_data else None
            curr_user = self.load_user(jwt_id) if jwt_id else None
            if curr_user:
                g.user = curr_user
            else:
                return responses.error('Please login to continue.', 401)
            return f(*args, **kwargs)
        return decorator

    def requires_fresh_auth(self, f):
        '''
        Requires non-expired and fresh JWT token in the 'X-JWT-TOKEN' header.
        Token must correspond to a valid user, defined by load_user function.
        '''
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get('X-JWT-TOKEN', None)
            jwt_data = self._decode_jwt(token) if token else None
            jwt_id = jwt_data.get('id') if jwt_data else None
            curr_user = self.load_user(jwt_id) if jwt_id else None
            if curr_user and jwt_data.get('fresh', None):
                g.user = curr_user
            else:
                return responses.error('Please login to continue.', 401)
            return f(*args, **kwargs)
        return decorator

    def encode_jwt(self, id: str) -> str:
        '''Creates encrypted JWT token'''
        jwt_data = {
            'iat': int(datetime.utcnow().timestamp()),
            'id': id
        }

        return jwt.encode(jwt_data, self.secret_key,
                          algorithm=self.jwt_algorithm).decode('utf-8')

    # Privates
    def _decode_jwt(self, token: str) -> dict:
        '''Returns JWT token, or None if JWT decode failed.'''
        try:
            jwt_data = jwt.decode(token, self.secret_key,
                                  algorithms=self.jwt_algorithm,
                                  options={'require_iat': True})

            iat_dt = datetime.fromtimestamp(jwt_data['iat'])
            # Check if token is still valid
            if self.jwt_lifespan >= 0:
                lifespan = timedelta(minutes=self.jwt_lifespan)
                expires_at = iat_dt + lifespan
                if datetime.utcnow() >= expires_at:
                    raise jwt.InvalidTokenError
            # Set freshness of token
            if self.jwt_freshspan < 0:
                jwt_data['fresh'] = True
            else:
                freshspan = timedelta(minutes=self.jwt_freshspan)
                fresh_until = iat_dt + freshspan
                if datetime.utcnow() < fresh_until:
                    jwt_data['fresh'] = True
                else:
                    jwt_data['fresh'] = False
            return jwt_data
        except jwt.InvalidTokenError:
            return None
