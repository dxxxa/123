import telebot, os
from telebot.types import InlineKeyboardMarkup as ikm
from telebot.types import InlineKeyboardButton as ikb
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from time import sleep
from gasfees import gasfee, uniswap, erc20, ens
from alive import keep_alive
from ethprice import getprice

keep_alive()  # This function is used to keep the bot alive on Replit's server

Token = os.environ["5416667430:AAFIkaLXaxd2nNaW7S4VUtTyjBIFUVNipS0"]  # Bot's API Token

bot = telebot.TeleBot(Token, parse_mode="HTML")

print("Bot started successfully! Running Now...")

knwn = []
with open('userids.txt', 'r') as uids:
    knwn = uids.read()
knwn = knwn.split()

wlcm = """Ciao! I'm ETH Gas Fee Tracker Bot, I can send you live Ethereum Gas Fees in GWEI & USD.

All Commands - /cmds

Donate to support the development of this bot: /donate
"""

donate = """Donate to support the development of this bot:
<b>Donate via <a href="https://nowpayments.io/donation/advik">Crypto</a></b>
<b>Blockchain Domain:</b> <a href="https://advik.click/ud">advik.wallet</a>

Thanks a ton!
"""

cmds = """<b><ins>All Commands:</ins></b>
/gas - Check live Ethereum gas fee
/uni - Check live Uniswap V3 & V2 gas fees
/erc20 - Check live ERC-20 Token's transfer fees
/ens - Check live ENS Domain Registration Fees
/p - Get Ethereum Live Price
/donate - Donate to support development of this bot
/contact - Contact my Dev regarding anything

<b>Check Bot Uptime:</b> https://bots.advik.dev/
"""


@bot.message_handler(commands=["start"])
def wlcmsg(msg):
    chatid = str(msg.chat.id)
    mrkp = ikm()
    mrkp.add(ikb("Join Channel For Updates", url="https://t.me/DevUpdate"))
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)
    bot.send_message(msg.chat.id, wlcm, reply_markup=mrkp, disable_web_page_preview=True)


@bot.message_handler(commands=["gas"])
def ethgas(msg):
    bot.send_message(msg.chat.id, gasfee(), disable_web_page_preview=True)
    chatid = str(msg.chat.id)
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)


@bot.message_handler(commands=['uni', 'uniswap'])
def unigas(msg):
    bot.send_message(msg.chat.id, uniswap(), disable_web_page_preview=True)
    chatid = str(msg.chat.id)
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)


@bot.message_handler(commands=['ens'])
def ensreg(msg):
    bot.send_message(msg.chat.id, ens(), disable_web_page_preview=True)
    chatid = str(msg.chat.id)
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)


@bot.message_handler(commands=['erc', 'erc20'])
def ercfees(msg):
    bot.send_message(msg.chat.id, erc20(), disable_web_page_preview=True)
    chatid = str(msg.chat.id)
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)


@bot.message_handler(commands=["donate"])
def donateme(msg):
    bot.send_message(msg.chat.id, donate, disable_web_page_preview=True)


@bot.message_handler(commands=["contact"])
def pingme(msg):
    mrkp = ikm()
    mrkp.add(ikb("Telegram", url="https://t.me/ETHGasFeeSupportBot"), ikb("Email", url="https://advik.click/ETHBot/"))
    mrkp.add(ikb("Join Channel For Updates", url="https://t.me/DevUpdate"))
    bot.send_message(msg.chat.id, "Ping me if you've any query or want some new features:", reply_markup=mrkp)


@bot.message_handler(commands=["dev"])
def iownit(msg):
    bot.reply_to(msg, "Made by @istoleabread")


@bot.message_handler(commands=["p"])
def usdbtc(msg):
    if len(msg.text) == 2 or msg.text.lower() == '/p@ethgasfeetrackerbot':
        bot.send_message(msg.chat.id, getprice(), disable_web_page_preview=True)


@bot.message_handler(commands=["uid", "uids"])
def getuid(msg):
    if msg.chat.id == 1060264505:
        users = open("userids.txt", "rb")
        bot.send_document(1060264505, users)
        users.close()
    else:
        bot.send_message(msg.chat.id, "Error, You're an unauthorized user!")


@bot.message_handler(commands=['send'])
def sendnotif(msg):
    if msg.chat.id == 1060264505:
        confirm = bot.send_message(msg.chat.id, "Send the message you'd like to be notified:")
        bot.register_next_step_handler(confirm, msgpreview)
    else:
        bot.reply_to(msg, "You're not allowed to use this command!")


def msgpreview(msg):
    global msgpre
    msgpre = msg.text
    confirmit = bot.send_message(msg.chat.id, f"{msgpre}\n-\nThis is the message. Are you sure you want to send it?",
                                 disable_web_page_preview=True)
    bot.register_next_step_handler(confirmit, sendit)


def sendit(msg):
    try:
        if msg.text.lower() == "yes" or msg.text.lower() == "y":
            allusers = 0
            for uid in knwn:
                try:
                    userid = int(uid)
                    bot.send_message(userid, msgpre, disable_web_page_preview=True)
                    sleep(0.04)
                    allusers += 1
                except:
                    sleep(0.04)
        bot.send_message(1060264505, f"Message has been sent to {allusers} users!")
    except:
        bot.send_message(1060264505, "Message sending cancelled!")


@bot.message_handler(commands=["active"])
def countactive(msg):
    actv = 0
    if msg.chat.id == 1060264505:
        for uid in knwn:
            try:
                userid = int(uid)
                bot.send_chat_action(userid, "typing")
                sleep(0.04)
                actv += 1
                iopo = actv
            except:
                knwn.remove(uid)
                sleep(0.04)
        bot.send_message(1060264505, f"No. of active users: {iopo}")
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)
    else:
        bot.reply_to(msg, "Unauthorised User: You don't have access to this command!")


@bot.message_handler(commands=["cmd", "cmds"])
def cmd(msg):
    if str(msg.chat.id).startswith('-'):
        bot.send_message(msg.chat.id, cmds, disable_web_page_preview=True)
    else:
        mrkp = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        gasfee = KeyboardButton("ETH Gas Fees")
        uniswap = KeyboardButton("Uniswap Fees")
        ensregistrar = KeyboardButton("ENS Fees")
        erc = KeyboardButton("ERC-20 Token Transfer Fees")
        price = KeyboardButton("Current Ethereum Price")
        mrkp.add(gasfee, uniswap, ensregistrar, erc, price)
        bot.send_message(msg.chat.id, cmds, disable_web_page_preview=True, reply_markup=mrkp)


@bot.message_handler(func=lambda message: True)
def forreply(message):
    chatid = str(message.chat.id)
    if chatid not in knwn:
        knwn.append(chatid)
        with open('userids.txt', 'w') as uids:
            for uid in knwn:
                uid = uid + ' '
                uids.write(uid)
    if message.text == "ETH Gas Fees":
        bot.send_message(message.chat.id, gasfee(), disable_web_page_preview=True)
    elif message.text == "Uniswap Fees":
        bot.send_message(message.chat.id, uniswap(), disable_web_page_preview=True)
    elif message.text == "ENS Fees":
        bot.send_message(message.chat.id, ens(), disable_web_page_preview=True)
    elif message.text == "Current Ethereum Price":
        bot.send_message(message.chat.id, getprice(), disable_web_page_preview=True)
    elif message.text == "ERC-20 Token Transfer Fees":
        bot.send_message(message.chat.id, erc20(), disable_web_page_preview=True)


while True:
    try:
        bot.infinity_polling(skip_pending=True)
        telebot.apihelper.SESSION_TIME_TO_LIVE = 2400
    except:
        sleep(1)
