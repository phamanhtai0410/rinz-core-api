import re
import pydash as py_
from bson import ObjectId
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
            obj = SchemaResource.ItemUpdate().load(payload, partial=True)
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
    item = Repo.PaymentGateway.map_item_info(
        item,
        Consts.RESOURCE_TYPE_TRACK,
        uid
    )
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
            obj_track = RepoResource.get_item_with({"url": obj["url"]})
            if obj_track:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.CONFLICT,
                    "data": {},
                    "msg": "This Track already exists!"
                }

            # Validate Category
            track_category = Repo.mMeta.get_item_with({
                "type": Consts.META_TYPE_TRACK_CATEGORY,
                "value": obj["category"]
            })
            if not track_category:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.BAD_REQUEST,
                    "data": {},
                    "msg": "Invalid Track Category"
                }

            obj["author_id"] = author_id
            obj["status"] = Consts.STATUS_PROCESSING
            print(obj)
            result = RepoResource.insert(obj)
            stream_obj = Repo.mStream.update_by_filter(
                {
                    "type": Consts.RESOURCE_TYPE_TRACK,
                    "oid": obj["url"],
                },
                {"author_id": author_id},
                True
            )
            print(stream_obj)
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
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "author_id": uid,
        "skip_geoip": True,
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


@bp.route('/paid', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login
def paid(user_info):
    uid = py_.get(user_info, 'id')
    _filter = {
        "status": Consts.PAYMENT_STATUS_PAID,
        "user_id": uid,
        "type": Consts.RESOURCE_TYPE_TRACK,
    }
    _sort = [("_id", -1)]

    s = request.args.get('s')
    if s:
        _filter["title"] = {"$regex": re.compile(s, re.IGNORECASE)}
        _sort = [("title", 1)]

    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    total = Repo.mPayment.get_count(_filter)
    paid_orders = Repo.mPayment.get_list(_filter, _sort, page)
    tracks_oid = [ObjectId(py_.get(ord, 'oid')) for ord in paid_orders]
    items = Repo.mTrack.get_list({
        "_id": {"$in": tracks_oid},
        "skip_geoip": True,
    })
    # data = py_.map_(items, Repo.mUser.map_item_user_info)
    resp_data = []
    for idt in items:
        idt = Repo.mUser.map_item_user_info(idt)
        idt['is_paid'] = True
        resp_data.append(idt)

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(resp_data),
        "total": total,
        "msg": "Success"
    }


@bp.route('/<string:oid>/related', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login_actions
def get_related(user_info, oid):
    item = RepoResource.get_item(oid)
    print(oid, item)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    uid = py_.get(user_info, 'id')
    _filter = {
        "status": {"$ne": Consts.STATUS_INACTIVE},
        "_id": {"$ne": ObjectId(oid)}
    }
    _sort = [("_id", -1)]

    data = RepoResource.get_list(_filter, _sort)
    resp_data = []
    for idt in data:
        idt = Repo.mUser.map_item_user_info(idt)
        idt = Repo.PaymentGateway.map_item_info(
            idt, Consts.RESOURCE_TYPE_TRACK, uid
        )
        resp_data.append(idt)

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(resp_data),
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
    # data = py_.map_(data, lambda item: Repo.mUser.map_author(item, author))
    resp_data = []
    for idt in data:
        idt = Repo.mUser.map_author(idt, author)
        idt = Repo.PaymentGateway.map_item_info(
            idt, Consts.RESOURCE_TYPE_TRACK, uid
        )
        resp_data.append(idt)

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaResource.Item(many=True).dump(resp_data),
        "msg": "Success"
    }
