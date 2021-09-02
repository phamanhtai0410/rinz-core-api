import pydash as py_
from hashlib import pbkdf2_hmac

from lib.rz_stream import RzStreamAPI
import src.constants as Consts
import src.schemas.stream as SchemaStream

from .base import BaseDAO


class StreamDAO(BaseDAO):
    def m_get_item_by_type(self, oid, rtype):
        return self.db.find_one({"oid": oid, "type": rtype})

    def get_stream(self, oid, rtype, obj={}):
        """CACHE GET STREAM FLOW

        Args:
            oid ([type]): [description]
            rtype ([type]): [Resource Type]
        """
        obj_stream = self.m_get_item_by_type(oid, rtype)
        print("1. GET STREAM INFO FROM DB")
        if obj_stream:
            return obj_stream

        print("2. CALL API GENERATE STREAM ")
        if rtype == Consts.RESOURCE_TYPE_EVENT:
            stream = RzStreamAPI.iapi_generate_stream(
                obj['author_id'],
                oid,
                obj['start_time']
            )
            obj_stream = SchemaStream.EventParserAPI().dump(stream)

        print("3. UPDATE STREAM TO DB")
        if obj_stream:
            # DATA FROM API GENERATE_STREAM
            obj_stream["type"] = rtype
            obj_stream["oid"] = oid
            self.update(oid, obj_stream, True)

        return obj_stream
