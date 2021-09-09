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
