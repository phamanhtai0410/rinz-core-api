import pydash as py_
from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.blocks as Blocks

bp = Blueprint('block', __name__, url_prefix='/api/block')


@bp.route('/<string:block_id>')
def get_item(block_id):
    print(block_id)
    page = py_.find(Blocks.MOCKS, {"id": block_id})

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
def cud_data():
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": Blocks.MOCKS,
        "msg": "success"
    }
