# Как установить на UNIX систему? (Linux, macOS)

Видео инструкция.

[![Установка Instabot на macOS](http://img.youtube.com/vi/aJUHmv3NhRE/0.jpg)](https://youtu.be/aJUHmv3NhRE)

## Пошаговая инструкция

* Откройте терминал
```
pip install -U instabot
git clone https://github.com/ohld/instabot
cd instabot/examples
```

* И после этого выбирайте любой скрипт из папки _examples/_, например, _unfollow_non_followers.py_ и запускайте так:
```
python unfollow_non_followers.py
```

## Что делать, если ошибки

* Если пишет `pip: command not found`, установите pip и попробуйте еще раз:
```
sudo easy_install pip
```

* Если после `pip install -U instabot` выведет много ошибок и текст `permission denied`, впишите sudo:
```
sudo pip install -U instabot
```
