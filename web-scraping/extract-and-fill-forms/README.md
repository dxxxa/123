# [How to Extract and Submit Web Forms from a URL using Python](https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To extract forms, use `form_extractor.py`:
    ```
    python form_extractor.py https://wikipedia.org
    ```
- To extract and submit forms, use `form_submitter.py`:
    ```
    python form_submitter.py https://wikipedia.org
    ```
    This will extract the first form (you can change that in the code) and prompt the user for each non-hidden input field, and then submits the form and loads the respond HTML in your default web browser, try it out!
##
# [[] / []]()
Одной из самых сложных задач в веб-парсинге является возможность автоматического входа в систему и извлечения данных из вашей учетной записи на этом веб-сайте. В этом учебнике вы узнаете, как извлечь все формы из веб-страниц, а также заполнить и отправить их с помощью библиотек requests_html и BeautifulSoup.

Чтобы начать работу, давайте установим их:

pip3 install requests_html bs4
Связанные с: Как автоматизировать вход с помощью Selenium в Python.

Извлечение форм из веб-страниц
Откройте новый файл. Я называю это form_extractor.py:

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
Для начала нам нужен способ убедиться, что после отправки запросов на целевой веб-сайт мы сохраняем файлы cookie, предоставляемые этим веб-сайтом, чтобы мы могли сохранить сеанс:

# initialize an HTTP session
session = HTMLSession()
Теперь переменная session является потребляемым сеансом для сохранения cookie; мы будем использовать эту переменную везде в нашем коде. Давайте напишем функцию, которая задает URL-адрес, запрашивает эту страницу, извлекает из нее все теги HTML-формы, а затем возвращает их (в виде списка):

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")
Вы можете заметить, что я прокомментировал, что строка res.html.render() выполняет Javascript перед попыткой извлечь что-либо, так как некоторые веб-сайты загружают свой контент динамически с помощью Javascript, раскомментируйте его, если вы чувствуете, что веб-сайт использует Javascript для загрузки форм.

Таким образом, вышеупомянутая функция сможет извлекать все формы с веб-страницы, но нам нужен способ извлечения деталей каждой формы, таких как входные данные, метод формы (GET, POST, DELETE и т. Д.) И действие (целевой URL-адрес для отправки формы), следующая функция делает это:

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
Вышесказанное отвечает только за извлечение входных HTML-тегов. Давайте также извлечем selects и textareas:

    for select in form.find_all("select"):
        # get the name attribute
        select_name = select.attrs.get("name")
        # set the type as select
        select_type = "select"
        select_options = []
        # the default select value
        select_default_value = ""
        # iterate over options and get the value of each
        for select_option in select.find_all("option"):
            # get the option value used to submit the form
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    # if 'selected' attribute is set, set this option as default    
                    select_default_value = option_value
        if not select_default_value and select_options:
            # if the default is not set, and there are options, take the first option as default
            select_default_value = select_options[0]
        # add the select to the inputs list
        inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        textarea_type = "textarea"
        # get the textarea value
        textarea_value = textarea.attrs.get("value", "")
        # add the textarea to the inputs list
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
Первый для цикла извлекает все теги select в форме. Мы также получаем все доступные опции и добавляем их в детали формы. Второй цикл заключается в поиске тегов textarea и добавлении их к деталям формы, а также о завершении функции:

    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details
Заметка: Вы всегда можете проверить весь код на этой странице.

Теперь давайте попробуем эти функции, прежде чем мы углубимся в отправку форм:

if __name__ == "__main__":
    import sys
    # get URL from the command line
    url = sys.argv[1]
    # get all form tags
    forms = get_all_forms(url)
    # iteratte over forms
    for i, form in enumerate(forms, start=1):
        form_details = get_form_details(form)
        print("="*50, f"form #{i}", "="*50)
        print(form_details)
Я использовал enumerate() только для нумерации извлеченных форм. Давайте сохраним файл Python как form_extractor.py и запустим его:

$ python form_extractor.py https://wikipedia.org
Вот вывод в случае домашней страницы Википедии:

================================================== form #1 ==================================================
{'action': '//www.wikipedia.org/search-redirect.php',
 'inputs': [{'name': 'family', 'type': 'hidden', 'value': 'Wikipedia'},
            {'name': 'language', 'type': 'hidden', 'value': 'en'},
            {'name': 'search', 'type': 'search', 'value': ''},
            {'name': 'go', 'type': 'hidden', 'value': 'Go'},
            {'name': 'language',
             'type': 'select',
             'value': 'en',
             'values': ['af', 'pl', 'sk', 'ar', 'ast', 'az', 'bg', 'nan', 'bn', 'be', 'ca', 'cs', 'cy', 'da', 'de', 'et', 'el', 'en', 'es', 'eo', 'eu', 'fa', 'fr', 'gl', 'hy', 'hi', 'hr', 'id', 'it', 'he', 'ka', 'la', 'lv', 'lt', 'hu', 'mk', 'arz', 'ms', 'min', 'nl', 'ja', 'no', 'nn', 'ce', 'uz', 'pt', 'kk', 'ro', 'ru', 'simple', 'ceb', 'sl', 'sr', 'sh', 'sv', 'ta', 'tt', 'th', 'tg', 'azb', 'tr', 'uk', 'ur', 'vi', 'vo', 'war', 'zh-yue', 'zh','my']}],
 'method': 'get'}
Как вы можете видеть, если вы попытаетесь перейти на эту страницу с помощью браузера, вы увидите простое окно поиска в Википедии. Вот почему мы видим здесь только одну форму.

Узнайте также: Как загрузить все изображения с веб-страницы на Python.

Отправка веб-форм
Вы также можете заметить, что большинство полей ввода, извлеченных ранее, получили скрытый тип; нас это не интересует. Вместо этого нам нужно заполнить входные данные, в которых он имеет имя «поиск» и тип «поиск», это единственное видимое поле для типичного пользователя. В более общем плане мы ищем любое поле ввода, которое не скрыто для пользователя, включая поля select и textarea.

Откройте новый файл Python. Я назову это form_submitter.py и импортирую библиотеки, которые нам понадобятся:

from bs4 import BeautifulSoup

from pprint import pprint
from urllib.parse import urljoin
import webbrowser
import sys

from form_extractor import get_all_forms, get_form_details, session
Мы берем функции, которые мы делали ранее, из файла form_extractor.py, давайте начнем их использовать.

Во-первых, давайте извлечем все доступные формы и распечатаем их на экране:

# get the URL from the command line
url = sys.argv[1]
all_forms = get_all_forms(url)
# get the first form (edit this as you wish)
# first_form = get_all_forms(url)[0]
for i, f in enumerate(all_forms, start=1):
    form_details = get_form_details(f)
    print(f"{i} #")
    pprint(form_details)
    print("="*50)
Теперь, чтобы сделать наш код максимально гибким (в котором мы можем работать для любого веб-сайта), давайте предложим пользователю скрипта выбрать, какую форму отправить:

choice = int(input("Enter form indice: "))
# extract all form details
form_details = get_form_details(all_forms[choice-1])
pprint(form_details)
Теперь давайте построим наши данные отправки:

# the data body we want to submit
data = {}
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] == "select":
        for i, option in enumerate(input_tag["values"], start=1):
            # iterate over available select options
            if option == input_tag["value"]:
                print(f"{i} # {option} (default)")
            else:
                print(f"{i} # {option}")
        choice = input(f"Enter the option for the select field '{input_tag['name']}' (1-{i}): ")
        try:
            choice = int(choice)
        except:
            # choice invalid, take the default
            value = input_tag["value"]
        else:
            value = input_tag["values"][choice-1]
        data[input_tag["name"]] = value
    elif input_tag["type"] != "submit":
        # all others except submit, prompt the user to set it
        value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
        data[input_tag["name"]] = value
Таким образом, приведенный выше код будет использовать значение по умолчанию скрытых полей (например, маркер CSRF) и запрашивать у пользователя другие поля ввода (такие как поиск, электронная почта, текст и другие). Он также предложит пользователю выбрать один из доступных вариантов выбора.

Давайте посмотрим, как мы можем отправить его на основе метода:

# join the url with the action (form request URL)
url = urljoin(url, form_details["action"])
# pprint(data)
if form_details["method"] == "post":
    res = session.post(url, data=data)
elif form_details["method"] == "get":
    res = session.get(url, params=data)
Здесь я использовал только GET или POST, но вы можете расширить это для других методов HTTP, таких как PUT и DELETE (используя методы session.put() и session.delete() соответственно).

Хорошо, теперь у нас есть переменная res, которая содержит HTTP-ответ; он должен содержать веб-страницу, отправленную сервером после отправки формы; давайте убедимся, что это сработало. Приведенный ниже код подготавливает HTML-содержимое веб-страницы для ее сохранения на локальном компьютере:

# the below code is only for replacing relative URLs to absolute ones
soup = BeautifulSoup(res.content, "html.parser")
for link in soup.find_all("link"):
    try:
        link.attrs["href"] = urljoin(url, link.attrs["href"])
    except:
        pass
for script in soup.find_all("script"):
    try:
        script.attrs["src"] = urljoin(url, script.attrs["src"])
    except:
        pass
for img in soup.find_all("img"):
    try:
        img.attrs["src"] = urljoin(url, img.attrs["src"])
    except:
        pass
for a in soup.find_all("a"):
    try:
        a.attrs["href"] = urljoin(url, a.attrs["href"])
    except:
        pass

# write the page content to a file
open("page.html", "w").write(str(soup))
Все это делается для замены относительных URL-адресов (таких как /wiki/Programming_language) абсолютными URL-адресами (такими как https://www.wikipedia.org/wiki/Programming_language), чтобы мы могли адекватно просматривать страницу локально на нашем компьютере. Я сохранил весь контент в локальный файл "page.html", давайте откроем его в нашем браузере:

import webbrowser
# open the page on the default browser
webbrowser.open("page.html")  
Хорошо, код готов. Вот как я это выполнил:

================================================== form #1 ==================================================
{'action': '//www.wikipedia.org/search-redirect.php',
 'inputs': [{'name': 'family', 'type': 'hidden', 'value': 'Wikipedia'},
            {'name': 'language', 'type': 'hidden', 'value': 'en'},
            {'name': 'search', 'type': 'search', 'value': ''},
            {'name': 'go', 'type': 'hidden', 'value': 'Go'},
            {'name': 'language',
             'type': 'select',
             'value': 'en',
             'values': ['af', 'pl', 'sk', 'ar', 'ast', 'az', 'bg', 'nan', 'bn', 'be', 'ca', 'cs', 'cy', 'da', 'de', 'et', 'el', 'en', 'es', 'eo', 'eu', 'fa', 'fr', 'gl', 'hy', 'hi', 'hr', 'id', 'it', 'he', 'ka', 'la', 'lv', 'lt', 'hu', 'mk', 'arz', 'ms', 'min', 'nl', 'ja', 'no', 'nn', 'ce', 'uz', 'pt', 'kk', 'ro', 'ru', 'simple', 'ceb', 'sl', 'sr', 'sh', 'sv', 'ta', 'tt', 'th', 'tg', 'azb', 'tr', 'uk', 'ur', 'vi', 'vo', 'war', 'zh-yue', 'zh','my']}],
 'method': 'get'}
Enter form indice: 1
{'action': '//www.wikipedia.org/search-redirect.php',
 'inputs': [{'name': 'family', 'type': 'hidden', 'value': 'Wikipedia'},
            {'name': 'language', 'type': 'hidden', 'value': 'en'},
            {'name': 'search', 'type': 'search', 'value': ''},
            {'name': 'go', 'type': 'hidden', 'value': 'Go'},
            {'name': 'language',
             'type': 'select',
             'value': 'en',
             'values': ['af', 'pl', 'sk', 'ar', 'ast', 'az', 'bg', 'nan', 'bn', 'be', 'ca', 'cs', 'cy', 'da', 'de', 'et', 'el', 'en', 'es', 'eo', 'eu', 'fa', 'fr', 'gl', 'hy', 'hi', 'hr', 'id', 'it', 'he', 'ka', 'la', 'lv', 'lt', 'hu', 'mk', 'arz', 'ms', 'min', 'nl', 'ja', 'no', 'nn', 'ce', 'uz', 'pt', 'kk', 'ro', 'ru', 'simple', 'ceb', 'sl', 'sr', 'sh', 'sv', 'ta', 'tt', 'th', 'tg', 'azb', 'tr', 'uk', 'ur', 'vi', 'vo', 'war', 'zh-yue', 'zh','my']}],
 'method': 'get'}
Enter the value of the field 'search' (type: search): python programming language
1 # af
2 # pl
3 # sk
4 # ar
5 # ast
...
<SNIPPED>
18 # en (default)
19 # es
...
<SNIPPED>
67 # vo
68 # war
69 # zh-yue
70 # zh
71 # my
Enter the option for the select field 'language' (1-71): 4
Вначале скрипт подсказывал мне выбирать из списка форм. В нашем случае существует только одна форма. После этого он предложил мне все доступные нескрытые формы, которые являются полем поиска и выбора языка.

Это в основном то же самое, что вручную заполнить форму в веб-браузере и выбрать язык:

Заполнение формы вручную с помощью браузера

После того, как я нажму enter in my code execution, это отправит форму, сохранит страницу результатов локально и автоматически откроет ее в веб-браузере по умолчанию:

Результирующая веб-страница после отправки формы с помощью Python

Именно так Python увидел результат, поэтому мы успешно отправили форму поиска автоматически и загрузили страницу результатов с помощью Python!

Заключение
Ладно, вот и все. В этом уроке мы искали Википедию. Тем не менее, как упоминалось ранее, вы можете использовать его в любой форме, особенно для форм входа, в которых вы можете войти в систему и продолжать извлекать данные, требующие аутентификации пользователя.

Посмотрите, как это можно расширить. Например, вы можете попытаться сделать отправитель для всех форм (так как мы использовали только первую форму здесь), или вы можете сделать сложный сканер, который извлекает все ссылки на веб-сайт и находит все формы конкретного веб-сайта. Однако имейте в виду, что веб-сайт может заблокировать ваш IP-адрес, если вы запросите много страниц в течение короткого времени. В этом случае вы можете замедлить работу сканера или использовать прокси-сервер.

Кроме того, вы можете расширить этот код, автоматизировав вход с помощью Selenium. Проверьте этот учебник о том, как вы можете это сделать!

Вы можете получить полный код этого учебника здесь.

Хотите узнать больше о веб-парсинге?
Наконец, если вы хотите углубиться в веб-парсинг с различными библиотеками Python, а не только BeautifulSoup, следующие курсы, безусловно, будут полезны для вас:

Современный веб-парсинг с помощью Python с использованием Scrapy Splash Selenium.
Основы веб-парсинга и API в Python.
Дополнительное обучение: Как конвертировать HTML-таблицы в CSV-файлы на Python.