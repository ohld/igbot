
import pytest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from instabot.api.config import API_URL

from .test_bot import TestBot
from .test_variables import (TEST_USERNAME_INFO_ITEM, TEST_PHOTO_ITEM, TEST_CAPTION_ITEM, TEST_COMMENT_ITEM)


class TestBotGet(TestBot):
    @pytest.mark.parametrize(
        'media_id,check_media,'
        'comment_txt,'
        'has_liked,'
        'like_count,'
        'has_anonymous_profile_picture,filter_users_without_profile_photo,'
        'expected', [
            (1234567890, False, False, True, float('inf'), True, True, True),
            (1234567890, False, False, True, float('inf'), True, False, True),
            (1234567890, False, False, True, float('inf'), False, True, True),
            (1234567890, False, False, True, float('inf'), False, False, True),
            (1234567890, True, False, True, float('inf'), True, True, False),
            (1234567890, True, False, True, float('inf'), True, False, False),
            (1234567890, True, False, True, float('inf'), False, True, False),
            (1234567890, True, False, True, float('inf'), False, False, False),
            (1234567890, False, False, False, float('inf'), True, True, True),
            (1234567890, False, False, False, float('inf'), True, False, True),
            (1234567890, False, False, False, float('inf'), False, True, True),
            (1234567890, False, False, False, float('inf'), False, False, True),
            (1234567890, True, False, False, float('inf'), True, True, False),
            (1234567890, True, False, False, float('inf'), True, False, False),
            (1234567890, True, False, False, float('inf'), False, True, False),
            (1234567890, True, False, False, float('inf'), False, False, False),
            (1234567890, False, False, True, False, True, True, True),
            (1234567890, False, False, True, False, True, False, True),
            (1234567890, False, False, True, False, False, True, True),
            (1234567890, False, False, True, False, False, False, True),
            (1234567890, True, False, True, False, True, True, False),
            (1234567890, True, False, True, False, True, False, False),
            (1234567890, True, False, True, False, False, True, False),
            (1234567890, True, False, True, False, False, False, False),
            (1234567890, False, False, False, False, True, True, True),
            (1234567890, False, False, False, False, True, False, True),
            (1234567890, False, False, False, False, False, True, True),
            (1234567890, False, False, False, False, False, False, True),
            (1234567890, True, False, False, False, True, True, False),
            (1234567890, True, False, False, False, True, False, True),
            (1234567890, True, False, False, False, False, True, True),
            (1234567890, True, False, False, False, False, False, True),
            (1234567890, False, True, True, float('inf'), True, True, True),
            (1234567890, False, True, True, float('inf'), True, False, True),
            (1234567890, False, True, True, float('inf'), False, True, True),
            (1234567890, False, True, True, float('inf'), False, False, True),
            (1234567890, True, True, True, float('inf'), True, True, False),
            (1234567890, True, True, True, float('inf'), True, False, False),
            (1234567890, True, True, True, float('inf'), False, True, False),
            (1234567890, True, True, True, float('inf'), False, False, False),
            (1234567890, False, True, False, float('inf'), True, True, True),
            (1234567890, False, True, False, float('inf'), True, False, True),
            (1234567890, False, True, False, float('inf'), False, True, True),
            (1234567890, False, True, False, float('inf'), False, False, True),
            (1234567890, True, True, False, float('inf'), True, True, False),
            (1234567890, True, True, False, float('inf'), True, False, False),
            (1234567890, True, True, False, float('inf'), False, True, False),
            (1234567890, True, True, False, float('inf'), False, False, False),
            (1234567890, False, True, True, False, True, True, True),
            (1234567890, False, True, True, False, True, False, True),
            (1234567890, False, True, True, False, False, True, True),
            (1234567890, False, True, True, False, False, False, True),
            (1234567890, True, True, True, False, True, True, False),
            (1234567890, True, True, True, False, True, False, False),
            (1234567890, True, True, True, False, False, True, False),
            (1234567890, True, True, True, False, False, False, False),
            (1234567890, False, True, False, False, True, True, True),
            (1234567890, False, True, False, False, True, False, True),
            (1234567890, False, True, False, False, False, True, True),
            (1234567890, False, True, False, False, False, False, True),
            (1234567890, True, True, False, False, True, True, False),
            (1234567890, True, True, False, False, True, False, False),
            (1234567890, True, True, False, False, False, True, False),
            (1234567890, True, True, False, False, False, False, False)])
    @responses.activate
    @patch('time.sleep', return_value=None)
    def test_bot_like(self, patched_time_sleep, media_id, check_media,
                      comment_txt,
                      has_liked,
                      like_count,
                      has_anonymous_profile_picture, filter_users_without_profile_photo,
                      expected):

        self.bot._following = [1]
        TEST_PHOTO_ITEM['has_liked'] = has_liked
        if not like_count:
            like_count = self.bot.min_likes_to_like + 1
        TEST_PHOTO_ITEM['like_count'] = like_count
        TEST_PHOTO_ITEM['user']['pk'] = self.bot.user_id + 1
        TEST_USERNAME_INFO_ITEM['pk'] = self.bot.user_id + 2
        TEST_USERNAME_INFO_ITEM['follower_count'] = 100
        TEST_USERNAME_INFO_ITEM['following_count'] = 15
        TEST_USERNAME_INFO_ITEM['has_anonymous_profile_picture'] = has_anonymous_profile_picture
        self.bot.filter_users_without_profile_photo = filter_users_without_profile_photo
        TEST_USERNAME_INFO_ITEM['is_business'] = False
        TEST_USERNAME_INFO_ITEM['is_private'] = False
        TEST_USERNAME_INFO_ITEM['is_verified'] = False
        TEST_USERNAME_INFO_ITEM['media_count'] = self.bot.min_media_count_to_follow + 1
        if comment_txt:
            comment_txt = ' '.join(self.bot.blacklist_hashtags)
        else:
            comment_txt = 'instabot'
        TEST_USERNAME_INFO_ITEM['biography'] = comment_txt

        responses.add(
            responses.POST, "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM]
            }, status=200)

        responses.add(
            responses.POST, "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM]
            }, status=200)

        results = 1
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": 4,
            "comment_likes_enabled": True,
            "comments": [TEST_COMMENT_ITEM for _ in range(results)],
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok"
        }
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

        responses.add(
            responses.POST, "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM]
            }, status=200)

        response_data = {
            'status': 'ok',
            'user': TEST_USERNAME_INFO_ITEM
        }
        responses.add(
            responses.GET, '{api_url}users/{user_id}/info/'.format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM['user']['pk']
            ), status=200, json=response_data)

        response_data = {
            'status': 'ok',
            'user': TEST_USERNAME_INFO_ITEM
        }
        responses.add(
            responses.GET, '{api_url}users/{user_id}/info/'.format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM['user']['pk']
            ), status=200, json=response_data)

        responses.add(
            responses.POST, '{api_url}media/{media_id}/like/'.format(
                api_url=API_URL, media_id=media_id
            ), status=200, json={'status': 'ok'})

        assert self.bot.like(media_id, check_media=check_media) == expected
