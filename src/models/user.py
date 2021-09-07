import pydash as py_
from hashlib import pbkdf2_hmac

from lib.rz_stream import RzStreamAPI
import src.constants as Consts
import src.schemas.stream as SchemaStream

from .base import BaseDAO


class UserDAO(BaseDAO):
    def map_item_user_info(self, item):
        print(item)
        author_id = py_.get(item, 'author_id')
        if not author_id:
            return item
        user_info = self.get_item(author_id)
        item["author_name"] = py_.get(user_info, 'user_full_name', '')
        item["author_avatar"] = py_.get(user_info, 'user_avatar', '')
        return item
