# [How to Download All Images from a Web Page in Python](https://www.thepythoncode.com/article/download-web-page-images-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python download_images.py --help
    ```
    **Output:**
    ```
    usage: download_images.py [-h] [-p PATH] url

    This script downloads all images from a web page

    positional arguments:
    url                   The URL of the web page you want to download images

    optional arguments:
    -h, --help            show this help message and exit
    -p PATH, --path PATH  The Directory you want to store your images, default
                            is the domain of URL passed
    ```
- If you want to download all images from https://www.thepythoncode.com/topic/web-scraping for example:
    ```
    python download_images.py https://www.thepythoncode.com/topic/web-scraping
    ```
    A new folder `www.thepythoncode.com` will be created automatically that contains all the images of that web page.
- If you want to download images from javascript-driven websites, consider using `download_images_js.py` script instead (it accepts the same parameters)
##
# [[] / []]()
Вы когда-нибудь хотели загрузить все изображения на определенную веб-страницу? В этом учебнике вы узнаете, как создать скребок Python, который извлекает все изображения с веб-страницы, заданной ее URL-адресом, и загружает их с помощью запросов и библиотек BeautifulSoup.

Чтобы начать, нам нужно довольно много зависимостей, давайте установим их:

pip3 install requests bs4 tqdm
Откройте новый файл Python и импортируйте необходимые модули:

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
Во-первых, давайте сделаем валидатор URL, который гарантирует, что переданный URL-адрес является допустимым, так как есть некоторые веб-сайты, которые помещают закодированные данные вместо URL-адреса, поэтому нам нужно пропустить их:

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
Функция urlparse() разбирает URL на шесть компонентов, нам просто нужно посмотреть, есть ли netloc (доменное имя) и схема (протокол).

Во-вторых, я собираюсь написать основную функцию, которая захватывает все URL-адреса изображений веб-страницы:

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
HTML-содержимое веб-страницы находится в объекте soup, чтобы извлечь все теги img в HTML, нам нужно использовать метод soup.find_all("img"), давайте посмотрим его в действии:

    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
При этом все элементы img будут извлечены в виде списка Python.

Я обернул его в объект tqdm только для того, чтобы напечатать индикатор выполнения. Чтобы получить URL-адрес тега img, существует атрибут src. Тем не менее, есть некоторые теги, которые не содержат атрибут src, мы пропускаем их, используя оператор continue выше.

Теперь нам нужно убедиться, что URL-адрес является абсолютным:

        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
Есть некоторые URL-адреса, содержащие пары ключ-значение HTTP GET, которые нам не нравятся (это заканчивается чем-то вроде этого «/image.png?c=3.2.5»), давайте удалим их:

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
Мы получаем позицию символа '?', а затем удаляем все после него, если его нет, это поднимет ValueError, поэтому я обернул его в блок try/except (конечно, вы можете реализовать его лучше, если это так, пожалуйста, поделитесь с нами в комментариях ниже).

Теперь давайте убедимся, что каждый URL-адрес является допустимым и возвращает все URL-адреса изображений:

        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls
Теперь, когда у нас есть функция, которая захватывает все URL-адреса изображений, нам нужна функция для загрузки файлов из Интернета с помощью Python, я принес следующую функцию из этого учебника:

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
Приведенная выше функция в основном принимает URL-адрес файла для загрузки и путь к папке для сохранения этого файла.

Связанные с: Как конвертировать HTML-таблицы в CSV-файлы на Python.

Наконец, вот основная функция:

def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(img, path)
Получение всех URL-адресов изображений с этой страницы и загрузка каждого из них по одному. Давайте проверим это:

main("https://yandex.com/images/", "yandex-images")
Это загрузит все изображения с этого URL и сохранит их в папке «яндекс-изображения», которая будет создана автоматически.

Обратите внимание, однако, что есть некоторые веб-сайты, которые загружают свои данные с помощью Javascript, в этом случае вы должны использовать requests_html библиотеку вместо этого, я уже сделал другой скрипт, который вносит некоторые изменения в оригинальный и обрабатывает рендеринг Javascript, проверьте это здесь.

Хорошо, мы закончили! Вот несколько идей, которые можно реализовать для расширения кода.

Извлечение всех ссылок на веб-странице и загрузка всех изображений на каждую.
Загрузите каждый PDF-файл на данном веб-сайте.
Используйте многопоточность для ускорения загрузки (так как это тяжелая задача ввода-вывода).
Используйте прокси-серверы, чтобы некоторые веб-сайты не блокировали ваш IP-адрес.
Хотите узнать больше о веб-парсинге?
Наконец, если вы хотите углубиться в веб-парсинг с различными библиотеками Python, а не только BeautifulSoup, следующие курсы, безусловно, будут полезны для вас:

Современный веб-парсинг с помощью Python с использованием Scrapy Splash Selenium.
Основы веб-парсинга и API в Python 2021.