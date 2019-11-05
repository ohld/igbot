import tempfile

import pytest
import responses

from instabot import utils
from instabot.api.config import API_URL, SIG_KEY_VERSION

from .test_bot import TestBot
from .test_variables import (
    TEST_CAPTION_ITEM,
    TEST_COMMENT_ITEM,
    TEST_COMMENT_LIKER_ITEM,
    TEST_FOLLOWER_ITEM,
    TEST_FOLLOWING_ITEM,
    TEST_INBOX_THREAD_ITEM,
    TEST_LOCATION_ITEM,
    TEST_MEDIA_LIKER,
    TEST_MOST_RECENT_INVITER_ITEM,
    TEST_PHOTO_ITEM,
    TEST_SEARCH_USERNAME_ITEM,
    TEST_TIMELINE_PHOTO_ITEM,
    TEST_USER_ITEM,
    TEST_USER_TAG_ITEM,
    TEST_USERNAME_INFO_ITEM,
)

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestBotGet(TestBot):
    @responses.activate
    def test_get_media_owner(self):
        media_id = 1234

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
        # responses.add(
        #     responses.POST, "{api_url}media/{media_id}/info/".format(
        #     api_url=API_URL, media_id=media_id),
        #     json={"status": "ok"}, status=200)

        owner = self.bot.get_media_owner(media_id)

        assert owner == str(TEST_PHOTO_ITEM["user"]["pk"])

        # owner = self.bot.get_media_owner(media_id)

        # assert owner is False

    @responses.activate
    def test_get_media_info(self):
        media_id = 1234

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
        # responses.add(
        #     responses.POST, "{api_url}media/{media_id}/info/".format(
        #     api_url=API_URL, media_id=media_id),
        #     json={"status": "ok"}, status=200)

        expected_result = {}
        for key in TEST_PHOTO_ITEM:
            expected_result[key] = TEST_PHOTO_ITEM[key]

        result = self.bot.get_media_info(media_id)

        assert result[0] == expected_result

    @responses.activate
    def test_get_popular_medias(self):
        results = 5
        responses.add(
            responses.GET,
            (
                "{api_url}feed/popular/?people_teaser_supported=1" +
                "&rank_token={rank_token}&ranked_content=true&"
            ).format(
                api_url=API_URL, rank_token=self.bot.api.rank_token
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results)],
            },
            status=200,
        )

        medias = self.bot.get_popular_medias()

        assert medias == [str(TEST_PHOTO_ITEM["id"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    def test_get_timeline_medias(self):
        self.bot.max_likes_to_like = TEST_PHOTO_ITEM["like_count"] + 1
        results = 8
        responses.add(
            responses.POST,
            "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "is_direct_v2_enabled": True,
                "status": "ok",
                "next_max_id": None,
                "more_available": False,
                "feed_items": [
                    TEST_TIMELINE_PHOTO_ITEM for _ in range(results)
                ],
            },
            status=200,
        )
        responses.add(
            responses.POST,
            "{api_url}feed/timeline/".format(api_url=API_URL),
            json={"status": "fail"},
            status=400,
        )

        medias = self.bot.get_timeline_medias()

        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_timeline_medias()

        assert medias == []
        assert len(medias) == 0

    @responses.activate
    def test_get_timeline_users(self):
        results = 8
        responses.add(
            responses.POST,
            "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "is_direct_v2_enabled": True,
                "status": "ok",
                "next_max_id": None,
                "more_available": False,
                "feed_items": [
                    TEST_TIMELINE_PHOTO_ITEM for _ in range(results)
                ],
            },
            status=200,
        )
        responses.add(
            responses.POST,
            "{api_url}feed/timeline/".format(api_url=API_URL),
            json={"status": "fail"},
            status=400,
        )

        users = self.bot.get_timeline_users()

        assert users == [
            str(TEST_TIMELINE_PHOTO_ITEM["media_or_ad"]["user"]["pk"])
            for _ in range(results)
        ]
        assert len(users) == results

        users = self.bot.get_timeline_users()

        assert users == []
        assert len(users) == 0

    @responses.activate
    def test_get_your_medias(self):
        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["user"]["pk"] = self.USER_ID
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results)],
        }
        responses.add(
            responses.GET,
            "{api_url}feed/user/{user_id}/".format(
                api_url=API_URL,
                user_id=self.bot.user_id,
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.get_your_medias()

        assert medias == [my_test_photo_item["id"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_your_medias(as_dict=True)

        assert medias == response_data["items"]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234567890, "1234567890"])
    def test_get_user_medias(self, user_id):
        results = 4
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["user"]["pk"] = user_id
        my_test_photo_items = []
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        expect_filtered = 0
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[3]["like_count"] = self.bot.max_likes_to_like - 1
        expect_filtered += 1
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": my_test_photo_items,
        }
        responses.add(
            responses.GET,
            "{api_url}feed/user/{user_id}/".format(
                api_url=API_URL,
                user_id=user_id,
                rank_token=self.bot.api.rank_token
            ),
            json=response_data,
            status=200,
        )

        # no need to test is_comment=True because there's no item 'comments' in
        # user feed object returned by `feed/user/{user_id}/` API call.

        medias = self.bot.get_user_medias(
            user_id,
            filtration=False,
            is_comment=False
        )
        assert medias == [
            test_photo_item["id"] for test_photo_item in my_test_photo_items
        ]
        assert len(medias) == results

        medias = self.bot.get_user_medias(
            user_id,
            filtration=True,
            is_comment=False
        )
        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == results - expect_filtered

    @responses.activate
    def test_get_archived_medias(self):
        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["user"]["pk"] = self.USER_ID
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}feed/only_me_feed/?rank_token={rank_token}&" +
                "ranked_content=true&"
            ).format(
                api_url=API_URL, rank_token=self.bot.api.rank_token
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.get_archived_medias()

        assert medias == [my_test_photo_item["id"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_archived_medias(as_dict=True)

        assert medias == response_data["items"]
        assert len(medias) == results

    @responses.activate
    def test_search_users(self):
        results = 5
        query = "test"
        my_test_user_item = TEST_USER_ITEM
        response_data = {
            "has_more": True,
            "num_results": results,
            "rank_token": self.bot.api.rank_token,
            "status": "ok",
            "users": [my_test_user_item for _ in range(results)],
        }
        responses.add(
            responses.GET,
            (
                "{api_url}users/search/?ig_sig_key_version={sig_key}&" +
                "is_typeahead=true&query={query}&rank_token={rank_token}"
            ).format(
                api_url=API_URL,
                rank_token=self.bot.api.rank_token,
                query=query,
                sig_key=SIG_KEY_VERSION,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.search_users(query)

        assert medias == [str(my_test_user_item["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    def test_search_users_failed(self):
        query = "test"
        response_data = {"status": "fail"}
        responses.add(
            responses.GET,
            (
                "{api_url}users/search/?ig_sig_key_version={sig_key}" +
                "&is_typeahead=true&query={query}&rank_token={rank_token}"
            ).format(
                api_url=API_URL,
                rank_token=self.bot.api.rank_token,
                query=query,
                sig_key=SIG_KEY_VERSION,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.search_users(query)

        assert medias == []

    @responses.activate
    def test_get_comments(self):
        results = 5
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

        comments = self.bot.get_media_comments(media_id)
        assert comments == response_data["comments"]
        assert len(comments) == results

    @responses.activate
    def test_get_comments_text(self):
        results = 5
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

        comments = self.bot.get_media_comments(media_id, only_text=True)
        expected_result = [
            comment["text"] for comment in response_data["comments"]
        ]

        assert comments == expected_result
        assert len(comments) == results

    @responses.activate
    def test_get_comments_failed(self):
        response_data = {"status": "fail"}
        media_id = 1234567890
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=200,
        )

        comments = self.bot.get_media_comments(media_id)
        assert comments == []

    @responses.activate
    def test_get_commenters(self):
        results = 5
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

        expected_commenters = [
            str(TEST_COMMENT_ITEM["user"]["pk"]) for _ in range(results)
        ]

        commenters = self.bot.get_media_commenters(media_id)
        assert commenters == expected_commenters
        assert len(commenters) == results

    @responses.activate
    def test_get_commenters_failed(self):
        response_data = {"status": "fail"}
        media_id = 1234567890
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/comments/?".format(
                api_url=API_URL, media_id=media_id
            ),
            json=response_data,
            status=200,
        )

        expected_commenters = []

        commenters = self.bot.get_media_commenters(media_id)
        assert commenters == expected_commenters

    @pytest.mark.parametrize(
        "url,result",
        [
            ("https://www.instagram.com/p/BfHrDvCDuzC/", 1713527555896569026),
            ("test", False),
        ],
    )
    def test_get_media_id_from_link_with_wrong_data(self, url, result):
        media_id = self.bot.get_media_id_from_link(url)

        assert result == media_id

    @responses.activate
    @pytest.mark.parametrize(
        "comments", [["comment1", "comment2", "comment3"], [], None]
    )
    def test_get_comment(self, comments):
        fname = tempfile.mkstemp()[1]  # Temporary file
        self.bot.comments_file = utils.file(fname, verbose=True)
        if comments:
            for comment in comments:
                self.bot.comments_file.append(comment)
            assert self.bot.get_comment() in self.bot.comments_file.list
        else:
            assert self.bot.get_comment() == "Wow!"

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234, "1234"])
    def test_get_username_info(self, user_id):
        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        expected_result = {}
        for key in TEST_USERNAME_INFO_ITEM:
            expected_result[key] = TEST_USERNAME_INFO_ITEM[key]

        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL,
                user_id=user_id
            ),
            status=200,
            json=response_data,
        )

        result = self.bot.get_user_info(user_id)

        assert result == expected_result

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234, "1234"])
    @patch("time.sleep", return_value=None)
    def test_get_username_from_user_id(self, patched_time_sleep, user_id):
        response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
        expected_user_id = str(TEST_USERNAME_INFO_ITEM["username"])

        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL,
                user_id=user_id
            ),
            status=200,
            json=response_data,
        )

        result = self.bot.get_username_from_user_id(user_id)

        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize("user_id", ["123231231231234", 123231231231234])
    @patch("time.sleep", return_value=None)
    def test_get_username_from_user_id_404(self, patched_time_sleep, user_id):
        response_data = {"status": "fail", "message": "User not found"}
        responses.add(
            responses.GET,
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL,
                user_id=user_id
            ),
            status=404,
            json=response_data,
        )

        assert not self.bot.get_username_from_user_id(user_id)

    @responses.activate
    @pytest.mark.parametrize("username", ["@test", "test", "1234"])
    @patch("time.sleep", return_value=None)
    def test_get_user_id_from_username(self, patched_time_sleep, username):
        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        expected_user_id = str(TEST_SEARCH_USERNAME_ITEM["pk"])

        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
            ),
            status=200,
            json=response_data,
        )

        result = self.bot.get_user_id_from_username(username)
        del self.bot._usernames[username]  # Invalidate cache

        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize(
        "username", ["usernotfound", "nottexisteduser", "123231231231234"]
    )
    @patch("time.sleep", return_value=None)
    def test_get_user_id_from_username_404(self, patched_time_sleep, username):
        response_data = {"status": "fail", "message": "User not found"}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=username
            ),
            status=404,
            json=response_data,
        )

        assert not self.bot.get_user_id_from_username(username)

    @responses.activate
    @pytest.mark.parametrize(
        "username,url,result",
        [
            ("@test", "test", str(TEST_SEARCH_USERNAME_ITEM["pk"])),
            ("test", "test", str(TEST_SEARCH_USERNAME_ITEM["pk"])),
            ("1234", "1234", "1234"),
            (1234, "1234", "1234"),
        ],
    )
    @patch("time.sleep", return_value=None)
    def test_convert_to_user_id(
        self,
        patched_time_sleep,
        username,
        url,
        result
    ):
        response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
        responses.add(
            responses.GET,
            "{api_url}users/{username}/usernameinfo/".format(
                api_url=API_URL, username=url
            ),
            status=200,
            json=response_data,
        )

        user_id = self.bot.convert_to_user_id(username)

        assert result == user_id

    @responses.activate
    @pytest.mark.parametrize("user_id", ["3998456661", 3998456661])
    def test_get_user_tags_medias(self, user_id):
        results = 8
        responses.add(
            responses.GET,
            (
                "{api_url}usertags/{user_id}/feed/?rank_token={rank_token}" +
                "&ranked_content=true&"
            ).format(
                api_url=API_URL,
                user_id=user_id,
                rank_token=self.bot.api.rank_token
            ),
            json={
                "status": "ok",
                "num_results": results,
                "auto_load_more_enabled": True,
                "items": [TEST_USER_TAG_ITEM for _ in range(results)],
                "more_available": False,
                "total_count": results,
                "requires_review": False,
                "new_photos": [],
            },
            status=200,
        )

        medias = self.bot.get_user_tags_medias(user_id)

        assert medias == [
            str(TEST_USER_TAG_ITEM["pk"]) for _ in range(results)
        ]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    def test_get_hashtag_medias(self, hashtag):

        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_items = []
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        expect_filtered = 0
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[3]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": my_test_photo_items,
        }

        responses.add(
            responses.GET,
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}&rank_token=" +
                "{rank_token}&ranked_content=true&"
            ).format(
                api_url=API_URL,
                hashtag=hashtag,
                max_id="",
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.get_hashtag_medias(hashtag, filtration=False)
        assert medias == [
            test_photo_item["id"] for test_photo_item in my_test_photo_items
        ]
        assert len(medias) == results

        medias = self.bot.get_hashtag_medias(hashtag, filtration=True)
        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == results - expect_filtered

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    def test_get_total_hashtag_medias(self, hashtag):

        amount = 5
        results = 10
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_items = []
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        expect_filtered = 0
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[3]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": True,
            "next_max_id": TEST_PHOTO_ITEM["id"],
            "items": my_test_photo_items,
        }

        responses.add(
            responses.GET,
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}" +
                "&rank_token={rank_token}&ranked_content=true&"
            ).format(
                api_url=API_URL,
                hashtag=hashtag,
                max_id="",
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.get_total_hashtag_medias(
            hashtag, amount=amount, filtration=False
        )
        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items[:amount]
        ]
        assert len(medias) == amount

        medias = self.bot.get_total_hashtag_medias(
            hashtag, amount=amount, filtration=True
        )
        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items[:amount]
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == amount - expect_filtered

    @responses.activate
    @pytest.mark.parametrize("media_id", ["1234567890", 1234567890])
    def test_get_media_likers(self, media_id):
        results = 5
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/likers/?".format(
                api_url=API_URL, media_id=media_id
            ),
            json={
                "user_count": results,
                "status": "ok",
                "users": [TEST_MEDIA_LIKER for _ in range(results)],
            },
            status=200,
        )

        medias = self.bot.get_media_likers(media_id)

        assert medias == [str(TEST_MEDIA_LIKER["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [19, "19"])
    def test_get_last_user_medias(self, user_id):

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
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp" +
                "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
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

        medias = self.bot.get_last_user_medias(user_id, count=results)

        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [19, "19"])
    def test_get_total_user_medias(self, user_id):

        results = 18
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
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp" +
                "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
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

        medias = self.bot.get_total_user_medias(user_id)
        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", ["1234567890", 1234567890])
    def test_get_user_likers(self, user_id):

        results_1 = 1
        responses.add(
            responses.GET,
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp" +
                "={min_timestamp}&rank_token={rank_token}&ranked_content=true"
            ).format(
                api_url=API_URL,
                user_id=user_id,
                max_id="",
                min_timestamp=None,
                rank_token=self.bot.api.rank_token,
            ),
            json={
                "auto_load_more_enabled": True,
                "num_results": results_1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results_1)],
            },
            status=200,
        )

        results_2 = 3
        responses.add(
            responses.GET,
            "{api_url}media/{media_id}/likers/?".format(
                api_url=API_URL, media_id=TEST_PHOTO_ITEM["id"]
            ),
            json={
                "user_count": results_2,
                "status": "ok",
                "users": [TEST_MEDIA_LIKER for _ in range(results_2)],
            },
            status=200,
        )

        user_ids = self.bot.get_user_likers(user_id)

        assert user_ids == list(
            {str(TEST_MEDIA_LIKER["pk"]) for _ in range(results_2)}
        )
        assert len(user_ids) == len(
            list({str(TEST_MEDIA_LIKER["pk"]) for _ in range(results_2)})
        )

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    def test_get_user_followers(self, username):

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
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL,
                user_id=username
            ),
            status=200,
            json=response_data_2,
        )

        results_3 = 5
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
                "{api_url}friendships/{user_id}/followers/?" +
                "rank_token={rank_token}"
            ).format(
                api_url=API_URL,
                user_id=username,
                rank_token=self.bot.api.rank_token
            ),
            json=response_data_3,
            status=200,
        )

        user_ids = self.bot.get_user_followers(username)

        assert user_ids == [
            str(TEST_FOLLOWER_ITEM["pk"]) for _ in range(results_3)
        ]

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    def test_get_user_following(self, username):

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
            "{api_url}users/{user_id}/info/".format(
                api_url=API_URL,
                user_id=username
            ),
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
                "{api_url}friendships/{user_id}/following/?max_id={max_id}" +
                "&ig_sig_key_version={sig_key}&rank_token={rank_token}"
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

        user_ids = self.bot.get_user_following(username)

        assert user_ids == [
            str(TEST_FOLLOWING_ITEM["pk"]) for _ in range(results_3)
        ]

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    def test_get_hashtag_users(self, hashtag):

        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_items = []
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        expect_filtered = 0
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[3]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": my_test_photo_items,
        }

        responses.add(
            responses.GET,
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}" +
                "&rank_token={rank_token}&ranked_content=true&"
            ).format(
                api_url=API_URL,
                hashtag=hashtag,
                max_id="",
                rank_token=self.bot.api.rank_token,
            ),
            json=response_data,
            status=200,
        )

        medias = self.bot.get_hashtag_users(hashtag)
        assert medias == [
            str(test_photo_item["user"]["pk"])
            for test_photo_item in my_test_photo_items
        ]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize(
        "comment_id",
        [
            "12345678901234567",
            12345678901234567
        ]
    )
    def test_get_comment_likers(self, comment_id):
        results = 5
        response_data = {
            "status": "ok",
            "users": [TEST_COMMENT_LIKER_ITEM for _ in range(results)],
        }
        responses.add(
            responses.GET,
            "{api_url}media/{comment_id}/comment_likers/?".format(
                api_url=API_URL, comment_id=comment_id
            ),
            json=response_data,
            status=200,
        )
        user_ids = self.bot.get_comment_likers(comment_id)
        assert user_ids == [
            str(TEST_COMMENT_LIKER_ITEM["pk"])
            for _ in range(results)
        ]
        assert len(user_ids) == results

    @responses.activate
    @pytest.mark.parametrize("latitude", [1.2345])
    @pytest.mark.parametrize("longitude", [9.8765])
    def test_get_locations_from_coordinates(self, latitude, longitude):
        results = 10
        response_data = {
            "has_more": False,
            "items": [TEST_LOCATION_ITEM for _ in range(results)],
            "rank_token": self.bot.api.rank_token,
            "status": "ok",
        }
        responses.add(
            responses.GET,
            (
                "{api_url}fbsearch/places/?rank_token={rank_token}" +
                "&query={query}&lat={lat}&lng={lng}"
            ).format(
                api_url=API_URL,
                rank_token=self.bot.api.rank_token,
                query="",
                lat=latitude,
                lng=longitude,
            ),
            json=response_data,
            status=200,
        )
        locations = self.bot.get_locations_from_coordinates(
            latitude,
            longitude
        )
        assert locations == [TEST_LOCATION_ITEM for _ in range(results)]
        assert len(locations) == results

    @responses.activate
    def test_get_messages(self):
        results = 5
        response_data = {
            u"status": "ok",
            u"pending_requests_total": 2,
            u"seq_id": 182,
            u"snapshot_at_ms": 1547815538244,
            u"most_recent_inviter": TEST_MOST_RECENT_INVITER_ITEM,
            u"inbox": {
                u"blended_inbox_enabled": True,
                u"has_older": False,
                u"unseen_count": 1,
                u"unseen_count_ts": 1547815538242025,
                u"threads": [TEST_INBOX_THREAD_ITEM for _ in range(results)],
            },
        }
        responses.add(
            responses.POST,
            "{api_url}direct_v2/inbox/".format(api_url=API_URL),
            json=response_data,
            status=200,
        )
        inbox = self.bot.get_messages()
        assert inbox == response_data
