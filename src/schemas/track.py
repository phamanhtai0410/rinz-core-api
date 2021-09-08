import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime, SchemaFunc
from .stream import StreamProfile


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = ma.fields.Str()

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=530)

    url = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    category = ma.fields.Str(default='')

    created_date = RzFieldDateTime()

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    streams = ma.fields.List(ma.fields.Nested(StreamProfile), default=[])
    download = ma.fields.Boolean(default=False)

    status = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.TRACKS_STATUS),
        default=Consts.STATUS_PROCESSING
    )
    share_link = ma.fields.Function(
        lambda obj: SchemaFunc.generate_share_link(
            obj,
            Consts.RESOURCE_TYPE_TRACK
        ))


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str(required=True)
    url = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str(default='')
    category = ma.fields.Str(required=True)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)
