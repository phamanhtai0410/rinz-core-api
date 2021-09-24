import re
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.tweet as SchemaResource
import src.decorators as Decorators

bp = Blueprint('tweet', __name__, url_prefix='/api/tweet')

RepoResource = Repo.mTweet


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

    uid = py_.get(user_info, 'id')
    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    tweet_type = py_.get(request.args, 'type')

    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": uid
    }
    if tweet_type == Consts.RESOURCE_TYPE_IMAGE:
        _filter["images"] = {"$ne": [], "$exists": True}
    if tweet_type == Consts.RESOURCE_TYPE_VIDEO:
        _filter["videos"] = {"$ne": [], "$exists": True}

    _sort = [("_id", -1)]

    s = request.args.get('s')
    if s:
        _filter["title"] = {"$regex": re.compile(s, re.IGNORECASE)}
        _sort = [("title", 1)]

    data = RepoResource.get_list(_filter, _sort, page)
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }


@bp.route('/author/<string:author_id>', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login
def get_by_author_id(user_info, author_id):
    uid = py_.get(user_info, 'id')
    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    author_id = py_.to_integer(author_id)

    tweet_type = py_.get(request.args, 'type')

    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": author_id
    }
    if tweet_type == Consts.RESOURCE_TYPE_IMAGE:
        _filter["images"] = {"$ne": [], "$exists": True}
    if tweet_type == Consts.RESOURCE_TYPE_VIDEO:
        _filter["videos"] = {"$ne": [], "$exists": True}

    _sort = [("_id", -1)]

    s = request.args.get('s')
    if s:
        _filter["title"] = {"$regex": re.compile(s, re.IGNORECASE)}
        _sort = [("title", 1)]

    data = RepoResource.get_list(_filter, _sort, page)
    # data = py_.map_(data, Repo.mUser.map_item_user_info)
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }
