# -*- coding: utf-8 -*-

import pydash as py_
import marshmallow as ma
import random as rd

import src.constants as Consts
from .base import RzFieldDateTime
from .tweet import Item as TweetItem


class SearchBarMeta(ma.Schema):
    placeholder = ma.fields.Str(default='Search...')
    voice = ma.fields.Boolean()


class BaseBlock(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Str(attribute='_id')
    type = ma.fields.Str()

    meta = ma.fields.Dict()
    data = ma.fields.List(ma.fields.Dict())


class SearchBar(BaseBlock):
    meta = ma.fields.Nested(SearchBarMeta)


class Idol(ma.Schema):
    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int()
    author_name = ma.fields.Str()
    author_avatar = ma.fields.Str()
    live_stream = ma.fields.Boolean(default=True)
    type = ma.fields.Str(default=True)

    followers = ma.fields.Function(lambda obj: rd.randrange(100, 10000))
    following = ma.fields.Function(lambda obj: rd.choice([True, False]))


class IdolLive(BaseBlock):
    data = ma.fields.List(ma.fields.Nested(Idol))


class MenuIcon(ma.Schema):
    id = ma.fields.Str(default='')
    name = ma.fields.Str()
    type = ma.fields.Str()
    icon = ma.fields.Str()


class WidgetIcons(BaseBlock):
    data = ma.fields.List(ma.fields.Nested(MenuIcon))


class SliderItem(ma.Schema):
    id = ma.fields.Str(attribute='_id')
    author_id = ma.fields.Int()
    author_name = ma.fields.Str()
    author_avatar = ma.fields.Str()

    on_air_time = RzFieldDateTime(attribute='start_time')
    banner = ma.fields.Url(default='')
    rz_point = ma.fields.Int(validate=ma.validate.Range(min=0), default=0)
    title = ma.fields.Str()

    followers = ma.fields.Function(lambda obj: rd.randrange(100, 10000))
    type = ma.fields.Str()
    duration = ma.fields.Function(lambda obj: rd.randrange(100, 1000))


class SliderMeta(ma.Schema):
    title = ma.fields.Str()
    type = ma.fields.Str()
    more_text = ma.fields.Str()
    more_href = ma.fields.Str()
    data_type = ma.fields.Str()

    rows = ma.fields.Int()


class Slider(BaseBlock):
    data = ma.fields.List(ma.fields.Nested(SliderItem))
    meta = ma.fields.Nested(SliderMeta)


class TopIdolMeta(ma.Schema):
    title = ma.fields.Str()
    type = ma.fields.Str()
    more_text = ma.fields.Str()
    more_href = ma.fields.Str()
    data_type = ma.fields.Str()


class TopIdol(BaseBlock):
    meta = ma.fields.Nested(TopIdolMeta)
    data = ma.fields.List(ma.fields.Nested(Idol))


class NewFeed(BaseBlock):
    meta = ma.fields.Nested(TopIdolMeta)
    data = ma.fields.List(ma.fields.Nested(TweetItem))


class TabItem(BaseBlock):
    name = ma.fields.Str()
    id = ma.fields.Str()


class TabMeta(BaseBlock):
    image = ma.fields.Str()
    type = ma.fields.Str()


class Tabs(BaseBlock):
    meta = ma.fields.Nested(TabMeta)
    data = ma.fields.List(ma.fields.Nested(TabItem))
