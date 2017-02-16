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

## Implemented [bot](https://github.com/ohld/instabot/blob/master/instabot/bot/bot.py) methods

  * like logged user's feed
  * like person's last medias
  * like medias by hashtag
  * comment media by hashtag
  * unfollow non followers

``` python
from instabot import Bot
bot = Bot()
```
### Get

| method        | description | example  |
| ------------- |:-------------:| ------:|
| get_timeline_medias | Get list of media_ids from you timeline feed| bot.get_timeline_medias()|
| get_user_medias | Get list of user_id's medias | bot.get_user_medias("352300017")|
| get_hashtag_medias| Get list of medias by hashtag| bot.get_hashtag_medias("Dog")|
| get_geotag_medias| Get list of medias by geotag| TODO |
| get_timeline_users| Get list of users from your timeline feed| bot.get_timeline_users()|
| get_hashtag_users| Get list of users who posted with hashtag| TODO |
| get_geotag_users| Get list of users who posted with geotag| TODO |
| get_userid_from_username| Convert username to user_id| TODO |
| get_user_followers| Get list of user's followers| TODO |
| get_user_following| Get list of user's following| TODO |
| get_media_likers | Get list of media likers| TODO |
| get_media_comments | Get list of media's comments| TODO |
| get_comment | Get comment from comment file| bot.get_comment()|
| get_media_commenters| Get list of users who commented media||


### Like

| method        | description | example  |
| ------------- |:-------------:| ------:|
| like | Like media_id | bot.like("123124128654712904742810")|
| like_medias | Like medias from list | bot.like_medias(["1323124", "123141245"])|
| like_timeline | Like medias from your timeline feed| bot.like_timeline()|
| like_user_id | Like last user's medias| bot.like_user_id("352300017")|
| like_hashtag | Like last medias with hashtag | bot.like_hashtag("Dog")|
| like_geotag | Like last medias with geotag| TODO|

### Unlike

| method        | description | example  |
| ------------- |:-------------:| ------:|

### Follow

| method        | description | example  |
| ------------- |:-------------:| ------:|

### Unfollow

| method        | description | example  |
| ------------- |:-------------:| ------:|

### Comment

| method        | description | example  |
| ------------- |:-------------:| ------:|

### Checkpoints

| method        | description | example  |
| ------------- |:-------------:| ------:|
| save_checkpoint() | Save [checkpoint](https://github.com/ohld/instabot/blob/master/instabot/bot/bot_checkpoint.py) of your account. Return path to it.|    bot.save_checkpoint() |
| load_checkpoint(path)| Load checkpoint from path. Return Checkpoint class.|  cp = bot.load_checkpoint( bot.last_checkpoint_path)|
| load_last_checkpoint()| Load last checkpoint if it was in current session| bot.load_last_checkpoint()|
| checkpoint_followers_diff(cp)| returns a list of users who become your followers after checkpoint| bot.checkpoint_followers_diff(cp)|
| checkpoint_following_diff(cp)| returns a list of users who become your following after checkpoint| bot.checkpoint_following_diff(cp)|
| revert_to_checkpoint(cp)| Unfollow the new following made after checkpoint creation| bot.revert_to_checkpoint(cp)|

## Sample usage

```python
from instabot import Bot
bot = Bot()
bot.login()
bot.like_timeline()
bot.like_hashtag("dog")
bot.comment_hashtag("dogs")
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
