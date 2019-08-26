import pytest
import responses

from instabot.api.config import API_URL

from .test_bot import TestBot
from .test_variables import (
    TEST_CAPTION_ITEM,
    TEST_COMMENT_ITEM,
    TEST_PHOTO_ITEM,
    TEST_USERNAME_INFO_ITEM,
)

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestBotFilter(TestBot):
    @responses.activate
    @pytest.mark.parametrize(
        "media_id,total,max_per_day",
        [
            [111111, 1, 2],
            [111111, 2, 2],
            [111111, 3, 2],
            ["111111", 1, 2],
            ["111111", 2, 2],
            ["111111", 3, 2],
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_unlike(self, patched_time_sleep, media_id, total, max_per_day):
        self.bot.total["unlikes"] = total
        self.bot.max_per_day["unlikes"] = max_per_day
        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/unlike/".format(
                api_url=API_URL, media_id=media_id
            ),
            json="{'status': 'ok'}",
            status=200,
        )
        _r = self.bot.unlike(media_id)
        test_r = _r if total < max_per_day else not _r
        test_unliked = (
            self.bot.total["unlikes"] == total + 1
            if total < max_per_day
            else self.bot.total["unlikes"] == total
        )
        assert test_r and test_unliked

    @responses.activate
    @pytest.mark.parametrize("comment_id", [111111, "111111"])
    @patch("time.sleep", return_value=None)
    def test_unlike_comment(self, patched_time_sleep, comment_id):
        responses.add(
            responses.POST,
            "{api_url}media/{comment_id}/comment_unlike/".format(
                api_url=API_URL, comment_id=comment_id
            ),
            json="{'status': 'ok'}",
            status=200,
        )
        _r = self.bot.unlike_comment(comment_id)
        assert _r

    @responses.activate
    @pytest.mark.parametrize(
        "media_ids,total,max_per_day",
        [
            [[111111, 222222], 1, 3],
            [[111111, 222222], 2, 3],
            [[111111, 222222], 3, 3],
            [["111111", "222222"], 1, 3],
            [["111111", "222222"], 2, 3],
            [["111111", "222222"], 3, 3],
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_unlike_medias(self, patched_time_sleep, media_ids, total, max_per_day):
        self.bot.total["unlikes"] = total
        self.bot.max_per_day["unlikes"] = max_per_day
        for media_id in media_ids:
            responses.add(
                responses.POST,
                "{api_url}media/{media_id}/unlike/".format(
                    api_url=API_URL, media_id=media_id
                ),
                json="{'status': 'ok'}",
                status=200,
            )
        broken_items = self.bot.unlike_medias(media_ids)
        test_unliked = self.bot.total["unlikes"] == max_per_day
        test_broken = len(broken_items) == len(media_ids) - (max_per_day - total)
        assert test_unliked and test_broken

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_unlike_media_comments(self, patched_time_sleep):
        my_test_comment_items = []
        results = 5
        for i in range(results):
            my_test_comment_items.append(TEST_COMMENT_ITEM.copy())
            my_test_comment_items[i]["pk"] = TEST_COMMENT_ITEM["pk"] + i
            if i % 2:
                my_test_comment_items[i]["has_liked_comment"] = False
            else:
                my_test_comment_items[i]["has_liked_comment"] = True
        media_id = 1234567890
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results,
            "comment_likes_enabled": True,
            "comments": my_test_comment_items,
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=200,
        )
        for my_test_comment_item in my_test_comment_items:
            responses.add(
                responses.POST,
                "{api_url}media/{comment_id}/comment_unlike/".format(
                    api_url=API_URL, comment_id=my_test_comment_item["pk"]
                ),
                json="{'status': 'ok'}",
                status=200,
            )
        broken_items = self.bot.unlike_media_comments(media_id)
        assert broken_items == []

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_unlike_user(self, patched_time_sleep):
        unliked_at_start = self.bot.total["unlikes"]
        user_id = 1234567890
        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=user_id
            ),
            status=200,
            json=response_data,
        )
        my_test_photo_items = []
        results = 5
        for i in range(results):
            my_test_photo_items.append(TEST_PHOTO_ITEM.copy())
            my_test_photo_items[i]["pk"] = TEST_PHOTO_ITEM["id"] + i
            if i % 2:
                my_test_photo_items[i]["has_liked"] = False
            else:
                my_test_photo_items[i]["has_liked"] = True
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": my_test_photo_items,
        }
        responses.add(
            responses.GET,
            "{api_url}feed/user/{user_id}/".format(api_url=API_URL, user_id=user_id),
            json=response_data,
            status=200,
        )
        for my_test_photo_item in my_test_photo_items:
            responses.add(
                responses.POST,
                "{api_url}media/{media_id}/unlike/".format(
                    api_url=API_URL, media_id=my_test_photo_item["id"]
                ),
                json="{'status': 'ok'}",
                status=200,
            )
        broken_items = self.bot.unlike_user(user_id)
        test_unliked = self.bot.total["unlikes"] == unliked_at_start + len(
            my_test_photo_items
        )
        test_broken = broken_items == []
        assert test_broken and test_unliked
