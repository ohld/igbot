# How to install and run the script on Unix? (Linux, macOS)
* Open terminal and run
```
pip install -U instabot
git clone https://github.com/ohld/instabot
cd instabot/examples
```

* And then you can run any example like this
```
python follow_user_following.py ohld
```

## Errors

* If you have `pip: command not found` error, try:
```
sudo easy_install pip
```

* If you have `permission denied` error after `pip install -U instabot`, try:
```
sudo pip install -U instabot
```
