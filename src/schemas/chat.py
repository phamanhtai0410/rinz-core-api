import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime, SchemaFunc, AuthorNameField


class GroupItem(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    name = ma.fields.Str()
    type = ma.fields.Str(default='private')
    event = ma.fields.Str(default='message')
    users = ma.fields.List(ma.fields.Integer())
    chat_type = ma.fields.Str(default=Consts.CHAT_TYPE_SINGLE)

    last_message = ma.fields.Dict()


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    group_id = ma.fields.Str(required=True)

    author_id = ma.fields.Int(required=True)
    author_name = AuthorNameField()
    author_avatar = ma.fields.Str()

    content = ma.fields.Str(default='')
    status = ma.fields.Str(default=Consts.CHAT_STATUS_SENT)


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    content = ma.fields.Str(required=True)
