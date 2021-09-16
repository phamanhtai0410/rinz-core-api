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
    author_avatar = ma.fields.Str()

    content = ma.fields.Str(required=True)
    images = ma.fields.List(ma.fields.Url())
    mode = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.TWEET_MODES),
        default=Consts.MODE_PUBLIC
    )

    created_date = RzFieldDateTime()
    type = ma.fields.Str(default=Consts.RESOURCE_TYPE_TWEET)

    enable_comment = ma.fields.Boolean(default=True)
    comment_type = ma.fields.Str(default=Consts.COMMENT_TYPE_NORMAL)


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    content = ma.fields.Str(required=True)
    images = ma.fields.List(ma.fields.Url())
    mode = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.TWEET_MODES),
        default=Consts.MODE_PUBLIC
    )

    enable_comment = ma.fields.Boolean(default=True)
