import re
import pydash as py_
from http import HTTPStatus
from bson import ObjectId
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.album as SchemaResource
import src.schemas.track as SchemaTrack
import src.decorators as Decorators

bp = Blueprint('album', __name__, url_prefix='/api/album')

RepoResource = Repo.mAlbum


@bp.route('/<string:oid>', methods=['GET', 'PUT', 'DELETE'])
@Http.make_cross_resp
@Decorators.require_login_actions
def get_item(user_info, oid):
    item = RepoResource.get_item(oid)
    print(oid, item)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    uid = py_.get(user_info, 'id', -1)
    if request.method in Consts.REQUEST_ACTTIONS_METHODS and uid != py_.get(item, 'author_id'):
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.FORBIDDEN,
            "data": {},
            "msg": "Permission Denied!"
        }

    if request.method == 'DELETE':
        force = py_.get(request.args, 'force', False)
        print(force)
        result = RepoResource.delete(oid, force)
        return {
            "status": Consts.STATUS_OK,
            "error_code": HTTPStatus.OK,
            "data": bool(result),
            "msg": "success"
        }

    if request.method == 'PUT':
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            print(obj)
            result = RepoResource.update(oid, obj, True)
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": SchemaResource.Item().dump(item),
        "msg": "success"
    }


@bp.route('', methods=['GET', 'POST'])
@Http.make_cross_resp
@Decorators.require_login
def crud(user_info):
    if request.method == 'POST':
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            author_id = user_info["id"]

            # Validate URL
            obj_track = RepoResource.get_item_with({"title": obj["title"]})
            if obj_track:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.CONFLICT,
                    "data": {},
                    "msg": "This Track already exists!"
                }

            obj["author_id"] = author_id
            obj["status"] = Consts.STATUS_ACTIVE

            result = RepoResource.insert(obj)
            return {
                "status": Consts.STATUS_OK,
                "error_code": HTTPStatus.OK,
                "data": bool(result),
                "msg": "Success"
            }
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    uid = py_.get(user_info, 'id')
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": uid
    }
    _sort = [("_id", -1)]

    s = request.args.get('s')
    if s:
        _filter["title"] = {"$regex": re.compile(s, re.IGNORECASE)}
        _sort = [("title", 1)]

    data = RepoResource.get_list(_filter, _sort)
    data = py_.map_(data, Repo.mUser.map_item_user_info)
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }


@bp.route('/<string:oid>/tracks', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login_actions
def get_tracks(user_info, oid):
    item = RepoResource.get_item(oid)
    print(oid, item)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    print(page)
    page_size = Consts.PAGE_SIZE_DEFAULT
    tracks = py_.get(item, 'tracks', [])
    tracks_id = py_.slice_(tracks,
                           (page - 1) * page_size, page * page_size)
    tracks_oid = [ObjectId(itm) for itm in tracks_id]
    items = Repo.mTrack.get_list({
        "_id": {"$in": tracks_oid},
        "status": {"$ne": Consts.STATUS_INACTIVE}
    })
    items = py_.map_(items, Repo.mUser.map_item_user_info)
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaTrack.Item(many=True).dump(items),
        "msg": "success"
    }
