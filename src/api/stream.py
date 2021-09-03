import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.stream as SchemaStream
import src.decorators as Decorators

bp = Blueprint('stream', __name__, url_prefix='/api/stream')

RepoResource = Repo.mStream


@bp.route('/event/<string:oid>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def get_event_stream(user_info, oid):
    event = Repo.mEvent.get_item(oid)
    if not event:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Event"
        }

    stream = Repo.mStream.get_stream(oid, Consts.RESOURCE_TYPE_EVENT, event)
    if not stream:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Stream"
        }

    uid = py_.get(user_info, 'id', -1)
    author_id = py_.get(event, 'author_id')
    is_owner = bool(uid == author_id)

    schema_item = SchemaStream.EventOwner() if is_owner else SchemaStream.EventConsumer()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema_item.dump(stream),
        "msg": "success"
    }


@bp.route('/track/<string:oid>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def get_music_stream(user_info, oid):
    default_strack = {
        "url": "/path/of/resource_track.mp3",
        "download": "https://v01.rinznetwork.com/source/mp3/2021/08/31/test.mp3",
        "streams": [
            {
                "profile": "128k",
                "url": "https://v01.rinznetwork.com/encode/mp3/2021/08/31/test/test_128k.m3u8"
            },
            {
                "profile": "320k",
                "url": "https://v01.rinznetwork.com/encode/mp3/2021/08/31/test/test_320k.m3u8"
            }
        ]
    }
    schema_item = SchemaStream.Track()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema_item.dump(default_strack),
        "msg": "success"
    }

    track = Repo.mTrack.get_item(oid)
    if not track:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Track"
        }

    stream = Repo.mStream.get_stream(oid, Consts.RESOURCE_TYPE_TRACK, track)
    if not stream:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Stream of this Track"
        }

    uid = py_.get(user_info, 'id', -1)
    author_id = py_.get(track, 'author_id')
    is_owner = bool(uid == author_id)

    schema_item = SchemaStream.Track()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema_item.dump(stream),
        "msg": "success"
    }
