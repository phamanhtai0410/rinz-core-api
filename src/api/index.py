from http import HTTPStatus
from flask import Blueprint

import src.constants as Consts
import src.middlewares.http as Http

bp = Blueprint('index', __name__, url_prefix='/common')


@bp.route('debug')
def debug():
    1/0
    return ''


@bp.route('health_check')
def health_check():
    return {
        "code": HTTPStatus.OK,
        "msg": "success"
    }


@bp.route('reset')
def reset_mock_data():
    return {
        "code": HTTPStatus.OK,
        "msg": "success"
    }
