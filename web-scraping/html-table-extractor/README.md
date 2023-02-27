# [How to Convert HTML Tables into CSV Files in Python](https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To extract all tables from this [wikipedia page](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population):
    ```
    python html_table_extractor.py https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
    ```
    This will download all HTML tables and save them as CSV files in your current directory.
##
# [[] / []]()
Вы когда-нибудь хотели автоматически извлекать HTML-таблицы из веб-страниц и сохранять их в правильном формате на своем компьютере? Если это так, то вы находитесь в правильном месте. В этом уроке мы будем использовать запросы и библиотеки BeautifulSoup для преобразования любой таблицы на любой веб-странице и сохранения ее на нашем диске.

Мы также будем использовать панд для легкого преобразования в формат CSV (или любой формат, который поддерживают панды). Если у вас нет запросов, BeautifulSoup и панды установлены, то установите их с помощью следующей команды:

pip3 install requests bs4 pandas
Если вы хотите сделать обратное, преобразовав фреймы данных Pandas в таблицы HTML, проверьте этот учебник.

Откройте новый файл Python и следуйте за ним. Давайте импортируем библиотеки:

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
Нам нужна функция, которая принимает целевой URL-адрес и дает нам правильный объект soup:

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")
Сначала мы инициализируем сеанс запросов, используем заголовок User-Agent, чтобы указать, что мы просто обычный браузер, а не бот (некоторые веб-сайты блокируют их), а затем мы получаем HTML-контент с помощью метода session.get(). После этого мы создаем объект BeautifulSoup с помощью html.parser.

Связанный туториал: Как сделать экстрактор электронной почты на Python.

Поскольку мы хотим извлечь каждую таблицу на любой странице, нам нужно найти HTML-тег таблицы и вернуть его. Следующая функция делает именно это:

def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")
Теперь нам нужен способ получить заголовки таблиц, имена столбцов или как вы хотите их назвать:

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers
Приведенная выше функция находит первую строку таблицы и извлекает все теги th (заголовки таблиц).

Теперь, когда мы знаем, как извлекать заголовки таблиц, оставшаяся часть состоит в том, чтобы извлечь все строки таблицы:

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows
Все, что делает вышеупомянутая функция, это найти теги tr (строки таблицы) и извлечь элементы td, которые затем добавляют их в список. Причина, по которой мы использовали table.find_all("tr")[1:], а не все теги tr, заключается в том, что первый тег tr соответствует заголовкам таблиц; мы не хотим добавлять его сюда.

Приведенная ниже функция принимает имя таблицы, заголовки таблиц и все строки и сохраняет их в формате CSV:

def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")
Теперь, когда у нас есть все основные функции, давайте объединим их все в функции main():

def main(url):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table)
        # save table as csv file
        table_name = f"table-{i}"
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)
Приведенная выше функция выполняет следующие действия:

Анализ HTML-содержимого веб-страницы с заданным URL-адресом путем создания объекта BeautifulSoup.
Поиск всех таблиц на этой HTML-странице.
Перебирая все эти извлеченные таблицы и сохраняя их одну за другой.
Напоследок назовем основную функцию:

if __name__ == "__main__":
    import sys
    try:
        url = sys.argv[1]
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(1)
    main(url)
Это примет URL-адрес из аргументов командной строки, давайте попробуем, если это работает:

C:\pythoncode-tutorials\web-scraping\html-table-extractor>python html_table_extractor.py https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
[+] Found a total of 2 tables.
[+] Saving table-1
[+] Saving table-2
Хорошо, два CSV-файла появились в моем текущем каталоге, который соответствует двум таблицам на этой странице Википедии, вот часть одной из извлеченных таблиц:

Таблица страниц Википедии успешно извлечена

Замечательно! Мы успешно создали скрипт Python, чтобы извлечь любую таблицу с любого веб-сайта, попытаться передать другие URL-адреса и посмотреть, работает ли она.

Для веб-сайтов, управляемых Javascript (которые динамически загружают данные веб-сайта с помощью Javascript), попробуйте вместо этого использовать библиотеку requests-html или selenium. Давайте посмотрим, что вы сделали в комментариях ниже!

Вы также можете создать веб-сканер, который загружает все таблицы с всего веб-сайта. Вы можете сделать это, извлекая все ссылки на веб-сайты и запуская этот скрипт на каждом из URL-адресов, которые вы получили от него.

Кроме того, если по какой-либо причине веб-сайт, который вы очищаете, блокирует ваш IP-адрес, вам нужно использовать прокси-сервер в качестве контрмеры.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Читайте также: Как извлекать и отправлять веб-формы из URL-адреса с помощью Python.