import pydash as py_
from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.event as Events

bp = Blueprint('event', __name__, url_prefix='/api/event')


@bp.route('/<string:event_id>')
@Http.make_cross_resp
def get_item(event_id):
    item = py_.find(Events.MOCKS, {"id": event_id})

    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": Consts.ERROR_MISSING_DATA,
            "data": {},
            "msg": ""
        }
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": item,
        "msg": "success"
    }
