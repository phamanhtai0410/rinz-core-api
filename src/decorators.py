# -*- coding: utf-8 -*-
from functools import wraps
from http import HTTPStatus
from flask import request

from lib.rz_id import RZ_ID
import src.constants as Consts


def get_user_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'] if 'Authorization' in request.headers else ''
        user_info = RZ_ID.get_user_info(token)
        return f(user_info=user_info, *args, **kwargs)

    return decorated


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'] if 'Authorization' in request.headers else ''
        user_info = RZ_ID.get_user_info(token)
        if not user_info:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.UNAUTHORIZED,
                "data": {},
                "msg": "Require login!"
            }

        return f(user_info=user_info, *args, **kwargs)

    return decorated
