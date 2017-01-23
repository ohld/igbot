# instabot
Cool instagram scripts and API wrapper. Written in Python.
___
As you may know, Instagram closed it's API in summer 2016. This Python module can do the same thing without any effort.

If you have any ideas, please, leave them in [issues section](https://github.com/ohld/instabot/issues).

*Your Contribution and Support through Stars will be highly appreciated.*

## How to install

Install latest stable version from pip

```
pip install -U instabot
```

Or from github

```
pip install git+git://github.com/ohld/instabot.git
```

If you have problems like "some package not found" try
```
pip install -r requirements.txt
```

## Sample usage

```
from instabot import Bot
bot = Bot()
bot.login()
bot.like_timeline()
bot.like_hashtag("dog")
bot.unfollow_non_followers()
bot.logout()
```

## How to run
Choose any example from [examples](https://github.com/ohld/instabot/tree/master/examples) and run
```
python example.py
```

## Implemented methods

Almost all Instagram API methods are implemented.
Bot can do:

  * like logged user's feed
  * like person's last medias
  * like medias by hashtag
  * unfollow non followers

___
_inspired by @mgp25 and @LevPasha_
