import random
import pydash as py_
import marshmallow as ma

import src.constants as Consts

from .base import SchemaFunc, RzAddress, RzCMND


class Item(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Int()
    balance = ma.fields.Int()

    user_address = ma.fields.Nested(RzAddress)
    user_avatar = ma.fields.Str()
    user_bio = ma.fields.Str()
    user_birthday = ma.fields.Int()
    user_email = ma.fields.Str()
    user_full_name = ma.fields.Str()
    user_gender = ma.fields.Str()
    user_name = ma.fields.Str()
    user_password = ma.fields.Str()
    user_phone = ma.fields.Str()

    user_cmnd = ma.fields.Nested(RzCMND)

    livestream_url = ma.fields.Str()

    type = ma.fields.Str()

    official = ma.fields.Boolean(default=False)
    rzm_type = ma.fields.Function(
        lambda obj: random.choice(Consts.USER_TYPES)
    )
    rzm_level = ma.fields.Function(
        lambda obj: random.choice(Consts.USER_LEVELS)
    )

    followers = ma.fields.Function(lambda obj: random.randrange(100, 10000))
    following = ma.fields.Function(lambda obj: random.randrange(100, 1000))
    products = ma.fields.Function(lambda obj: random.randrange(0, 100))
    share_link = ma.fields.Function(
        lambda obj: SchemaFunc.generate_share_link(
            obj,
            Consts.RESOURCE_TYPE_IDOL
        ))


class ItemUpdate(ma.Schema):
    class Meta:
        ordered = True

    user_email = ma.fields.Email()
    user_address = ma.fields.Nested(RzAddress)
    user_avatar = ma.fields.Str()
    user_bio = ma.fields.Str()
    user_birthday = ma.fields.Str()
    user_full_name = ma.fields.Str()
    user_gender = ma.fields.Str()
    user_name = ma.fields.Str(
        validate=ma.validate.Regexp(r"^[a-zA-Z0-9\.-]+$")
    )

    user_cmnd = ma.fields.Nested(RzCMND)


class PublicItem(ma.Schema):
    id = ma.fields.Int()

    user_address = ma.fields.Str()
    user_avatar = ma.fields.Str()
    user_bio = ma.fields.Str()
    user_birthday = ma.fields.Int()
    user_email = ma.fields.Str()
    user_full_name = ma.fields.Str()
    user_gender = ma.fields.Str()
    user_name = ma.fields.Str()
    user_password = ma.fields.Str()
    user_phone = ma.fields.Str()

    type = ma.fields.Str()

    official = ma.fields.Boolean(default=False)
    rzm_type = ma.fields.Function(
        lambda obj: random.choice(Consts.USER_TYPES)
    )
    rzm_level = ma.fields.Function(
        lambda obj: random.choice(Consts.USER_LEVELS)
    )

    followers = ma.fields.Function(
        lambda obj: len(py_.get(obj, "followers", []))
    )
    following = ma.fields.Boolean(default=False)
    products = ma.fields.Function(lambda obj: random.randrange(0, 100))
    share_link = ma.fields.Function(
        lambda obj: SchemaFunc.generate_share_link(
            obj,
            Consts.RESOURCE_TYPE_IDOL
        ))