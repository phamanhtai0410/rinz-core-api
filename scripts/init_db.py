import requests

TRACKS_CATEGORIES = [
    "Dance & EDM",
    "Vinahouse",
    "Deep House",
    "Hip-hop & Rap",
    "Remix",
    "Nonstop",
    "Pop",
    "Classical",
    "Drum & Bass",
    "House",
    "Jazz & Blues",
    "Latin",
    "Metal",
    "Piano",
    "Soundtrack",
    "Rock",
    "Trap",
    "Triphop",
    "World",
    "Speech",
    "Indie",
    "Disco",
    "Dubstep",
    "Classical",
    "Other"
]

META_TYPE_TRACK_CATEGORY = 'track-category'


def create_metadate(name, type):
    resp = requests.post(
        "http://localhost:5000/v1/core-api/api/meta",
        json={
            "type": "track-category",
            "name": name
        }
    )
    print(resp)
    return resp.json()


for category in TRACKS_CATEGORIES:
    result = create_metadate(category, META_TYPE_TRACK_CATEGORY)
