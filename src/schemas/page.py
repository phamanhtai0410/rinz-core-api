import pydash as py_
import marshmallow as ma

import src.constants as Consts
from .base import RzFieldDateTime


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')

    slug = ma.fields.Str()
    title = ma.fields.Str(default='')

    blocks = ma.fields.List(ma.fields.Str())


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    pass
