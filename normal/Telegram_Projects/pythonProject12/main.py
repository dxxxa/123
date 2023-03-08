from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

bot=Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

async def on_startup(_):
    print("Бот вышел в онлайн")
"*****************************КЛИЕНТСКАЯ ЧАСТЬ*****************************"


@dp.message_handler(commands=["start", "help"])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Приятного аппетита")
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите eMy:\nhttps://t.me/Pizza_SheefBot")

@dp.message_handler(commonds=["Режим_работы"])
async def pizza_open_command(messoge : types.Message):
    await bot.send_message(message.from_user.id, "Вс-Чт c 9:00 до 20:00, Пт-Сб с 10:00 до 23:00")

#@dp.message_handler(commands["Расположение"])
#async def pizza_place_command(message : types.Message):
    for ret in cur.execute("SELECT FROM Message")

"*****************************Админская ЧАСТЬ*****************************"
"*******************************Общая ЧАСТЬ*******************************"

@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text == 'Привет':
        await message.answer('И тебе привет')
    # await message.reply(message.text)
    # await bot.sen_message(message.from_user.id, message.text)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
