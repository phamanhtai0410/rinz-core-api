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
            "name": "Trang Moon",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": True,
            "href": "/live/artist/trang-moon"
        },
        {
            "name": "Soda",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": True,
            "href": "/live/artist/soda"
        },
        {
            "name": "Alan Walker",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": True,
            "href": "/live/artist/alan-walker"
        },
        {
            "name": "Đen Vâu",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": False,
            "href": "/live/artist/den-vau"
        },
        {
            "name": "Binz",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": False,
            "href": "/live/artist/binz"
        },
        {
            "name": "Juno Bigboi",
            "image": "https://via.placeholder.com/100x100.png",
            "live_stream": False,
            "href": "/live/artist/juno"
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
            "icon": "https://via.placeholder.com/100x100.png",
            "name": "Newfeed",
            "href": "/newfeed"
        },
        {
            "icon": "https://via.placeholder.com/100x100.png",
            "name": "Artist",
            "href": "/artist"
        },
    ]
}
BLOCK_SLIDER = "BLOCK_SLIDER"
mock_slider_lich_livestream = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_lich_livestream",
    "meta": {
        "title": "Lịch Live Stream",
        "href": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "/live/all",
        "data_type": "event"
    },
    "data": [
        {
            "id": "event1",
            "artist_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://via.placeholder.com/100x100.png",
            "rz_point": 50000,
            "title": "Phá đảo mọi giới hạn Bứt phá mọi cuộc chơi",
            "followers": 10000,
            "href": "/event/event1",
            "duration": 3600
        },
        {
            "id": "event2",
            "artist_id": "alan-walker",
            "artst_name": "Alan Walker",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://via.placeholder.com/100x100.png",
            "rz_point": 50000,
            "title": "Quẩy lên nào bà coan ư ư ư....",
            "followers": 10000,
            "href": "/event/event2",
            "duration": 3600
        }
    ]
}
mock_slider_top_music = {
    "type": BLOCK_SLIDER,
    "id": "mock_slider_top_music",
    "meta": {
        "title": "Top Music",
        "href": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "/music",
        "data_type": "music"
    },
    "data": [
        {
            "id": "track1",
            "artist_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://via.placeholder.com/100x100.png",
            "rz_point": 50000,
            "title": "Phá đảo mọi giới hạn Bứt phá mọi cuộc chơi",
            "followers": 10000,
            "href": "/play/music/track1",
            "duration": 3600
        },
        {
            "id": "track2",
            "artist_id": "dj-quang-minnh",
            "artst_name": "DJ Quang Minh",
            "on_air_time": "2021-08-10 10:10:10",
            "banner": "https://via.placeholder.com/100x100.png",
            "rz_point": 50000,
            "title": "Phá đảo mọi giới hạn Bứt phá mọi cuộc chơi",
            "followers": 10000,
            "href": "/play/music/track2",
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
        "href": "#",
        "more_text": "Xem tất cả >>",
        "more_href": "/idols",
        "data_type": "idols"
    },
    "data": [
        {
            "id": "justin-bieber",
            "name": "Justin Bieber",
            "avatar": "https://via.placeholder.com/100x100.png",
            "href": "/artist/justin-bieber",
            "following": False,
        },
        {
            "id": "soda",
            "name": "Soda",
            "avatar": "https://via.placeholder.com/100x100.png",
            "href": "/artist/soda",
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
            "astist_id": "alan-walker",
            "content": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo culpa blanditiis neque veritatis animi non facere dicta dolores ratione accusamus pariatur, aut quos rem earum consectetur! Ducimus assumenda itaque voluptas.Quasi veritatis corporis odit mollitia, autem iusto fugit perferendis fugiat, perspiciatis voluptatibus molestiae dolore optio ea voluptatem dolores non laboriosam quam nobis. Inventore nulla illo perspiciatis, at officia consequuntur adipisci.",
            "name": "Alan Walker",
            "avatar": "https://via.placeholder.com/100x100.png",
            "created_date": "Thời gian đăng",
            "images": [
                "https://via.placeholder.com/100x100.png",
                "https://via.placeholder.com/100x100.png",
                "https://via.placeholder.com/100x100.png",
            ]
        },
        {
            "id": "feed2",
            "astist_id": "alan-walker",
            "content": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo culpa blanditiis neque veritatis animi non facere dicta dolores ratione accusamus pariatur, aut quos rem earum consectetur! Ducimus assumenda itaque voluptas.Quasi veritatis corporis odit mollitia, autem iusto fugit perferendis fugiat, perspiciatis voluptatibus molestiae dolore optio ea voluptatem dolores non laboriosam quam nobis. Inventore nulla illo perspiciatis, at officia consequuntur adipisci.",
            "name": "Alan Walker",
            "avatar": "https://via.placeholder.com/100x100.png",
            "created_date": "Thời gian đăng",
            "images": [
                "https://via.placeholder.com/100x100.png",
                "https://via.placeholder.com/100x100.png",
                "https://via.placeholder.com/100x100.png",
            ]
        },
    ]
}
mock_tabs = {
    "type": BLOCK_TABS,
    "id": "mock_tabs",
    "meta": {
        "image": "Top Idol",
        "href": "https://via.placeholder.com/100x100.png",
    },
    "data": [
        {
            "id": "mock_feed_all",  # block_id
            "name": "Tất cả",
            "type": "render",
            "href": ""
        },
        {
            "id": "",
            "name": "RinZ Music",
            "type": "direct",
            "href": "<site-map-route>"
        },
        {
            "id": "",
            "name": "Idol",
            "type": "direct",
            "href": "<site-map-route>"
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
    mock_tabs
]
