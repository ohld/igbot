import pytest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from instabot.api.config import API_URL

from .test_bot import TestBot
from .test_variables import TEST_USERNAME_INFO_ITEM


class TestBotFilter(TestBot):
    @pytest.mark.parametrize('filter_users,filter_business_accounts,filter_verified_accounts,expected', [
        (False, False, False, True),
        (True, False, False, True),
        (True, True, False, False),
        (True, False, True, False),
        (True, True, True, False),
    ])
    @responses.activate
    @patch('time.sleep', return_value=None)
    def test_check_user(self, patched_time_sleep, filter_users, filter_business_accounts, filter_verified_accounts, expected):
        self.BOT.filter_users = filter_users
        self.BOT.filter_business_accounts = filter_business_accounts
        self.BOT.filter_verified_accounts = filter_verified_accounts
        self.BOT.following = [1]

        user_id = TEST_USERNAME_INFO_ITEM['pk']
        TEST_USERNAME_INFO_ITEM['is_verified'] = True
        TEST_USERNAME_INFO_ITEM['is_business'] = True

        response_data = {
            'status': 'ok',
            'user': TEST_USERNAME_INFO_ITEM
        }
        responses.add(
            responses.GET, '{API_URL}users/{user_id}/info/'.format(
                API_URL=API_URL, user_id=user_id
            ), status=200, json=response_data)

        result = self.BOT.check_user(user_id)

        assert result == expected
