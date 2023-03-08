# https://pastebin.com/WfZwvHdG

from pyrogram import Client, filters  # телеграм клиент
import tgcrypto
import shelve  # файловая БД


db = shelve.open('data.db', writeback=True)


# Для входа в телеграм (Создать можно на my.telegram.org)
API_ID = 28297361
API_HASH = "e0eed1ec03e7de3c444d73f3aef9ce68"
PHONE_NUMBER = '+79693053554'  # номер зарегистрованный в телеге


my_priv_channel = 'gvghhq'  # скрытый паблик для управления ботом
my_public_channel = 'opopoq'  # паблик куда репостить
source_channels = ['sfgddygff',
                   'AnyDataBases',
                   'EvaDataBases']  # список пабликов-доноров, откуда бот будет пересылать посты


# Создаем клиент телеграм
app = Client("cyberpunk", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)  # cyberpunk - файл сессии


# Обработчик нового сообщения
# Вызывается при появлении нового поста в одном из пабликов-доноров
@app.on_message(filters.chat(source_channels))
def new_channel_post(client, message):
    post_id = add_post_to_db(message)  # сохраняем пост в базу (функцию add_post_to_db)
    message.forward(my_priv_channel)  # пересылаем пост в скрытый паблик
    client.send_message(my_priv_channel, post_id)  # в скрытый паблик отправляем присвоенный id поста
    # для пересылки в публичный паблик админ должен отправить боту этот id
    print(message, "\n\n ################################################################################\n")


# Функция сохранения поста в БД
# Генерирует уникальный id для поста и возвратит этот id
def add_post_to_db(message):
    try:
        new_id = max(int(k) for k in db.keys() if k.isdigit()) + 1  # генерация id для поста, равен max. в базе + 1

    except:  # если постов еще нет в базе - вылетит ошибка и мы попадем сюда
        new_id = 1  # тогда id ставим = 1

    # Запись в БД необходимой информации про пост ### Обратите внимание, shelve поддеживает только строковые ключи ###
    db[str(new_id)] = {
        'username': message.chat.username,  # паблик-донор
        'message_id': message.id,  # внутренний id сообщения
    }
    return new_id


# Обработчик нового сообщения из скрытого паблика
# Если админ пишет в приватном паблике `123+` - это значит переслать пост с id = 123 в публичный паблик
@app.on_message(filters.chat(my_priv_channel)
                & filters.regex(r'\d+\+'))  # фильтр текста сообщения `{число}+`
def post_request(client, message):
    post_id = str(message.text).strip('+')  # получаем id поста из сообщения (обрезаем "+" в конце)
    # Получаем из БД пост по id
    post = db.get(post_id)
    if post is None:  # если нет в БД - выводит в скрытый паблик ошибку
        client.send_message(my_priv_channel, '`ERROR NO POST ID IN DB`')
        return  # и выходим

    try:
        # по данным из базы, получаем pyrogram обьект сообщения
        msg = client.get_messages(post['username'], post['message_id'])
        # пересылаем его в паблик

        # as_copy=True значит, что мы не будем отображать паблик донор, будто это наш пост XD
        # msg.forward(my_public_channel, as_copy=True)
        msg.copy(my_public_channel)

        client.send_message(my_priv_channel, f'`SUCCESS REPOST!`')  # вывод сообщения в скрытый паблик о успехе

    except Exception as e:  # если произойдет какая-то ошибка в 3 строчках выше - выведем админу
        client.send_message(my_priv_channel, f'`ERROR {e}`')


if __name__ == '__main__':
    print('Atempt to run Telegrabber')
    app.run()  # строка запуска всех обработчиков
