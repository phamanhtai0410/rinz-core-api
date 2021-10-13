from datetime import datetime, date, timedelta


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
