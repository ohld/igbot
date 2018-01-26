import responses

from instabot.api.config import API_URL, SIG_KEY_VERSION

from .test_bot import TestBot
from .test_variables import TEST_PHOTO_ITEM, TEST_USER_ITEM


class TestBotGet(TestBot):
    @responses.activate
    def test_get_media_owner(self):
        media_id = 1234

        responses.add(
            responses.POST, "{API_URL}media/{media_id}/info/".format(
                API_URL=API_URL, media_id=media_id),
            json={
                "auto_load_more_enabled": True,
                "num_results": 1,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM]
            }, status=200)
        responses.add(
            responses.POST, "{API_URL}media/{media_id}/info/".format(
                API_URL=API_URL, media_id=media_id),
            json={"status": "ok"}, status=200)

        owner = self.BOT.get_media_owner(media_id)

        assert owner == str(TEST_PHOTO_ITEM["user"]["pk"])

        owner = self.BOT.get_media_owner(media_id)

        assert owner is False

    @responses.activate
    def test_get_popular_medias(self):
        results = 5
        responses.add(
            responses.GET, "{API_URL}feed/popular/?people_teaser_supported=1&rank_token={rank_token}&ranked_content=true&".format(
                API_URL=API_URL, rank_token=self.BOT.rank_token),
            json={
                "auto_load_more_enabled": True,
                "num_results": results,
                "status": "ok",
                "more_available": False,
                "items": [TEST_PHOTO_ITEM for _ in range(results)]
            }, status=200)

        medias = self.BOT.get_popular_medias()

        assert medias == [str(TEST_PHOTO_ITEM["pk"]) for _ in range(results)]
        assert len(medias) == results

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
            responses.GET, '{API_URL}feed/user/{user_id}/?max_id=&min_timestamp=&rank_token={rank_token}&ranked_content=true'.format(
                API_URL=API_URL, user_id=self.BOT.user_id, rank_token=self.BOT.rank_token),
            json=response_data, status=200)

        medias = self.BOT.get_your_medias()

        assert medias == [my_test_photo_item["pk"] for _ in range(results)]
        assert len(medias) == results

        medias = self.BOT.get_your_medias(as_dict=True)

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
            responses.GET, '{API_URL}feed/only_me_feed/?rank_token={rank_token}&ranked_content=true&'.format(
                API_URL=API_URL, rank_token=self.BOT.rank_token),
            json=response_data, status=200)

        medias = self.BOT.get_archived_medias()

        assert medias == [my_test_photo_item["pk"] for _ in range(results)]
        assert len(medias) == results

        medias = self.BOT.get_archived_medias(as_dict=True)

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
            "rank_token": self.BOT.rank_token,
            "status": "ok",
            "users": [my_test_user_item for _ in range(results)]
        }
        responses.add(
            responses.GET, '{API_URL}users/search/?ig_sig_key_version={SIG_KEY}&is_typeahead=true&query={query}&rank_token={rank_token}'.format(
                API_URL=API_URL, rank_token=self.BOT.rank_token, query=query, SIG_KEY=SIG_KEY_VERSION), json=response_data, status=200)

        medias = self.BOT.search_users(query)

        assert medias == [str(my_test_user_item["pk"]) for _ in range(results)]
        assert len(medias) == results
