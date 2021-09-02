import pydash as py_
import marshmallow as ma

import src.constants as Consts


class StreamItem(ma.Schema):
    profile = ma.fields.Str(required=True)
    url = ma.fields.Str(required=True)


class EventParserAPI(ma.Schema):
    class Meta:
        ordered = True

    full_rtmp_url = ma.fields.Str()
    live_event_id = ma.fields.Str()
    streams = ma.fields.List(
        ma.fields.Nested(StreamItem),
        attribute='live_event_url'
    )

    rtmp_url = ma.fields.Str()
    stream_key = ma.fields.Str()
    stream_password = ma.fields.Str()
    stream_user = ma.fields.Str()


class EventOwner(ma.Schema):
    class Meta:
        ordered = True

    full_rtmp_url = ma.fields.Str()
    live_event_id = ma.fields.Str()
    streams = ma.fields.List(ma.fields.Nested(StreamItem))

    rtmp_url = ma.fields.Str()
    stream_key = ma.fields.Str()
    stream_password = ma.fields.Str()
    stream_user = ma.fields.Str()


class EventConsumer(ma.Schema):
    class Meta:
        ordered = True

    full_rtmp_url = ma.fields.Str()
    streams = ma.fields.List(ma.fields.Nested(StreamItem))


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    pass
