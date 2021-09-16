import json
import traceback
import requests
import os
import datetime as dt
import marshmallow as ma
from http import HTTPStatus

import pydash as py_

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class RzPaymentAPI(object):
    API_URL = os.getenv('RZ_PAYMENT_API') \
        or 'https://paygw-staging.rinznetwork.com/v1/payment'
    API_KEY = os.getenv('RZ_PAYMENT_KEY') \
        or '8b65e82396d4c53296f36a1531ededca'

    def __init__(self, db):
        if not db:
            raise Exception("Must has db orders info")
        self.db = db

    @classmethod
    def iapi_transaction(cls, user_id, price, order_type, items, merchant_id, noted, provider='rinz_points', return_url='webview') -> dict:
        try:
            headers = {
                'ApiKey': cls.API_KEY,
            }
            payload = {
                "price": price,
                "noted": "noted",
                "from_service": "rinz-music",
                "orders": [
                    {
                        "price": price,
                        "order_type": order_type,
                        "address": {},
                        "items": items,
                        "transport_fee": 0,
                        "user_id": user_id,
                        "noted": "noted",
                        "merchant_id": "khoapd",
                        "coupon": {},
                        "discount": 0,
                        "delivery": {}
                    }
                ],
                "provider": "rinz_points",
                "user_id": user_id,
                "return_url": "webview"
            }
            resp = requests.post(
                f"{cls.API_URL}/transaction/init",
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
