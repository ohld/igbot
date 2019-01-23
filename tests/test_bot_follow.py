
import pytest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from instabot.api.config import API_URL

from .test_bot import TestBot
from .test_variables import (TEST_SEARCH_USERNAME_ITEM, TEST_USERNAME_INFO_ITEM)


def reset_files(_bot):
    for x in _bot.followed_file.list:
        _bot.followed_file.remove(x)
    for x in _bot.unfollowed_file.list:
        _bot.unfollowed_file.remove(x)
    for x in _bot.skipped_file.list:
        _bot.skipped_file.remove(x)


class TestBotFilter(TestBot):

    @responses.activate
    @pytest.mark.parametrize('username', [TEST_SEARCH_USERNAME_ITEM['username'],
                                          TEST_SEARCH_USERNAME_ITEM['pk'],
                                          str(TEST_SEARCH_USERNAME_ITEM['pk'])])
    @patch('time.sleep', return_value=None)
    def test_follow(self, patched_time_sleep, username):
        follows_at_start = self.bot.total['follows']
        self.bot._following = [1]
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
            responses.POST, '{api_url}friendships/create/{user_id}/'.format(
                api_url=API_URL, user_id=user_id
            ), json=response_data, status=200)

        assert self.bot.follow(username)
        assert self.bot.total['follows'] == follows_at_start + 1
        assert self.bot.followed_file.list[-1] == str(user_id)
        assert str(user_id) in self.bot.following

    @responses.activate
    @pytest.mark.parametrize('user_ids', [
        [str(TEST_SEARCH_USERNAME_ITEM['pk']),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 1),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 2),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 3)],
        [str(TEST_SEARCH_USERNAME_ITEM['pk']),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 4),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 5),
         str(TEST_SEARCH_USERNAME_ITEM['pk'] + 6)]]
    )
    @patch('time.sleep', return_value=None)
    def test_follow_users(self, patched_time_sleep, user_ids):
        self.bot._following = [1]
        reset_files(self.bot)
        follows_at_start = self.bot.total['follows']
        self.bot.followed_file.append(str(user_ids[1]))
        self.bot.unfollowed_file.append(str(user_ids[2]))
        self.bot.skipped_file.append(str(user_ids[3]))

        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()

        my_test_search_username_item['is_verified'] = False
        my_test_search_username_item['is_business'] = False
        my_test_search_username_item['is_private'] = False
        my_test_search_username_item['follower_count'] = 100
        my_test_search_username_item['following_count'] = 15
        my_test_search_username_item['media_count'] = self.bot.min_media_count_to_follow + 1
        my_test_search_username_item['has_anonymous_profile_picture'] = False
        my_test_username_info_item['username'] = TEST_SEARCH_USERNAME_ITEM['username']
        my_test_username_info_item['is_verified'] = False
        my_test_username_info_item['is_business'] = False
        my_test_username_info_item['is_private'] = False
        my_test_username_info_item['follower_count'] = 100
        my_test_username_info_item['following_count'] = 15
        my_test_username_info_item['media_count'] = self.bot.min_media_count_to_follow + 1
        my_test_username_info_item['has_anonymous_profile_picture'] = False

        for user_id in user_ids:
            my_test_search_username_item['pk'] = user_id
            my_test_username_info_item['pk'] = user_id

            response_data = {
                'status': 'ok',
                'user': my_test_search_username_item
            }
            responses.add(
                responses.GET, '{api_url}users/{username}/usernameinfo/'.format(
                    api_url=API_URL, username=user_id
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
                responses.POST, '{api_url}friendships/create/{user_id}/'.format(
                    api_url=API_URL, user_id=user_id
                ), json=response_data, status=200)

        test_broken_items = [] == self.bot.follow_users(user_ids)
        test_follows = self.bot.total['follows'] == follows_at_start + 1
        test_following = self.bot.following == [1, user_ids[0]]
        test_followed = str(user_ids[0]) in self.bot.followed_file.list
        assert (test_broken_items and test_follows and test_followed and test_following)
