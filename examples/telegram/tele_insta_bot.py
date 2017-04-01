# -*- coding: utf-8 -*-
from examples.telegram import config
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands='addaccount')
def addaccount():
    bot.send_message("Enter login and password for instagramm:\n"
                     "Example: myusername:password")


if __name__ == '__main__':
    bot.polling(none_stop=True)
