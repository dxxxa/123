import requests, schedule
from time import sleep
from threading import Thread

url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd%2Cbtc&include_market_cap=true&include_24hr_change=true"

data = {"ethereum": {"usd": 1980.41,
                     "usd_market_cap": 237918648974.43015,
                     "usd_24h_change": 2.77539909768854,
                     "btc": 0.08101106,
                     "btc_market_cap": 9731003.413739137,
                     "btc_24h_change": 1.9080086966334162}}


def getdetails():
    global data
    data = requests.get(url).json()


schedule.every(30).seconds.do(getdetails)


def forever():
    while True:
        schedule.run_pending()
        sleep(1)


def forgwei():
    pusd = round(data['ethereum']['usd'], 2)
    return pusd


t1 = Thread(target=forever)
t1.start()


def getprice():
    pusd = round(data['ethereum']['usd'], 2)
    pusd = format(pusd, ",")
    pbtc = round(data["ethereum"]["btc"], 8)
    pchange = round(data["ethereum"]["usd_24h_change"], 2)
    market = round(data["ethereum"]["usd_market_cap"])
    market = format(market, ",")

    price = f"""<b><ins><a href='https://coingecko.com/en/coins/ethereum/'>Ethereum | $ETH</a> Price:</ins></b>
<b>💰 USD:</b> ${pusd}
<b>🗿 BTC:</b> ฿{pbtc}
<b>📈 24h change:</b> {pchange}%
<b>💎 Market Cap:</b> ${market}
	"""

    return price
