BLOCK_SEARCH_BAR = "BLOCK_SEARCH_BAR"
mock_search_bar = {
    "id": "block_search_bar",
    "type": BLOCK_SEARCH_BAR,
    "meta": {
        "placeholder": "Tìm kiếm",
        "voice": True,
    }
}

BLOCK_IDOL_LIVE = "BLOCK_IDOL_LIVE"
mock_idol_live = {
    "type": BLOCK_IDOL_LIVE,
    "id": "block_idol_live",
    "data": [
        {
            "author_name": "Trang Moon",
            "author_id": 248,
            "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835153.22718_1.png",
            "live_stream": True,
            "type": "livestream" 
        },
        {
            "author_name": "Soda",
            "author_id": 248,
            "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835169.962013_2.png",
            "live_stream": True,
            "type": "livestream" 
        },
        {
            "author_name": "Alan Walker",
            "author_id": 248,
            "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835186.406358_3.png",
            "live_stream": True,
            "type": "livestream" 
        },
        {
            "author_name": "Đen Vâu",
            "author_id": 248,
            "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835197.565234_4.png",
            "live_stream": False,
            "type": "livestream" 
        },
        {
            "author_name": "Binz",
            "author_id": 248,
            "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835210.724095_5.png",
            "live_stream": False,
            "type": "livestream" 
        },
    ],
    "meta": {}
}
BLOCK_WIDGET_ICONS = "BLOCK_WIDGET_ICONS"
mock_widget_menus = {
    "type": BLOCK_WIDGET_ICONS,
    "id": "block_widget_icons_1",
    "meta": {},
    "data": [
        {
            "name": "Newfeed",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718338.634737_news.png",
            "type": "#"
        },
        {
            "name": "Single",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718555.391836_micrro.png",
            "type": "#"
        },
        {
            "name": "Group",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718593.756582_group.png",
            "type": "#"
        },
        {
            "name": "Artist",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718909.944816_artist.png",
            "type": "#"
        },
        {
            "name": "Producer",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718946.179783_dj.png",
            "type": "#"
        },
        {
            "name": "Music",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718986.420902_headphone.png",
            "type": "#"
        },
        {
            "name": "Rapper",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629719033.21609_rapper.png",
            "type": "#"
        },
        {
            "name": "Talks Video",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629719058.737185_video.png",
            "type": "#"
        },
    ]
}
BLOCK_SLIDER = "BLOCK_SLIDER"
mock_slider_lich_livestream = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_lich_livestream",
    "meta": {
        "title": "Lịch Live Stream",
        "type": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "#",
        "data_type": "event",
        "rows": 1
    },
    "data": [
        {
            "id": "613033af6c5a390b818098c7",
            "author_id": 248,
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718809.065704_live1.png",
            "rz_point": 50000,
            "title": "Phá đảo mọi giới hạn Bứt phá mọi cuộc chơi",
            "followers": 10000,
            "type": "livestream",
            "duration": 3600
        },
        {
            "id": "613033af6c5a390b818098c7",
            "author_id": 248,
            "artst_name": "Alan Walker",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718820.854798_live2.png",
            "rz_point": 50000,
            "title": "Quẩy lên nào bà coan ư ư ư....",
            "followers": 10000,
            "type": "livestream",
            "duration": 3600
        }
    ]
}
mock_slider_top_music = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_top_music",
    "meta": {
        "title": "Top Music",
        "type": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "/music",
        "data_type": "music",
        "rows": 1
    },
    "data": [
        {
            "id": "track1",
            "author_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png",
            "rz_point": 50000,
            "title": "Mixtape lên mây",
            "followers": 10000,
            "type": "music",
            "duration": 3600
        },
        {
            "id": "track2",
            "author_id": "dj-quang-minnh",
            "artst_name": "Justin Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Mixtape Peaches",
            "followers": 10000,
            "type": "music",
            "duration": 3600
        },
        {
            "id": "track3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "music",
            "duration": 3600
        },
    ]
}
BLOCK_TOP_IDOL = "BLOCK_TOP_IDOL"
mock_top_idol = {
    "type": BLOCK_TOP_IDOL,
    "id": "mock_top_idol",
    "meta": {
        "title": "Top Idol",
        "type": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "/idols",
        "data_type": "idols"
    },
    "data": [
        {
            "id": 248,
            "name": "Justin Bieber",
            "avatar": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835210.724095_5.png",
            "type": "livestream",
            "following": False,
        },
        {
            "id": 248,
            "name": "Soda",
            "avatar": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835197.565234_4.png",
            "type": "livestream",
            "following": True,
        },
        {
            "id": "justin-bieber",
            "name": "BinZ",
            "avatar": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835186.406358_3.png",
            "type": "livestream",
            "following": True,
        },
    ]
}
BLOCK_NEW_FEED = "BLOCK_NEW_FEED"
BLOCK_TABS = "BLOCK_TABS"
mock_feed_all = {
    "type": BLOCK_NEW_FEED,
    "id": 'mock_feed_all',
    "meta": {},
    "data": [
        {
            "id": "feed1",
            "author_id": "alan-walker",
            "content": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo culpa blanditiis neque veritatis animi non facere dicta dolores ratione accusamus pariatur, aut quos rem earum consectetur! Ducimus assumenda itaque voluptas.Quasi veritatis corporis odit mollitia, autem iusto fugit perferendis fugiat, perspiciatis voluptatibus molestiae dolore optio ea voluptatem dolores non laboriosam quam nobis. Inventore nulla illo perspiciatis, at officia consequuntur adipisci.",
            "name": "Alan Walker",
            "avatar": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835186.406358_3.png",
            "created_date": "2021-08-10 10:10:10",
            "images": [
                "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718661.597107_feed1.png",
                "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718687.819476_feed2.png"
            ]
        },
        {
            "id": "feed2",
            "author_id": "binz",
            "content": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo culpa blanditiis neque veritatis animi non facere dicta dolores ratione accusamus pariatur, aut quos rem earum consectetur! Ducimus assumenda itaque voluptas.Quasi veritatis corporis odit mollitia, autem iusto fugit perferendis fugiat, perspiciatis voluptatibus molestiae dolore optio ea voluptatem dolores non laboriosam quam nobis. Inventore nulla illo perspiciatis, at officia consequuntur adipisci.",
            "name": "BinZ",
            "avatar": "https://static.rinznetwork.com/rinzmusic/images/2021/08/25/1629835210.724095_5.png",
            "created_date": "2021-08-10 10:10:10",
            "images": [
                "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718661.597107_feed1.png"
            ]
        },
    ]
}
mock_tabs = {
    "type": BLOCK_TABS,
    "id": "mock_tabs",
    "meta": {
        "image": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629719775.600669_newfeed.png",
        "type": "/feed",
    },
    "data": [
        {
            "id": "mock_feed_all",  # block_id
            "name": "Tất cả",
            "type": "render",
            "type": ""
        },
        {
            "id": "",
            "name": "RinZ Music",
            "type": "direct",
            "type": "<site-map-route>"
        },
        {
            "id": "",
            "name": "Idol",
            "type": "direct",
            "type": "<site-map-route>"
        },
    ]
}

BLOCK_NEW_TWEET = 'BLOCK_NEW_TWEET'
mock_creator_new_tweet = {
    "id": "new_tweet_1",
    "type": BLOCK_NEW_TWEET,
    "meta": {
        "text": u"Bạn đang nghĩ gì?"
    },
    "data": {}
}

mock_creator_icons = {
    "id": "block_creator_icons",
    "type": BLOCK_WIDGET_ICONS,
    "meata": {},
    "data": [
        {
            "name": "Upload nhạc",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718338.634737_news.png",
            "type": "#"
        },
        {
            "name": "Tạo Album",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718338.634737_news.png",
            "type": "#"
        },
        {
            "name": "Tạo Private call",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718338.634737_news.png",
            "type": "#"
        },
        {
            "name": "Tạo Livestream",
            "icon": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718338.634737_news.png",
            "type": "#"
        },
    ]
}

mock_slider_lich_livestream_us = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_lich_livestream_us",
    "meta": {
        "title": "Livestream của tối",
        "type": "#",
        "more_text": "",
        "more_href": "#",
        "data_type": "event"
    },
    "data": [
        {
            "id": "event1",
            "author_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718809.065704_live1.png",
            "rz_point": 50000,
            "title": "Phá đảo mọi giới hạn Bứt phá mọi cuộc chơi",
            "followers": 10000,
            "type": "/event/event1",
            "duration": 3600
        },
        {
            "id": "event2",
            "author_id": "alan-walker",
            "artst_name": "Alan Walker",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718820.854798_live2.png",
            "rz_point": 50000,
            "title": "Quẩy lên nào bà coan ư ư ư....",
            "followers": 10000,
            "type": "/event/event2",
            "duration": 3600
        }
    ]
}
mock_slider_music_uploaded = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_music_uploaded",
    "meta": {
        "title": "Nhạc đã upload",
        "type": "#",
        "more_text": "",
        "more_href": "",
        "data_type": "music",
        "rows": 2
    },
    "data": [
        {
            "id": "track1",
            "author_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png",
            "rz_point": 50000,
            "title": "Mixtape lên mây",
            "followers": 10000,
            "type": "/play/music/track1",
            "duration": 3600
        },
        {
            "id": "track2",
            "author_id": "dj-quang-minnh",
            "artst_name": "Justin Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Mixtape Peaches",
            "followers": 10000,
            "type": "/play/music/track2",
            "duration": 3600
        },
        {
            "id": "track3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/music/track2",
            "duration": 3600
        },
        {
            "id": "track3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/music/track2",
            "duration": 3600
        },
        {
            "id": "track3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/music/track2",
            "duration": 3600
        },
    ]
}
mock_albums_us = {
    "type": BLOCK_SLIDER,
    "id": "mock_albums_us",
    "meta": {
        "title": "Album Nhạc",
        "type": "#",
        "more_text": "",
        "more_href": "",
        "data_type": "album",
        "rows": 2
    },
    "data": [
        {
            "id": "album-1",
            "author_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": [
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718474.255522_music3.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png',
            ],
            "rz_point": 50000,
            "title": "Mixtape lên mây",
            "followers": 10000,
            "type": "/play/album/album-1",
            "duration": 3600,
            "banner_mixed": True,
        },
        {
            "id": "album-2",
            "author_id": "dj-quang-minnh",
            "artst_name": "Justin Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Mixtape Peaches",
            "followers": 10000,
            "type": "/play/album/album-2",
            "duration": 3600
        },
        {
            "id": "album-3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-3",
            "duration": 3600
        },
        {
            "id": "album-4",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-4",
            "duration": 3600
        },
        {
            "id": "album-5",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-5",
            "duration": 3600
        },
    ]
}
mock_albums_hot = {
    "type": BLOCK_SLIDER,
    "id": "mock_albums_hot",
    "meta": {
        "title": "Đang HOT",
        "type": "#",
        "more_text": "",
        "more_href": "",
        "data_type": "album",
        "rows": 2
    },
    "data": [
        {
            "id": "album-1",
            "author_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": [
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718474.255522_music3.png',
                'https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718422.122064_music1.png',
            ],
            "rz_point": 50000,
            "title": "Mixtape lên mây",
            "followers": 10000,
            "type": "/play/album/album-1",
            "duration": 3600,
            "banner_mixed": True,
        },
        {
            "id": "album-2",
            "author_id": "dj-quang-minnh",
            "artst_name": "Justin Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Mixtape Peaches",
            "followers": 10000,
            "type": "/play/album/album-2",
            "duration": 3600
        },
        {
            "id": "album-3",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-3",
            "duration": 3600
        },
        {
            "id": "album-4",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-4",
            "duration": 3600
        },
        {
            "id": "album-5",
            "author_id": "dj-quang-minnh",
            "artst_name": "Alan Bieber",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://static.rinznetwork.com/rinzmusic/images/2021/08/23/1629718459.087283_music2.png",
            "rz_point": 50000,
            "title": "Khu tao sống",
            "followers": 10000,
            "type": "/play/album/album-5",
            "duration": 3600
        },
    ]
}


MOCKS = [
    mock_search_bar,
    mock_idol_live,
    mock_widget_menus,
    mock_slider_lich_livestream,
    mock_slider_top_music,
    mock_top_idol,
    mock_feed_all,
    mock_tabs,
    mock_creator_new_tweet,
    mock_creator_icons,
    mock_slider_lich_livestream_us,
    mock_slider_music_uploaded,
    mock_albums_us,
    mock_albums_hot
]
