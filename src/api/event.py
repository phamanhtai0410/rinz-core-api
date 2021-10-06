import re
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
from lib.rz_chat import RzChatAPI


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
            obj = SchemaResource.ItemUpdate().load(payload, partial=True)
            o_cmt = py_.get(obj, "enable_comment")
            i_cmt = py_.get(item, "enable_comment", True)

            # Check user update group rule
            if o_cmt != i_cmt:
                # Publish Message to Socket Channel
                payload_pub = {
                    "type": "control",
                    "content": "enable_comment" if item['enable_comment'] else "disable_comment",
                    # "user": {
                    #     "user_name": py_.get(user_info, 'user_full_name', ''),
                    #     "user_avatar": py_.get(user_info, 'user_avatar', ''),
                    # }
                }

                RzChatAPI.send_public_message(payload_pub, oid)

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
    uid = py_.get(user_info, 'id')
    if request.method == 'POST':
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            obj["author_id"] = uid
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

    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": uid
    }
    _sort = [("_id", -1)]

    rzm_author = py_.get(request.args, 'rzm_author')
    if rzm_author:
        _filter = {
            "status": {"$ne": Consts.STATUS_INACTIVE},
            "rzm_author": rzm_author
        }

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
    author = Repo.mUser.get_item(author_id)
    if not author:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": author_id
    }
    _sort = [("_id", -1)]

    s = request.args.get('s')
    if s:
        _filter["title"] = {"$regex": re.compile(s, re.IGNORECASE)}
        _sort = [("title", 1)]

    data = RepoResource.get_list(_filter, _sort, page)
    data = py_.map_(data, lambda item: Repo.mUser.map_author(item, author))
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }
