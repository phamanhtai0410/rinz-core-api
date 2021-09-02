import json
import traceback
import requests
import os
import datetime as dt

from http import HTTPStatus

import pydash as py_

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class RzStreamAPI(object):
    API_URL = os.getenv('RZ_STREAM_API') \
        or 'https://api-staging.rinznetwork.com/v1/livestream'
    API_KEY = os.getenv('RZ_STREAM_KEY') \
        or '8b65e82396d4c53296f36a1531ededca'

    @classmethod
    def iapi_generate_stream(cls, user_id, live_id, event_start_time, service='rinzmusic', user_phone="") -> dict:
        try:
            if not any(field for field in [user_id, live_id, event_start_time]):
                raise Exception("Missing require fields iapi_generate_stream")

            if isinstance(event_start_time, dt.datetime):
                event_start_time = event_start_time.strftime(DATETIME_FORMAT)

            headers = {
                'ApiKey': cls.API_KEY,
            }
            payload = {
                "user_id": user_id,
                "live_event_id": live_id,
                "service": service,
                "event_start_time": event_start_time,
                "user_phone": user_phone
            }
            resp = requests.post(
                f"{cls.API_URL}/iapi/generate_stream",
                json=payload,
                headers=headers,
            )
            if resp.status_code == HTTPStatus.OK:
                obj = resp.json()
                return py_.get(obj, "data", {})
            return {}
        except:
            traceback.print_exc()
            return {}
