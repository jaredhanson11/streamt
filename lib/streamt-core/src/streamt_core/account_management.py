'''
Functions used for general account management.

Functions like creating a new user, checking password, changing password, etc.
go here.
'''
import bcrypt
import uuid
import logging

from streamt_db.user import User

logger = logging.getLogger(__name__)


class AccountManager:
    '''
    Class for managing accounts.
    '''
    PW_SALT = bcrypt.gensalt(rounds=12)
    session = None  # DB session

    def __init__(self, db_session):
        self.session = db_session

    def create_new_user(self, email, password, f_name=None, l_name=None):
        '''Creates and returns a new user record.'''
        # Metadata
        new_user = User()
        new_user.first_name = f_name
        new_user.last_name = l_name
        # Login
        new_user.email = email
        new_user.password_hash = self._encrypt_pw(password)
        new_user.last_name = l_name
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def authenticate_user(self, email, password) -> User:
        '''Returns user if email/password combo is valid, else None'''
        user = self.session.query(User).filter_by(email=email).one()
        if user is not None:
            if self._check_pw(password, user.password_hash):
                return user

    # Privates
    def _encrypt_pw(self, password: str) -> str:
        '''Generate salted password hash'''
        hashed = bcrypt.hashpw(str(password).encode('utf-8'), self.PW_SALT)
        return hashed.decode('utf-8')

    def _check_pw(self, password: str, password_hash: str) -> bool:
        '''Check that password and password_hash match'''
        _password = password.encode('utf-8')
        _password_hash = password_hash.encode('utf-8')
        return bcrypt.checkpw(_password, _password_hash)

    def _generate_stream_key(self):
        '''Generate stream key'''
        return uuid.uuid4()
