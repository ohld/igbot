# Popular questions on instabota.

### How do I install a bot?

The installation depends on your operating system. [Installation for Windows](/docs/en/Installation_on_Windows.md). [Installation for Unix](/docs/en/Installation_on_Unix.md) (Linux, MacOS).

All the work with the bot, like installation, occurs through the command line (terminal / CMD). Do not be afraid of it - there is nothing complicated in it.

### How do I start a bot?

First you need to install it. Then go to the sample folder and run any script via the command line, for example:
``` python
python multi_script_CLI.py
```

If the script needs to pass any parameters to run, for example, a list of hashtags for the liking, then the script will output it to you. In the example with like_hashtags.py, it will output:
```
Usage: Pass hashtags to like
Example: python like_hashtags.py dog cat
```

It immediately becomes clear how to work with this script. For example, if you want to like the latest media with a hashtag **#cat** or **#dog**, then:
``` python
python like_hashtags.py cat dog
```

### Where do I enter the username and password from the Instagram account?

They can not be specified at all: the bot itself will ask them to enter at the first start. They will be saved to the file secret.txt and will be downloaded from there when further starts. You can also pass them manually to the function login():
``` python
bot.login(username=«my_username», password=«my_password»)
```

Also, when you start the script for the first time, you will be able to add several accounts to Instabot. In the future, if you specify more than one account, before each start, you will have the opportunity to choose an accent to work with.

### When you enter the password, it is not displayed! What to do?

The password is not displayed specially so that no one can spy on it. Не переживайте, он вводится корректно. Если вы случайно ввели неправильный пароль, то при следующем запуске, если пароль не подойдет, Вас попросят ввести его еще раз. 

### When entering the login and password for the Instagram account, where do they go? Are they sent remotely?

The entered login and password are stored locally on your computer in the secret.txt file. It is not transmitted anywhere.

### Will my account be banned?

Instabot has limits both on the number of subscriptions / likes / comments and so on per day, and on the frequency of requests - for example, do not subscribe too quickly. Instabot already has its own limits, which guarantee safe use. You can set your own values, but be careful. More details about this can be read here (make a page with a description of these parameters and how to change). The bot saves the number of likes / subscriptions / unsubscriptions and so on. And dumps them once a day.

### Is it possible to speed up, for example, an answer from everyone? Is it safe?

There are parameters for the class `instabot.Bot ()`. If you run the __milti_script_CLI__ code, open it with a text editor, find the value __unfollow_delay = 30__ there, change it to whatever you want. Similarly, you can change other settings. But note, this can be unsafe.

Agree that if you unsubscribe from 100 people per second, you will be banned for sure. The limits depend on the age and size of the account, so their fine-tuning is everyone's business. The values that stand by default in Instabot are safe for _most_. No one was banned because of them.

### I want the bot to unsubscribe from accounts that did not respond with a mutual subscription.

For your task, the already written script, which lies in the examples folder: unfollow_non_followes.py, is suitable. Просто перейдите папку с этим скриптом на вашем компьютере и выполните в терминале. 
``` python
python unfollow_non_followers.py
```

### I want the bot to put the likes of posts with hashtags, which I will list.

Everything again is very simple! Run the example like_hashtags.py, for example, like this:
``` python
python like_hashtags.py dog cat
```

### Too many scripts! Is there anything in one bottle?

There is. Thanks to the efforts of our community, a very cool script was written. You can find it under the name [multi_script_CLI.py](/examples/multi_script_CLI.py). He is in English, but I think everything will be clear. I strongly advise you to try it!

### How can I organize an auto-posting photo in the Instagram?

For this, we have a daddy in [examples](/examples/autopost). Below on that page you will find how to configure and run auto-hosting.

### AutoPost publishes only a photo or description and a hashtag, too?

Hashtags is the same description - just add them there.

### Can I publish video via autoposting?

Unfortunately no. This would increase the size of the project several times.

### How can I help the project?

Вы можете:
* Put the star in Github. To do this, just click on the star here https://github.com/instagrambot (top right), May need to register (for free).
* Login to [Telegram Group](https://t.me/instabotproject) and help newcomers to understand the installation and configuration of Instabot. 
* Tell us about our project wherever possible. It will be enough to throw off the link: https://instagrambot.github.io.
* You can find bugs and errors found in [Issues](https://github.com/instagrambot/instabot/issues), be sure to attach the _screenshots_ and _commands_ that you entered. This will help correct these errors and make Instabot better!
* Correct these errors if you are a developer. Do this through the Pull request, following the standard PEP8.
* To develop our [site](https://github.com/instagrambot/instagrambot.github.io). We need both a designer and a frontend developer. If you have long wanted to do something from scratch, welcome.
