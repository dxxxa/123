# [How to Make a Telegram Bot in Python](https://www.thepythoncode.com/article/make-a-telegram-bot-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Get an API key contacting @FatherBot in Telegram
- Run `telegram_bot.py`
##
# [[] / []]()
Автоматизация становится все более и более популярной с каждым днем, и поэтому популярные сервисы и приложения в настоящее время часто предлагают интерфейс для программного использования, этот интерфейс мы называем API, или интерфейс прикладного программирования, примеры приложений, предлагающих API, включают Google Drive, Google Search и Github.

API — это набор конечных точек, которые любой программист может использовать для связи со службой, не пытаясь имитировать пользователя с помощью приложения, что часто невозможно из-за того, что капчи становятся все более и более широко используемыми. 

Когда популярное приложение предлагает API, программисты обычно пишут простые в использовании библиотеки (которые действуют как уровень абстракции для API, часто называемый оболочками), для программиста, который хочет общаться с приложением, вместо того, чтобы читать ссылку о конечных точках API, проще просто загрузить библиотеку на выбранном языке программирования,  и читать его документацию, которая зачастую более идиоматична, и к ней быстрее привыкнуть.

В этом уроке мы увидим, как написать Telegram Bot на Python, бот — это пользователь, управляемый кодом, пишущий бот может иметь множество приложений, например; автоматически отвечает на запросы клиентов. 

Telegram предлагает два API, один для создания ботов, а другой для создания клиентов, мы будем использовать первый, документацию по Bot API можно найти здесь.

Мы будем использовать популярную оболочку python-telegram-bot, чтобы облегчить нам работу:

pip3 install python-telegram-bot
Теперь нам нужно будет получить ключ API для связи с API Telegram, чтобы получить его, нам нужно вручную связаться с @BotFather в Telegram, например:

Связь с BotFather в TelegramМы получаем список команд, когда начинаем обсуждение, мы создаем бота с командой, как только он создан, мы получаем токен для связи с ботом (в нашем случае он скрыт красным цветом)./newbot

Теперь мы можем начать писать нашего бота на Python:

import telegram
import telegram.ext
import re
from random import randint
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# The API Key we received for our bot
API_KEY = "<INSERT_API_KEY_HERE>"
# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
Обратите внимание, что мы добавили ведение журнала в начале скрипта, и мы установили уровень ведения журнала в DEBUG, это поможет нам, что происходит с ботом, работает ли он, сообщения, которые мы получаем от наших пользователей и т. Д. Если вы не знакомы с ведением журнала в Python, ознакомьтесь с этим руководством.

Диспетчер - это объект, который будет отправлять запросы своим обработчикам, нам нужно добавить к нему обработчик разговора, чтобы описать, как наш бот будет отвечать на сообщения.

Api Telegram позволяет определить бота как конечный автомат, мы можем обрабатывать различные события, а также изменять состояния в зависимости от ввода пользователя или типа действий.

В этом руководстве мы создадим следующий FSM:

Конечный автомат Telegram-ботВыполнение начинается с start, Welcome спросит пользователя, хочет ли он ответить на вопрос, если ответ да или y, он отправит вопрос и переключит состояние на Correct, если ответ правильный. В противном случае он будет зацикливаться на Вопросе, каждый раз генерируя другой вопрос.

Как только ответ будет правильным, он спросит пользователя, нашел ли он учебник полезным, и перейдет в конечное состояние, которое является окончательным.

Определение наших государств:

# Our states, as integers
WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3
Теперь давайте определимся с нашими обработчиками:

# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello there, do you want to answer a question? (Yes/No)",
        reply_markup=telegram.ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
    )
    # go to the WELCOME state
    return WELCOME

# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0,1000), randint(0, 1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        # send question, and go to the QUESTION state
        randomize_numbers(update_obj, context)
        return QUESTION
    else:
        # go to the CANCEL state
        return CANCEL

# in the QUESTION state
def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    # check if the solution was correct
    if solution == int(update_obj.message.text):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Was this tutorial helpful to you?")
        return CORRECT
    else:
        # wrong answer, reply, send a new question, and loop on the QUESTION state
        update_obj.message.reply_text("Wrong answer :'(")
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION

# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! ^^")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END
Каждая функция представляет состояние, теперь, когда мы определили наши обработчики, давайте добавим их в наш диспетчер, создав ConversationHandler:

# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('start', start)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
            QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
      },
      fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
      )
# add the handler to the dispatcher
dispatcher.add_handler(handler)
ConversationHandler - это объект, который обрабатывает разговоры, его определение просто, мы просто указываем состояние для начала, предоставляя CommandHandler для команды start.

Для других состояний мы создаем MessageHandler для каждого из них, который принимает два аргумента; фильтр регулярных выражений, описывающий, как должен выглядеть пользовательский ввод для доступа к каждому состоянию, и функции (обработчики), определенные ранее.

Теперь мы можем дождаться общения с пользователями, нам просто нужно вызвать эти два метода:

# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()
Возвращаясь к приложению Telegram, давайте протестируем нашего бота:

Тестирование Telegram-бота
Обратите внимание, что вы можете начать разговор с помощью команды /start.

Заключение
Telegram предлагает очень удобный API для разработчиков, позволяя им расширить его использование за пределы сквозной связи, мы видели в этом учебнике, как его можно использовать для реализации бота, имеющего несколько состояний.

Я советую вам узнать больше о функциях API, которые он предлагает, о том, как обрабатывать изображения и файлы, отправленные от пользователей, платежах и многом другом.

Писать Telegram-ботов было весело, не так ли? Вы можете использовать обработку естественного языка и построить модель ИИ для чат-бота, отвечающего на вопросы. На самом деле, проверьте этот учебник, где мы сделали разговорный чат-бот AI!