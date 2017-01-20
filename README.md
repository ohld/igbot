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
import instabot
api = instabot.API()
api.login()
api.follow('ohld')
api.logout()
```

## How to run
Choose any example from [examples](https://github.com/ohld/instabot/tree/master/examples) and run
```
python example.py
```

## Implemented methods

### API

* login / logout
* like / unlike
* follow / unfollow
* comment
* get profile info
* get following
* get user id by username
* get current feed

## Examples

### Bot

* subscribe_to_following.py

subscribes to person's following

* unfollow_non_followers.py

unsubscribes from persons that are not follow you

* like_current_feed.py

likes last medias from your feed

### Statistics

* save_my_stats.py

Saves every hour to track your growth

* save_my_following.py

Saves your followings list into *.tsv format

*More information you can find in examples folder.*
___
_inspired by @mgp25 and @LevPasha_
