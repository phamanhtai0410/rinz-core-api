from pymongo import MongoClient
import pydash as py_

mdb = MongoClient('mongodb://18.140.62.59:27017')['rzmusic']

for stream in mdb.stream.find({"type": "track"}):
    track_url = stream["oid"]
    track = mdb.track.find_one({"url": track_url})
    if track:
        mdb.track.update(
            {"url": track_url},
            {"$set": {
                "duration": py_.get(stream, "duration", 0),
                "streams": py_.get(stream, "streams", []),
                "screenshot": py_.get(stream, 'screenshot', ''),
                "waveform": py_.get(stream, 'waveform', {}),
                "status": "encoded"
            }},
            multi=True
        )
        print(track["title"])
    else:
        print("No track found", track_url)
        # break
