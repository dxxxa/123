# [How to Make a Currency Converter in Python](https://www.thepythoncode.com/article/make-a-currency-converter-in-python)
To run the scripts:
- `pip3 install -r requirements.txt`
- Here is an example: To convert 1000 EUR to USD by scraping Yahoo Finance:
    ```
    $ python currency_converter_yahoofin.py EUR USD 1000
    ```
    Output:
    ```
    Last updated datetime: 2022-02-02 12:37:39
    1000.0 EUR = 1132.6310634613037 USD
    ```
##
# [[] / []]()
Конвертер валют - это приложение или инструмент, который позволяет быстро конвертировать из одной валюты в другую. Мы можем легко найти такие инструменты бесплатно в Интернете. В этом учебнике будет сделан конвертер валют в реальном времени, используя несколько методов, использующих методы веб-парсинга и API.

Этот учебник будет охватывать пять различных способов получения самых последних валютных курсов, некоторые из них анализируют курсы с общедоступных веб-страниц, таких как X-RATES и Xe, а другие используют официальные API для более коммерческого и надежного использования, такие как Fixer API и ExchangeRate API, не стесняйтесь использовать любой из них.

Не стесняйтесь переходить к методу, который вы хотите использовать:

Соскоб X-RATES
Скребок Xe
Парсинг Yahoo Финансы
Использование API ExchangeRate
Использование API Fixer
Чтобы начать, мы должны установить необходимые библиотеки для всех методов ниже:

$ pip install python-dateutil requests bs4 yahoo_fin
Соскоб X-RATES
В этом разделе мы извлечем данные с веб-сайта x-rates.com. Если вы перейдете на целевую веб-страницу, вы увидите большинство валют вместе с самой последней датой и временем. Давайте почистим страницу:

import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from pprint import pprint
Следующая функция отвечает за выполнение запроса к этой странице и извлечение данных из таблиц:

def get_exchange_list_xrates(currency, amount=1):
    # make the request to x-rates.com to get current exchange rates for common currencies
    content = requests.get(f"https://www.x-rates.com/table/?from={currency}&amount={amount}").content
    # initialize beautifulsoup
    soup = bs(content, "html.parser")
    # get the last updated time
    price_datetime = parse(soup.find_all("span", attrs={"class": "ratesTimestamp"})[1].text)
    # get the exchange rates tables
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            # for each row in the table
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                # get the exchange rate
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate        
    return price_datetime, exchange_rates
Вышеуказанная функция принимает валюту и сумму в качестве параметров и возвращает обменные курсы большинства валют вместе с датой и временем последнего обновления.

Время последнего обновления находится в теге span, который имеет класс ratesTimestamp. Обратите внимание, что мы используем функцию parse() из модуля dateutil.parser для автоматического синтаксического анализа строки в объект Python DateTime.

Курсы валют расположены в двух таблицах. Мы извлекаем их с помощью метода find_all() из объекта BeautifulSoup и получаем имя валюты и обменный курс в каждой строке таблиц, а также добавляем их в наш exchange_rates словарь, который мы вернем. Воспользуемся этой функцией:

if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    amount = float(sys.argv[3])
    target_currency = "GBP"
    price_datetime, exchange_rates = get_exchange_list_xrates(source_currency, amount)
    print("Last updated:", price_datetime)
    pprint(exchange_rates)
Отлично, мы используем встроенный sys модуль для получения целевой валюты и суммы из командной строки. Давайте запустим это:

$ python currency_converter_xrates.py EUR 1000
Вышеупомянутый пробег пытается конвертировать 1000 евро во все другие валюты. Вот выходные данные:

Last updated: 2022-02-01 12:13:00+00:00
{'Argentine Peso': 118362.205708,     
 'Australian Dollar': 1586.232315,    
 'Bahraini Dinar': 423.780164,        
 'Botswana Pula': 13168.450636,       
 'Brazilian Real': 5954.781483,       
 'British Pound': 834.954104,
 'Bruneian Dollar': 1520.451015,      
 'Bulgarian Lev': 1955.83,
 'Canadian Dollar': 1430.54405,       
 'Chilean Peso': 898463.818465,       
 'Chinese Yuan Renminbi': 7171.445692,
 'Colombian Peso': 4447741.922165,    
 'Croatian Kuna': 7527.744707,        
 'Czech Koruna': 24313.797041,
 'Danish Krone': 7440.613895,
 'Emirati Dirham': 4139.182587,
 'Hong Kong Dollar': 8786.255952,
 'Hungarian Forint': 355958.035747,
 'Icelandic Krona': 143603.932438,
 'Indian Rupee': 84241.767127,
 'Indonesian Rupiah': 16187150.010697,
 'Iranian Rial': 47534006.535121,
 'Israeli Shekel': 3569.191411,
 'Japanese Yen': 129149.364679,
 'Kazakhstani Tenge': 489292.515538,
 'Kuwaiti Dinar': 340.959682,
 'Libyan Dinar': 5196.539901,
 'Malaysian Ringgit': 4717.485104,
 'Mauritian Rupee': 49212.933037,
 'Mexican Peso': 23130.471272,
 'Nepalese Rupee': 134850.008728,
 'New Zealand Dollar': 1703.649473,
 'Norwegian Krone': 9953.078431,
 'Omani Rial': 433.360301,
 'Pakistani Rupee': 198900.635421,
 'Philippine Peso': 57574.278782,
 'Polish Zloty': 4579.273862,
 'Qatari Riyal': 4102.552652,
 'Romanian New Leu': 4946.638369,
 'Russian Ruble': 86197.012666,
 'Saudi Arabian Riyal': 4226.530892,
 'Singapore Dollar': 1520.451015,
 'South African Rand': 17159.831129,
 'South Korean Won': 1355490.097163,
 'Sri Lankan Rupee': 228245.645722,
 'Swedish Krona': 10439.125427,
 'Swiss Franc': 1037.792217,
 'Taiwan New Dollar': 31334.286611,
 'Thai Baht': 37436.518169,
 'Trinidadian Dollar': 7636.35428,
 'Turkish Lira': 15078.75981,
 'US Dollar': 1127.074905,
 'Venezuelan Bolivar': 511082584.868731}
Это около 1127,07 долларов США на момент написания этого урока. Обратите внимание на дату и время последнего обновления; он обычно обновляется каждую минуту.

Скребок Xe
Xe - это онлайн-компания по обмену валюты и услуг. Он наиболее известен своим онлайн-конвертером валют. В этом разделе мы используем запросы и библиотеки BeautifulSoup, чтобы сделать конвертер валют на его основе.

Откройте новый файл Python и импортируйте необходимые библиотеки:

import requests
from bs4 import BeautifulSoup as bs
import re
from dateutil.parser import parse
Теперь давайте создадим функцию, которая принимает исходную валюту, целевую валюту и сумму, которую мы хотим конвертировать, а затем возвращает конвертированную сумму вместе с датой и временем обменного курса:

def convert_currency_xe(src, dst, amount):
    def get_digits(text):
        """Returns the digits and dots only from an input `text` as a float
        Args:
            text (str): Target text to parse
        """
        new_text = ""
        for c in text:
            if c.isdigit() or c == ".":
                new_text += c
        return float(new_text)
    
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
    content = requests.get(url).content
    soup = bs(content, "html.parser")
    exchange_rate_html = soup.find_all("p")[2]
    # get the last updated datetime
    last_updated_datetime = parse(re.search(r"Last updated (.+)", exchange_rate_html.parent.parent.find_all("div")[-2].text).group()[12:])
    return last_updated_datetime, get_digits(exchange_rate_html.text)
На момент написания этого учебника обменный курс находится в третьем абзаце на HTML-странице. Это объясняет soup.find_all("p")[2]. Обязательно изменяйте извлечение всякий раз, когда в HTML-страницу вносятся изменения. Надеюсь, я буду следить за тем, когда будут внесены изменения.

Последняя дата и время обменного курса находятся во втором родительском элементе обменного курса в HTML DOM.

Поскольку обменный курс содержит строковые символы, я сделал функцию get_digits() для извлечения только цифр и точек из заданной строки, что полезно в нашем случае.

Теперь воспользуемся функцией:

if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]
    amount = float(sys.argv[3])
    last_updated_datetime, exchange_rate = convert_currency_xe(source_currency, destination_currency, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {source_currency} = {exchange_rate} {destination_currency}")
На этот раз мы получаем исходную и целевую валюты, а также сумму из командных строк, пытаясь конвертировать 1000 EUR в USD:

$ python currency_converter_xe.py EUR USD 1000
Выпуск:

Last updated datetime: 2022-02-01 13:04:00+00:00
1000.0 EUR = 1125.8987 USD
Это здорово! Xe обычно обновляется каждую минуту, так что это в режиме реального времени!

Парсинг Yahoo Финансы
Yahoo Finance предоставляет финансовые новости, валютные данные, котировки акций, пресс-релизы и финансовые отчеты. В этом разделе используется библиотека yahoo_fin в Python для создания обменника валют на основе данных Yahoo Finance.

Импорт библиотек:

import yahoo_fin.stock_info as si
from datetime import datetime, timedelta
yahoo_fin отлично справляется с извлечением данных с веб-страницы Yahoo Finance, и она все еще поддерживается в настоящее время; используем метод get_data() из модуля stock_info и передаем ему символ валюты.

Ниже приведена функция, которая использует эту функцию и возвращает конвертированную сумму из одной валюты в другую:

def convert_currency_yahoofin(src, dst, amount):
    # construct the currency pair symbol
    symbol = f"{src}{dst}=X"
    # extract minute data of the recent 2 days
    latest_data = si.get_data(symbol, interval="1m", start_date=datetime.now() - timedelta(days=2))
    # get the latest datetime
    last_updated_datetime = latest_data.index[-1].to_pydatetime()
    # get the latest price
    latest_price = latest_data.iloc[-1].close
    # return the latest datetime with the converted amount
    return last_updated_datetime, latest_price * amount
Мы передаем "1m" параметру interval в методе get_data() для извлечения минутных данных вместо ежедневных данных (по умолчанию). Мы также получаем мельчайшие данные за предыдущие два дня, так как это может вызвать проблемы в выходные дни, просто чтобы быть осторожными.

Существенным преимуществом этого метода является то, что вы можете получить исторические данные, просто изменив start_date и end_date параметры по этому методу. Вы также можете изменить интервал на «1d» для ежедневного, «1wk» для еженедельного и «1mo» для ежемесячного.

Теперь воспользуемся функцией:

if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]
    amount = float(sys.argv[3])
    last_updated_datetime, exchange_rate = convert_currency_yahoofin(source_currency, destination_currency, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {source_currency} = {exchange_rate} {destination_currency}")
Выполнение кода:

$ python currency_converter_yahoofin.py EUR USD 1000
Выпуск:

Last updated datetime: 2022-02-01 13:26:34
1000.0 EUR = 1126.1261701583862 USD
Использование API ExchangeRate
Как упоминалось в начале этого урока, если вы хотите более надежный способ сделать конвертер валют, вы должны выбрать API для этого. Для этой цели существует несколько API. Тем не менее, мы выбрали два API, которые кажутся удобными и простыми для начала.

ExchangeRate API поддерживает 161 валюту и предлагает бесплатные ежемесячные 1 500 запросов, если вы хотите попробовать его, а также есть открытый API, который предлагает ежедневно обновляемые данные, и это то, что мы собираемся использовать:

import requests
from dateutil.parser import parse 

def get_all_exchange_rates_erapi(src):
    url = f"https://open.er-api.com/v6/latest/{src}"
    # request the open ExchangeRate API and convert to Python dict using .json()
    data = requests.get(url).json()
    if data["result"] == "success":
        # request successful
        # get the last updated datetime
        last_updated_datetime = parse(data["time_last_update_utc"])
        # get the exchange rates
        exchange_rates = data["rates"]
    return last_updated_datetime, exchange_rates
Вышеуказанная функция запрашивает открытый API и возвращает обменные курсы для всех валют с последней датой и временем. Давайте используем эту функцию, чтобы сделать функцию конвертера валют:

def convert_currency_erapi(src, dst, amount):
    # get all the exchange rates
    last_updated_datetime, exchange_rates = get_all_exchange_rates_erapi(src)
    # convert by simply getting the target currency exchange rate and multiply by the amount
    return last_updated_datetime, exchange_rates[dst] * amount
Как обычно, сделаем основной код:

if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]
    amount = float(sys.argv[3])
    last_updated_datetime, exchange_rate = convert_currency_erapi(source_currency, destination_currency, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {source_currency} = {exchange_rate} {destination_currency}")
Запуск его:

$ python currency_converter_erapi.py EUR USD 1000
Выпуск:

Last updated datetime: 2022-02-01 00:02:31+00:00
1000.0 EUR = 1120.0 USD
Курсы обновляются ежедневно, и он не предлагает точный номер обмена, так как это открытый API; вы можете свободно подписаться на ключ API, чтобы получить точные обменные курсы.

Использование API Fixer
Одной из перспективных альтернатив является Fixer API. Это простой и легкий API для реальных и исторических валютных курсов. Вы можете легко создать учетную запись и получить ключ API.

После этого вы можете использовать конечную точку /convert для преобразования из одной валюты в другую. Однако это не включено в бесплатный план и требует обновления вашей учетной записи.

Существует конечная точка /latest, которая не требует обновления и отлично работает в бесплатной учетной записи. Он возвращает обменные курсы для валюты вашего региона. Мы можем передать исходную и целевую валюты, которые мы хотим конвертировать, и рассчитать обменный курс между обоими. Вот функция:

import requests
from datetime import datetime

API_KEY = "<YOUR_API_KEY_HERE>"

def convert_currency_fixerapi_free(src, dst, amount):
    """converts `amount` from the `src` currency to `dst` using the free account"""
    url = f"http://data.fixer.io/api/latest?access_key={API_KEY}&symbols={src},{dst}&format=1"
    data = requests.get(url).json()
    if data["success"]:
        # request successful
        rates = data["rates"]
        # since we have the rate for our currency to src and dst, we can get exchange rate between both
        # using below calculation
        exchange_rate = 1 / rates[src] * rates[dst]
        last_updated_datetime = datetime.fromtimestamp(data["timestamp"])
        return last_updated_datetime, exchange_rate * amount
Ниже приведена функция, которая использует конечную точку /convert в случае, если у вас есть обновленная учетная запись:

def convert_currency_fixerapi(src, dst, amount):
    """converts `amount` from the `src` currency to `dst`, requires upgraded account"""
    url = f"https://data.fixer.io/api/convert?access_key={API_KEY}&from={src}&to={dst}&amount={amount}"
    data = requests.get(url).json()
    if data["success"]:
        # request successful
        # get the latest datetime
        last_updated_datetime = datetime.fromtimestamp(data["info"]["timestamp"])
        # get the result based on the latest price
        result = data["result"]
        return last_updated_datetime, result
Воспользуемся любой функцией:

if __name__ == "__main__":
    import sys
    source_currency = sys.argv[1]
    destination_currency = sys.argv[2]
    amount = float(sys.argv[3])
    # free account
    last_updated_datetime, exchange_rate = convert_currency_fixerapi_free(source_currency, destination_currency, amount)
    # upgraded account, uncomment if you have one
    # last_updated_datetime, exchange_rate = convert_currency_fixerapi(source_currency, destination_currency, amount)
    print("Last updated datetime:", last_updated_datetime)
    print(f"{amount} {source_currency} = {exchange_rate} {destination_currency}")
Перед запуском скрипта обязательно замените API_KEY ключом API, который вы получаете при регистрации учетной записи.

Запуск скрипта:

Last updated datetime: 2022-02-01 15:54:04
1000.0 EUR = 1126.494 USD
Вы можете ознакомиться с документацией Fixer API здесь.

Заключение
Есть много способов сделать конвертер валют, и мы рассмотрели пять из них. Если один метод не работает для вас, вы можете выбрать другой!

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Вы можете получить полный код для всех файлов здесь.

Узнайте также: Веб-перехватчики в Python с помощью Flask.