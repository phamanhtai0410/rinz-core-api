# -*- coding: utf-8 -*-
from functools import wraps
from src.utils import json_encode_hook, json_decode_hook, jsonify_dict, log_any
from src.extensions import redis_cache, redis_cluster
from flask import request, abort
from sentry_sdk import capture_exception
import msgpack
import jwt
import traceback
import json


CACHE_TIMEOUT_FACTOR = 1
OPEN_CACHE = True


# timeout = 1 day
def cache_filter(timeout=86400, key_prefix='common', key_fields=[], options=[], keep_timeout=False):
    """
    Decorator for caching functions by filter
    Returns the cached value, or the function if the cache is disabled
    """
    if timeout is None:
        timeout = 86400

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _filter = dict()
            for key_field in key_fields:
                _filter[key_field] = kwargs.get(key_field)
            _options = kwargs.get('options', {})
            for option in options:
                _filter[option] = _options.get(option)

            key = "%s:%s" % (key_prefix, jsonify_dict(_filter))
            output = redis_cluster.get(key)
            if output:
                return json.loads(output, object_hook=json_decode_hook)
            output = f(*args, **kwargs)
            # log_any(output)
            # Set data to redis
            redis_cluster.setex(key, timeout, json.dumps(
                output, default=json_encode_hook))
            return output

        return wrapper

    return decorator


def auth_user():
    """
    Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request:  # Outside flask app context
                decorated_kwargs = {**kwargs, 'user_info': None}
                return f(*args, **decorated_kwargs)

            rq_user_token = request.headers.get('Authorization')
            if not rq_user_token or 'Bearer ' not in rq_user_token:
                abort(401)

            log_any(rq_user_token)

            rq_user_token = rq_user_token.split(' ')[1]
            # Get user token on Redis user info
            token_existed = redis_cluster.get("token:{}".format(rq_user_token))
            user_info = None
            if token_existed:  # In case user info exists, decode it
                try:
                    user_info = jwt.decode(rq_user_token, algorithm="RS256", options={
                                           "verify_signature": False})
                except:
                    traceback.print_exc()
                    capture_exception()

            if not user_info:
                abort(401)

            decorated_kwargs = {
                **kwargs, 'user_info': user_info.get('payload', {})}
            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator
