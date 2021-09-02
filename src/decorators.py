# -*- coding: utf-8 -*-
from functools import wraps
from http import HTTPStatus
from src.api import user
from flask import request

from lib.rz_id import RzID
import src.constants as Consts
import src.models.repo as Repo
import src.schemas.user as SchemaUser


def get_rz_music_user_info():
    # FIXME: NEED ADD CACHE FUNCTION
    token = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    user_info = RzID.get_user_info(token)
    if not user_info:
        return {}

    uid = user_info["id"]
    rzm_user_info = Repo.mUser.get_item(uid) or {}
    user_info = {**user_info, **rzm_user_info}
    return user_info


def get_user_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info = get_rz_music_user_info()
        return f(user_info=user_info, *args, **kwargs)

    return decorated


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info = get_rz_music_user_info()
        if not user_info:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.UNAUTHORIZED,
                "data": {},
                "msg": "Require login!"
            }

        return f(user_info=user_info, *args, **kwargs)

    return decorated


def require_login_actions(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info = get_rz_music_user_info()
        if not user_info and request.method in Consts.REQUEST_ACTTIONS_METHODS:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.UNAUTHORIZED,
                "data": {},
                "msg": "Require login!"
            }

        return f(user_info=user_info, *args, **kwargs)

    return decorated
