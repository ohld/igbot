import pytest
import responses

from instabot.api.config import API_URL
from tests.test_bot import reset_files
from tests.test_variables import TEST_SEARCH_USERNAME_ITEM, TEST_USERNAME_INFO_ITEM

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from .test_bot import TestBot


class TestBotUnfollow(TestBot):
    @responses.activate
    @pytest.mark.parametrize('username', [TEST_SEARCH_USERNAME_ITEM['username'],
                                          TEST_SEARCH_USERNAME_ITEM['pk'],
                                          str(TEST_SEARCH_USERNAME_ITEM['pk'])])
    @patch('time.sleep', return_value=None)
    def test_unfollow(self, _patched_time_sleep, username):
        unfollows_at_start = self.bot.total['unfollows']
        self.bot._following = ['7777777']
        reset_files(self.bot)
        user_id = TEST_SEARCH_USERNAME_ITEM['pk']
        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
        my_test_search_username_item['is_verified'] = False
        my_test_search_username_item['is_business'] = False
        my_test_search_username_item['is_private'] = False
        my_test_search_username_item['follower_count'] = 100
        my_test_search_username_item['following_count'] = 15
        my_test_search_username_item['media_count'] = self.bot.min_media_count_to_follow + 1
        my_test_search_username_item['has_anonymous_profile_picture'] = False
        my_test_username_info_item['pk'] = TEST_SEARCH_USERNAME_ITEM['pk']
        my_test_username_info_item['username'] = TEST_SEARCH_USERNAME_ITEM['username']
        my_test_username_info_item['is_verified'] = False
        my_test_username_info_item['is_business'] = False
        my_test_username_info_item['is_private'] = False
        my_test_username_info_item['follower_count'] = 100
        my_test_username_info_item['following_count'] = 15
        my_test_username_info_item['media_count'] = self.bot.min_media_count_to_follow + 1
        my_test_username_info_item['has_anonymous_profile_picture'] = False

        response_data = {
            'status': 'ok',
            'user': my_test_search_username_item
        }
        responses.add(
            responses.GET, '{api_url}users/{username}/usernameinfo/'.format(
                api_url=API_URL, username=username
            ), status=200, json=response_data)

        response_data = {
            'status': 'ok',
            'user': my_test_username_info_item
        }
        responses.add(
            responses.GET, '{api_url}users/{user_id}/info/'.format(
                api_url=API_URL, user_id=user_id
            ), status=200, json=response_data)

        response_data = {'status': 'ok'}
        responses.add(
            responses.POST, '{api_url}friendships/destroy/{user_id}/'.format(
                api_url=API_URL, user_id=user_id
            ), json=response_data, status=200)

        assert self.bot.unfollow(username)
        assert self.bot.total['unfollows'] == unfollows_at_start + 1
        assert self.bot.unfollowed_file.list[-1] == str(user_id)
        assert str(user_id) not in self.bot.following
        self.bot._db.record_unfollow.assert_called_once_with(str(user_id))

    def test_unfollow_after(self):
        with patch.object(self.bot, 'unfollow') as patched_unfollow:
            self.bot._db.get_followed_before.return_value = ['87654321']
            self.bot.unfollow_after(99)
            self.bot._db.get_followed_before.assert_called_once_with(99)
            patched_unfollow.assert_called_once_with('87654321')
