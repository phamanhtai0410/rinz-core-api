from http import HTTPStatus
from flask import (
    Blueprint,
    request
)

from marshmallow import ValidationError

import src.models.repo as Repo
import src.constants as Consts
import src.middlewares.http as Http
import src.decorators as Decorators
import src.schemas.user as SchemaUser

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/me', methods=['GET', 'PUT'])
@Http.make_cross_resp
@Decorators.require_login
def user_info(user_info):
    uid = user_info["id"]
    if request.method == 'PUT':
        payload = request.json
        try:
            obj = SchemaUser.ItemUpdate().load(payload)
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
        "status": Consts.STATUS_NOT_OK,
        "error_code": HTTPStatus.OK,
        "data": SchemaUser.Item().dump(user_info),
        "msg": "Success"
    }
