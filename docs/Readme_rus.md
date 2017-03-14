![Instabot is better that other open-source bots!](https://github.com/instagrambot/instabot/blob/master/docs/img/tag%20instabot.png "Instabot is better that other open-source bots!")
# Instabot
Полезные скрипты для раскрутки аккаунтов Instagram.

## Что это?

Instabot - это модуль для языка Python, в котором не только реализована обертка над Instagram API, но и разные полезные функции, такие как "подписаться на список людей", "пролайкать фотки по хэштегам", "отписаться от невзаимных подписчиков" и тд. Instabot достаточно умный: [почитайте](https://github.com/instagrambot/instabot/blob/master/docs/Filtration_rus.md), например, как он фильтрует людей, на которых собирается подписаться.

## Установка

Если Вы знакомы с языком программирования Python, то установите его так:
``` python
pip install instabot
```

Если же Вы совсем в этом не разбираетесь, то прошу на страницу [вопросов и ответов](https://github.com/instagrambot/instabot/blob/master/docs/FAQ_rus.md) - там есть более подробная инструкция по установки.

## Запуск

Написано огромное множество различных скриптов на основе нашего питоновского модуля. Вся они лежат в папке _examples_. Скачайте архив с ботом с главной странице репозитория (кнопка **Clone or download**).

Скрипт, с которого стоит начать знакомство, называется **multi_script_CLI.py**. Он объединяет большинство самых крутых скриптов в один удобный интерфейс. Запустить его можно так:

```
python multi_script_CLI.py
```

Перед запуском убедитесь, что вы находитесь в папке examples, иначе будет ошибка: _file not found_. Подробнее: [Вопросы и ответы](https://github.com/instagrambot/instabot/blob/master/docs/FAQ_rus.md).


## Обновление

Так как проект Instabot молодой и активно развивается, то обновления будут выходить довольно часто. Поэтому если вы наткнулись на ошибку, не спешите бить в колокола: попробуйте обновить Instabot - может быть, эту ошибку уже поправили.

``` python
pip install -U instabot
```

## Ничего не понятно

Задайте вопрос в [Telegram группе](https://t.me/joinchat/AAAAAEHxHAtKhKo4X4r7xg). Не забудьте приложить скриншоты.

## Разработчикам

Разработчикам лучше почитать нормальный [Readme.md](https://github.com/instagrambot/instabot/blob/master/README.md). Если Вы хотите помочь проекту, то feel free to do anything that might help the project. Cheers!
