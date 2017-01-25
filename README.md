# instabot
Cool instagram scripts and API wrapper. Written in Python.
___
As you may know, Instagram closed it's API in summer 2016. This Python module can do the same thing without any effort.

If you have any ideas, please, leave them in [issues section](https://github.com/ohld/instabot/issues) or in our [telegram chat](https://t.me/joinchat/AAAAAAuPofDcEgHBSysAGg).

*Your Contribution and Support through Stars will be highly appreciated.*

## How to install

Install latest stable version from pip

```
pip install -U instabot
```

If you have problems like "some package not found" try
```
pip install -r requirements.txt
```

## Implemented [bot](https://github.com/ohld/instabot/blob/master/instabot/bot/bot.py) methods

  * like logged user's feed
  * like person's last medias
  * like medias by hashtag
  * unfollow non followers

``` python
from instabot import Bot
bot = Bot()
```
| method        | description | example  |
| ------------- |:-------------:| -----:|
| login(username=None, password=None)  | Login to into Instagram, you can pass your login and password as params | bot.login()|
| logout()     | Safe logout from bot      |   bot.logout() |
| save_checkpoint() | Save [checkpoint](https://github.com/ohld/instabot/blob/master/instabot/bot/bot_checkpoint.py) of your account. Return path to it.|    bot.save_checkpoint() |
| load_checkpoint(path)| Load checkpoint from path. Return Checkpoint class.|  cp = bot.load_checkpoint( bot.last_checkpoint_path)|
| load_last_checkpoint()| Load last checkpoint if it was in current session| bot.load_last_checkpoint()|
| checkpoint_followers_diff(cp)| returns a list of users who become your followers after checkpoint| bot.checkpoint_followers_diff(cp)|
| checkpoint_following_diff(cp)| returns a list of users who become your following after checkpoint| bot.checkpoint_following_diff(cp)|
| revert_to_checkpoint(cp)| Unfollow the new following made after checkpoint creation| bot.revert_to_checkpoint(cp)|
| like_medias(medias_list)| Like every media in list of media ids| bot.like_medias(medias)|
| follow_users(userids_list)| Follow users in list | bot.follow_users(userids)|
| unfollow_users(userids)| Unfollow users in list | bot.unfollow_users(userids)|
| like_timeline(amount=None)| Likes your timeline feed| bot.like_timeline()|
| like_user_id(user_id, amount=None)| Likes user_id's last medias| bot.like_user_id("352300017")|
| unfollow_non_followers()| Unfollow users that don't follow you| bot.unfollow_non_followers()|
| like_hashtag(tag, amount=None)| Like last medias by hashtag| bot.like_hashtag("mipt)|
| like_and_follow(user_id, nlikes=None)| Likes last person's medias and follow him. | bot.like_and_follow("352300017")|
| like_and_follow_media_likers( media, nlikes=3)| Take likers of media and do like_and_follow() with them| bot.like_and_follow_your_feed_likers()|
| like_and_follow_your_feed_likers( nlikes=3)| Take likers of your last media and do like_and_follow() with them| bot.like_and_follow_your_feed_likers()|


## Sample usage

```python
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
___
_inspired by @mgp25 and @LevPasha_
