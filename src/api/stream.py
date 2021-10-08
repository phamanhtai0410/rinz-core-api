import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.event as SchemaEvent
import src.schemas.track as SchemaTrack
import src.schemas.stream as SchemaStream
import src.decorators as Decorators

bp = Blueprint('stream', __name__, url_prefix='/api/stream')

RepoResource = Repo.mStream


@bp.route('/event/<string:oid>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def get_event_stream(user_info, oid):
    event = Repo.mEvent.get_item(oid)
    rtype = Consts.RESOURCE_TYPE_EVENT
    if not event:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Event"
        }

    stream = Repo.mStream.get_stream(oid, rtype, event)
    if not stream:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Stream"
        }

    uid = py_.get(user_info, 'id', -1)
    author_id = py_.get(event, 'author_id')
    is_owner = bool(uid == author_id)

    schema_item = SchemaStream.EventOwner() if is_owner else SchemaStream.EventConsumer()

    rz_point = py_.get(event, 'rz_point', 0)
    if not is_owner and rz_point > 0:
        # FLOW PAYMENT ORDER
        paid_order = Repo.PaymentGateway.get_paid_order(
            oid,
            rtype,
            uid,
            author_id
        )
        if not paid_order:
            items = [{
                "type": rtype,
                "value": SchemaEvent.Item().dump(event),
            }]
            exec_order = Repo.PaymentGateway.exec_order(
                oid, rtype, uid, items, rz_point, author_id
            )
            payment_url = py_.get(exec_order, 'transaction.payment_url', '')
            if not payment_url:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "data": {},
                    "msg": Consts.RESP_MSG["payment_error"]
                }

            obj_transaction = py_.get(exec_order, 'transaction', {})
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.NOT_ACCEPTABLE,
                "data": obj_transaction,
                "msg": Consts.RESP_MSG["payment_require"]
            }

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema_item.dump(stream),
        "msg": "success"
    }


@bp.route('/track/<string:oid>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def get_music_stream(user_info, oid):
    # results = Repo.mStream.get_random_items(
    #     {"type": "track", "streams": {"$exists": True}},
    #     size=1
    # )
    # stream = py_.get([item for item in results], 0)
    # schema_item = SchemaStream.Track()
    # return {
    #     "status": Consts.STATUS_OK,
    #     "error_code": HTTPStatus.OK,
    #     "data": schema_item.dump(stream),
    #     "msg": "success"
    # }
    rtype = Consts.RESOURCE_TYPE_TRACK
    track = Repo.mTrack.get_item(oid)
    if not track:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Track"
        }

    stream = Repo.mStream.get_stream(oid, rtype, track)
    if not stream:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": "Not found Stream of this Track"
        }

    uid = py_.get(user_info, 'id', -1)
    author_id = py_.get(track, 'author_id')
    is_owner = bool(uid == author_id)
    rz_point = py_.get(track, 'rz_point', 0)

    is_rz_vip = py_.get(user_info, 'rz_vip')
    if not is_rz_vip and not is_owner and rz_point > 0:
        # FLOW PAYMENT ORDER
        paid_order = Repo.PaymentGateway.get_paid_order(
            oid, rtype, uid, author_id)
        if not paid_order:
            items = [{
                "type": rtype,
                "value": SchemaTrack.Item().dump(track),
            }]
            exec_order = Repo.PaymentGateway.exec_order(
                oid, rtype, uid, items, rz_point, author_id
            )
            payment_url = py_.get(exec_order, 'transaction.payment_url', '')
            if not payment_url:
                return {
                    "status": Consts.STATUS_NOT_OK,
                    "error_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "data": {},
                    "msg": Consts.RESP_MSG["payment_error"]
                }

            obj_transaction = py_.get(exec_order, 'transaction', {})
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.NOT_ACCEPTABLE,
                "data": obj_transaction,
                "msg": Consts.RESP_MSG["payment_require"]
            }

    schema_item = SchemaStream.Track()
    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": schema_item.dump(stream),
        "msg": "success"
    }


@bp.route('', methods=['POST'])
@Http.make_cross_resp
@Decorators.require_api_key
def sync_encoded():
    payload = request.json
    try:
        rtype = py_.get(payload, 'type')
        if rtype not in Consts.RESOURCE_TYPE_ENCODEDS:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": {},
                "msg": "Invalid format resource type, It's must in `track, music, video` type!"
            }

        schema_update = SchemaStream.EncodedTrack()
        if rtype in [Consts.RESOURCE_TYPE_MUSIC, Consts.RESOURCE_TYPE_TRACK]:
            rtype = Consts.RESOURCE_TYPE_TRACK
        else:
            rtype = Consts.RESOURCE_TYPE_VIDEO
            schema_update = SchemaStream.EncodedVideo()

        obj = schema_update.load(payload)
        # # Check Item exists
        # obj_stream = RepoResource.get_item_with({
        #     "oid": obj["oid"],
        #     "type": rtype
        # })
        # if not obj_stream:
        #     return {
        #         "status": Consts.STATUS_NOT_OK,
        #         "error_code": HTTPStatus.NOT_FOUND,
        #         "data": {
        #             "url": obj["oid"],
        #             "type": rtype,
        #         },
        #         "msg": "This resource not available in our system. Please try again later."
        #     }
        obj["type"] = rtype
        print(obj)
        result = RepoResource.m_update_item_by_type(
            obj["oid"], rtype,
            obj, True
        )
        result = Repo.mTrack.update_by_filter(
            {"url": obj["oid"]},
            {"status": Consts.STATUS_ENCODED}
        )
        print(result)
        return {
            "status": Consts.STATUS_OK,
            "error_code": HTTPStatus.OK,
            "data": payload,
            "msg": "success"
        }

    except ValidationError as err:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.BAD_REQUEST,
            "data": err.messages,
            "msg": "Invalid format!"
        }
