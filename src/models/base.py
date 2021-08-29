from bson import ObjectId
import datetime as dt

from .type import *


class BaseDAO(object):
    def __init__(self, collection):
        self.db = collection

    def insert(self, obj):
        if not isinstance(obj, dict):
            raise TypeError("obj must be dictionary!")

        obj["created_date"] = dt.datetime.utcnow()
        return self.db.insert(obj)

    def update(self, oid, obj, upsert=False):
        if ObjectId.is_valid(oid):
            oid = ObjectId(oid)

        if not isinstance(obj, dict):
            raise TypeError("obj must be dictionary!")

        obj["last_updated"] = dt.datetime.utcnow()
        return self.db.update({"_id": oid}, {"$set": obj}, upsert=upsert)

    def delete(self, oid, force=False):
        if ObjectId.is_valid(oid):
            oid = ObjectId(oid)

        if force:
            return self.db.delete_one({"_id": oid})

        return self.update(oid, {"status": STATUS_INACTIVE})

    def get_item(self, oid):
        if ObjectId.is_valid(oid):
            oid = ObjectId(oid)

        return self.db.find_one({"_id": oid})

    def get_list(self, filter={}, page=1, per_page=PER_PAGE_DEFAULT, ):
        if not page:
            page = 1
        if not per_page or per_page > PER_PAGE_MAX:
            per_page = PER_PAGE_DEFAULT

        return self.db.find(filter).sort("_id", -1).skip(int((page - 1) * per_page)).limit(per_page)
