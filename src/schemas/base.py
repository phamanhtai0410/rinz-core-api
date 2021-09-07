
import datetime as dt
import marshmallow as ma
import pydash as py_

import src.constants as Consts


class RzFieldDateTime(ma.fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, dt.datetime):
            raise ma.ValidationError("Value must be a datetime object")
        return int(value.timestamp())


class SchemaFunc(object):
    @classmethod
    def generate_share_link(cls, obj, rtype):
        print(obj)
        oid = py_.get(obj, '_id') or py_.get(obj, 'oid') or py_.get(obj, 'id')
        if rtype == Consts.RESOURCE_TYPE_IDOL:
            user_name = py_.get(obj, 'user_name') or 'rzmusic'
            return f"{Consts.RZ_SHARE_WEBSITE}/artist/{user_name}"
        if rtype == Consts.RESOURCE_TYPE_EVENT:
            return f"{Consts.RZ_SHARE_WEBSITE}/event/{oid}"
        rtype = Consts.RESOURCE_TYPE_TRACK
        return f"{Consts.RZ_SHARE_WEBSITE}/track/{oid}"
