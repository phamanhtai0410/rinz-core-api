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


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    content = ma.fields.Str(required=True)
    images = ma.fields.List(ma.fields.Url())
    mode = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.TWEET_MODES),
        default=Consts.MODE_PUBLIC
    )
