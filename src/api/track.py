import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.track as SchemaResource
import src.decorators as Decorators

bp = Blueprint('track', __name__, url_prefix='/api/track')

RepoResource = Repo.mTrack


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
@Decorators.require_login_actions
def crud(user_info):
    if request.method == 'POST':
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            author_id = user_info["id"]
            author_name = user_info["user_full_name"]

            obj_track = RepoResource.get_item_with({"url": obj["url"]})
            if obj_track:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.CONFLICT,
                    "data": {},
                    "msg": "This Track already exists!"
                }

            obj["author_id"] = author_id
            obj["author_name"] = author_name
            obj["status"] = Consts.STATUS_PROCESSING
            print(obj)
            result = RepoResource.insert(obj)
            stream_obj = Repo.mStream.insert({
                "type": Consts.RESOURCE_TYPE_TRACK,
                "oid": obj["url"],
                "author_id": author_id,
                "author_name": author_name
            })
            print(stream_obj)
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

    data = RepoResource.get_list_active()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }
