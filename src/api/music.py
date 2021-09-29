import random as rd
from bson import ObjectId
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.album as SchemaAlbum
import src.schemas.track as SchemaTrack
import src.decorators as Decorators

bp = Blueprint('music', __name__, url_prefix='/api/music')


@bp.route('/<ms_type>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def list_hot(user_info, ms_type):
    if ms_type not in Consts.MUSIC_TYPES:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.BAD_REQUEST,
            "data": [],
            "msg": ""
        }

    fee = py_.get(request.args, 'fee')
    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1

    # TODO: MIX of album & track
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE}
    }
    if fee is not None:
        fee = py_.to_boolean(fee)
        if fee:
            _filter["rz_point"] = {"$gt": 0}
        else:
            _filter["rz_point"] = 0

    _sort = [("_id", -1)]
    randomize = True
    ordered = False

    music_data = [Consts.RESOURCE_TYPE_TRACK, Consts.RESOURCE_TYPE_ALBUM]
    page_size = Consts.PAGE_SIZE_DEFAULT
    if ms_type == Consts.MUSIC_TYPE_ALL:
        randomize = False
        page_size = int(Consts.PAGE_SIZE_DEFAULT/2)

    if ms_type == Consts.MUSIC_TYPE_NEW:
        randomize = False
        ordered = True
        page_size = int(Consts.PAGE_SIZE_DEFAULT/2)

    if ms_type == Consts.MUSIC_TYPE_RANKING:
        randomize = True
        ordered = True
        page_size = int(Consts.PAGE_SIZE_DEFAULT * 2)
        music_data = [Consts.RESOURCE_TYPE_TRACK]

    print(music_data)
    if randomize:
        _sort = {"_id": -1}
        albums = Repo.mAlbum.get_random_items(
            _filter,
            _sort,
            page_size
        ) if page == 1 and Consts.RESOURCE_TYPE_ALBUM in music_data else []
        tracks = Repo.mTrack.get_random_items(
            _filter,
            _sort,
            page_size
        ) if page == 1 and Consts.RESOURCE_TYPE_TRACK in music_data else []
    else:
        albums = Repo.mAlbum.get_list(
            _filter,
            _sort,
            page,
            page_size
        ) if Consts.RESOURCE_TYPE_ALBUM in music_data else []
        tracks = Repo.mTrack.get_list(
            _filter,
            _sort,
            page,
            page_size
        ) if Consts.RESOURCE_TYPE_TRACK in music_data else []

    albums = py_.map_(albums, Repo.mUser.map_item_user_info)
    tracks = py_.map_(tracks, Repo.mUser.map_item_user_info)
    data = SchemaAlbum.Item(many=True).dump(albums) \
        + SchemaTrack.Item(many=True).dump(tracks)

    if not ordered:
        rd.shuffle(data)

    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": data,
        "msg": "success"
    }
