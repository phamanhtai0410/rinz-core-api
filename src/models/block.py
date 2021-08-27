from src.extensions import mdb as db
from .base import BaseDocument


class Page(BaseDocument):
    meta = {'strict': False}

    title = db.StringField()
    slug = db.StringField()

    status = db.StringField()