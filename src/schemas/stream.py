import pydash as py_
import marshmallow as ma

import src.constants as Consts


class StreamItem(ma.Schema):
    profile = ma.fields.Str(required=True)
    url = ma.fields.Str(required=True)


class StreamProfile(ma.Schema):
    profile = ma.fields.Str(required=True)
    name = ma.fields.Str(required=True)


class EventParserAPI(ma.Schema):
    class Meta:
        ordered = True

    full_rtmp_url = ma.fields.Str()
    live_event_id = ma.fields.Str()
    key_url = ma.fields.Str()
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
    key_url = ma.fields.Str()
    streams = ma.fields.List(ma.fields.Nested(StreamItem))

    rtmp_url = ma.fields.Str()
    stream_key = ma.fields.Str()
    stream_password = ma.fields.Str()
    stream_user = ma.fields.Str()


class EventConsumer(ma.Schema):
    class Meta:
        ordered = True

    # full_rtmp_url = ma.fields.Str()
    streams = ma.fields.List(ma.fields.Nested(StreamItem))


class Track(ma.Schema):
    class Meta:
        ordered = True

    download = ma.fields.Str()
    streams = ma.fields.List(ma.fields.Nested(StreamItem))
    waveform = ma.fields.Dict(default={})
    screenshot = ma.fields.Str(default='')


class EncodedTrack(ma.Schema):
    class Meta:
        ordered = True

    type = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.RESOURCE_TYPE_ENCODEDS)
    )
    oid = ma.fields.Str(data_key='url', required=True)
    download = ma.fields.Str(default='')
    duration = ma.fields.Int(default=0)
    streams = ma.fields.List(ma.fields.Nested(StreamItem), required=True)
    waveform = ma.fields.Dict(default={})
    screenshot = ma.fields.Str(default='')


class EncodedVideo(ma.Schema):
    class Meta:
        ordered = True

    type = ma.fields.Str(
        validate=ma.validate.OneOf(Consts.RESOURCE_TYPE_ENCODEDS)
    )
    oid = ma.fields.Str(data_key='url', required=True)
    download = ma.fields.Str(default='')
    duration = ma.fields.Int(default=0)
    thumb = ma.fields.Str(default='')
    streams = ma.fields.List(ma.fields.Nested(StreamItem), required=True)

    waveform = ma.fields.Dict(default={})
    screenshot = ma.fields.Str(default='')


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    pass
