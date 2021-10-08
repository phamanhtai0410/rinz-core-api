from bson import ObjectId
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError
from sentry_sdk import capture_message

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.event as SchemaEvent
import src.schemas.track as SchemaTrack
import src.schemas.tweet as SchemaTweet
import src.schemas.album as SchemaAlbum
import src.decorators as Decorators

bp = Blueprint('report', __name__, url_prefix='/api/report')

RepoResource = Repo.mReport


@bp.route('/<string:rtype>/<string:oid>', methods=['POST'])
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
            "reports": []
        })

    report_type = py_.get(request.args, 'rpt_type', Consts.REPORT_TYPE_SPAM)
    uid = py_.get(user_info, 'id', -1)
    reports = py_.get(obj, 'reports', [])
    is_reported = py_.find(reports, lambda x: x["uid"] == uid)
    if request.method == 'POST' and not is_reported:
        result = RepoResource.update_raw(
            {
                "oid": oid,
                "type": rtype
            },
            {
                "$push": {
                    "reports": {
                        "uid": uid,
                        "type": report_type
                    }
                }
            }
        )
        len_reports = len(reports)
        if len_reports > Consts.NUM_REPORT_ALERT:
            # Alert Telegram for Admin
            capture_message(
                f"{rtype}-{oid}:-NEED REVIEW CONTENT. ({len_reports})")

        if len_reports > Consts.NUM_REPORT_PENDING:
            # Update resource to pending review
            collection.update_raw(
                {"_id": ObjectId(oid)},
                {"$set": {"status": Consts.STATUS_PENDING}}
            )

    obj = RepoResource.get_item_with({
        "oid": oid,
        "type": rtype
    })
    reports = py_.get(obj, 'reports', [])
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": {
            "reports": reports
        },
        "msg": "success"
    }
