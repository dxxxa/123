from pyrogram import Client, filters

api_id = 28297361
api_hash = "e0eed1ec03e7de3c444d73f3aef9ce68"
# +79693053554

bot = Client("Bot", api_id, api_hash)  # Создание сессии авторизации


# 1)обработчик команды /start
@bot.on_message(filters.command("start"))
def start(bot, msg):
    bot.send_message(msg.chat.id, "Ну допустим привет")


# 2)обработчик команды /id
@bot.on_message(filters.command("id1"))
def id_reply(bot, msg):
    bot.send_message(msg.chat.id, text=f"Твой ID: {msg.from_user.id}"
                                       f"\nТвой username: @{msg.from_user.username}", reply_to_message_id=msg.id)

# 3)обработчик команды /id еще один метод
@bot.on_message(filters.command("id2"))
def id_reply(bot, msg):
    msg.reply(f"Твой ID: {msg.from_user.id}\nТвой username: @{msg.from_user.username}")


# 4)обработчик команды /send с отправкой файлов
@bot.on_message(filters.command("send"))
def new_(bot, msg):
    #bot.send_photo(msg.chat.id,	"photo.jpg")
    bot.send_document(msg.chat.id,	"config.ini")


# 5)обработчик команды /get
@bot.on_message(filters.command("get"))
def new_func(bot, msg):
    id = msg.from_user.id
    msg.reply("Твой ID: {}".format(id))


# 6)обработчик команды /echo повторяет сообщение пользователя
@bot.on_message(filters.command("echo"))
def echo(bot, msg):
    text = msg. text. split(None, 1)[1]
    msg.reply(text)


# 7)
@bot.on_message(filters.voice)
def anything(bot, msg):
    msg.reply(msg.voice.file_id)


# 7)
@bot.on_message(filters.command("s"))
def anything(bot, msg):
    msg.reply_voice("AwACAgIAAxkBAAIWY2FPv2hYYAMql3aUDuE4vrPT-xXhAAJUEQACUZt5SrjJcv3WVAzSHgQ")


# 8) Удаляет вводимые сообщения пользователей кроме указанного пользователя(id)
#@bot.on_message(filters.text)
#def text_delete(bot, msg):
#    if msg.from_user.id != 5195681649:
#        bot.delete_messages(msg.chat.id, message_ids=msg.id)


# 9) Удаляет слова в чате если они совпадают со словоми из словаря
@bot.on_message(filters.text)
def text_delete(bot, msg):
    word = ["мат", "хер", "чтото"]
    if msg.text in word:
        bot.delete_messages(msg.chat.id, message_ids=msg.id)



# 10)
@bot.on_message(filters.command("kick"))
def kick(bot, msg):
    if msg.reply_to_message:
        user = msg.reply_to_message.from_user.id
        bot.kick_chat_member(msg.chat.id, user)



# 11)
@bot.on_message(filters.command("unban"))
def unban(bot, msg):
    if msg.reply_to_message:
        user = msg.reply_to_message.from_user.id
        bot.unban_chat_member(msg.chat.id, user)



# 11)
@bot.on_message(filters.command("leave"))
def leave(bot, msg):
    msg.reply("I will leave")
    bot.leave_chat(msg.chat.id)


bot.run()  # Цикл постоянной работы


#  1)"Bot telegram with lib pyrogram - Python"                      https://www.youtube.com/watch?v=QrAJZIJ5HrY
#  2)"Bot telegram with pyrogram get id & reply - Python"           https://www.youtube.com/watch?v=H6WOZXqV95k
#  3)"Bot telegram with pyrogram bound method - Python"             https://www.youtube.com/watch?v=vB9scUbB66U
#  4)"Bot telegram with pyrogram method - Python"                   https://www.youtube.com/watch?v=NkX1w8VqvDY
#  5)
#  6)"Bot telegram with pyrogram split & echo bot - Python"         https://www.youtube.com/watch?v=HqeT_K8-3i4
#  7)"Bot telegram with pyrogram filters - Python"                  https://www.youtube.com/watch?v=HOYt6pNyCg0
#  8)"Bot telegram with pyrogram filters & delete - Python"         https://www.youtube.com/watch?v=Kt3dXAULugI
#  9)"Bot telegram with pyrogram filters & delete part2 - Python"   https://www.youtube.com/watch?v=xgDeQQeQG-0

# 10)"Bot telegram with pyrogram method kick_chat_member - Python"  https://www.youtube.com/watch?v=GPBMz4SoDC8
# 11)"Bot telegram with pyrogram method unban_chat_member & leave_chat - Python"    https://www.youtube.com/watch?v=3eNwbsfvkTY



# 12)"Bot telegram with pyrogram & database redis - Python"         https://www.youtube.com/watch?v=m-6wFAzhQu8
# 13)"Bot telegram with pyrogram & database redis - broadcast to users - Python"    https://www.youtube.com/watch?v=UnZ2u-0QNFQ
# 14)"Bot telegram with pyrogram & database redis - get users - Python" https://www.youtube.com/watch?v=K2QPY5L2bCw
# 15)"Bot telegram with pyrogram & database redis - save chat id and locks filters - Python"    https://www.youtube.com/watch?v=t0K9CZiaMuk
# 16)"Bot telegram with pyrogram & database redis - hset & hget & hdel - Python"    https://www.youtube.com/watch?v=YR4GvXSOaXI




