import pydash as py_

from src.extensions import mdb, mdb_payment
import src.constants as Consts

from lib.rz_payment import RzPaymentAPI

from .type import *
from .base import BaseDAO
from .stream import StreamDAO
from .user import UserDAO
from .follow import FollowDAO
from .comment import CommentDAO

mPage = BaseDAO(mdb.db.page)
mBlock = BaseDAO(mdb.db.block)
mSiteMap = BaseDAO(mdb.db.site_map)

mMeta = BaseDAO(mdb.db.meta)
mUser = UserDAO(mdb.db.user)
mFollow = FollowDAO(mdb.db.follow)
mComment = CommentDAO(mdb.db.comment)

mStream = StreamDAO(mdb.db.stream)
mEvent = BaseDAO(mdb.db.event)
mTrack = BaseDAO(mdb.db.track)
mTweet = BaseDAO(mdb.db.tweet)
mAlbum = BaseDAO(mdb.db.album)

mChat = BaseDAO(mdb.db.chat)
mChatGroup = BaseDAO(mdb.db.chat_group)

mPayment = BaseDAO(mdb.db.order)
mRzPayment = BaseDAO(mdb_payment.db.orders)


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


class PaymentGateway(object):
    @classmethod
    def get_paid_order(cls, oid, rtype, user_id, author_id):
        rzm_order = mPayment.get_item_with({
            "oid": oid,
            "type": rtype,
            "user_id": user_id,
            "status": Consts.PAYMENT_STATUS_PAID,
        })
        if rzm_order:
            return rzm_order

        tct_order = mRzPayment.get_item_with({
            "order_type": rtype,
            "status": Consts.PAYMENT_STATUS_PAID,
            "gateway": Consts.PAYMENT_RZ_MUSIC_GATEWAY,
            "user_id": user_id,
            "items.value.id": oid,
        })
        if not tct_order:
            return {}

        transaction_id = py_.get(tct_order, 'transaction_id', '')
        pay_provider = py_.get(tct_order, 'pay_provider', '')
        items = py_.get(tct_order, 'items', {})
        rzm_order = {
            "oid": oid,
            "type": rtype,
            "user_id": user_id,
            "author_id": author_id,
            "status": Consts.PAYMENT_STATUS_PAID,
            "transaction_id": transaction_id,
            "pay_provider": pay_provider,
            "items": items,
        }
        mPayment.update_by_filter({
            "oid": oid,
            "type": rtype,
            "user_id": user_id,
            "author_id": author_id,
        }, rzm_order, upsert=True)

        return rzm_order

    @classmethod
    def exec_order(cls, oid, rtype, user_id, items, rz_point, author_id):
        tct_order = RzPaymentAPI.iapi_transaction(
            user_id,
            rz_point,
            rtype,
            items
        )
        payment_url = py_.get(tct_order, 'transaction.payment_url', '')
        if not payment_url:
            return {}

        transaction = py_.get(tct_order, 'transaction', {})
        rzm_order = {
            "oid": oid,
            "type": rtype,
            "user_id": user_id,
            "author_id": author_id,
            "status": Consts.PAYMENT_STATUS_UNPAID,
            "items": items,
            "transaction": transaction,
        }
        mPayment.insert(rzm_order)
        return rzm_order
