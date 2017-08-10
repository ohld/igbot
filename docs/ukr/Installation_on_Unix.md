# Як встановити на UNIX систему? (Linux, macOS)

Відео інструкція.

[! [Установка Instabot на macOS] (http://img.youtube.com/vi/aJUHmv3NhRE/0.jpg)] (https://youtu.be/aJUHmv3NhRE)

## Покрокова інструкція

* Відкрийте термінал.
```
pip install -U instabot
git clone https://github.com/instagrambot/instabot
cd instabot/examples
```

*І після цього обирайте будь-який скрипт з папки _examples/_, наприклад, _multi_script_CLI.py_ і виконайте так:
```
python multi_script_CLI.py
```

## Що робити, якщо помилки

* Якщо пише `pip: command not found`, встановіть pip і спробуйте ще раз:
```
sudo easy_install pip
```

* Якщо після `pip install -U instabot` виведе багато помилок і текст `permission denied`, впишіть sudo:
```
sudo pip install -U instabot
```