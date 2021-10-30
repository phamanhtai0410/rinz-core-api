import pydash as py_

from .type import *

import src.constants as Consts
import src.functions as func

from .base import BaseDAO


class BaseGeoIP_DAO(BaseDAO):
    def _makup_item(self, obj):
        rz_point = py_.get(obj, 'rz_point')
        if rz_point is not None:
            if rz_point > 0:
                # FEE only for 'VN'
                obj["geo_ip"] = [Consts.GEO_IP_VN]
            else:
                # FREE for 'ALL'
                obj["geo_ip"] = [
                    Consts.GEO_IP_VN,
                    Consts.GEO_IP_OTHER
                ]
        return obj

    def _makup_filter(self, filter):
        # Add Geoip rule
        headers = func.get_headers()
        # with author of this resource, fetch all not block geoip
        is_author = py_.get(filter, 'is_author')
        if not is_author:
            geo_ip = py_.get(headers, 'geo_ip')
            filter["geo_ip"] = geo_ip
        filter.pop('is_author', None)
        return filter

    def insert(self, obj):
        obj = self._makup_item(obj)
        return super().insert(obj)

    def update(self, oid, obj, upsert=False):
        obj = self._makup_item(obj)
        return super().update(oid, obj, upsert)

    def update_raw(self, filter, raw_obj, upsert=False):
        raw_obj = self._makup_item(raw_obj)
        return super().update_raw(filter, raw_obj, upsert)

    def update_by_filter(self, filter, obj, upsert=False, multi=False):
        obj = self._makup_item(obj)
        return super().update_by_filter(filter, obj, upsert, multi)

    def get_list(self, filter={}, sort={}, page=1, page_size=PAGE_SIZE_DEFAULT):
        # print("- Before", filter)
        filter = self._makup_filter(filter)
        # print("- After", filter)
        return super().get_list(filter, sort, page, page_size)

    def get_random_items(self, filter={}, sort={}, size=1):
        # print("- Before", filter)
        filter = self._makup_filter(filter)
        # print("- After", filter)
        return super().get_random_items(filter, sort, size)
