import datetime as dt
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.block as SchemaBlock
import src.decorators as Decorators

bp = Blueprint('block', __name__, url_prefix='/api/block')

RepoResource = Repo.mBlock


@bp.route('/<string:oid>', methods=['GET'])
@Http.make_cross_resp
def get_item(oid):
    item = RepoResource.get_item(oid)
    print(oid, item)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    block_type = py_.get(item, 'type')
    schema = SchemaBlock.BaseBlock()
    if block_type == Consts.BLOCK_SEARCH_BAR:
        schema = SchemaBlock.SearchBar()
        data = []

    if block_type == Consts.BLOCK_IDOL_LIVE:
        schema = SchemaBlock.IdolLive()
        data = Repo.mEvent.get_list({
            "status": {"$ne": Consts.STATUS_INACTIVE},
            # "start_time": {"$gte": dt.datetime.now()},
        }, [("start_time", -1)])

    item["data"] = data
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": schema.dump(item),
        "msg": "success"
    }
