track_1 = {
    "id": "track-1",
    "name": "Trai Thành Phố Lớn",
    "astist_id": "binz",
    "astist_name": "BinZ",
    "duration": 180,
    "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png",
    "rz_point": 50000,
    "profiles": [
        {
            "id": "track-stream-1",
            "type": "free",
            "name": "FREE",
        },
        {
            "id": "track-stream-2",
            "type": "vip",
            "name": "VIP",
        }
    ],
    "lyric": "lyric_id_1",
    "download": True,
    "create_date": "2021-08-10 10:10:10",
}

MOCKS = [track_1]
MOCKS_STREAMS = [
    {
        "id": "track-stream-1",
        "track_id": "track-1",
        "type": "free",
        "name": "FREE",
        "stream_url": "http://test.rinznetwork.com/hls/vinaluxhouse_320/playlist.m3u8"
    },
    {
        "id": "track-stream-2",
        "track_id": "track-1",
        "type": "vip",
        "name": "VIP",
        "stream_url": "http://test.rinznetwork.com/hls/vinaluxhouse_320/playlist.m3u8"
    },
]
