from .user import bp as rest_user
from .index import bp as rest_index
from .page import bp as rest_page
from .block import bp as rest_block
from .sitemaps import bp as rest_sitemap
from .artist import bp as rest_artist
from .track import bp as rest_track
from .event import bp as rest_event
from .meta import bp as rest_meta
from .stream import bp as rest_stream
from .tweet import bp as rest_tweet
from .album import bp as rest_album
from .follow import bp as rest_follow
from .music import bp as rest_music

DEFAULT_BLUEPRINTS = [
    rest_index,
    rest_user,
    rest_page,
    rest_block,
    rest_sitemap,
    rest_artist,
    rest_track,
    rest_event,
    rest_meta,
    rest_stream,
    rest_tweet,
    rest_album,
    rest_follow,
    rest_music,
]
