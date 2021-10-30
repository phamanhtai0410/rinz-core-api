from datetime import datetime, date, timedelta

from flask import request

import src.constants as Consts


def json_decode_hook(obj):
    if '__datetime__' in obj:
        return datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")
    if b'__datetime__' in obj:
        return datetime.strptime(obj[b'as_str'], "%Y%m%dT%H:%M:%S.%f")
    return obj


def json_encode_hook(obj):
    if isinstance(obj, datetime):
        obj = {'__datetime__': True,
               'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    if isinstance(obj, date):
        dt = datetime.combine(obj.today(), datetime.min.time())
        obj = {'__datetime__': True,
               'as_str': dt.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


def json_encode_response(obj):
    if isinstance(obj, datetime):
        return obj.timestamp()
    if isinstance(obj, date):
        return datetime.combine(obj.today(), datetime.min.time()).timestamp()
    return obj


def get_headers():
    geo_ip = request.headers.get('X-GeoIP-Country-Code')
    geo_ip = Consts.GEO_IP_VN if geo_ip == Consts.GEO_IP_VN else Consts.GEO_IP_OTHER
    return {
        'geo_ip': geo_ip
    }
