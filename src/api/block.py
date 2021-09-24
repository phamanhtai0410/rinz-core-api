import json
import datetime as dt
import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.block as SchemaBlock
import src.schemas.album as SchemaAlbum
import src.schemas.track as SchemaTrack
import src.schemas.tweet as SchemaTweet
import src.schemas.event as SchemaEvent
import src.decorators as Decorators

bp = Blueprint('block', __name__, url_prefix='/api/block')

RepoResource = Repo.mBlock


@bp.route('/<string:oid>', methods=['GET'])
@Http.make_cross_resp
@Decorators.get_user_info
def get_item(user_info, oid):
    page = py_.get(request.args, 'page', 1)
    page = py_.to_integer(page) or 1
    block = RepoResource.get_item(oid)
    print(oid, block)
    if not block:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    block_type = py_.get(block, 'type')
    data = py_.get(block, 'data') or []
    schema = SchemaBlock.BaseBlock()
    if block_type == Consts.BLOCK_SEARCH_BAR:
        schema = SchemaBlock.SearchBar()

    if block_type == Consts.BLOCK_WIDGET_ICONS:
        schema = SchemaBlock.WidgetIcons()

    if block_type == Consts.BLOCK_SLIDER:
        schema = SchemaBlock.Slider()

    if block_type == Consts.BLOCK_NEW_FEED:
        schema = SchemaBlock.NewFeed()

    if block_type == Consts.BLOCK_TABS:
        schema = SchemaBlock.Tabs()

    if block_type == Consts.BLOCK_IDOL_LIVE and page == 1:
        schema = SchemaBlock.IdolLive()
        mdata = Repo.mEvent.get_list({
            "status": {"$ne": Consts.STATUS_INACTIVE},
            "start_time": {"$gte": dt.datetime.now()},
        }, [("start_time", 1)])

        for idt in mdata:
            print(idt)
            idt = Repo.mUser.map_item_user_info(idt)
            idt["live_stream"] = bool(
                py_.get(idt, "status") == Consts.STATUS_LIVE)
            idt["type"] = Consts.RESOURCE_TYPE_EVENT
            data.append(idt)

    if block_type == Consts.BLOCK_TOP_IDOL and page == 1:
        schema = SchemaBlock.TopIdol()
        mdata = Repo.mUser.get_random_items({
            "status": {"$ne": Consts.STATUS_INACTIVE},
        }, size=Consts.PAGE_SIZE_DEFAULT)

        for idt in mdata:
            idt["author_name"] = py_.get(idt, 'user_full_name', '')
            idt["author_avatar"] = py_.get(idt, 'user_avatar', '')
            data.append(idt)

    if isinstance(data, str):
        args_data = json.loads(data)
        args_data["user_id"] = py_.get(user_info, 'id', -1)
        args_data["page"] = int(page)
        item_type = py_.get(args_data, 'type')

        randomize = py_.get(args_data, 'randomize', False)
        if not(page > 1 and randomize):
            mdata = []
        else:
            mdata = Repo.factory_get_list(**args_data)
        print("GO HERE", item_type)
        # print(mdata)
        data = []
        for idt in mdata:
            # print(idt)
            idt = Repo.mUser.map_item_user_info(idt)
            idt["type"] = item_type
            data.append(idt)

        if item_type == Consts.RESOURCE_TYPE_ALBUM:
            data = SchemaAlbum.Item(many=True).dump(data)
        if item_type == Consts.RESOURCE_TYPE_TRACK:
            data = SchemaTrack.Item(many=True).dump(data)
        if item_type == Consts.RESOURCE_TYPE_TWEET:
            data = SchemaTweet.Item(many=True).dump(data)
        if item_type == Consts.RESOURCE_TYPE_EVENT:
            data = SchemaEvent.Item(many=True).dump(data)

    block["data"] = data
    # print(data)
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": schema.dump(block),
        "msg": "success"
    }
