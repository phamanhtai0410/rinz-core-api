# -*- coding: utf-8 -*-

# .....%%%%%!.....%%%!!........%%!.......%!.........
# .....%!........%!..........%....%!.....%!.........
# .....%%%%%!.....%%%!!.....%......%!....%!.........
# .....%!.............%!.....%....%!.....%!.........
# .....%%%%%!.....%%%!.........%%!.......%%%%%%!....

# Created by ESOL TECHNOLOGY SOLUTION JOINT STOCK COMPANY
# More information: https://esoltech.net
# ----****----****----****----****----****----***----

# File: iapi.py	
# Created at 01/11/2021
"""
   Description: 
        - Allow internal calls
        -
"""
import traceback

import sentry_sdk
from flask import Blueprint, request

import src.constants as Consts
import src.models.repo as Repo
import src.middlewares.http as Http

bp = Blueprint('iapi', __name__, url_prefix='/iapi')


@bp.route('/event/<string:event_id>', methods=['PUT'])
@Http.make_cross_resp
def u_livestream_status(event_id: str):
    try:
        body = request.get_json()
        status = body.get('status')

        if status not in Consts.LIVE_STATUS:
            return {
                "status": Consts.STATUS_NOT_OK,
                "error_code": '',
                "data": {},
                "msg": f"'status' must be one of {str(Consts.LIVE_STATUS)}"
            }

        # TODO worker
        Repo.mEvent.update(event_id, {
            'status': status
        }, True)

        return {
            "status": Consts.STATUS_OK,
            "error_code": '',
            "data": {},
            "msg": ""
        }

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return {
            "status": Consts.STATUS_NOT_OK,
            "error_code": 'E_UNKNOWN',
            "data": {},
            "msg": "unknown error"
        }
