'''
This script tears down and brings up a fresh database for a dev environment.

1. Drop all tables
2. Create all tables
3. Add one test user
4. (Configurable) Add one stream for user
5. (Configurable) Add one clip for stream
6. (Configurable) Add on highlight for user
'''
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import streamt_db
import streamt_core
from streamt_core import account_management, clip_management, \
    highlight_management, stream_management

# Setup DB
db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI',
                        'postgresql://postgres@localhost/streamt')
db_engine = create_engine(db_uri, echo=True)
Session = sessionmaker(bind=db_engine)
session = Session()

# Setup models
streamt_db.base.Base.metadata.drop_all(db_engine)
streamt_db.base.Base.metadata.create_all(db_engine)

# Insert fresh user
am = account_management.AccountManager(session)
user1 = am.create_new_user('test@test.com', 'test', 'Test', 'User')
user1.login_id = '0cee6229-4af3-4c97-a950-214f51271d31'
session.add(user1)
session.commit()

# Insert one stream
sm = stream_management.StreamManager(session)
stream1 = sm.start_stream(user1.stream_key)
sm.end_stream(stream1.id)

# Insert one clip
cm = clip_management.ClipManager(session)
clip1 = cm.create_clip(stream1.id, 'Test Clip 1', 0, 10)

# Insert one highligh
hm = highlight_management.HighlightManager(session)
higlight1 = hm.create_highlight(user1, 'Test Highlight 1')
hm.update_highlight_clips(higlight1.id, [clip1])
