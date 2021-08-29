import pydash as py_
import marshmallow as ma

import src.constants as Consts


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    astist_id = ma.fields.Str()
    astist_name = ma.fields.Str()

    title = ma.fields.Str(required=True)
    description = ma.fields.Str()

    start_time = ma.fields.DateTime(Consts.DATETIME_FORMAT, required=True)
    end_time = ma.fields.DateTime(Consts.DATETIME_FORMAT)

    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)

    tracks = ma.fields.List(ma.fields.Str())
