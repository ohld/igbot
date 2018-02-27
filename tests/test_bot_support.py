import pytest

from .test_bot import TestBot


class TestBotSupport(TestBot):

    @pytest.mark.parametrize('url,result', [
        ('https://google.com', ['https://google.com']),
        ('google.com', ['google.com']),
        ('google.com/search?q=instabot', ['google.com/search?q=instabot']),
        ('https://google.com/search?q=instabot', ['https://google.com/search?q=instabot']),
        ('мвд.рф', ['мвд.рф']),
        ('https://мвд.рф', ['https://мвд.рф']),
        ('http://мвд.рф/news/', ['http://мвд.рф/news/']),
        ('hello, google.com/search?q=test and bing.com', ['google.com/search?q=test', 'bing.com']),
    ])
    def test_extract_urls(self, url, result):
        assert self.BOT.extract_urls(url) == result
