import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime, SchemaFunc, AuthorNameField
from .stream import StreamProfile


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = AuthorNameField()
    author_avatar = ma.fields.Str()

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=530)

    url = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    category = ma.fields.Str(default='')
    rzm_author = ma.fields.Str()

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

    type = ma.fields.Str(default=Consts.RESOURCE_TYPE_TRACK)
    enable_comment = ma.fields.Boolean(default=True)
    comment_type = ma.fields.Str(default=Consts.COMMENT_TYPE_NORMAL)

    followers = ma.fields.Function(
        lambda obj: len(py_.get(obj, "followers", []))
    )
    following = ma.fields.Boolean(default=False)


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str(required=True)
    url = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    description = ma.fields.Str(default='')
    category = ma.fields.Str(required=True)
    rzm_author = ma.fields.Str(required=True)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)
    enable_comment = ma.fields.Boolean(default=True)
