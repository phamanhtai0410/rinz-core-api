# -*- coding: utf-8 -*-
import json
from functools import wraps
from http import HTTPStatus
from src.api import user
from flask import request
import pydash as py_

from lib.rz_id import RzID
from src.extensions import redis_cluster
import src.functions as func
import src.constants as Consts
from src.extensions import faker
# import src.schemas.user as SchemaUser


def cache_filter(timeout=86400, key_prefix='common', key_fields=[], options=[], expires_time=False):
    """
    Decorator for caching functions by filter
    Returns the cached value, or the function if the cache is disabled
    """
    if timeout is None:
        timeout = 86400

    if not expires_time:
        expires_time = timeout

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # print(args, kwargs)
            # user_id, limit, offset {}
            _filter = dict()
            for key_field in key_fields:
                _filter[key_field] = kwargs.get(key_field)
            _options = kwargs.get('options', {})
            for option in options:
                _filter[option] = _options.get(option)
            # Remove below to clear cache
            #_filter['expires_time'] = expires_time
            key = "%s:%s" % (
                key_prefix,
                json.dumps(_filter, default=func.json_encode_hook)
            )
            output = redis_cluster.get(key)
            if output:
                # print('HIT', key)
                return json.loads(output, object_hook=func.json_decode_hook)
            print('MISS', key)
            output = f(*args, **kwargs)
            # Set data to redis
            redis_cluster.setex(
                key, timeout,
                json.dumps(output, default=func.json_encode_hook)
            )

            return output

        return wrapper

    return decorator


def get_rz_music_user_info():
    import src.models.repo as Repo
    # FIXME: NEED ADD CACHE FUNCTION
    token = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    user_info = RzID.get_user_info(token)
    if not user_info:
        return {}

    uid = user_info["id"]
    rzm_user_info = Repo.mUser.get_item(uid) or {}
    if not rzm_user_info:
        # print(user_info)
        #FIXME: fake name and avatar for new users to demo - remove later
        if not py_.get(user_info, 'user_full_name', ''):
            user_info['user_full_name'] = faker.name()
        if not py_.get(user_info, 'user_avatar', ''):
            # hard code random image for user
            user_info['user_avatar'] = f'https://s3.ap-southeast-1.amazonaws.com/images.rinz.io/rinz/2022/11/28/{random.randint(1, 30)}.jpeg'
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
