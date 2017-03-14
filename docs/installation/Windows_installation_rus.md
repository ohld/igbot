# Установка для Windows

Так как эта система изначально не приспособлена для Питона, придется его установить. Самый простой способ - установить Анаконду.

1. Скачиваем и устанавливаем Анаконду: [Anaconda](https://www.continuum.io/downloads) (неважно 2 или 3 питон).
2. Запускаем **Anaconda Prompt** из меню Пуск.
3. Устанавливаем Instabot через pip:

	```
	pip install -U instabot
	```

4. Если хотите запустить любой из [готовых скриптов](https://github.com/instagrambot/instabot/tree/master/examples), нужно скачать их и перейти в папку с примерами:

	```
	conda install git
	git clone https://github.com/ohld/instabot
	cd instabot/examples
	```

5. Выберете любой скрипт и запустите его. Например, скрипт с дилоговым интерфейсом:

  ```
  python multi_script_CLI.py
  ```
