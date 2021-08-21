import pydash as py_
from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http
import src.mocks.sitemaps as Sitemaps

bp = Blueprint('sitemaps', __name__, url_prefix='/api/sitemaps')


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cud_data():
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": Sitemaps.MOCKS,
        "msg": "success"
    }
