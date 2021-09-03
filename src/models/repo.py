from src.extensions import mdb
from .base import BaseDAO
from .stream import StreamDAO

mPage = BaseDAO(mdb.db.page)
mBlock = BaseDAO(mdb.db.block)
mSiteMap = BaseDAO(mdb.db.site_map)

mMeta = BaseDAO(mdb.db.meta)
mUser = BaseDAO(mdb.db.user)

mStream = StreamDAO(mdb.db.stream)
mEvent = BaseDAO(mdb.db.event)
mTrack = BaseDAO(mdb.db.track)
mTweet = BaseDAO(mdb.db.track)
