import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime

class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = ma.fields.Str()

    banner = ma.fields.Str()
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    start_time = RzFieldDateTime(required=True)
    end_time = RzFieldDateTime()

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str()
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    start_time = ma.fields.DateTime(Consts.DATETIME_FORMAT, required=True)
    end_time = ma.fields.DateTime(Consts.DATETIME_FORMAT)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())
