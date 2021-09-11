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

    banner = ma.fields.Function(
        lambda obj: SchemaFunc.generate_album_banner(obj)
    )
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str()
    # category = ma.fields.Str(default='')

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    banner = ma.fields.Str(default='')
    duration = ma.fields.Int(default=0)

    title = ma.fields.Str(required=True)
    description = ma.fields.Str(default='')
    # category = ma.fields.Str(required=True)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())
