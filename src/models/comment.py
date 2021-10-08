from bson import ObjectId
import pydash as py_

import src.constants as Consts

from .base import BaseDAO
from .type import *


class CommentDAO(BaseDAO):
    def get_list_comments(self, content_id, content_type, sort_type, page, page_size):
        # sort_type: default lastest
        _sort = {'pin_top': -1, '_id': -1}
        if sort_type == Consts.SORT_TYPE_OLDEST:
            _sort = {'pin_top': -1, '_id': 1}
        if sort_type == Consts.SORT_TYPE_LIKE:
            _sort = {'pin_top': -1, 'nlike': -1}

        page_size = page_size if page_size and page_size <= PAGE_SIZE_MAX else PAGE_SIZE_DEFAULT
        page = 1 if not page else page
        _skip = (page - 1) * page_size

        _filter = {
            "content_id": content_id,
            "content_type": content_type,
            "parent_id": "",
            "status": Consts.STATUS_ACTIVE,
        }

        total = self.db.find(_filter).count()

        datas = self.db.aggregate([
            {'$match': _filter},
            {'$sort': _sort},
            {'$skip': _skip},
            {'$limit': page_size},
            {
                "$addFields": {
                    "s_id": {
                        "$toString": "$_id"
                    }
                }
            },
            {
                '$lookup': {
                    'from': "comment",
                    'localField': "s_id",
                    'foreignField': "parent_id",
                    'as': "childs"
                }
            },
            {
                '$addFields': {
                    'nreply': {'$size': '$childs'}
                }
            },
            {
                "$project": {
                    "childs": 0,
                    "logs": 0,
                    "note": 0,
                    "s_id": 0,
                    "author_ip": 0,
                    "platform": 0,
                    "approved": 0,
                    "approved_by": 0,
                    "approved_time": 0,
                }
            }
        ])

        return list(datas), int(total)

    def get_childs(self, parent_id, sort_type, page, page_size):
        _filter = {'parent_id': parent_id, "status": Consts.STATUS_ACTIVE}

        # default is _type == 'lastest':
        _sort = [('_id', -1)]
        if sort_type == Consts.SORT_TYPE_OLDEST:
            _sort = [('_id', 1)]
        if sort_type == Consts.SORT_TYPE_LIKE:
            _sort = [('nlike', -1)]

        page_size = page_size if page_size and page_size <= PAGE_SIZE_MAX else PAGE_SIZE_DEFAULT
        page = 1 if not page else page

        _skip = (page - 1) * page_size

        query = self.db.find(_filter)
        total = query.count()
        datas = query.sort(_sort).skip(_skip).limit(page_size)

        # pipelines = [
        #     {'$match': _filter},
        #     {'$sort': _sort},
        #     {'$skip': _skip},
        #     {'$limit': page_size},
        #     {
        #         '$addFields': {
        #             'nreply': 0,
        #         }
        #     },
        #     {
        #         "$project": {
        #             "childs": 0,
        #             "logs": 0,
        #             "note": 0,
        #             "s_id": 0,
        #             "author_ip": 0,
        #             "platform": 0,
        #             "approved": 0,
        #             "approved_by": 0,
        #             "approved_time": 0,
        #         }
        #     }
        # ]

        return list(datas), int(total)

    def action_user_like(self, user_id, comment_id):
        self.db.update_one(
            {"_id": ObjectId(comment_id)},
            {
                '$push': {'likes': user_id},
                '$inc': {'nlike': 1}
            }
        )

    def action_user_dislike(self, user_id, comment_id):
        self.db.update_one(
            {"_id": ObjectId(comment_id)},
            {
                '$pull': {'likes': user_id},
                '$inc': {'nlike': -1}
            }
        )
