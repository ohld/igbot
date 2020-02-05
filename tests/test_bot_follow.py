import pytest
import responses

from instabot.api.config import API_URL, SIG_KEY_VERSION

from .test_bot import TestBot
from .test_variables import (
    TEST_FOLLOWER_ITEM,
    TEST_FOLLOWING_ITEM,
    TEST_SEARCH_USERNAME_ITEM,
    TEST_USERNAME_INFO_ITEM,
)

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def reset_files(_bot):
    for x in _bot.followed_file.list:
        _bot.followed_file.remove(x)
    for x in _bot.unfollowed_file.list:
        _bot.unfollowed_file.remove(x)
    for x in _bot.skipped_file.list:
        _bot.skipped_file.remove(x)


class TestBotFilter(TestBot):
    @responses.activate
    @pytest.mark.parametrize(
        "username",
        [
            TEST_SEARCH_USERNAME_ITEM["username"],
            TEST_SEARCH_USERNAME_ITEM["pk"],
            str(TEST_SEARCH_USERNAME_ITEM["pk"]),
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_follow(self, patched_time_sleep, username):
        follows_at_start = self.bot.total["follows"]
        self.bot._following = [1]
        reset_files(self.bot)
        user_id = TEST_SEARCH_USERNAME_ITEM["pk"]
        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
        my_test_search_username_item["is_verified"] = False
        my_test_search_username_item["is_business"] = False
        my_test_search_username_item["is_private"] = False
        my_test_search_username_item["follower_count"] = 100
        my_test_search_username_item["following_count"] = 15
        my_test_search_username_item["media_count"] = (
            self.bot.min_media_count_to_follow + 1
        )
        my_test_search_username_item["has_anonymous_profile_picture"] = False
        my_test_username_info_item["pk"] = TEST_SEARCH_USERNAME_ITEM["pk"]
        my_test_username_info_item["username"] = TEST_SEARCH_USERNAME_ITEM["username"]
        my_test_username_info_item["is_verified"] = False
        my_test_username_info_item["is_business"] = False
        my_test_username_info_item["is_private"] = False
        my_test_username_info_item["follower_count"] = 100
        my_test_username_info_item["following_count"] = 15
        my_test_username_info_item["media_count"] = (
            self.bot.min_media_count_to_follow + 1
        )
        my_test_username_info_item["has_anonymous_profile_picture"] = False

        response_data = {"status": "ok", "user": my_test_search_username_item}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
            ),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok", "user": my_test_username_info_item}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(api_url=API_URL, user_id=user_id),
            status=200,
            json=response_data,
        )

        response_data = {"status": "ok"}
        responses.add(
            responses.POST,
            "{api_url}friendships/create/{user_id}/".format(
                api_url=API_URL, user_id=user_id
            ),
            json=response_data,
            status=200,
        )

        assert self.bot.follow(username)
        assert self.bot.total["follows"] == follows_at_start + 1
        assert self.bot.followed_file.list[-1] == str(user_id)
        assert str(user_id) in self.bot.following

    @responses.activate
    @pytest.mark.parametrize(
        "user_ids",
        [
            [
                str(TEST_SEARCH_USERNAME_ITEM["pk"]),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 1),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 2),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 3),
            ],
            [
                str(TEST_SEARCH_USERNAME_ITEM["pk"]),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 4),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 5),
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 6),
            ],
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_follow_users(self, patched_time_sleep, user_ids):
        self.bot._following = [1]
        reset_files(self.bot)
        follows_at_start = self.bot.total["follows"]
        self.bot.followed_file.append(str(user_ids[1]))
        self.bot.unfollowed_file.append(str(user_ids[2]))
        self.bot.skipped_file.append(str(user_ids[3]))

        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()

        my_test_search_username_item["is_verified"] = False
        my_test_search_username_item["is_business"] = False
        my_test_search_username_item["is_private"] = False
        my_test_search_username_item["follower_count"] = 100
        my_test_search_username_item["following_count"] = 15
        my_test_search_username_item["media_count"] = (
            self.bot.min_media_count_to_follow + 1
        )
        my_test_search_username_item["has_anonymous_profile_picture"] = False
        my_test_username_info_item["username"] = TEST_SEARCH_USERNAME_ITEM["username"]
        my_test_username_info_item["is_verified"] = False
        my_test_username_info_item["is_business"] = False
        my_test_username_info_item["is_private"] = False
        my_test_username_info_item["follower_count"] = 100
        my_test_username_info_item["following_count"] = 15
        my_test_username_info_item["media_count"] = (
            self.bot.min_media_count_to_follow + 1
        )
        my_test_username_info_item["has_anonymous_profile_picture"] = False

        for user_id in user_ids:
            my_test_search_username_item["pk"] = user_id
            my_test_username_info_item["pk"] = user_id

            response_data = {"status": "ok", "user": my_test_search_username_item}
            responses.add(
                responses.GET,
                "{api_url}users/{username}/usernameinfo/".format(
                    api_url=API_URL, username=user_id
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok", "user": my_test_username_info_item}
            responses.add(
                responses.GET,
                "{api_url}users/{user_id}/info/".format(
                    api_url=API_URL, user_id=user_id
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok"}
            responses.add(
                responses.POST,
                "{api_url}friendships/create/{user_id}/".format(
                    api_url=API_URL, user_id=user_id
                ),
                json=response_data,
                status=200,
            )

        test_broken_items = [] == self.bot.follow_users(user_ids)
        test_follows = self.bot.total["follows"] == follows_at_start + 1
        test_following = self.bot.following == [1, user_ids[0]]
        test_followed = str(user_ids[0]) in self.bot.followed_file.list
        assert test_broken_items and test_follows and test_followed and test_following

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value=None)
    def test_follow_followers(self, patched_time_sleep, username):
        self.blacklist = []
        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
        my_test_follower_item = TEST_FOLLOWER_ITEM.copy()

        self.bot._following = []
        reset_files(self.bot)
        follows_at_start = self.bot.total["follows"]

        response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
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
        my_test_follower_items = [
            my_test_follower_item.copy() for _ in range(results_3)
        ]
        my_test_search_username_items = [
            my_test_search_username_item.copy() for _ in range(results_3)
        ]
        my_test_username_info_items = [
            my_test_username_info_item.copy() for _ in range(results_3)
        ]

        for i, _ in enumerate(range(results_3)):
            my_test_follower_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_follower_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
        response_data_3 = {
            "status": "ok",
            "big_list": False,
            "next_max_id": None,
            "sections": None,
            "users": my_test_follower_items,
        }
        responses.add(
            responses.GET,
            (
                "{api_url}friendships/{user_id}/followers/?" + "rank_token={rank_token}"
            ).format(
                api_url=API_URL, user_id=username, rank_token=self.bot.api.rank_token
            ),
            json=response_data_3,
            status=200,
        )

        for i, _ in enumerate(range(results_3)):
            my_test_search_username_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
            my_test_search_username_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_search_username_items[i]["is_verified"] = False
            my_test_search_username_items[i]["is_business"] = False
            my_test_search_username_items[i]["is_private"] = False
            my_test_search_username_items[i]["follower_count"] = 100
            my_test_search_username_items[i]["following_count"] = 15
            my_test_search_username_items[i]["media_count"] = (
                self.bot.min_media_count_to_follow + 1
            )
            my_test_search_username_items[i]["has_anonymous_profile_picture"] = False

            my_test_username_info_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
            my_test_username_info_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_username_info_items[i]["is_verified"] = False
            my_test_username_info_items[i]["is_business"] = False
            my_test_username_info_items[i]["is_private"] = False
            my_test_username_info_items[i]["follower_count"] = 100
            my_test_username_info_items[i]["following_count"] = 15
            my_test_username_info_items[i]["media_count"] = (
                self.bot.min_media_count_to_follow + 1
            )
            my_test_username_info_items[i]["has_anonymous_profile_picture"] = False

            response_data = {"status": "ok", "user": my_test_search_username_items[i]}
            responses.add(
                responses.GET,
                "{api_url}users/{username}/usernameinfo/".format(
                    api_url=API_URL,
                    username=my_test_search_username_items[i]["username"],
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok", "user": my_test_username_info_items[i]}
            responses.add(
                responses.GET,
                "{api_url}users/{user_id}/info/".format(
                    api_url=API_URL, user_id=my_test_username_info_items[i]["pk"]
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok"}
            responses.add(
                responses.POST,
                "{api_url}friendships/create/{user_id}/".format(
                    api_url=API_URL, user_id=my_test_username_info_items[i]["pk"]
                ),
                json=response_data,
                status=200,
            )

        self.bot.follow_followers(username)

        test_follows = self.bot.total["follows"] == follows_at_start + results_3
        test_following = sorted(self.bot.following) == [
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        test_followed = sorted(self.bot.followed_file.list) == [
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        assert test_follows and test_following and test_followed

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value=None)
    def test_follow_following(self, patched_time_sleep, username):
        self.blacklist = []
        my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
        my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
        my_test_following_item = TEST_FOLLOWING_ITEM.copy()

        self.bot._following = []
        reset_files(self.bot)
        follows_at_start = self.bot.total["follows"]

        response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
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
        my_test_following_items = [
            my_test_following_item.copy() for _ in range(results_3)
        ]
        my_test_search_username_items = [
            my_test_search_username_item.copy() for _ in range(results_3)
        ]
        my_test_username_info_items = [
            my_test_username_info_item.copy() for _ in range(results_3)
        ]

        for i, _ in enumerate(range(results_3)):
            my_test_following_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_following_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
        response_data_3 = {
            "status": "ok",
            "big_list": False,
            "next_max_id": None,
            "sections": None,
            "users": my_test_following_items,
        }
        responses.add(
            responses.GET,
            (
                "{api_url}friendships/{user_id}/following/?max_id={max_id}&"
                + "ig_sig_key_version={sig_key}&rank_token={rank_token}"
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

        for i, _ in enumerate(range(results_3)):
            my_test_search_username_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
            my_test_search_username_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_search_username_items[i]["is_verified"] = False
            my_test_search_username_items[i]["is_business"] = False
            my_test_search_username_items[i]["is_private"] = False
            my_test_search_username_items[i]["follower_count"] = 100
            my_test_search_username_items[i]["following_count"] = 15
            my_test_search_username_items[i]["media_count"] = (
                self.bot.min_media_count_to_follow + 1
            )
            my_test_search_username_items[i]["has_anonymous_profile_picture"] = False

            my_test_username_info_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
            my_test_username_info_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_username_info_items[i]["is_verified"] = False
            my_test_username_info_items[i]["is_business"] = False
            my_test_username_info_items[i]["is_private"] = False
            my_test_username_info_items[i]["follower_count"] = 100
            my_test_username_info_items[i]["following_count"] = 15
            my_test_username_info_items[i]["media_count"] = (
                self.bot.min_media_count_to_follow + 1
            )
            my_test_username_info_items[i]["has_anonymous_profile_picture"] = False

            response_data = {"status": "ok", "user": my_test_search_username_items[i]}
            responses.add(
                responses.GET,
                "{api_url}users/{username}/usernameinfo/".format(
                    api_url=API_URL,
                    username=my_test_search_username_items[i]["username"],
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok", "user": my_test_username_info_items[i]}
            responses.add(
                responses.GET,
                "{api_url}users/{user_id}/info/".format(
                    api_url=API_URL, user_id=my_test_username_info_items[i]["pk"]
                ),
                status=200,
                json=response_data,
            )

            response_data = {"status": "ok"}
            responses.add(
                responses.POST,
                "{api_url}friendships/create/{user_id}/".format(
                    api_url=API_URL, user_id=my_test_username_info_items[i]["pk"]
                ),
                json=response_data,
                status=200,
            )

        self.bot.follow_following(username)

        test_follows = self.bot.total["follows"] == follows_at_start + results_3
        test_following = sorted(self.bot.following) == [
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        test_followed = sorted(self.bot.followed_file.list) == [
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        assert test_follows and test_following and test_followed

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
        user_id = 1234567890
        response_data = {
            u"status": u"fail",
            u"feedback_title": u"feedback_required",
            u"feedback_message": u"This action was blocked. Please"
            u" try again later. We restrict certain content and "
            u"actions to protect our community. Tell us if you think"
            u" we made a mistake.",
            u"spam": True,
            u"feedback_action": u"report_problem",
            u"feedback_appeal_label": u"Report problem",
            u"feedback_ignore_label": u"OK",
            u"message": u"feedback_required",
            u"feedback_url": u"repute/report_problem/instagram_like_add/",
        }
        responses.add(
            responses.POST,
            "{api_url}friendships/create/{user_id}/".format(
                api_url=API_URL, user_id=user_id
            ),
            json=response_data,
            status=400,
        )
        responses.add(
            responses.POST,
            "{api_url}friendships/create/{user_id}/".format(
                api_url=API_URL, user_id=user_id
            ),
            status=200,
            json={"status": "ok"},
        )
        self.bot.follow(user_id, check_user=False)
        self.bot.follow(user_id, check_user=False)
        assert self.bot.blocked_actions["follows"] == result

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
        user_id = 1234567890
        response_data = {
            u"status": u"fail",
            u"feedback_title": u"feedback_required",
            u"feedback_message": u"This action was blocked. Please"
            u" try again later. We restrict certain content and "
            u"actions to protect our community. Tell us if you think"
            u" we made a mistake.",
            u"spam": True,
            u"feedback_action": u"report_problem",
            u"feedback_appeal_label": u"Report problem",
            u"feedback_ignore_label": u"OK",
            u"message": u"feedback_required",
            u"feedback_url": u"repute/report_problem/instagram_like_add/",
        }
        responses.add(
            responses.POST,
            "{api_url}friendships/create/{user_id}/".format(
                api_url=API_URL, user_id=user_id
            ),
            json=response_data,
            status=400,
        )
        responses.add(
            responses.POST,
            "{api_url}friendships/create/{user_id}/".format(
                api_url=API_URL, user_id=user_id
            ),
            json=response_data,
            status=400,
        )
        self.bot.follow(user_id, check_user=False)
        self.bot.follow(user_id, check_user=False)
        assert self.bot.blocked_actions["follows"] == result
