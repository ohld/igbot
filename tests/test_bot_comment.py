
import pytest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from instabot.api.config import API_URL

from .test_bot import TestBot
from .test_variables import (TEST_CAPTION_ITEM, TEST_COMMENT_ITEM)


class TestBotGet(TestBot):

    @responses.activate
    @pytest.mark.parametrize('blocked_actions_protection,blocked_actions', [
        (True, True),
        (True, False),
        (False, True),
        (False, False)])
    @patch('time.sleep', return_value=None)
    def test_comment_feedback(self, patched_time_sleep, blocked_actions_protection, blocked_actions):
        self.bot.blocked_actions_protection = blocked_actions_protection
        self.bot.blocked_actions['comments'] = blocked_actions
        media_id = 1234567890
        comment_txt = "Yeah great!"

        TEST_COMMENT_ITEM['user']['pk'] = self.bot.user_id + 1

        results = 3
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results,
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

        response_data = {
            "message": "feedback_required",
            "spam": True,
            "feedback_title": "Sorry, this feature isn't available right now",
            "feedback_message": "An error occurred while processing this request. Please try again later. We restrict certain content and actions to protect our community. Tell us if you think we made a mistake.",
            "feedback_url": "repute/report_problem/instagram_comment/",
            "feedback_appeal_label": "Report problem",
            "feedback_ignore_label": "OK",
            "feedback_action": "report_problem",
            "status": "fail"}
        responses.add(
            responses.POST, '{api_url}media/{media_id}/comment/'.format(
                api_url=API_URL, media_id=media_id
            ), json=response_data, status=400
        )

        assert not self.bot.comment(media_id, comment_txt)

    @responses.activate
    @pytest.mark.parametrize('blocked_actions_protection,blocked_actions', [
        (True, False),
        (False, False)])
    @patch('time.sleep', return_value=None)
    def test_comment(self, patched_time_sleep, blocked_actions_protection, blocked_actions):
        self.bot.blocked_actions_protection = blocked_actions_protection
        self.bot.blocked_actions['comments'] = blocked_actions
        media_id = 1234567890
        comment_txt = "Yeah great!"

        TEST_COMMENT_ITEM['user']['pk'] = self.bot.user_id + 1

        results = 3
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results,
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

        response_data = {
            "status": "ok"}
        responses.add(
            responses.POST, '{api_url}media/{media_id}/comment/'.format(
                api_url=API_URL, media_id=media_id
            ), json=response_data, status=200
        )

        assert self.bot.comment(media_id, comment_txt)
