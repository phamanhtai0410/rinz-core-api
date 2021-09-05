from pymongo import MongoClient


mdb = MongoClient('mongodb://18.140.62.59:27017')['rzmusic']

for item in mdb.encoded.find({"type": "music"}):
    obj = {
        'streams': item['streams'],
        "type": "track",
        "oid": item["url"],
        "download": item["download"],
        "author_id": -1,
        "author_name": "Rz Music",
    }
    mdb.stream.insert(obj)
