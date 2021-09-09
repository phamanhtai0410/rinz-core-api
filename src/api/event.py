from bson import ObjectId
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.event as SchemaResource
import src.schemas.track as SchemaTrack
import src.decorators as Decorators

bp = Blueprint('event', __name__, url_prefix='/api/event')

RepoResource = Repo.mEvent


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
            result = RepoResource.update(oid, obj, True)
            item = RepoResource.get_item(oid)
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    item = Repo.mUser.map_item_user_info(item)
    item = Repo.mFollow.map_follow_info(
        Consts.RESOURCE_TYPE_EVENT,
        oid, uid, item
    )

    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": SchemaResource.Item().dump(item),
        "msg": "success"
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


@bp.route('', methods=['GET', 'POST'])
@Http.make_cross_resp
@Decorators.require_login
def crud(user_info):
    if request.method == 'POST':
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            obj["author_id"] = user_info["id"]
            print(obj)
            result = RepoResource.insert(obj)
            return {
                "status": Consts.STATUS_OK,
                "error_code": HTTPStatus.OK,
                "data": SchemaResource.Item().dump(obj),
                "msg": "Success"
            }
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    data = RepoResource.get_list_active()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }
