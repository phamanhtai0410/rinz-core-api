import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.comment as SchemaResource
import src.decorators as Decorators

bp = Blueprint('comment', __name__, url_prefix='/api/comment')

RepoResource = Repo.mComment


@bp.route('/<string:oid>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@Http.make_cross_resp
@Decorators.require_login
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
    if request.method == 'PATCH':
        action = py_.get(request.args, 'action', Consts.COMMENT_ACTION_LIKE)
        if action not in Consts.COMMENT_ACTIONS:
            action = Consts.COMMENT_ACTION_LIKE

        if action == Consts.COMMENT_ACTION_LIKE:
            RepoResource.action_user_like(uid, oid)
        if action == Consts.COMMENT_ACTION_UNLIKE:
            RepoResource.action_user_dislike(uid, oid)

        return {
            "status": Consts.STATUS_OK,
            "error_code": HTTPStatus.OK,
            "data": {},
            "msg": "success"
        }

    if request.method in Consts.REQUEST_ACTTIONS_METHODS \
            and uid in [py_.get(item, 'author_id'), py_.get(item, 'owner_id')]:
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
    content_id = py_.get(request.args, 'content_id')
    content_type = py_.get(request.args, 'content_type')
    parent_id = py_.get(request.args, 'parent_id', '')
    page = py_.get(request.args, 'page', 1)
    page_size = py_.get(request.args, 'page_size', 0)
    sort_type = py_.get(request.args, 'sort_type', Consts.SORT_TYPE_LASTEST)

    if not content_id or content_type not in Consts.RESOURCE_TYPES:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.BAD_REQUEST,
            "data": {},
            "msg": "Invalid content_id or content_type!"
        }

    collection = Repo.mTrack
    if content_type == Consts.RESOURCE_TYPE_EVENT:
        collection = Repo.mEvent
    if content_type == Consts.RESOURCE_TYPE_ALBUM:
        collection = Repo.mAlbum
    if content_type == Consts.RESOURCE_TYPE_TWEET:
        collection = Repo.mTweet
    if content_type == Consts.RESOURCE_TYPE_AUTHOR:
        collection = Repo.mUser
    item = collection.get_item(content_id)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    if request.method == 'POST':
        payload = request.json
        try:
            obj_default = {
                "owner_id": item["author_id"],
                "author_id": user_info["id"],
                "content_id": content_id,
                "content_type": content_type,
                "parent_id": parent_id,
                "status": Consts.STATUS_ACTIVE,
                "likes": [],
            }
            obj = SchemaResource.ItemUpdate().load(payload)
            obj = {**obj_default, **obj}
            print(obj)
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

    # Response Comment Level 1
    if not parent_id:
        data, total = RepoResource.get_list_comments(
            content_id,
            content_type,
            sort_type,
            page,
            page_size
        )
    else:
        data, total = RepoResource.get_childs(
            parent_id,
            sort_type,
            page,
            page_size
        )

    user_id = py_.get(user_info, 'id', -1)
    if user_id:
        for d in data:
            d['ucomment'] = bool(d['author_id'] == user_id)
            d['uliked'] = bool(user_id in d['likes'])

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(data),
        "total": total,
        "msg": "Success"
    }
