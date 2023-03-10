#!/usr/bin/python
# -*- coding: utf-8 -*-

# Сообщение по середине перед входом в бота
# Перейти в BotFather и /setdescription


import telebot
import re
import os
import time

from logger import get_logger
import datetime

log = get_logger("bot")


with open("TOKEN", "r") as tfile:  # local run
    TOKEN = tfile.readline().strip('\n')
    log.info("[LOCAL] read token: '%s'" % TOKEN)
    tfile.close()

bot = telebot.TeleBot(TOKEN)

BOT_USERNAME = 'raidpinbot'



@bot.message_handler(commands=['start', 'help'])
def command_starthelp(m):
    log.debug("User %s used command %s" % (m.from_user.username, m.text))
    text = "Приветствую! 👋\n" + \
           "Я - бот-автопиннер сообщений.\n" + \
           "Для моей активации добавьте меня в чат.\n" + \
           "Важно: мне следует дать права админа (хотя бы на закрепление сообщений)!\n\n" + \
           ":\n" + \
           "- @RaidBattlesBot\n\n" + \
           "При добавлении сообщения о рейде я автоматически закреплю его (с оповещением всех участников чата)."
    bot.send_message(m.chat.id, text)
#
# Bot should pin only raid messages (assume they should have reply_markup keyboard)








@bot.message_handler(func=lambda message: 'reply_markup' in message.json)
def check_raidmessage(m):
    log.debug("Detected potential raid message:")
    log.debug(str(m.json))
    is_raid = False
    # series of conditions to detect @RaidBattlesBot inline raid message
    rep_mkup = m.json['reply_markup']
    if 'inline_keyboard' in rep_mkup:
        kb = rep_mkup['inline_keyboard'][0]
        if 'switch_inline_query' in kb[-1]:
            # final check is by 'share' button existence in reply keyboard
            share_button = re.findall(r'^share:.*', kb[-1]['switch_inline_query'])
            if share_button != [] and len(share_button) == 1:
                is_raid = True
    if is_raid:
        log.debug("Raid message confirmed, pinning")
        time.sleep(1)
        bot.pin_chat_message(m.chat.id, m.message_id)
        log.debug("Message pinned: %s" % m.text)
    else:
        log.error("Not a raid message, skipping")


log.warning("Running locally, start polling")  # Запуск локально, начните опрос
bot.polling(none_stop=True, interval=0, timeout=20)