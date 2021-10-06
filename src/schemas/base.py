from bson import ObjectId
import random as rd
import datetime as dt
import marshmallow as ma
import pydash as py_

import src.constants as Consts
import src.models.repo as Repo


class RzFieldDateTime(ma.fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, dt.datetime):
            raise ma.ValidationError("Value must be a datetime object")
        return int(value.timestamp())


class AuthorNameField(ma.fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value.isdigit():
            return '***' + value[-3:]
        return value


class SchemaFunc(object):
    @classmethod
    def generate_share_link(cls, obj, rtype):
        # print(obj)
        oid = py_.get(obj, '_id') or py_.get(obj, 'oid') or py_.get(obj, 'id')
        if rtype == Consts.RESOURCE_TYPE_IDOL:
            user_name = py_.get(obj, 'user_name') or 'rzmusic'
            return f"{Consts.RZ_SHARE_WEBSITE}/artist/{user_name}"
        if rtype == Consts.RESOURCE_TYPE_EVENT:
            return f"{Consts.RZ_SHARE_WEBSITE}/event/{oid}"
        rtype = Consts.RESOURCE_TYPE_TRACK
        return f"{Consts.RZ_SHARE_WEBSITE}/track/{oid}"

    @classmethod
    def generate_album_banner(cls, obj):
        img_banner = py_.get(obj, 'banner', '')
        if img_banner:
            return [img_banner]

        # Try to get banner from tracks images
        tracks = py_.get(obj, 'tracks', [])
        # print(len(tracks))
        n_imgs = 4 if len(tracks) >= 4 else 1
        track_oids = [ObjectId(track) for track in rd.sample(tracks, n_imgs)]
        # print(track_oids)
        # track_oids = []
        images = [py_.get(item, 'banner', '') for item in Repo.mTrack.get_list({
            "_id": {"$in": track_oids},
            "status": {"$ne": Consts.STATUS_INACTIVE}
        })]
        return images


class RzAddress(ma.Schema):
    tp_code = ma.fields.Str(required=True)
    qh_code = ma.fields.Str(required=True)
    xp_code = ma.fields.Str(required=True)
    so_nha = ma.fields.Str(required=True)


class RzCMND(ma.Schema):
    numbers = ma.fields.Str(required=True)
    issue_date = ma.fields.DateTime(format="%Y/%m/%d", required=True)
    issue_from = ma.fields.Str(required=True)
