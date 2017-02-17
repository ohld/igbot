# instabot
Cool instagram scripts and API wrapper. Written in Python.
___
As you may know, Instagram closed it's API in summer 2016. This Python module can do the same thing without any effort. Also it has lots of example scripts to start with.

If you have any ideas, please, leave them in [issues section](https://github.com/ohld/instabot/issues) or in our [telegram chat](https://t.me/joinchat/AAAAAAuPofDcEgHBSysAGg).

*Your **Contribution** and Support through **Stars** will be highly appreciated.*

## How to install

Install latest stable version from pip

```
pip install -U instabot
```

## How to run
Choose any script from [examples](https://github.com/ohld/instabot/tree/master/examples) and run
```
python example.py
```

If you have any problems with script, please ask questions in [telegram chat](https://t.me/joinchat/AAAAAAuPofDcEgHBSysAGg).

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

### Bot Class

| parameter| description | example |
| ------------- |:-------------:| ------:|
| max_likes_per_day| How many likes will bot put per day| max_likes_per_day = 1000|
| max_follows_per_day| Max number of follow per day| max_follows_per_day = 350|
| max_comments_per_day| Max number of comments per day| max_comments_per_day = 100|
| whitelist | Path to the file with user_ids that shoudn't be unfollowed| whitelist="whitelist.txt"|
| blacklist | Path to the file with user_ids that shoudn't be followed, liked or commented | blacklist="blacklist.txt"|
| comments_file | Path to the comments database | comments_file="comments.txt"|

In all files one line - one item (comment or user_id).

### Get

| method        | description | example  |
| ------------- |:-------------:| ------:|
| get_your_medias | Get list of your last medias | bot.get_you_medias()|
| get_timeline_medias | Get list of media_ids from you timeline feed| bot.get_timeline_medias()|
| get_user_medias | Get list of user_id's medias | bot.get_user_medias("352300017")|
| get_hashtag_medias| Get list of medias by hashtag| bot.get_hashtag_medias("Dog")|
| get_geotag_medias| Get list of medias by geotag| TODO |
| get_timeline_users| Get list of users from your timeline feed| bot.get_timeline_users()|
| get_hashtag_users| Get list of users who posted with hashtag| TODO |
| get_geotag_users| Get list of users who posted with geotag| TODO |
| get_userid_from_username| Convert username to user_id| TODO |
| get_user_followers| Get list of user's followers| bot.get_user_followers("352300017") |
| get_user_following| Get list of user's following| bot.get_user_following("352300017") |
| get_media_likers | Get list of media likers| bot.get_media_likers("12312412") |
| get_media_comments | Get list of media's comments| TODO |
| get_comment | Get comment from comment file| bot.get_comment()|
| get_media_commenters| Get list of users who commented media| bot.get_media_commenters("12321")|


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
| unlike | Remove like from media | bot.unlike("12321412512")|
| unlike_medias | Remove likes from medias in list| bot.unlike_medias(["123", "321"])|

### Follow

| method        | description | example  |
| ------------- |:-------------:| ------:|
| follow | Follow user_id| bot.follow("352300017")|
| follow_users | Follow users from list | bot.follow(["123", "321"])|

### Unfollow

| method        | description | example  |
| ------------- |:-------------:| ------:|
| unfollow | Unfollow user_id | bot.unfollow("352300017")|
| unfollow_users | Unfollow users from list | bot.unfollow(["123", "321"])|
| unfollow_non_followers | Unfollow users who don't follow you | bot.unfollow_non_followers()|

### Comment

| method        | description | example  |
| ------------- |:-------------:| ------:|
| comment | Put a comment under media | bot.comment("1231234", "Nice pic!")|
| comment_medias | Put comments under medias from list | bot.comment_medias(["123", "321"])|
| comment_hashtag | Put comments under medias by hashtag| bot.comment_hashtag("Dog")|
| comment_geotag | Put comments under medias by geotag | TODO |
| comment_users | Put comments under users' last medias | TODO |
| is_commented | Check if media is already commented | bot.is_commented("123321") |

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
___
_by @ohld_
