import pydash as py_
import marshmallow as ma

import src.constants as Consts


class Item(ma.Schema):
    class Meta:
        ordered = True

    type = ma.fields.Str(validate=ma.validate.OneOf(Consts.META_TYPES))
    id = ma.fields.Str(attribute='slug')
    name = ma.fields.Str(required=True)
    value = ma.fields.Str(default='')


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    type = ma.fields.Str(validate=ma.validate.OneOf(Consts.META_TYPES))
    name = ma.fields.Str(required=True)
    value = ma.fields.Str(default='')
