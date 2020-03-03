'''
Models related to videos.
'''
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, \
    Table
from sqlalchemy.orm import relationship

from . import base


class Stream(base.Base):
    '''Stream table. Full length video of a video session.'''
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True)

    # Metadata
    name = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # Duration of video in seconds

    # Media
    filename = Column(String(500), nullable=False)
    thumbnail = Column(String(100))

    # Relationships
    user_id = Column(ForeignKey('users.id'), nullable=False)


class Clip(base.Base):
    '''
    Clip table.
    Smaller portion of a stream, consisting of a singular moment.
    '''
    __tablename__ = 'clips'

    id = Column(Integer, primary_key=True)

    # Metadata
    name = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    start = Column(Float(precision=4))  # Second of start clip
    end = Column(Float(precision=4))  # Second of end clip


class Highlight(base.Base):
    '''Highlight table. Ordered list of clips make up a highlight tape.'''
    __tablename__ = 'highlights'

    id = Column(Integer, primary_key=True)

    # Metadata
    title = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    clips = relationship('ClipToHighlight')


class ClipToHighlight(base.Base):
    '''
    Many to many association table between clips and highlights.
    This table also handles the ordering of clips for a particular highlight.
    '''
    __tablename__ = 'clips_to_highlights'

    # Associations
    highlight_id = Column(Integer, ForeignKey(
        'highlights.id'), primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'), primary_key=True)

    # Order
    clip_rank = Column(Integer, nullable=False)

    # Relationships
    clip = relationship('Clip')
