import pydash as py_
from hashlib import pbkdf2_hmac

from lib.rz_stream import RzStreamAPI
import src.constants as Consts
import src.schemas.stream as SchemaStream

from .base import BaseDAO


class FollowDAO(BaseDAO):
    def map_follow_info(self, rtype, oid, uid, item):
        if not uid:
            return item
        obj_flw = self.get_item_with({
            "type": rtype,
            "oid": oid,
        })
        followers = py_.get(obj_flw, 'followers', []) or []
        item["followers"] = followers
        item["following"] = bool(uid in followers)
        return item
