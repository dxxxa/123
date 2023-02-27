# [How to Extract Weather Data from Google in Python](https://www.thepythoncode.com/article/extract-weather-data-python)
To run this:
- `pip3 install -r requirements.txt`
- To get the Google weather data of your current region you live in:
    ```
    python weather.py
    ```
- To get the weather of a specific region in the world:
    ```
    python weather.py "New York"
    ```
    This will grab the weather information of "New York" state in the US:
    ```
    Weather for: New York, NY, USA
    Now: wednesday 2:00 PM
    Temperature now: 20°C
    Description: Mostly Cloudy
    Precipitation: 0%
    Humidity: 52%
    Wind: 13 km/h
    Next days:
    ======================================== wednesday ========================================
    Description: Mostly Cloudy
    Max temperature: 21°C
    Min temperature: 12°C
    ======================================== thursday ========================================
    Description: Sunny
    Max temperature: 22°C
    Min temperature: 14°C
    ======================================== friday ========================================
    Description: Partly Sunny
    Max temperature: 28°C
    Min temperature: 18°C
    ======================================== saturday ========================================
    Description: Sunny
    Max temperature: 30°C
    Min temperature: 19°C
    ======================================== sunday ========================================
    Description: Partly Sunny
    Max temperature: 29°C
    Min temperature: 21°C
    ======================================== monday ========================================
    Description: Partly Cloudy
    Max temperature: 30°C
    Min temperature: 19°C
    ======================================== tuesday ========================================
    Description: Mostly Sunny
    Max temperature: 26°C
    Min temperature: 16°C
    ======================================== wednesday ========================================
    Description: Mostly Sunny
    Max temperature: 25°C
    Min temperature: 19°C
```
##
# [[] / []]()
Как вы, возможно, знаете, веб-парсинг - это, по сути, извлечение данных с веб-сайтов. Выполнение такой задачи на языке программирования высокого уровня, таком как Python, очень удобно и мощно. В этом уроке вы узнаете, как использовать запросы и BeautifulSoup для очистки данных о погоде из поисковой системы Google.

Хотя это не идеальный и официальный способ получить фактическую погоду для конкретного места, потому что есть сотни погодных APIдля использования. Тем не менее, это отличное упражнение для вас, чтобы ознакомиться со соскобами.

Есть также удобные инструменты, которые уже созданы с помощью Python, такие как wttr.in. Ознакомьтесь с этим туториалом о том, как его использовать.

Связанные с: Как сделать экстрактор электронной почты в Python.

Хорошо, давайте начнем с установки необходимых зависимостей:

pip3 install requests bs4
Во-первых, давайте немного поэкспериментируем, откроем строку поиска Google и введем, например: «погода в Лондоне», вы увидите официальную погоду, давайте щелкнем правой кнопкой мыши и проверим HTML-код, как показано на следующем рисунке:

Проверка элемента в погодном регионе Google

Примечание: Google не имеет соответствующего API погоды, так как он также очищает данные о погоде из weather.com, поэтому мы, по сути, извлекаем из него.

Вы будете перенаправлены на HTML-код, который отвечает за отображение региона, дня и часа, а также фактической погоды:

HTML-теги для извлечения в Python

Отлично, давайте попробуем быстро извлечь эту информацию в интерактивной оболочке Python:

In [7]: soup = BeautifulSoup(requests.get("https://www.google.com/search?q=weather+london").content)

In [8]: soup.find("div", attrs={'id': 'wob_loc'}).text
Out[8]: 'London, UK'
Не беспокойтесь о том, как мы создали объект soup, все, о чем вам нужно беспокоиться прямо сейчас, это о том, как вы можете захватить эту информацию из HTML-кода, все, что вам нужно указать методу soup.find(), это имя тега HTML и соответствующие атрибуты, в этом случае элемент div с идентификатором «wob_loc» даст нам местоположение.

Аналогично давайте извлечем текущий день и время:

In [9]: soup.find("div", attrs={"id": "wob_dts"}).text
Out[9]: 'Wednesday 3:00 PM'
Фактическая погода:

In [10]: soup.find("span", attrs={"id": "wob_dc"}).text
Out[10]: 'Sunny'
Хорошо, теперь вы знакомы с ним, давайте создадим наш быстрый скрипт для получения дополнительной информации о погоде (как можно больше информации). Откройте новый скрипт Python и следуйте за мной.

Для начала импортируем необходимые модули:

from bs4 import BeautifulSoup as bs
import requests
Стоит отметить, что Google пытается помешать нам соскрести его веб-сайт программным путем, так как это неофициальный способ получения данных, потому что он предоставляет нам удобную альтернативу, которой является Custom Search Engine (проверьте этот учебник о том, как его использовать), но только в образовательных целях мы собираемся притворяться, что мы являемся законным веб-браузером, определим user-agent:

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"
Эта ссылка предоставляет вам последние версии браузера, убедитесь, что вы заменяете USER_AGENT на новейшие.

Определим функцию, которая, задавая URL, пытается извлечь всю полезную информацию о погоде и вернуть ее в словарь:

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")
Все, что мы здесь сделали, это создали сеанс с этим браузером и языком, а затем загрузили HTML-код с помощью session.get(url) из Интернета и, наконец, создали объект BeautifulSoup с помощью синтаксического анализатора HTML.

Давайте получим текущий регион, погоду, температуру и фактический день и час:

    # store all results on this dictionary
    result = {}
    # extract region
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
Поскольку текущие осадки, влажность и ветер отображаются, почему бы не захватить их?

    # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
Давайте попробуем получить информацию о погоде о следующих нескольких днях, если вы потратите некоторое время на поиск ее HTML-кода, вы найдете что-то похожее на это:

<div class="wob_df"
    style="display:inline-block;line-height:1;text-align:center;-webkit-transition-duration:200ms,200ms,200ms;-webkit-transition-property:background-image,border,font-weight;font-weight:13px;height:90px;width:73px"
    data-wob-di="3" role="button" tabindex="0" data-ved="2ahUKEwifm-6c6NrkAhUBdBQKHVbBADoQi2soAzAAegQIDBAN">
    <div class="Z1VzSb" aria-label="Saturday">Sat</div>
    <div style="display:inline-block"><img style="margin:1px 4px 0;height:48px;width:48px" alt="Sunny"
            src="//ssl.gstatic.com/onebox/weather/48/sunny.png" data-atf="1"></div>
    <div style="font-weight:normal;line-height:15px;font-size:13px">
        <div class="vk_gy" style="display:inline-block;padding-right:5px"><span class="wob_t"
                style="display:inline">25</span><span class="wob_t" style="display:none">77</span>°</div>
        <div class="vk_lgy" style="display:inline-block"><span class="wob_t" style="display:inline">17</span><span
                class="wob_t" style="display:none">63</span>°</div>
    </div>
</div>
Я знаю, что это не читаемо человеком, но этот родительский div содержит всю информацию об одном следующем дне, который является «субботой», как показано в первом дочернем элементе div с классом Z1VzSb в атрибуте aria-label, информация о погоде находится в атрибуте alt в элементе img, в данном случае «Sunny». Температура, однако, есть max и min как с Цельсием, так и с Фаренгейтом, эти строки кода заботятся обо всем:

    # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
        max_temp = temp[0].text
        # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    # append to result
    result['next_days'] = next_days
    return result
Теперь словарь результатов получил все, что нам нужно, давайте закончим скрипт, разбирая аргументы командной строки с помощью argparse:

if __name__ == "__main__":
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    import argparse
    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default="")
    # parse arguments
    args = parser.parse_args()
    region = args.region
    URL += region
    # get data
    data = get_weather_data(URL)
Отображение всего:

    # print data
    print("Weather for:", data["region"])
    print("Now:", data["dayhour"])
    print(f"Temperature now: {data['temp_now']}°C")
    print("Description:", data['weather_now'])
    print("Precipitation:", data["precipitation"])
    print("Humidity:", data["humidity"])
    print("Wind:", data["wind"])
    print("Next days:")
    for dayweather in data["next_days"]:
        print("="*40, dayweather["name"], "="*40)
        print("Description:", dayweather["weather"])
        print(f"Max temperature: {dayweather['max_temp']}°C")
        print(f"Min temperature: {dayweather['min_temp']}°C")
Если вы запустите этот скрипт, он автоматически захватит погоду вашего текущего региона, определяемого вашим IP-адресом. Однако, если вам нужен другой регион, вы можете передать его в качестве аргументов:

C:\weather-extractor>python weather.py "New York"
Это покажут погодные данные штата Нью-Йорк в США:

Weather for: New York, NY, USA
Now: wednesday 2:00 PM
Temperature now: 20°C
Description: Mostly Cloudy
Precipitation: 0%
Humidity: 52%
Wind: 13 km/h
Next days:
======================================== wednesday ========================================
Description: Mostly Cloudy
Max temperature: 21°C
Min temperature: 12°C
======================================== thursday ========================================
Description: Sunny
Max temperature: 22°C
Min temperature: 14°C
======================================== friday ========================================
Description: Partly Sunny
Max temperature: 28°C
Min temperature: 18°C
======================================== saturday ========================================
Description: Sunny
Max temperature: 30°C
Min temperature: 19°C
======================================== sunday ========================================
Description: Partly Sunny
Max temperature: 29°C
Min temperature: 21°C
======================================== monday ========================================
Description: Partly Cloudy
Max temperature: 30°C
Min temperature: 19°C
======================================== tuesday ========================================
Description: Mostly Sunny
Max temperature: 26°C
Min temperature: 16°C
======================================== wednesday ========================================
Description: Mostly Sunny
Max temperature: 25°C
Min temperature: 19°C
Хорошо, мы закончили с этим учебником, я надеюсь, что это было полезно для вас, чтобы понять, как вы можете объединить запросы и BeautifulSoup для захвата данных с веб-страниц.