from bson import ObjectId
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.event as SchemaEvent
import src.schemas.track as SchemaTrack
import src.schemas.tweet as SchemaTweet
import src.schemas.album as SchemaAlbum
import src.schemas.user as SchemaUser
import src.decorators as Decorators

bp = Blueprint('follow', __name__, url_prefix='/api/follow')

RepoResource = Repo.mFollow


@bp.route('/<string:rtype>/<string:oid>', methods=['GET', 'POST', 'DELETE'])
@Http.make_cross_resp
@Decorators.require_login
def item_action(user_info, rtype, oid):
    collection = Repo.mTrack
    if rtype == Consts.RESOURCE_TYPE_EVENT:
        collection = Repo.mEvent
    if rtype == Consts.RESOURCE_TYPE_ALBUM:
        collection = Repo.mAlbum
    if rtype == Consts.RESOURCE_TYPE_TWEET:
        collection = Repo.mTweet
    if rtype == Consts.RESOURCE_TYPE_AUTHOR:
        collection = Repo.mUser
        oid = int(oid)
    item = collection.get_item(oid)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    obj = RepoResource.get_item_with({
        "oid": oid,
        "type": rtype
    })
    if not obj:
        RepoResource.insert({
            "oid": oid,
            "type": rtype,
            "followers": []
        })
    uid = py_.get(user_info, 'id', -1)
    if request.method == 'DELETE':
        result = RepoResource.update_raw(
            {
                "oid": oid,
                "type": rtype
            },
            {
                "$pull": {"followers": uid}
            }
        )

    followers = py_.get(obj, 'followers', [])
    if request.method == 'POST' and uid not in followers:
        result = RepoResource.update_raw(
            {
                "oid": oid,
                "type": rtype
            },
            {
                "$push": {"followers": uid}
            }
        )

    obj = RepoResource.get_item_with({
        "oid": oid,
        "type": rtype
    })
    followers = py_.get(obj, 'followers', [])
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": {
            "followers": followers
        },
        "msg": "success"
    }


@bp.route('/<string:rtype>', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login
def item_follow_list(user_info, rtype):
    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    page_size = Consts.PAGE_SIZE_DEFAULT
    uid = py_.get(user_info, 'id', -1)
    pipelines = [
        {"$match": {"type": rtype, "followers": uid}},
        {"$addFields": {"_oid": {"$toObjectId": "$oid"}}},
        {"$project": {"followers": 0}},
        {
            '$lookup': {
                'from': rtype,
                'localField': "_oid",
                'foreignField': "_id",
                'as': "data"
            }
        },
        {"$unwind": "$data"},
        {"$match": {"data.status": {"$ne": "inactive"}}},
        {"$sort": {"data.title": 1}},
        {'$skip': int((page - 1) * page_size)},
        {'$limit': page_size},
    ]
    collection = Repo.mTrack
    schema = SchemaTrack.Item
    if rtype == Consts.RESOURCE_TYPE_EVENT:
        collection = Repo.mEvent
        schema = SchemaEvent.Item
    if rtype == Consts.RESOURCE_TYPE_ALBUM:
        collection = Repo.mAlbum
        schema = SchemaAlbum.Item
    if rtype == Consts.RESOURCE_TYPE_TWEET:
        collection = Repo.mTweet
        schema = SchemaTweet.Item
    if rtype == Consts.RESOURCE_TYPE_AUTHOR:
        collection = Repo.mUser
        schema = SchemaUser.PublicItem
        pipelines = [
            {"$match": {"type": rtype, "followers": uid}},
            {"$project": {"followers": 0}},
            {
                '$lookup': {
                    'from': 'user',
                    'localField': "oid",
                    'foreignField': "_id",
                    'as': "data"
                }
            },
            {"$unwind": "$data"},
            {"$match": {"data.status": {"$ne": "inactive"}}},
            {"$sort": {"data.title": 1}},
            {'$skip': int((page - 1) * page_size)},
            {'$limit': page_size},
        ]

    objs = RepoResource.aggregate(pipelines)
    data = [py_.get(obj, 'data') for obj in objs]
    data = py_.map_(data, Repo.mUser.map_item_user_info)

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema(many=True).dump(data),
        "msg": "success"
    }
