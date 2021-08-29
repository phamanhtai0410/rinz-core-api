from src.extensions import mdb
from .base import BaseDAO

# mPage = BaseDAO(mdb.db.page)
# mBlock = mdb.db.block
# mSiteMap = mdb.db.site_map
mMeta = BaseDAO(mdb.db.meta)

mUser = BaseDAO(mdb.db.user)

mEvent = BaseDAO(mdb.db.event)
# mTweet = mdb.db.tweet

# mTrack = mdb.db.track
# mTrackStream = mdb.db.track_stream
