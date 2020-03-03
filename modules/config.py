'''General config options'''
import os

# JWT
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_LIFESPAN = os.environ.get('JWT_LIFESPAN')
JWT_FRESHSPAN = os.environ.get('JWT_FRESHSPAN', 5)

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
