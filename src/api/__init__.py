from .index import bp as rest_index
from .page import bp as rest_page
from .block import bp as rest_block
from .sitemaps import bp as rest_sitemap
from .artist import bp as rest_artist
from .track import bp as rest_track

DEFAULT_BLUEPRINTS = [
    rest_index,
    rest_page,
    rest_block,
    rest_sitemap,
    rest_artist,
    rest_track,
]
