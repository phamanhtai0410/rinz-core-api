import pydash as py_
from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.tracks as Tracks

bp = Blueprint('track', __name__, url_prefix='/api/track')


@bp.route('/<string:track_id>')
@Http.make_cross_resp
def get_item(track_id):
    page = py_.find(Tracks.MOCKS, {"id": track_id})

    if not page:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": Consts.ERROR_MISSING_DATA,
            "data": {},
            "msg": ""
        }
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": page,
        "msg": "success"
    }


@bp.route('/<string:track_id>/stream/<string:profile_id>')
@Http.make_cross_resp
def get_stream(track_id, profile_id):
    page = py_.find(
        Tracks.MOCKS_STREAMS,
        {"id": profile_id, 'track_id': track_id}
    )

    if not page:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": Consts.ERROR_MISSING_DATA,
            "data": {},
            "msg": ""
        }
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": page,
        "msg": "success"
    }


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
@Http.make_cross_resp
def cud_data():
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": Tracks.MOCKS,
        "msg": "success"
    }
