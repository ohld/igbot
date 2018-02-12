DEFAULT_RESPONSE = {'status': 'ok'}

TEST_CAPTION_ITEM = {
    "bit_flags": 0,
    "content_type": "comment",
    "created_at": 1494733796,
    "created_at_utc": 1494733796,
    "did_report_as_spam": False,
    "pk": 17856098620165444,
    "status": "Active",
    "text": "Old Harry Rocks, Dorset, UK\n\n#oldharryrocks #dorset #uk #rocks #clouds #water #photoshoot #nature #amazing #beautifulsky #sky #landscape #nice #beautiful #awesome #landscapes #l4l #f4f",
    "type": 1,
    "user": {
            "full_name": "The best earth places",
            "is_private": False,
            "is_verified": False,
            "pk": 182696006,
            "profile_pic_id": "1477989239094674784_182696006",
            "profile_pic_url": "https://scontent-arn2-1.cdninstagram.com/vp/703a0877fc8653d8b1ec17d57cf0aed6/5B2669EF/t51.2885-19/s150x150/17332952_229750480834181_3303899473574363136_a.jpg",
            "username": "best.earth.places"
    },
    "user_id": 182696006
}

TEST_COMMENT_ITEM = {
    "bit_flags": 0,
    "comment_like_count": 1,
    "content_type": "comment",
    "created_at": 1494751960,
    "created_at_utc": 1494751960,
    "did_report_as_spam": False,
    "has_liked_comment": True,
    "inline_composer_display_condition": "never",
    "pk": 17856583722163490,
    "status": "Active",
    "text": "Wow awesome take!",
    "type": 0,
    "user": {
        "full_name": "Jon",
        "is_private": False,
        "is_verified": False,
        "pk": 4236956175,
        "profile_pic_id": "1699734799357160789_42369123453",
        "profile_pic_url": "https://scontent-arn2-1.cdninstagram.com/vp/cf320d98994fasdasdas5fa53c698996bfa/5B0AD6BE/t51.2885-19/s150x150/26398129_141825939841889_6195199731287719936_n.jpg",
        "username": "test_user_name"
    },
    "user_id": 4236736455
}

TEST_USER_ITEM = {
    "pk": 1234543212321,
    "username": "test_username",
    "full_name": "Test Username",
    "is_private": False,
    "profile_pic_url": "https://scontent-arn2-1.cdninstagram.com/vp/6f3e8913b4e9c3153bc15669c47c9519/5AE4F003/t51.2885-19/s150x150/21827786_319483561795594_805639369123123123_n.jpg",
    "profile_pic_id": "120334920291626198135_614512764",
    "friendship_status": {
                "following": True,
                "is_private": False,
                "incoming_request": False,
                "outgoing_request": False,
                "is_bestie": False
    },
    "is_verified": False,
    "has_anonymous_profile_picture": False,
    "follower_count": 470,
    "byline": "470 followers",
    "social_context": "Following",
    "search_social_context": "Following",
    "mutual_followers_count": 0.0,
    "unseen_count": 0
}

TEST_PHOTO_ITEM = {
    'taken_at': 1281669687,
    'pk': 1234,
    'id': '1234_19',
    'device_timestamp': 1281669538,
    'media_type': 1,
    'code': 'TS',
    'client_cache_key': 'MTIzNA==.2',
    'filter_type': 0,
    'image_versions2': {
        'candidates': [
            {
                'width': 612,
                'height': 612,
                'url': 'https://scontent-amt2-1.cdninstagram.com/vp/9ef94dbfea2b8cdb2ba5c9b45f1945fd/5AEFE328/t51.2885-15/e15/11137637_1567371843535625_96536034_n.jpg?ig_cache_key=MTIzNA%3D%3D.2'
            },
            {
                'width': 240,
                'height': 240,
                'url': 'https://scontent-amt2-1.cdninstagram.com/vp/3f4554f2e45bf356951b2a437ab7d5b1/5ADE3631/t51.2885-15/s240x240/e15/11137637_1567371843535625_96536034_n.jpg?ig_cache_key=MTIzNA%3D%3D.2'}]
    },
    'original_width': 612,
    'original_height': 612,
    'lat': 37.3988349713,
    'lng': -122.027721405,
    'user': {
        'pk': 19,
        'username': 'chris',
        'full_name': 'Chris Messina',
        'is_private': False,
        'profile_pic_url': 'https://scontent-amt2-1.cdninstagram.com/t51.2885-19/s150x150/23824744_1036957976446940_7940760494346862592_n.jpg',
        'profile_pic_id': '1654528278723030076_19',
        'friendship_status': {
            'following': False,
            'outgoing_request': False,
            'is_bestie': False
        },
        'is_verified': False,
        'has_anonymous_profile_picture': False,
        'is_unpublished': False,
        'is_favorite': False
    },
    'caption': None,
    'caption_is_edited': False,
    'like_count': 260,
    'has_liked': False,
    'top_likers': [],
    'comment_likes_enabled': True,
    'comment_threading_enabled': False,
    'has_more_comments': True,
    'max_num_visible_preview_comments': 2,
    'preview_comments': [],
    'comment_count': 18,
    'photo_of_you': False,
    'can_viewer_save': True,
    'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiYmVkOTQ3ODIzODlkNDE2Nzg2ZTExNDc5ZmExMTkyYTIxMjM0Iiwic2VydmVyX3Rva2VuIjoiMTUxNjIyMTI0MzYxMXwxMjM0fDE4MjY5NjAwNnw5NGQzMjMyMmUxYzgxM2U3MWJmYTZjYzkzZjgxMTgyYzZmMzFmMGUyZTA2ODFjZjI1YzA4YzBiZDFkMWQ3M2U5In0sInNpZ25hdHVyZSI6IiJ9'
}
