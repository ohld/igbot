
import tempfile

import pytest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from instabot.api.config import API_URL, SIG_KEY_VERSION
from instabot import utils

from .test_bot import TestBot
from .test_variables import (TEST_CAPTION_ITEM, TEST_COMMENT_ITEM,
                             TEST_PHOTO_ITEM, TEST_SEARCH_USERNAME_ITEM,
                             TEST_USER_ITEM, TEST_USERNAME_INFO_ITEM)


class TestBotGet(TestBot):
    @responses.activate
    def test_get_media_owner(self):
        media_id = 1234

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
            json={"status": "ok"}, status=200)

        owner = self.bot.get_media_owner(media_id)

        assert owner == str(TEST_PHOTO_ITEM["user"]["pk"])

        owner = self.bot.get_media_owner(media_id)

        assert owner is False

    @responses.activate
    def test_get_popular_medias(self):
        results = 5
        responses.add(
            responses.GET, "{api_url}feed/popular/?people_teaser_supported=1&rank_token={rank_token}&ranked_content=true&".format(
                api_url=API_URL, rank_token=self.bot.api.rank_token),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results)]
            }, status=200)

        medias = self.bot.get_popular_medias()

        assert medias == [str(TEST_PHOTO_ITEM["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    def test_get_timeline_medias(self):
        self.bot.max_likes_to_like = TEST_PHOTO_ITEM['like_count'] + 1
        results = 8
        responses.add(
            responses.GET, "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "is_direct_v2_enabled": True,
                "status": "ok",
                "next_max_id": None,
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results)]
            }, status=200)
        responses.add(
            responses.GET, "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "status": "fail"
            }, status=400)

        medias = self.bot.get_timeline_medias()

        assert medias == [TEST_PHOTO_ITEM["pk"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_timeline_medias()

        assert medias == []
        assert len(medias) == 0

    @responses.activate
    def test_get_timeline_users(self):
        results = 8
        responses.add(
            responses.GET, "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "is_direct_v2_enabled": True,
                "status": "ok",
                "next_max_id": None,
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results)]
            }, status=200)
        responses.add(
            responses.GET, "{api_url}feed/timeline/".format(api_url=API_URL),
            json={
                "status": "fail"
            }, status=400)

        users = self.bot.get_timeline_users()

        assert users == [str(TEST_PHOTO_ITEM["user"]["pk"]) for _ in range(results)]
        assert len(users) == results

        users = self.bot.get_timeline_users()

        assert users == []
        assert len(users) == 0

    @responses.activate
    def test_get_your_medias(self):
        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item['user']['pk'] = self.USER_ID
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results)]
        }
        responses.add(
            responses.GET, '{api_url}feed/user/{user_id}/?max_id=&min_timestamp=&rank_token={rank_token}&ranked_content=true'.format(
                api_url=API_URL, user_id=self.bot.user_id, rank_token=self.bot.api.rank_token),
            json=response_data, status=200)

        medias = self.bot.get_your_medias()

        assert medias == [my_test_photo_item["pk"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_your_medias(as_dict=True)

        assert medias == response_data['items']
        assert len(medias) == results

    @responses.activate
    def test_get_archived_medias(self):
        results = 5
        my_test_photo_item = TEST_PHOTO_ITEM.copy()
        my_test_photo_item['user']['pk'] = self.USER_ID
        response_data = {
            "auto_load_more_enabled": True,
            "num_results": results,
            "status": "ok",
            "more_available": False,
            "items": [my_test_photo_item for _ in range(results)]
        }
        responses.add(
            responses.GET, '{api_url}feed/only_me_feed/?rank_token={rank_token}&ranked_content=true&'.format(
                api_url=API_URL, rank_token=self.bot.api.rank_token),
            json=response_data, status=200)

        medias = self.bot.get_archived_medias()

        assert medias == [my_test_photo_item["pk"] for _ in range(results)]
        assert len(medias) == results

        medias = self.bot.get_archived_medias(as_dict=True)

        assert medias == response_data['items']
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
            "users": [my_test_user_item for _ in range(results)]
        }
        responses.add(
            responses.GET, '{api_url}users/search/?ig_sig_key_version={sig_key}&is_typeahead=true&query={query}&rank_token={rank_token}'.format(
                api_url=API_URL, rank_token=self.bot.api.rank_token, query=query, sig_key=SIG_KEY_VERSION), json=response_data, status=200)

        medias = self.bot.search_users(query)

        assert medias == [str(my_test_user_item["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    def test_search_users_failed(self):
        query = "test"
        response_data = {'status': 'fail'}
        responses.add(
            responses.GET, '{api_url}users/search/?ig_sig_key_version={sig_key}&is_typeahead=true&query={query}&rank_token={rank_token}'.format(
                api_url=API_URL, rank_token=self.bot.api.rank_token, query=query, sig_key=SIG_KEY_VERSION), json=response_data, status=200)

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
            "status": "ok"
        }
        media_id = 1234567890
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

        comments = self.bot.get_media_comments(media_id)
        assert comments == response_data['comments']
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
            "status": "ok"
        }
        media_id = 1234567890
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

        comments = self.bot.get_media_comments(media_id, only_text=True)
        expected_result = [comment['text'] for comment in response_data['comments']]

        assert comments == expected_result
        assert len(comments) == results

    @responses.activate
    def test_get_comments_failed(self):
        response_data = {"status": "fail"}
        media_id = 1234567890
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

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
            "status": "ok"
        }
        media_id = 1234567890
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

        expected_commenters = [str(TEST_COMMENT_ITEM['user']['pk']) for _ in range(results)]

        commenters = self.bot.get_media_commenters(media_id)
        assert commenters == expected_commenters
        assert len(commenters) == results

    @responses.activate
    def test_get_commenters_failed(self):
        response_data = {"status": "fail"}
        media_id = 1234567890
        responses.add(
            responses.GET, '{api_url}media/{media_id}/comments/?'.format(
                api_url=API_URL, media_id=media_id), json=response_data, status=200)

        expected_commenters = []

        commenters = self.bot.get_media_commenters(media_id)
        assert commenters == expected_commenters

    @pytest.mark.parametrize('url,result', [
        ('https://www.instagram.com/p/BfHrDvCDuzC/', 1713527555896569026),
        ('test', False)
    ])
    def test_get_media_id_from_link_with_wrong_data(self, url, result):
        media_id = self.bot.get_media_id_from_link(url)

        assert result == media_id

    @pytest.mark.parametrize('comments', [
        ['comment1', 'comment2', 'comment3'],
        [],
        None
    ])
    def test_get_comment(self, comments):
        fname = tempfile.mkstemp()[1]  # Temporary file
        self.bot.comments_file = utils.file(fname, verbose=True)
        if comments:
            for comment in comments:
                self.bot.comments_file.append(comment)
            assert self.bot.get_comment() in self.bot.comments_file.list
        else:
            assert self.bot.get_comment() == 'Wow!'

    @responses.activate
    @pytest.mark.parametrize('user_id', [
        1234, '1234'
    ])
    def test_get_username_from_user_id(self, user_id):
        response_data = {
            'status': 'ok',
            'user': TEST_USERNAME_INFO_ITEM
        }
        expected_user_id = str(TEST_USERNAME_INFO_ITEM['username'])

        responses.add(
            responses.GET, '{api_url}users/{user_id}/info/'.format(
                api_url=API_URL, user_id=user_id
            ), status=200, json=response_data)

        result = self.bot.get_username_from_user_id(user_id)

        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize('user_id', [
        '123231231231234', 123231231231234
    ])
    def test_get_username_from_user_id_404(self, user_id):
        response_data = {
            'status': 'fail',
            'message': 'User not found'
        }
        responses.add(
            responses.GET, '{api_url}users/{user_id}/info/'.format(
                api_url=API_URL, user_id=user_id
            ), status=404, json=response_data)

        assert not self.bot.get_username_from_user_id(user_id)

    @responses.activate
    @pytest.mark.parametrize('username', [
        '@test', 'test', '1234'
    ])
    def test_get_user_id_from_username(self, username):
        response_data = {
            'status': 'ok',
            'user': TEST_SEARCH_USERNAME_ITEM
        }
        expected_user_id = str(TEST_SEARCH_USERNAME_ITEM['pk'])

        responses.add(
            responses.GET, '{api_url}users/{username}/usernameinfo/'.format(
                api_url=API_URL, username=username
            ), status=200, json=response_data)

        result = self.bot.get_user_id_from_username(username)
        del self.bot._usernames[username]  # Invalidate cache

        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize('username', [
        'usernotfound', 'nottexisteduser', '123231231231234'
    ])
    def test_get_user_id_from_username_404(self, username):
        response_data = {
            'status': 'fail',
            'message': 'User not found'
        }
        responses.add(
            responses.GET, '{api_url}users/{username}/usernameinfo/'.format(
                api_url=API_URL, username=username
            ), status=404, json=response_data)

        assert not self.bot.get_user_id_from_username(username)

    @responses.activate
    @pytest.mark.parametrize('username,url,result', [
        ('@test', 'test', str(TEST_SEARCH_USERNAME_ITEM['pk'])),
        ('test', 'test', str(TEST_SEARCH_USERNAME_ITEM['pk'])),
        ('1234', '1234', '1234'),
        (1234, '1234', '1234')
    ])
    @patch('time.sleep', return_value=None)
    def test_convert_to_user_id(self, patched_time_sleep, username, url, result):
        response_data = {
            'status': 'ok',
            'user': TEST_SEARCH_USERNAME_ITEM
        }
        responses.add(
            responses.GET, '{api_url}users/{username}/usernameinfo/'.format(
                api_url=API_URL, username=url
            ), status=200, json=response_data)

        user_id = self.bot.convert_to_user_id(username)

        assert result == user_id
