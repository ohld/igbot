[![Telegram Chat](https://img.shields.io/badge/chat%20on-Telegram-blue.svg)](https://t.me/instabotproject) ![Python 2.7, 3.5, 3.6, 3.7](https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7-blue.svg) [![PyPI version](https://badge.fury.io/py/instabot.svg)](https://badge.fury.io/py/instabot) [![Build Status](https://travis-ci.org/instagrambot/instabot.svg?branch=master)](https://travis-ci.org/instagrambot/instabot) [![codecov](https://codecov.io/gh/instagrambot/instabot/branch/master/graph/badge.svg)](https://codecov.io/gh/instagrambot/instabot)

# Instabot with Stories, Location and more!

Instagram promotion and SMM scripts. Forever free. Written in Python.

<p align="center">
<img src="https://raw.githubusercontent.com/instagrambot/docs/master/img/instabot_3_bots.png" alt="Instabot is better than other open-source bots!" width="300" />
</p>
#### This fork of the original **Instabot** library includes many additional great features:

- Stories download, using `bot.download_stories("username")`

- Like location feed, using `bot.like_location_feed("location name", amount)`

- Approve or Reject pending follow requests on private accounts, using `bot.approve_pending_follow_requests(amount=None)` and `bot.reject_pending_follow_requests(amount=None)`

    


### Installation and usage
Install the dependencies
```
pip install -r requirements.txt
```
Import the library

```
from instabot.instabot import Bot
```

Start from the [examples](https://github.com/marco2012/instabot/tree/master/examples)!

---
### [Read the Docs](https://instagrambot.github.io/docs/) | [Contribute](https://github.com/instagrambot/docs/blob/master/CONTRIBUTING.md)
---

*Support the original authors* [![paypal](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/okhlopkov) <a href="https://www.buymeacoffee.com/okhlopkov" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a> 