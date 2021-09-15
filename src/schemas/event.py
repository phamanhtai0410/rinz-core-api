import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime, SchemaFunc


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = ma.fields.Str()
    author_avatar = ma.fields.Str()

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    start_time = RzFieldDateTime(required=True)
    end_time = RzFieldDateTime()

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())

    status = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.LIVE_STATUS),
        default=Consts.STATUS_ACTIVE
    )
    share_link = ma.fields.Function(
        lambda obj: SchemaFunc.generate_share_link(
            obj,
            Consts.RESOURCE_TYPE_EVENT
        ))

    followers = ma.fields.Function(
        lambda obj: len(py_.get(obj, "followers", []))
    )
    following = ma.fields.Boolean(default=False)

    type = ma.fields.Str(default=Consts.RESOURCE_TYPE_EVENT)


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str(default='')

    start_time = ma.fields.DateTime(Consts.DATETIME_FORMAT, required=True)
    end_time = ma.fields.DateTime(Consts.DATETIME_FORMAT)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())

    status = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.LIVE_STATUS),
        default=Consts.STATUS_ACTIVE
    )
