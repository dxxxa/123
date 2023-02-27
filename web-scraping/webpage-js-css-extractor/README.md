# [How to Extract Script and CSS Files from Web Pages in Python](https://www.thepythoncode.com/article/extract-web-page-script-and-css-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Extracting `http://books.toscrape.com`'s CSS & Script files:
    ```
    python extractor.py http://books.toscrape.com/
    ```
    2 files will appear, one for javascript files (`javascript_files.txt`) and the other for CSS files (`css_files.txt`)
##
# [[] / []]()
Скажем, вам поручено проанализировать какой-то веб-сайт, чтобы проверить его производительность, и вам нужно извлечь общее количество файлов, необходимых для загрузки веб-страницы для правильной загрузки, в этом уроке я помогу вам достичь этого, создав инструмент Python для извлечения всех ссылок на скрипты и css-файлы, которые связаны с конкретным веб-сайтом.

Мы будем использовать запросы и BeautifulSoup в качестве синтаксического анализатора HTML, если они не установлены на вашем Python, пожалуйста, сделайте:

pip3 install requests bs4
Давайте начнем с инициализации HTTP-сеанса и настройки агента пользователя в качестве обычного браузера, а не бота Python:

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# URL of the web page you want to extract
url = "http://books.toscrape.com"

# initialize a session
session = requests.Session()
# set the User-agent as a regular browser
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
Теперь, чтобы загрузить все HTML-содержимое этой веб-страницы, все, что нам нужно сделать, это вызвать метод session.get(), который возвращает объект ответа, нас интересует только HTML-код, а не весь ответ:

# get the HTML content
html = session.get(url).content

# parse HTML using beautiful soup
soup = bs(html, "html.parser")
Теперь у нас есть наш суп, давайте извлечем все скриптовые и CSS-файлы, мы используем метод soup.find_all(), который возвращает все объекты HTML-супа, отфильтрованные с помощью переданных тегов и атрибутов:

# get the JavaScript files
script_files = []

for script in soup.find_all("script"):
    if script.attrs.get("src"):
        # if the tag has the attribute 'src'
        script_url = urljoin(url, script.attrs.get("src"))
        script_files.append(script_url)
Итак, в основном мы ищем теги скриптов, которые имеют атрибут src, это обычно ссылается на файлы Javascript, необходимые для этого сайта.

Аналогично, мы можем использовать его для извлечения CSS-файлов:

# get the CSS files
css_files = []

for css in soup.find_all("link"):
    if css.attrs.get("href"):
        # if the link tag has the 'href' attribute
        css_url = urljoin(url, css.attrs.get("href"))
        css_files.append(css_url)
Как вы, возможно, знаете, CSS-файлы находятся в атрибутах href в тегах ссылок. Мы используем функцию urljoin(), чтобы убедиться, что ссылка является абсолютной (т.е. с полным путем, а не относительным путем, таким как /js/script.js).

Наконец, давайте распечатаем общие файлы скрипта и CSS и запишем ссылки в отдельные файлы:

print("Total script files in the page:", len(script_files))
print("Total CSS files in the page:", len(css_files))

# write file links into files
with open("javascript_files.txt", "w") as f:
    for js_file in script_files:
        print(js_file, file=f)

with open("css_files.txt", "w") as f:
    for css_file in css_files:
        print(css_file, file=f)
После его выполнения появятся 2 файла, один для ссылок Javascript, а другой для CSS-файлов:

css_files.txt

http://books.toscrape.com/static/oscar/favicon.ico
http://books.toscrape.com/static/oscar/css/styles.css
http://books.toscrape.com/static/oscar/js/bootstrap-datetimepicker/bootstrap-datetimepicker.css
http://books.toscrape.com/static/oscar/css/datetimepicker.css
javascript_files.txt

http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js
http://books.toscrape.com/static/oscar/js/bootstrap3/bootstrap.min.js
http://books.toscrape.com/static/oscar/js/oscar/ui.js
http://books.toscrape.com/static/oscar/js/bootstrap-datetimepicker/bootstrap-datetimepicker.js
http://books.toscrape.com/static/oscar/js/bootstrap-datetimepicker/locales/bootstrap-datetimepicker.all.js
Хорошо, в конце концов, я призываю вас еще больше расширить этот код, чтобы создать сложный инструмент аудита, который способен идентифицировать различные файлы, их размеры и, возможно, может внести предложения по оптимизации веб-сайта!

В качестве вызова попробуйте загрузить все эти файлы и сохранить их на локальном диске (этот учебник может помочь).

У меня есть еще один учебник, чтобы показать вам, как вы можете извлечь все ссылки на веб-сайт, проверьте это здесь.

Кроме того, если веб-сайт, который вы анализируете, случайно блокирует ваш IP-адрес, в этом случае вам необходимо использовать прокси-сервер.