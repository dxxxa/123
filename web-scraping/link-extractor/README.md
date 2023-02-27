# [How to Extract All Website Links in Python](https://www.thepythoncode.com/article/extract-all-website-links-python)
To run this:
- `pip3 install -r requirements.txt`
-
    ```
    python link_extractor.py --help
    ```
    **Output:**
    ```
    usage: link_extractor.py [-h] [-m MAX_URLS] url

    Link Extractor Tool with Python

    positional arguments:
    url                   The URL to extract links from.

    optional arguments:
    -h, --help            show this help message and exit
    -m MAX_URLS, --max-urls MAX_URLS
                            Number of max URLs to crawl, default is 30.
    ```
- For instance, to extract all links from 2 first URLs appeared in github.com:
    ```
    python link_extractor.py https://github.com -m 2
    ```
    This will result in a large list, here is the last 5 links:
    ```
    [!] External link: https://developer.github.com/
    [*] Internal link: https://help.github.com/
    [!] External link: https://github.blog/
    [*] Internal link: https://help.github.com/articles/github-terms-of-service/
    [*] Internal link: https://help.github.com/articles/github-privacy-statement/
    [+] Total Internal links: 85
    [+] Total External links: 21
    [+] Total URLs: 106
    ```
    This will also save these URLs in `github.com_external_links.txt` for external links and `github.com_internal_links.txt` for internal links.
##
# [[] / []]()
Извлечение всех ссылок веб-страницы является распространенной задачей среди веб-скребков. Полезно создавать продвинутые скребки, которые сканируют каждую страницу определенного веб-сайта для извлечения данных. Он также может быть использован для процесса диагностики SEO или даже для этапа сбора информации для тестеров на проникновение.

В этом уроке вы узнаете, как создать инструмент извлечения ссылок на Python с нуля, используя только запросы и библиотеки BeautifulSoup.

Обратите внимание, что существует множество экстракторов ссылок, таких как Link Extractor от Sitechecker. Цель этого учебника - создать его самостоятельно, используя язык программирования Python.

Получите: Этический взлом с помощью электронной книги Python

Установим зависимости:

pip3 install requests bs4 colorama
Мы будем использовать запросы для удобного выполнения HTTP-запросов, BeautifulSoup для синтаксического анализа HTML и colorama для изменения цвета текста.

Откройте новый файл Python и следуйте за ним. Давайте импортируем нужные нам модули:

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
Мы собираемся использовать colorama только для использования разных цветов при печати, чтобы различать внутренние и внешние ссылки:

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
Нам понадобятся две глобальные переменные, одна для всех внутренних ссылок веб-сайта, а другая для всех внешних ссылок:

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
Внутренние ссылки - это URL-адреса, которые ссылаются на другие страницы того же веб-сайта.
Внешние ссылки - это URL-адреса, которые ссылаются на другие веб-сайты.
Поскольку не все ссылки в якорных тегах (тегах a) являются допустимыми (я экспериментировал с этим), некоторые из них являются ссылками на части веб-сайта, а некоторые - javascript, поэтому давайте напишем функцию для проверки URL-адресов:

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
Это обеспечит наличие в URL-адресе правильной схемы (протокола, например, http или https) и доменного имени.

Теперь давайте создадим функцию для возврата всех допустимых URL-адресов веб-страницы:

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
Во-первых, я инициализировал переменную urls set; Я использовал здесь наборы Python, потому что нам не нужны избыточные ссылки.

Во-вторых, я извлек доменное имя из URL-адреса. Он нам понадобится, чтобы проверить, является ли ссылка, которую мы захватили, внешней или внутренней.

В-третьих, я загрузил HTML-содержимое веб-страницы и обернул его объектом soup, чтобы облегчить синтаксический анализ HTML.

Давайте получим все теги HTML a (теги привязки, которые содержат все ссылки веб-страницы):

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
Таким образом, мы получаем атрибут href и проверяем, есть ли там что-то. В противном случае мы просто перейдем к следующей ссылке.

Поскольку не все ссылки являются абсолютными, нам нужно будет объединить относительные URL-адреса с их доменным именем (например, когда href - "/search", а URL - "google.com", результатом будет "google.com/search"):

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
Теперь нам нужно удалить параметры HTTP GET из URL-адресов, так как это вызовет избыточность в наборе, следующий код обрабатывает это:

        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
Давайте закончим функцию:

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls
Связанные с: Этический взлом с python EBook

Все, что мы здесь сделали, это проверили:

Если URL-адрес недействителен, перейдите к следующей ссылке.
Если URL-адрес уже находится в internal_urls, нам это тоже не нужно.
Если URL-адрес является внешней ссылкой, распечатайте его серым цветом и добавьте в наш глобальный external_urls задать и перейти к следующей ссылке.
Наконец, после всех проверок, URL будет внутренней ссылкой, мы распечатаем его и добавим в наши URL-адреса и наборы internal_urls.

Вышеупомянутая функция будет захватывать только ссылки одной конкретной страницы, что, если мы хотим извлечь все ссылки всего сайта? Давайте сделаем:

# number of urls visited so far will be stored here
total_urls_visited = 0

def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)
Эта функция сканирует веб-сайт, что означает, что он получает все ссылки первой страницы, а затем вызывает себя рекурсивно, чтобы перейти по всем ссылкам, извлеченным ранее. Однако это может вызвать некоторые проблемы; программа застрянет на крупных веб-сайтах (которые получили много ссылок), таких как google.com. В результате я добавил параметр max_urls для выхода, когда мы достигнем определенного количества проверенных URL-адресов.

Хорошо, давайте проверим это; убедитесь, что вы используете его на веб-сайте, на который вы авторизованы. В противном случае я не несу ответственности за любой вред, который вы причиняете.

if __name__ == "__main__":
    crawl("https://www.thepythoncode.com")
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)
Получите -35 OFF: Этический взлом с помощью электронной книги Python

Я тестирую на этом сайте. Однако я настоятельно призываю вас не делать этого; это вызовет много запросов и заполнит веб-сервер, а также может заблокировать ваш IP-адрес.

Вот часть выходных данных:

Результат выполнения Link Extractor

После завершения обхода будет напечатано общее количество ссылок, извлеченных и просканированных:

[+] Total Internal links: 90
[+] Total External links: 137
[+] Total URLs: 227
[+] Total crawled URLs: 30
Потрясающе, правда? Я надеюсь, что этот учебник был полезен для вас, чтобы вдохновить вас на создание таких инструментов с использованием Python.

Есть некоторые веб-сайты, которые загружают большую часть своего контента с помощью JavaScript. Поэтому вместо этого нам нужно использовать библиотеку requests_html, что позволяет нам выполнять Javascript с помощью Chromium; Я уже написал сценарий для этого, добавив всего несколько строк (так как requests_html очень похож на запросы). Проверьте это здесь.

Запрос одного и того же веб-сайта много раз за короткий период может привести к тому, что веб-сайт заблокирует ваш IP-адрес. В таком случае для таких целей необходимо использовать прокси-сервер.

Если вы заинтересованы в захвате изображений, ознакомьтесь с этим учебником: Как загрузить все изображения с веб-страницы на Python или, если вы хотите извлечь html-таблицы, ознакомьтесь с этим учебником.

Я немного отредактировал код, чтобы вы могли сохранить выходные URL-адреса в файле и передать URL-адреса из аргументов командной строки. Я настоятельно рекомендую вам проверить полный код здесь.

В электронной книге Ethical Hacking with Python мы использовали этот код для создания расширенного почтового паука, который входит в каждую извлеченную ссылку и ищет адреса электронной почты. Обязательно проверьте это здесь!

Хотите узнать больше о веб-парсинге?
Наконец, если вы хотите углубиться в веб-парсинг с различными библиотеками Python, а не только BeautifulSoup, следующие курсы, безусловно, будут полезны для вас:

Современный веб-парсинг с помощью Python с использованием Scrapy Splash Selenium.
Основы веб-парсинга и API в Python.