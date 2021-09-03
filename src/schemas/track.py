import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime
from .stream import StreamProfile


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = ma.fields.Str()

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=530)

    url = ma.fields.Url(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    category = ma.fields.Str(default='')

    created_date = RzFieldDateTime()

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    streams = ma.fields.List(ma.fields.Nested(StreamProfile), default=[])
    download = ma.fields.Boolean(default=False)

    status = ma.fields.Str(validate=ma.validate.OneOf(Consts.TRACKS_STATUS), default=Consts.STATUS_PROCESSING)


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str(default='')
    url = ma.fields.Url(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str(default='')
    category = ma.fields.Str(default='')

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)
