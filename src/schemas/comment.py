from src.models.type import STATUS_ACTIVE, STATUS_INACTIVE
import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime, AuthorNameField


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int(required=True)
    author_name = AuthorNameField()
    avatar = ma.fields.Str()

    nlike = ma.fields.Int(default=0)
    nreply = ma.fields.Int(default=0)

    parent_id = ma.fields.Str(default='')
    pin_top = ma.fields.Boolean(default=False)
    ucomment = ma.fields.Boolean(default=False)
    uliked = ma.fields.Boolean(default=False)

    content_id = ma.fields.Str()
    content_type = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.RESOURCE_TYPES)
    )
    content = ma.fields.Str(default='')

    status = ma.fields.Str(
        validate=ma.validate.OneOf([
            Consts.STATUS_ACTIVE,
            Consts.STATUS_INACTIVE
        ])
    )


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    content = ma.fields.Str(default='')
