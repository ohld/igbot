import pytest
import responses

from instabot.api.config import API_URL, SIG_KEY_VERSION

from .test_bot import TestBot
from .test_variables import (
    TEST_CAPTION_ITEM,
    TEST_COMMENT_ITEM,
    TEST_FOLLOWER_ITEM,
    TEST_FOLLOWING_ITEM,
    TEST_PHOTO_ITEM,
    TEST_SEARCH_USERNAME_ITEM,
    TEST_TIMELINE_PHOTO_ITEM,
    TEST_USERNAME_INFO_ITEM,
)

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestBotGet(TestBot):
    @pytest.mark.parametrize(
        "media_id,check_media,"
        "comment_txt,"
        "has_liked,"
        "like_count,"
        "has_anonymous_profile_picture,filter_users_without_profile_photo,"
        "expected",
        [
            (1234567890, False, False, True, float("inf"), True, True, True),
            (1234567890, False, False, True, float("inf"), True, False, True),
            (1234567890, False, False, True, float("inf"), False, True, True),
            (1234567890, False, False, True, float("inf"), False, False, True),
            (1234567890, True, False, True, float("inf"), True, True, False),
            (1234567890, True, False, True, float("inf"), True, False, False),
            (1234567890, True, False, True, float("inf"), False, True, False),
            (1234567890, True, False, True, float("inf"), False, False, False),
            (1234567890, False, False, False, float("inf"), True, True, True),
            (1234567890, False, False, False, float("inf"), True, False, True),
            (1234567890, False, False, False, float("inf"), False, True, True),
            (1234567890, False, False, False, float("inf"), False, False, True),
            (1234567890, True, False, False, float("inf"), True, True, False),
            (1234567890, True, False, False, float("inf"), True, False, False),
            (1234567890, True, False, False, float("inf"), False, True, False),
            (1234567890, True, False, False, float("inf"), False, False, False),
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
            (1234567890, False, True, True, float("inf"), True, True, True),
            (1234567890, False, True, True, float("inf"), True, False, True),
            (1234567890, False, True, True, float("inf"), False, True, True),
            (1234567890, False, True, True, float("inf"), False, False, True),
            (1234567890, True, True, True, float("inf"), True, True, False),
            (1234567890, True, True, True, float("inf"), True, False, False),
            (1234567890, True, True, True, float("inf"), False, True, False),
            (1234567890, True, True, True, float("inf"), False, False, False),
            (1234567890, False, True, False, float("inf"), True, True, True),
            (1234567890, False, True, False, float("inf"), True, False, True),
            (1234567890, False, True, False, float("inf"), False, True, True),
            (1234567890, False, True, False, float("inf"), False, False, True),
            (1234567890, True, True, False, float("inf"), True, True, False),
            (1234567890, True, True, False, float("inf"), True, False, False),
            (1234567890, True, True, False, float("inf"), False, True, False),
            (1234567890, True, True, False, float("inf"), False, False, False),
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
            (1234567890, True, True, False, False, False, False, False),
        ],
    )
    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_bot_like(
        self,
        patched_time_sleep,
        media_id,
        check_media,
        comment_txt,
        has_liked,
        like_count,
        has_anonymous_profile_picture,
        filter_users_without_profile_photo,
        expected,
    ):

        self.bot._following = [1]
        TEST_PHOTO_ITEM["has_liked"] = has_liked
        if not like_count:
            like_count = self.bot.min_likes_to_like + 1
        TEST_PHOTO_ITEM["like_count"] = like_count
        TEST_PHOTO_ITEM["user"]["pk"] = self.bot.user_id + 1
        TEST_USERNAME_INFO_ITEM["pk"] = self.bot.user_id + 2
        TEST_USERNAME_INFO_ITEM["follower_count"] = 100
        TEST_USERNAME_INFO_ITEM["following_count"] = 15
        TEST_USERNAME_INFO_ITEM[
            "has_anonymous_profile_picture"
        ] = has_anonymous_profile_picture
        self.bot.filter_users_without_profile_photo = filter_users_without_profile_photo
        TEST_USERNAME_INFO_ITEM["is_business"] = False
        TEST_USERNAME_INFO_ITEM["is_private"] = False
        TEST_USERNAME_INFO_ITEM["is_verified"] = False
        TEST_USERNAME_INFO_ITEM["media_count"] = self.bot.min_media_count_to_follow + 1
        if comment_txt:
            comment_txt = " ".join(self.bot.blacklist_hashtags)
        else:
            comment_txt = "instabot"
        TEST_USERNAME_INFO_ITEM["biography"] = comment_txt

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM],
            },
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM],
            },
            status=200,
        )

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

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=media_id
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM],
            },
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=media_id
            ),
            status=200,
            json={"status": "ok"},
        )
        # this should be fixed acording to the new end_points
        # assert self.bot.like(media_id, check_media=check_media) == expected

    @pytest.mark.parametrize("comment_id", [12345678901234567, "12345678901234567"])
    @responses.activate
    def test_bot_like_comment(self, comment_id):
        responses.add(
            responses.POST,
            "{api_url}media/{comment_id}/comment_like/".format(
                api_url=API_URL, comment_id=comment_id
            ),
            json={"status": "ok"},
            status=200,
        )
        assert self.bot.like_comment(comment_id)

    @responses.activate
    @pytest.mark.parametrize(
        "has_liked_comment,comment_id",
        [(True, True), (True, False), (False, False), (False, True)],
    )
    @patch("time.sleep", return_value=None)
    def test_like_media_comments(
        self, patched_time_sleep, has_liked_comment, comment_id
    ):
        TEST_COMMENT_ITEM["has_liked_comment"] = has_liked_comment
        results = 2
        if comment_id or has_liked_comment:
            comment_id = TEST_COMMENT_ITEM["pk"]
            expected_broken_items = []
        else:
            comment_id = "wrong_comment_id"
            expected_broken_items = [TEST_COMMENT_ITEM["pk"] for _ in range(results)]
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
            "status": "ok",
        }
        media_id = 1234567890
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=200,
        )
        responses.add(
            responses.POST,
            "{api_url}media/{comment_id}/comment_like/".format(
                api_url=API_URL, comment_id=comment_id
            ),
            json={"status": "ok"},
            status=200,
        )
        broken_items = self.bot.like_media_comments(media_id)
        assert broken_items == expected_broken_items

    @responses.activate
    @pytest.mark.parametrize("user_id", ["1234567890", 1234567890])
    @patch("time.sleep", return_value=None)
    def test_like_user(self, patched_time_sleep, user_id):
        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"

        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=user_id
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=user_id),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=user_id),
            status=200,
            json=response_data,
        )

        results = 5
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": [TEST_PHOTO_ITEM for _ in range(results)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
            ).format(
                api_url=API_URL,
                user_id=user_id,
                max_id="",
                min_timestamp=None,
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM],
            },
            status=200,
        )

        results = 2
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
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json=response_data,
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            status=200,
            json={"status": "ok"},
        )

        broken_items = self.bot.like_user(user_id)
        assert [] == broken_items

    @responses.activate
    @pytest.mark.parametrize("user_ids", [["1234567890"], [1234567890]])
    @patch("time.sleep", return_value=None)
    def test_like_users(self, patched_time_sleep, user_ids):

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"

        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=user_ids[0]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=user_ids[0]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=user_ids[0]
            ),
            status=200,
            json=response_data,
        )

        results_1 = 5
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results_1,
            "status": "ok",
            "more_available": False,
            "items": [TEST_PHOTO_ITEM for _ in range(results_1)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&"
                + "min_timestamp={min_timestamp}&rank_token={rank_token}"
                + "&ranked_content=true"
            ).format(
                api_url=API_URL,
                user_id=user_ids[0],
                max_id="",
                min_timestamp=None,
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM],
            },
            status=200,
        )

        results_2 = 2
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results_2,
            "comment_likes_enabled": True,
            "comments": [TEST_COMMENT_ITEM for _ in range(results_2)],
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json=response_data,
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            status=200,
            json={"status": "ok"},
        )

        self.bot.like_users(user_ids)
        assert self.bot.total["likes"] == results_1

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection,blocked_actions_sleep,result",
        [
            (True, True, False),
            (True, False, True),
            (False, True, False),
            (False, False, False),
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_sleep_feedback_successful(
        self,
        patched_time_sleep,
        blocked_actions_protection,
        blocked_actions_sleep,
        result,
    ):
        self.bot.blocked_actions_protection = blocked_actions_protection
        # self.bot.blocked_actions["likes"] = False
        self.bot.blocked_actions_sleep = blocked_actions_sleep
        media_id = 1234567890
        response_data = {
            u"status": u"fail",
            u"feedback_title": u"You\u2019re Temporarily Blocked",
            u"feedback_message": u"It looks like you were misusing this "
            + u"feature by going too fast. You\u2019ve been temporarily "
            + u"blocked from using it. We restrict certain content and "
            + u"actions to protect our community. Tell us if you think we "
            + u"made a mistake.",
            u"spam": True,
            u"feedback_action": u"report_problem",
            u"feedback_appeal_label": u"Report problem",
            u"feedback_ignore_label": u"OK",
            u"message": u"feedback_required",
            u"feedback_url": u"repute/report_problem/instagram_like_add/",
        }
        # first like blocked
        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=400,
        )
        # second like successful
        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=media_id
            ),
            status=200,
            json={"status": "ok"},
        )
        # do 2 likes
        self.bot.like(media_id, check_media=False)
        self.bot.like(media_id, check_media=False)
        assert self.bot.blocked_actions["likes"] == result

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection,blocked_actions_sleep,result",
        [
            (True, True, True),
            (True, False, True),
            (False, True, False),
            (False, False, False),
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_sleep_feedback_unsuccessful(
        self,
        patched_time_sleep,
        blocked_actions_protection,
        blocked_actions_sleep,
        result,
    ):
        self.bot.blocked_actions_protection = blocked_actions_protection
        # self.bot.blocked_actions["likes"] = False
        self.bot.blocked_actions_sleep = blocked_actions_sleep
        media_id = 1234567890
        response_data = {
            u"status": u"fail",
            u"feedback_title": u"You\u2019re Temporarily Blocked",
            u"feedback_message": u"It looks like you were misusing this "
            + u"feature by going too fast. You\u2019ve been temporarily "
            + u"blocked from using it. We restrict certain content and "
            + u"actions to protect our community. Tell us if you think we "
            + u"made a mistake.",
            u"spam": True,
            u"feedback_action": u"report_problem",
            u"feedback_appeal_label": u"Report problem",
            u"feedback_ignore_label": u"OK",
            u"message": u"feedback_required",
            u"feedback_url": u"repute/report_problem/instagram_like_add/",
        }
        # both likes blocked
        for x in range(1, 2):
            responses.add(
                responses.POST,
                "{api_url}media/{media_id}/like/".format(
                    api_url=API_URL, media_id=media_id
                ),
                json=response_data,
                status=400,
            )
        # do 2 likes
        self.bot.like(media_id, check_media=False)
        self.bot.like(media_id, check_media=False)
        assert self.bot.blocked_actions["likes"] == result

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection,blocked_actions",
        [(True, True), (True, False), (False, True), (False, True)],
    )
    @patch("time.sleep", return_value=None)
    def test_like_feedback(
        self, patched_time_sleep, blocked_actions_protection, blocked_actions
    ):
        self.bot.blocked_actions_protection = blocked_actions_protection
        self.bot.blocked_actions["likes"] = blocked_actions
        media_id = 1234567890
        response_data = {
            u"status": u"fail",
            u"feedback_title": u"You\u2019re Temporarily Blocked",
            u"feedback_message": u"It looks like you were misusing this "
            + u"feature by going too fast. You\u2019ve been temporarily "
            + u"blocked from using it. We restrict certain content and "
            + u"actions to protect our community. Tell us if you think we "
            + u"made a mistake.",
            u"spam": True,
            u"feedback_action": u"report_problem",
            u"feedback_appeal_label": u"Report problem",
            u"feedback_ignore_label": u"OK",
            u"message": u"feedback_required",
            u"feedback_url": u"repute/report_problem/instagram_like_add/",
        }
        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=400,
        )
        assert not self.bot.like(media_id, check_media=False)

    @responses.activate
    @pytest.mark.parametrize("medias", [[1234567890, 9876543210]])
    @patch("time.sleep", return_value=None)
    def test_like_medias(self, patched_time_sleep, medias):
        self.bot._following = [1]

        for media in medias:
            TEST_PHOTO_ITEM["id"] = media
            responses.add(
                responses.GET,
                "{api_url}media/{media_id}/info/".format(
                    api_url=API_URL, media_id=media
                ),
                json={
                    "auto_load_more_enabled": True,
                    "num_results": 1,
                    "status": "ok",
                    "more_available": False,
                    "items": [TEST_PHOTO_ITEM],
                },
                status=200,
            )

            results = 2
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
                "status": "ok",
            }
            responses.add(
                responses.GET,
                "{api_url}media/{media_id}/comments/?".format(
                    api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
                ),
                json=response_data,
                status=200,
            )

            response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
            responses.add(
                responses.GET,
                "{api_url}users/{user_id}/info/".format(
                    api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
            responses.add(
                responses.GET,
                "{api_url}users/{user_id}/info/".format(
                    api_url=API_URL, user_id=TEST_PHOTO_ITEM["user"]["pk"]
                ),
                status=200,
                json=response_data,
            )

            responses.add(
                responses.POST,
                "{api_url}media/{media_id}/like/".format(
                    api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
                ),
                status=200,
                json={"status": "ok"},
            )

        broken_items = self.bot.like_medias(medias)
        assert [] == broken_items

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["like_hashtag1", "like_hashtag2"])
    @patch("time.sleep", return_value=None)
    def test_like_hashtag(self, patche_time_sleep, hashtag):
        self.bot._following = [1]
        liked_at_start = self.bot.total["likes"]
        results_1 = 10
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results_1,
            "status": "ok",
            "more_available": True,
            "next_max_id": my_test_photo_item["id"],
            "items": [my_test_photo_item for _ in range(results_1)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}"
                + "&rank_token={rank_token}&ranked_content=true&"
            ).format(
                api_url=API_URL,
                hashtag=hashtag,
                max_id="",
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        response_tag = {
            "results": [
                {
                    "id": 17841563287125205,
                    "name": hashtag,
                    "media_count": 7645915,
                    "follow_status": None,
                    "following": None,
                    "allow_following": None,
                    "allow_muting_story": None,
                    "profile_pic_url": "https://instagram.fmxp6-1.fna.fbcdn."
                    + "net/vp/8e512ee62d218765d3ac46f3da6869de/5E0E0DE3/t51.28"
                    + "85-15/e35/c148.0.889.889a/s150x150/67618693_24674373801"
                    + "56007_7054420538339677194_n.jpg?_nc_ht=instagram.fmxp6-"
                    + "1.fna.fbcdn.net&ig_cache_key=MjExMzI5MDMwNDYxNzY3MDExMQ"
                    + "%3D%3D.2.c",
                    "non_violating": None,
                    "related_tags": None,
                    "subtitle": None,
                    "social_context": None,
                    "social_context_profile_links": None,
                    "follow_button_text": None,
                    "show_follow_drop_down": None,
                    "formatted_media_count": "7.6M",
                    "debug_info": None,
                    "search_result_subtitle": "7.6M posts",
                }
            ]
        }

        responses.add(
            responses.GET,
            (
                "{api_url}tags/search/?is_typeahead=true&q={query}"
                + "&rank_token={rank_token}"
            ).format(
                api_url=API_URL, query=hashtag, rank_token=self.bot.api.rank_token
            ),
            json=response_tag,
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [my_test_photo_item],
            },
            status=200,
        )

        results_2 = 2
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results_2,
            "comment_likes_enabled": True,
            "comments": [TEST_COMMENT_ITEM for _ in range(results_2)],
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json=response_data,
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            status=200,
            json={"status": "ok"},
        )

        broken_items = self.bot.like_hashtag(hashtag)
        assert [] == broken_items
        assert self.bot.total["likes"] == liked_at_start + results_1

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value=None)
    def test_like_followers(self, patched_time_sleep, username):

        liked_at_start = self.bot.total["likes"]

        test_username = "test.username"

        response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=test_username
            ),
            status=200,
            json=response_data_1,
        )

        response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data_2,
        )

        results_3 = 2
        response_data_3 = {
            "status": "ok",
            "big_list": False,
            "next_max_id": None,
            "sections": None,
            "users": [TEST_FOLLOWER_ITEM for _ in range(results_3)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}friendships/{user_id}/followers/" + "?rank_token={rank_token}"
            ).format(
                api_url=API_URL, user_id=username, rank_token=self.bot.api.rank_token
            ),
            json=response_data_3,
            status=200,
        )

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False

        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data,
        )

        results_4 = 3
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results_4,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results_4)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
            ).format(
                api_url=API_URL,
                user_id=username,
                max_id="",
                min_timestamp=None,
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [my_test_photo_item],
            },
            status=200,
        )

        results_5 = 2
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results_5,
            "comment_likes_enabled": True,
            "comments": [TEST_COMMENT_ITEM for _ in range(results_5)],
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            json=response_data,
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            status=200,
            json={"status": "ok"},
        )

        self.bot.like_followers(username)
        assert self.bot.total["likes"] == liked_at_start + results_3 * results_4

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value=None)
    def test_like_following(self, patched_time_sleep, username):

        liked_at_start = self.bot.total["likes"]

        test_username = "test.username"

        response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=test_username
            ),
            status=200,
            json=response_data_1,
        )

        response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data_2,
        )

        results_3 = 5
        response_data_3 = {
            "status": "ok",
            "big_list": False,
            "next_max_id": None,
            "sections": None,
            "users": [TEST_FOLLOWING_ITEM for _ in range(results_3)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}friendships/{user_id}/following/?max_id={max_id}"
                + "&ig_sig_key_version={sig_key}&rank_token={rank_token}"
            ).format(
                api_url=API_URL,
                user_id=username,
                rank_token=self.bot.api.rank_token,
                sig_key=SIG_KEY_VERSION,
                max_id="",
            ),
            json=response_data_3,
            status=200,
        )

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False

        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=username),
            status=200,
            json=response_data,
        )

        results_4 = 3
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results_4,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results_4)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
            ).format(
                api_url=API_URL,
                user_id=username,
                max_id="",
                min_timestamp=None,
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/info/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [my_test_photo_item],
            },
            status=200,
        )

        results_5 = 2
        response_data = {
            "caption": TEST_CAPTION_ITEM,
            "caption_is_edited": False,
            "comment_count": results_5,
            "comment_likes_enabled": True,
            "comments": [TEST_COMMENT_ITEM for _ in range(results_5)],
            "has_more_comments": False,
            "has_more_headload_comments": False,
            "media_header_display": "none",
            "preview_comments": [],
            "status": "ok",
        }
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            json=response_data,
            status=200,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL, user_id=my_test_photo_item["user"]["pk"]
            ),
            status=200,
            json=response_data,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL, media_id=my_test_photo_item["id"]
            ),
            status=200,
            json={"status": "ok"},
        )

        self.bot.like_following(username)
        assert self.bot.total["likes"] == liked_at_start + results_3 * results_4

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_like_timeline(self, patched_time_sleep):

        my_test_timelime_photo_item = TEST_TIMELINE_PHOTO_ITEM.copy()
        my_test_timelime_photo_item["media_or_ad"]["like_count"] = (
            self.bot.max_likes_to_like - 1
        )
        my_test_timelime_photo_item["media_or_ad"]["has_liked"] = False

        liked_at_start = self.bot.total["likes"]

        results_1 = 8
        responses.add(
            responses.POST,
            "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "auto_load_more_enabled": True,
                "num_results": results_1,
                "is_direct_v2_enabled": True,
                "status": "ok",
                "next_max_id": None,
                "more_available": False,
                "feed_items": [my_test_timelime_photo_item for _ in range(results_1)],
            },
            status=200,
        )

        responses.add(
            responses.POST,
            "{api_url}media/{media_id}/like/".format(
                api_url=API_URL,
                media_id=my_test_timelime_photo_item["media_or_ad"]["id"],
            ),
            status=200,
            json={"status": "ok"},
        )

        broken_items = self.bot.like_timeline()
        assert [] == broken_items
        assert self.bot.total["likes"] == liked_at_start + results_1
