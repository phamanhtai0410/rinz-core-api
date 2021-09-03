import pydash as py_
from http import HTTPStatus
from flask import (Blueprint, request)

from marshmallow import ValidationError

import src.constants as Consts
import src.middlewares.http as Http
import src.models.repo as Repo
import src.schemas.meta as SchemaMeta

from slugify import slugify

bp = Blueprint('meta', __name__, url_prefix='/api/meta')


@bp.route('/<string:oid>', methods=['GET', 'PUT', 'DELETE'])
@Http.make_cross_resp
def get_item(oid):
    item = Repo.mMeta.get_item(oid)
    print(oid, item)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": Consts.ERROR_MISSING_DATA,
            "data": {},
            "msg": ""
        }

    if request.method == 'DELETE':
        force = py_.get(request.args, 'force', False)
        print(force)
        result = Repo.mMeta.delete(oid, force)
        return {
            "status": Consts.STATUS_OK,
            "error_code": Consts.NOT_E,
            "data": bool(result),
            "msg": "success"
        }

    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": SchemaMeta.Item().dump(item),
        "msg": "success"
    }


@bp.route('', methods=['GET', 'POST'])
@Http.make_cross_resp
def crud():
    if request.method == 'POST':
        payload = request.json
        try:
            obj = SchemaMeta.ItemUpdate().load(payload)
            print(obj)
            slug = slugify(obj["name"])
            obj["slug"] = slug
            if not py_.get(obj, "value"):
                obj["value"] = slug

            item = Repo.mMeta.insert(obj)
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.OK,
                "data": SchemaMeta.Item().dump(item),
                "msg": "Success"
            }
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    _filter = {}
    _type = py_.get(request.args, 'type')

    if _type and _type in Consts.META_TYPES:
        _filter = {'type': _type}

    data = Repo.mMeta.get_list(_filter, [("name", 1)])
    return {
        "status": Consts.STATUS_OK,
        "error_code": Consts.NOT_E,
        "data": SchemaMeta.Item(many=True).dump(data),
        "msg": "Success"
    }
