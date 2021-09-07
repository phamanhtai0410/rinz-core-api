# -*- coding: utf-8 -*-

import pydash as py_
import marshmallow as ma

import src.constants as Consts


class SearchBarMeta(ma.Schema):
    placeholder = ma.fields.Str(default='Search...')
    voice = ma.fields.Boolean()


class BaseBlock(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    type = ma.fields.Str()


class SearchBar(BaseBlock):
    meta = ma.fields.Nested(SearchBarMeta)


class IdolLiveData(ma.Schema):
    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int()
    author_name = ma.fields.Str()

    image = ma.fields.Str()
    live_stream = ma.fields.Boolean(default=True)
    type = ma.fields.Str(default=True)


class IdolLive(BaseBlock):
    data = ma.fields.List(ma.fields.Nested(IdolLiveData))
