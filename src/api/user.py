from http import HTTPStatus
from flask import (
    Blueprint,
    request
)

from marshmallow import ValidationError
import random

import pydash as py_
import src.models.repo as Repo
import src.constants as Consts
import src.middlewares.http as Http
import src.decorators as Decorators
import src.schemas.user as SchemaUser
from src.extensions import faker

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/me', methods=['GET', 'PUT'])
@Http.make_cross_resp
@Decorators.require_login
def user_info(user_info):
    uid = user_info["id"]
    if request.method == 'PUT':
        payload = request.json
        try:
            obj = SchemaUser.ItemUpdate().load(payload, partial=True)    
            user_info = {**user_info, **obj}
            result = Repo.mUser.update(uid, user_info, True)
        except ValidationError as err:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": HTTPStatus.BAD_REQUEST,
                "data": err.messages,
                "msg": "Invalid format!"
            }

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaUser.Item().dump(user_info),
        "msg": "Success"
    }


@bp.route('/author/<author_id>', methods=['GET'])
@Http.make_cross_resp
@Decorators.require_login
def author_info(user_info, author_id):
    uid = user_info["id"]
    author_id = py_.to_integer(author_id)
    item = Repo.mUser.get_item(author_id)
    if not item:
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": HTTPStatus.NOT_FOUND,
            "data": {},
            "msg": ""
        }

    item = Repo.mFollow.map_follow_info(
        Consts.RESOURCE_TYPE_AUTHOR,
        author_id, uid, item
    )

    return {
        "status": Consts.STATUS_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaUser.PublicItem().dump(item),
        "msg": "Success"
    }
