import pydash as py_
import marshmallow as ma

import src.constants as Consts


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    type = ma.fields.Str(validate=ma.validate.OneOf(Consts.META_TYPES))
    slug = ma.fields.Str()

    name = ma.fields.Str(required=True)
    value = ma.fields.Str()
