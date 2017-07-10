# Instabot
![Instabot is better than other open-source bots!](https://github.com/instagrambot/instabot/blob/master/docs/img/tag%20instabot.png "Instabot is better than other open-source bots!")
Cool Instagram scripts for promotion and API wrapper. Written in Python.
___
[![Telegram Chat](https://img.shields.io/badge/chat%20on-Telegram-blue.svg)](https://t.me/joinchat/AAAAAEHxHAtKhKo4X4r7xg)
[![Build Status](https://travis-ci.org/instagrambot/instabot.svg?branch=master)](https://travis-ci.org/instagrambot/instabot)

As you may know, Instagram closed its API in summer 2016. This Python module can do the same things without any effort.

## Highly recommended
*Make sure* you check out the example scripts [here](https://github.com/ohld/instabot/tree/master/examples). Chances are, your desired functions are *already there and ready to use*. Examples include *unfollowing non-followers*, *following competitor's followings and followers*, *liking posts of a specific hashtag*, and *more*...

If you have any ideas, please report them in the [Issues section](https://github.com/ohld/instabot/issues) or in our [Telegram chat](https://t.me/joinchat/AAAAAEHxHAtKhKo4X4r7xg).
**Your __contribution__ and support through __stars and reporting issues__ will be highly appreciated. After all, this project is dependent on your testing and support. :)**

## Before you bot!
Before you follow bot, make sure you run *reset_following.py*, it will allow you to reset your following to what you had before botting. Very helpful.

## How to install and update

Install latest stable version or update current from pip.

``` python
pip install -U instabot
```

Full installation steps for UNIX (Linux, macOS) users [here](https://github.com/ohld/instabot/blob/master/docs/installation/Unix_installation.md). If you are Windows user, go to [Windows installation](https://github.com/ohld/instabot/blob/master/docs/installation/Windows_installation.md).

## How to run the bot
Choose any script from [examples](https://github.com/ohld/instabot/tree/master/examples) and run:
```
python example.py
```

If you have any problems with the script, regarding any issue or inquiry, please ask questions in the [Telegram chat](https://t.me/joinchat/AAAAAEHxHAtKhKo4X4r7xg).

## Implemented [bot](https://github.com/ohld/instabot/blob/master/instabot/bot/bot.py) methods

### Bot Class

``` python
from instabot import Bot
bot = Bot(
            proxy=None,
            max_likes_per_day=1000,
            max_unlikes_per_day=1000,
            max_follows_per_day=350,
            max_unfollows_per_day=350,
            max_comments_per_day=100,
            max_likes_to_like=100,
            filter_users=True,
            max_followers_to_follow=2000,
            min_followers_to_follow=10,
            max_following_to_follow=7500,
            min_following_to_follow=10,
            max_followers_to_following_ratio=10,
            max_following_to_followers_ratio=2,
            max_following_to_block=2000,
            min_media_count_to_follow=3,
            like_delay=10,
            unlike_delay=10,
            follow_delay=30,
            unfollow_delay=30,
            comment_delay=60,
            whitelist=False,
            blacklist=False,
            comments_file=False,
            stop_words=['shop', 'store', 'free']
)
```

| parameter| description | example |
| ------------- |:-------------:| ------:|
| proxy | Proxy for Instabot | None|
| max_likes_per_day| How many likes the bot will perform per day| 1000|
| max_unlikes_per_day | How many medias the bot will unlike in a day| 1000|
| max_follows_per_day| Max number of follow per day| 350|
| max_unfollows_per_day| Max number of follow per day| 350|
| max_comments_per_day| Max number of comments per day| 100|
| max_likes_to_like| If the media has more likes then this value - it will be ignored and not be liked | 200|
| filter_users | Filter users if True | True|
| max_followers_to_follow| If the user has more followers than this value - the user will not be followed or liked. | 2000|
| min_followers_to_follow| If the user has fewer followers than this value - the user will not be followed or liked.| 10|
| max_following_to_follow| If the user has more followings than this value - the user will not be followed or liked.| 10000|
| min_following_to_follow| If the user has fewer followings than this value - the user will not be followed or liked.| 10|
| max_followers_to_following_ratio| if the user's followers/following is greater than this value - the user will not be followed or liked.| 10|
| max_following_to_followers_ratio| if user's following/followers is greater than this value - he will not be followed or liked.| 2|
| min_media_count_to_follow| If the user has fewer media count than this value - the user will not be followed. | 3|
|max_following_to_block|If the user have a following more than this value - the user will be blocked in blocking scripts because he is a massfollower| 2000|
| max_likes_to_like | Max number of likes that can media have to be liked | 100 |
| like_delay | Delay between likes in seconds| 10|
| unlike_delay | Delay between unlikes in seconds | 10|
| follow_delay | Delay between follows in seconds| 30|
| unfollow_delay | Delay between unfollows in seconds| 30|
| comment_delay | Delay between comments in seconds|  60|
| whitelist | Path to the file with users that shouldn't be unfollowed| "whitelist.txt"|
| blacklist | Path to the file with users that shouldn't be followed, liked or commented | "blacklist.txt"|
| comments_file | Path to the comments database | "comments.txt" |
| stop_words| A list of stop words: don't follow a user if they have any of these stop words in their description| ['shop', 'store', 'free']|

In all files:

*one item*

*one line*

This is in regards to comments or users in a file.

### Get

| method        | description | example  |
| ------------- |:-------------:| ------:|
| get_your_medias | Get list of your last medias | bot.get_you_medias()|
| get_timeline_medias | Get list of media_ids from your timeline feed| bot.get_timeline_medias()|
| get_user_medias | Get list of user's medias | bot.get_user_medias("ohld")|
| get_hashtag_medias| Get list of medias by hashtag| bot.get_hashtag_medias("Dog")|
| get_geotag_medias| Get list of medias by geotag| TODO |
| get_timeline_users| Get list of users from your timeline feed| bot.get_timeline_users()|
| get_hashtag_users| Get list of users who posted with hashtag| bot.get_hashtag_users("Dog") |
| get_geotag_users| Get list of users who posted with geotag| TODO |
| get_userid_from_username| Convert username to user_id| bot.get_userid_from_username("ohld") |
| get_user_followers| Get list of user's followers| bot.get_user_followers("competitor") |
| get_user_following| Get list of user's following| bot.get_user_following("competitor") |
| get_media_likers | Get list of media likers| bot.get_media_likers("12312412") |
| get_media_comments | Get list of media's comments| bot.get_media_comments("12312412") |
| get_comment | Get comment from comment file| bot.get_comment()|
| get_media_commenters| Get list of users who commented on the media| bot.get_media_commenters("12321")|


### Like

| method        | description | example  |
| ------------- |:-------------:| ------:|
| like | Like media_id | bot.like("1231241210")|
| like_medias | Like medias from list | bot.like_medias(["1323124", "123141245"])|
| like_timeline | Like medias from your timeline feed| bot.like_timeline()|
| like_user | Like last user's medias| bot.like_user("activefollower")|
| like_hashtag | Like last medias with hashtag | bot.like_hashtag("dog")|
| like_geotag | Like last medias with geotag| TODO|

### Unlike

| method        | description | example  |
| ------------- |:-------------:| ------:|
| unlike | Remove like from media | bot.unlike("12321412512")|
| unlike_medias | Remove likes from medias in list| bot.unlike_medias(["123", "321"])|

### Follow

| method        | description | example  |
| ------------- |:-------------:| ------:|
| follow | Follow user | bot.follow("activefollower")|
| follow_users | Follow users from list | bot.follow(["activefollower1", "activefollower2"])|

### Unfollow

| method        | description | example  |
| ------------- |:-------------:| ------:|
| unfollow | Unfollow user | bot.unfollow("competitor")|
| unfollow_users | Unfollow users from list | bot.unfollow(["competitor1", "competitor2"])|
| unfollow_non_followers | Unfollow users who don't follow you | bot.unfollow_non_followers()|

### Comment

| method        | description | example  |
| ------------- |:-------------:| ------:|
| comment | Put a comment under the media | bot.comment("1231234", "Nice pic!")|
| comment_medias | Put comments under medias from list | bot.comment_medias(["123", "321"])|
| comment_hashtag | Put comments under medias by hashtag| bot.comment_hashtag("Dog")|
| comment_geotag | Put comments under medias by geotag | TODO |
| comment_users | Put comments under users' last medias | bot.comment_users(["activefollower1", "activefollower2"]) |
| is_commented | Check if media is already commented | bot.is_commented("123321") |

## Sample usage

```python
from instabot import Bot
bot = Bot()
bot.login()
bot.like_timeline()
bot.like_hashtag("dog")
bot.comment_hashtag("dogs")
bot.like_user("activefollower")
bot.follow("activefollower")
bot.unfollow_non_followers()
```

## Docker
As long as docker is running on your machine you can build an instabot docker image like this
```
docker build -t instabot .
```

Then run your image with an example or your custom script:
```
docker run --name instabot -p 80:80 -i -t instabot python examples/like_example.py
```
