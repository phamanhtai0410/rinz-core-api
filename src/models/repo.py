from src.extensions import mdb
import src.constants as Consts

from .type import *
from .base import BaseDAO
from .stream import StreamDAO
from .user import UserDAO

mPage = BaseDAO(mdb.db.page)
mBlock = BaseDAO(mdb.db.block)
mSiteMap = BaseDAO(mdb.db.site_map)

mMeta = BaseDAO(mdb.db.meta)
mUser = UserDAO(mdb.db.user)

mStream = StreamDAO(mdb.db.stream)
mEvent = BaseDAO(mdb.db.event)
mTrack = BaseDAO(mdb.db.track)
mTweet = BaseDAO(mdb.db.tweet)
mAlbum = BaseDAO(mdb.db.album)


def factory_get_list(type, filter, sort, user_id=0, page=1, page_size=PAGE_SIZE_DEFAULT, randomize=True, personalize=False):
    collection = mTrack
    if type == Consts.RESOURCE_TYPE_EVENT:
        collection = mEvent
    if type == Consts.RESOURCE_TYPE_ALBUM:
        collection = mAlbum
    if type == Consts.RESOURCE_TYPE_TWEET:
        collection = mTweet

    if user_id and personalize:
        filter["author_id"] = user_id

    print(collection, filter, sort)
    if randomize:
        print("randomize", page, page_size)
        return collection.get_random_items(filter, sort, PAGE_SIZE_DEFAULT)
    print("normalize", page, page_size)
    return collection.get_list(filter, sort, page, page_size)
