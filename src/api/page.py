import pydash as py_
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.pages as Pages

bp = Blueprint('page', __name__, url_prefix='/api/page')


@bp.route('/<string:page_id>')
@Http.make_cross_resp
def get_item(page_id):
    print(page_id)
    page = py_.find(Pages.MOCKS, {"id": page_id})

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
        "data": Pages.MOCKS,
        "msg": "success"
    }
