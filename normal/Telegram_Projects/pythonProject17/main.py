# https://github.com/AREEG94FAHAD/currencies_bot
# Цифровая криптовалюта
# С помощью этого бота теперь вы можете отслеживать цены на более чем 12 цифровых криптовалют


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import time
from pycoingecko import CoinGeckoAPI

from telethon import TelegramClient

cg = CoinGeckoAPI()

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))  # Конвертация даты в читабельный вид
#
#@bot.message_handler(content_types=["text"])
#def get_text_messages(message):
#    print(tconv(message.date))  # Вывод даты типо 20:58:30 05.07.2020

currencies = ["Bitcoin", "Ethereum", "Tether", "Cardano",
              "Chainlink", "Chainlink", "Dogecoin", "Ethereum-Classic",
              "Polkadot", "USD-Coin", "Internet-Computer", "Bitcoin-Cash",
              "THORChain", "Uniswap", "Algorand"]

APITOKEN = "5416667430:AAFIkaLXaxd2nNaW7S4VUtTyjBIFUVNipS0"
bot = telebot.TeleBot(APITOKEN)


api_id = 28297361
api_hash = "e0eed1ec03e7de3c444d73f3aef9ce68"
# ----
my_channel = 'opopoq'  # куда
channels = 'sfgddygff', 'gvghhq'  # откуда


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(0, 14, 3):
        markup.add(InlineKeyboardButton(currencies[i], callback_data=currencies[i]),
                   InlineKeyboardButton(currencies[i+1], callback_data=currencies[i+1]),
                   InlineKeyboardButton(currencies[i+2], callback_data=currencies[i+2]))
    return markup


with TelegramClient('myApp13', api_id, api_hash) as client:
    print("～Activated～")

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Select the currency", reply_markup=gen_markup())

    @bot.message_handler(content_types=["text", "photo"])
    def get_text_messages(message):
        #print("               Date:Time      | UserID:Username |TypeMes:Text")
        print("Сообщение:", tconv(
            message.date),  # Вывод даты типо 20:58:30 05.07.2020
            message.chat.id,  # Вывод id пользователя
            message.chat.username,  # Вывод username пользователя
            message.content_type,  # Вывод тип сообщения
            message.text)  # Вывод сообщения

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        x_time = time.strftime("%H:%M:%S", time.localtime())
        x_date = time.strftime("%d.%m.%Y", time.localtime())
        date_time = ("Date: " + str(x_date) + "    " + "Time: " + str(x_time))
        try:
            x0 = cg.get_price(ids=call.data, vs_currencies="usd")
            x1 = cg.get_price(ids=call.data, vs_currencies="rub")
            x2 = x1[str(call.data).lower()]["rub"] / x0[str(call.data).lower()]["usd"]
            x3 = round(x2, 2)  # Сокращение вывода float
            print("Запрос:   ", date_time, "   UserID:", call.from_user.id, "   1$ ≈", str(x3) + "Rub")
            bot.send_message(call.from_user.id,
                             "\n┌─ Coin: " + str(call.data) +
                             "\n│ " +
                             "\n├─ Date: " + str(x_date) +
                             "\n├─ Time: " + str(x_time) +
                             "\n│ "
                             "\n├─ Rate: 1$ ≈ " + str(x3) + "Rub" +
                             "\n│ "
                             "\n├─ Coin Price: " + str(x0[str(call.data).lower()]["usd"]) + " $" +
                             "\n└─ Coin Price: " + str(x1[str(call.data).lower()]["rub"]) + " Rub")

        except:
            bot.send_message(call.from_user.id, "Something went wrong, try again later")


bot.polling()
