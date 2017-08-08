# Instructions for use

**Important! Read the instructions from start to finish, and then act! Good luck!**

## How to work?

You will need a downloaded project. In the ***instabot/examples/*** folder there are scripts for work.

## How do I run the script?

Open the command line, use ***cd*** to go to the project directory, namely ***instabot/examples***. Type.

``` python
python name.py param
```

Where ***name*** is the name of the script, ***param*** is the required parameter for running the script. Not all scripts need a parameter.

## How do I know if I need an input parameter for a script?

Run the script by typing.

``` python
python name.py
```

If there are no necessary parameters, the script will stop and display an error.
Example.
Run the script.

``` python
python like_hashtags.py. 
```

The script stops and displays a message:

``` python
error: the following arguments are required: hashtags.
```

That is, we had to enter a hashtag. Correct example:

``` python
python like_hashtags.py follow
```

## All inclusive

***multi_script_CLI.py*** is a script that contains all the functions. The first time you run it, you will be prompted to configure the script. Script settings are stored in the ***setting.txt*** file. Also files will be created: ***hashtag_file.txt, users_file.txt, whitelist.txt, blacklist.txt, comment.txt***.

## 24/7

Yes, there is a script that rounds up subscribers and subscriptions of certain people around the clock, and also likes photos by nickname and hashtag. All this allows the script - ***ultimate.py***, which is in the ***instabot/examples/ultimate*** folder. The folder also contains other text files for running the script. In these files, each new parameter needs to be written from a new line.

## Schedule

Also there is a script that will work around the clock, BUT this script will act according to plan. This script is ***ultimate.py*** in the ***instabot/examples/ultimate_schedule*** folder. You can open the code with any editor and fix it. This will be easy, since there are comments in important parts of the code.

## How to configure the script correctly

To ensure that your account has not been banned, you need to configure the script Example. Suppose we need to keep photos on the hashtag every minute. First of all, time in seconds. Open ***like_hashtags.py*** with a text editor. Find such lines (approximately so they should look).

``` python
bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
```

Next in line.

``` python
bot = Bot()
```

We need to write a parameter in parentheses. This parameter is ***like_delay***. This parameter needs to be set to 60, since we need every minute the bot to be happy with the photo on the hashtag. In the end, it will look like this.

``` python
bot = Bot(like_delay=60)
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
```

## Parameter List

| parameter| description | example |
| ------------- |:-------------:| ------:|
| proxy | Proxy for Instabot | None|
| max_likes_per_day| How many likes the bot will perform per day| 1000|
| max_unlikes_per_day | How many medias the bot will unlike in a day| 1000|
| max_follows_per_day| Max number of follow per day| 350|
| max_unfollows_per_day| Max number of unfollow per day| 350|
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























