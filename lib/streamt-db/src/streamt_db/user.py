from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, Integer, String,  DateTime, Boolean
from sqlalchemy.orm import relationship

from . import base


class User(base.Base):
    '''User table'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    # login_id = UUID for JWT
    login_id = Column(String(50), unique=True, default=lambda: str(uuid4()))

    # User metadata
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Login info and stream_key
    email = Column(String(320), nullable=False, unique=True)
    email_verified = Column(Boolean, default=False)
    password_hash = Column(String(60), nullable=False)
    stream_key = Column(String(50), unique=True)

    # Relationships
    streams = relationship('Stream', back_populates='user')
    highlights = relationship('Highlight', back_populates='owner')
