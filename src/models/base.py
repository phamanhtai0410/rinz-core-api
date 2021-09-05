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

    def update_by_filter(self, filter, obj, upsert=False, multi=False):
        obj["last_updated"] = dt.datetime.utcnow()
        return self.db.update(filter, {"$set": obj}, upsert=upsert, multi=multi)

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

    def get_item_with(self, filter):
        return self.db.find_one(filter)

    def get_list_active(self):
        return self.get_list({"status": {"$ne": STATUS_INACTIVE}})

    def get_list(self, filter={}, sort={}, page=1, per_page=PER_PAGE_DEFAULT, ):
        if not page:
            page = 1
        if not per_page or per_page > PER_PAGE_MAX:
            per_page = PER_PAGE_DEFAULT

        if not sort:
            sort = [("_id", -1)]

        return self.db.find(filter).sort(sort).skip(int((page - 1) * per_page)).limit(per_page)

    def get_random_items(self, filter={}, sort={}, size=1):
        return self.db.aggregate([
            {"$match": filter},
            {"$sample": {"size": size}}
        ])
