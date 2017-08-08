# How does the Instabot filter people?

It's no secret that Instabot, before subscribing to people, filters them so as not to subscribe to a knowingly inactive and fake audience. Below you will find the entire list of conditions that apply in this filtration.

## Options

To begin with, it is worth pointing out the conditions that you are free to change. Below I will give those parameters of the bot constructor, which are related to filtering.

``` python
bot = Bot(max_likes_to_like=100,
          max_followers_to_follow=2000,
          min_followers_to_follow=10,
          max_following_to_follow=10000,
          min_following_to_follow=10,
          max_followers_to_following_ratio=10,
          max_following_to_followers_ratio=2,
          min_media_count_to_follow=3,
          stop_words=['shop', 'store', 'free'])
```
If you want to change these values to your own in some example, just replace the `bot = Bot ()` line with this one, but with your values.
Next, I will write the names of these parameters instead of the values themselves.

## User Filtering

_Notation_: True - you can subscribe, False - can not.
* If the white list is True,
* If in black - False,
* If you have already subscribed to it - False,
* If the business account is False,
* If the confirmed account is False,
* If the number of subscribers is less than min_followers_to_follow - False,
* If the number of subscribers is greater than max_followers_to_follow - False,
* If the number of subscriptions is less than min_following_to_follow - False,
* If the number of subscriptions is greater than max_following_to_follow - False,
* Если отношение подписки / подписчики больше max_following_to_followers_ratio - False,
* If the subscriber / subscription ratio is greater than max_followers_to_following_ratio - False,
* If the amount of media is less than min_media_count_to_follow - False,
* If at least one stop word from stop_words is in user's state, its name or description is False,
* If still not filtered - True.
