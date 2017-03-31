# -*- coding: utf-8 -*-
from examples.telegram import config
import telebot, sys, os
from instabot import Bot
from instabot.api import API
from instabot.api import prepare
from telebot import types

sys.path.append(os.path.join(sys.path[0], '../'))

bot = telebot.TeleBot(config.token)
iBot = Bot()
userStep = {}

@bot.message_handler(commands=['logout'])
def iBot_logout(message):
    if iBot.isLoggedIn:
        login_account = iBot.username
        iBot.logout()
        sent = bot.send_message(message.chat.id,'%s is logout!' % login_account)
        bot.register_next_step_handler(sent, listaccount(message))
    else:
        sent = bot.send_message(message.chat.id,'Bot is not login!')
        listaccount(message)


@bot.message_handler(commands=['listaccount'])
def listaccount(message):
    try:
        m = message
        list_from_file = iBot.read_list_from_file(prepare.SECRET_FILE)
        out_text = ''
        i = 1
        out_text = 'YOUR "Secret.txt" FILE ACCOUNT:\n'
        for line in list_from_file:
            out_text =out_text + '%s - /%s \n' % (i, line.split(':')[0])
            i = i + 1
        sent = bot.send_message(message.chat.id, out_text)
        bot.register_next_step_handler(sent, iBot_login)
    except Exception as e:
        bot.send_message(message.chat.id, e)

def iBot_login(message):
    try:
        # print(message.text)
        if get_account_from_login(message) is True:
            # print(message.text.replace('/',''))
            iBot.login(username=message.text.replace('/',''))
            if iBot.isLoggedIn:
                # bot.send_message(message.chat.id, str(iBot.isLoggedIn))
                get_iBot_Function(message)
        else:
            sent = bot.send_message(message.chat.id, 'No login, please re choose account')
            bot.register_next_step_handler(sent, listaccount(message))
    except Exception as e:
        bot.send_message(message.chat.id, e)
        iBot.logout()

def get_account_from_login(message):
    try:
        accounts = iBot.read_list_from_file(prepare.SECRET_FILE)
        for line in accounts:
            username = line.split(':')[0]
            if username == message.text.replace('/',''):
                return True
                exit()
        return False
    except Exception as e:
        bot.send_message(message.chat.id, e)


def get_iBot_Function(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        b_Logout = types.InlineKeyboardButton(text="Logout", callback_data='Logout')
        b_Like_hashtags = types.InlineKeyboardButton(text="Like hashtags", callback_data='Like_hashtags')
        b_Like_followers_of = types.InlineKeyboardButton(text="Like followers of", callback_data='Like_followers_of')
        b_Like_following_of = types.InlineKeyboardButton(text="Like following of", callback_data='Like_following_of')
        b_Like_your_timeline_feed = types.InlineKeyboardButton(text="Like your timeline feed", callback_data='Like_your_timeline_feed')
        b_Follow_users_by_hashtags = types.InlineKeyboardButton(text="Follow users by hashtags",
                                                               callback_data='Follow_users_by_hashtags')
        keyboard.add(b_Logout)
        keyboard.add(b_Like_hashtags, b_Follow_users_by_hashtags)
        keyboard.add(b_Like_followers_of)
        keyboard.add(b_Like_following_of)
        keyboard.add(b_Like_your_timeline_feed)

        bot.send_message(message.chat.id, "Support functions:", reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands = ['addaccount'])
def addaccount(message):
    pass
    # keyboard = types.InlineKeyboardMarkup()
    # url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", callback_data='test2')
    # url_button2 = types.InlineKeyboardButton(text="callback_data", callback_data='test')
    # keyboard.add(url_button, url_button2)
    # bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "Logout":
            iBot_logout(call.message)
        if call.data == "Like_your_timeline_feed":
            result = iBot.like_timeline()
            bot.send_message(call.message.chat.id, str(result))
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        if call.data == "test2":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="test2")
    # Если сообщение из инлайн-режима
    # elif call.inline_message_id:
    #     if call.data == "test":
    #         bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")

try:
    if __name__ == '__main__':
        bot.polling()
except Exception as e:
    print(e)