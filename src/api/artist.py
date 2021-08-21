import pydash as py_
from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.artist as Artist

bp = Blueprint('artist', __name__, url_prefix='/api/artist')


@bp.route('/<string:artist_id>')
def get_item(artist_id):
    print(artist_id)
    page = py_.find(Artist.MOCKS, {"id": artist_id})

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
        "data": Artist.MOCKS,
        "msg": "success"
    }
