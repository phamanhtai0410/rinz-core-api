import traceback
import requests
import os

from http import HTTPStatus

import pydash as py_


class RZ_ID(object):
    RZ_ID_API = os.getenv('RZ_ID_API') or 'https://api-staging.thecuatui.net'
    RZ_ID_KEY = os.getenv('RZ_ID_KEY') or '8b65e82396d4c53296f36a1531ededca'

    @classmethod
    def get_user_info(cls, token: str) -> dict:
        try:
            if not token:
                return {}

            if not token.startswith('Bearer'):
                token = f"Bearer {token}"

            headers = {
                'ApiKey': cls.RZ_ID_KEY,
                'Authorization': token,
            }
            resp = requests.get(
                f"{cls.RZ_ID_API}/v1/id/user/me",
                headers=headers,
            )
            if resp.status_code == HTTPStatus.OK:
                obj = resp.json()
                return py_.get(obj, "data", {})
            return {}
        except:
            traceback.print_exc()
            return {}
