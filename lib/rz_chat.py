import json
import traceback
import requests
import os
import datetime as dt
import marshmallow as ma
from http import HTTPStatus

import pydash as py_

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class RzChatAPI(object):
    API_URL = os.getenv('RZ_SOCKET_API') \
        or 'https://socket-staging.rinznetwork.com'

    @classmethod
    def send_messgae(cls, users, payload, room_id) -> dict:
        try:
            payload = {
                "type": "private",
                "room": room_id,
                "event": "message",
                "payload": payload,
                "users": users
            }
            resp = requests.post(
                f"{cls.API_URL}/v1/socket/send_to_room",
                json=payload,
            )
            if resp.status_code == HTTPStatus.OK:
                obj = resp.json()
                return py_.get(obj, "data", {})
            return {}
        except:
            traceback.print_exc()
            return {}

    @classmethod
    def send_public_message(cls, payload, room_id, author_id, event='message') -> dict:
        try:
            payload = {
                "type": "public",
                "room": room_id,
                "author_id": author_id,
                "event": event,
                "payload": payload,
                "users": []
            }
            resp = requests.post(
                f"{cls.API_URL}/v1/socket/send_to_room",
                json=payload,
            )
            if resp.status_code == HTTPStatus.OK:
                print("Publish Chat MSG Successfull")
                obj = resp.json()
                return py_.get(obj, "data", {})
            return {}
        except:
            traceback.print_exc()
            return {}
