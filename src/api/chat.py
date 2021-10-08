import re
from bson import ObjectId
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.chat as SchemaResource
import src.decorators as Decorators

from lib.rz_chat import RzChatAPI

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@bp.route('/groups', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login
def get_groups_chat(user_info):
    uid = py_.get(user_info, 'id')

    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    page_size = Consts.PAGE_SIZE_DEFAULT

    pipelines = [
        {'$match': {
            "status": {"$ne": Consts.STATUS_INACTIVE},
            "users": uid,
        }},
    ]
    items = Repo.mChatGroup.aggregate(pipelines)

    items = py_.map_(items, Repo.mUser.map_item_user_info)
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.GroupItem(many=True).dump(items),
        "msg": "success"
    }


@bp.route('/author/<string:author_id>', methods=['GET', 'POST'])
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

    group_users = [author_id, uid]
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "users": {"$all": group_users},
        "chat_type": Consts.CHAT_TYPE_SINGLE
    }
    group_chat = Repo.mChatGroup.get_item_with(_filter)
    if request.method == 'POST':
        if not group_chat:
            group_chat = {
                "users": group_users,
                "chat_type": Consts.CHAT_TYPE_SINGLE
            }
            group_chat = Repo.mChatGroup.insert(group_chat)
        group_id = str(group_chat['id'])
        payload = request.json
        try:
            obj = SchemaResource.ItemUpdate().load(payload)
            obj["group_id"] = group_id
            result = Repo.mChat.insert(obj)
            # Publish Message to Socket Channel
            payload_pub = {
                "type": "live_chat",
                "content": obj["content"],
                "user": {
                    "user_name": py_.get(user_info, 'user_full_name', ''),
                    "user_avatar":  py_.get(user_info, 'user_avatar', ''),
                }
            }
            RzChatAPI.send_messgae(group_users, payload_pub, group_id)
            return {
                "status": Consts.OK,
                "error_code": HTTPStatus.OK,
                "data": SchemaResource.Item().dump(obj),
                "msg": ""
            }
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    data = []
    if group_chat:
        group_id = str(group_chat['_id'])
        _filter = {
            "status": {"$ne": Consts.STATUS_INACTIVE},
            "group_id": group_id
        }
        _sort = [("_id", -1)]
        data = Repo.mChat.get_list(_filter, _sort, page)
        data = py_.map_(data, lambda item: Repo.mUser.map_author(item, author))
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "msg": "Success"
    }


@bp.route('/groups/<string:oid>', methods=['POST'])
@Http.make_cross_resp
@Decorators.require_login
def chat_to_group(user_info, oid):
    item = Repo.mChatGroup.get_item(oid)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    uid = py_.get(user_info, 'id', -1)
    if uid not in item["users"]:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.FORBIDDEN,
            "data": {},
            "msg": ""
        }
    payload = request.json
    try:
        obj = SchemaResource.ItemUpdate().load(payload)
        obj["group_id"] = oid
        result = Repo.mChat.insert(obj)
        # Publish Message to Socket Channel
        payload_pub = {
            "type": "live_chat",
            "content": obj["content"],
            "user": {
                "user_name": py_.get(user_info, 'user_full_name', ''),
                "user_avatar":  py_.get(user_info, 'user_avatar', ''),
            }
        }
        RzChatAPI.send_messgae(item["users"], payload_pub, oid)
    except ValidationError as err:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.BAD_REQUEST,
            "data": err.messages,
            "msg": "Invalid format!"
        }

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item().dump(obj),
        "msg": "success"
    }
