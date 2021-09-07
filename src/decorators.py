# -*- coding: utf-8 -*-
from functools import wraps
from http import HTTPStatus
from src.api import user
from flask import request
import pydash as py_

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
    if not rzm_user_info:
        # print(user_info)
        Repo.mUser.update(uid, user_info, True)
        print(f"- CREATED NEW USER SUCCESSFUL: {uid}")

    # This information get realtime from thecuatui, not saved in rzmusic
    # Get latest balance or change to check redis key if have any user info caching before this line
    REALTIME_INFO = ['balance']
    for attr in REALTIME_INFO:
        rzm_user_info.pop(attr, None)
    user_info = {**user_info, **rzm_user_info}

    return user_info


def get_user_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info = get_rz_music_user_info()
        return f(user_info=user_info, *args, **kwargs)

    return decorated


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = py_.get(request.headers, 'ApiKey', '')
        if api_key not in Consts.VALIDATE_API_KEYS:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.FORBIDDEN,
                "data": {},
                "msg": "API KEY INVALID!"
            }
        return f(*args, **kwargs)

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
