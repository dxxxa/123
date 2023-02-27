# [How to Use Google Custom Search Engine API in Python](https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python)
To run this:
- `pip3 install -r requirements.txt`
- You need to setup a CSE account, check [the tutorial](https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python) on how you can set up one. 
- Change `API_KEY` and `SEARCH_ENGINE_ID` variables to yours, and then:
    ```
    python search_engine.py "python"
    ```
    This will use the query "python" to search for results, here is a cropped output:
    ```
    ========== Result #1 ==========
    Title: Welcome to Python.org
    Description: The official home of the Python Programming Language.
    URL: https://www.python.org/

    ========== Result #2 ==========
    Title: The Python Tutorial — Python 3.8.2 documentation
    Description: It has efficient high-level data structures and a simple but effective approach to 
    object-oriented programming. Python's elegant syntax and dynamic typing,
    together ...
    URL: https://docs.python.org/3/tutorial/

    ========== Result #3 ==========
    Title: Download Python | Python.org
    Description: Looking for Python with a different OS? Python for Windows, Linux/UNIX, Mac OS     
    X, Other. Want to help test development versions of Python? Prereleases ...
    URL: https://www.python.org/downloads/
    <..SNIPPED..>
    ```
- You can specify the page number, let's get 3rd result page for instance:
    ```
    python search_engine.py "python" 3
    ```
    Here is a **truncated output**:
    ```
    ========== Result #21 ==========
    Title: Python Tutorial - Tutorialspoint
    Description: Python is a general-purpose interpreted, interactive, object-oriented, and high-  
    level programming language. It was created by Guido van Rossum during 1985-
    ...
    URL: https://www.tutorialspoint.com/python/index.htm

    ========== Result #22 ==========
    Title: Google Python Style Guide
    Description: Python is the main dynamic language used at Google. This style guide is a list of 
    dos and don'ts for Python programs. To help you format code correctly, we've ...
    URL: http://google.github.io/styleguide/pyguide.html

    ========== Result #23 ==========
    Title: Individual Edition | Anaconda
    Description: Open Source Anaconda Individual Edition is the world's most popular Python        
    distribution platform with over 20 million users worldwide. You can trust in…
    URL: https://www.anaconda.com/products/individual
    <..SNIPPED..>
    ```
##
# [[] / []]()
Google Custom Search Engine (CSE) - это поисковая система, которая подходит для разработчиков, в которой она позволяет включать поисковую систему в ваше приложение, будь то веб-сайт, мобильное приложение или что-либо еще.

Поскольку ручная очистка Google Search очень незагружена, так как она будет ограничиваться повторным CAPTCHA каждые несколько запросов, в этом учебнике вы узнаете, как настроить CSE и использовать его API на Python.

В CSE вы можете настроить свой движок, который ищет результаты на определенных веб-сайтах, или вы можете использовать только свой веб-сайт. Тем не менее, мы позволим нашей поисковой системе искать этот учебник по всему Интернету.

Узнайте также: Как использовать API Google Диска в Python.

Настройка CSE
Во-первых, вам нужно иметь учетную запись Google для настройки поисковой системы. После этого перейдите на страницу CSE и войдите в пользовательскую поисковую систему, как показано на следующем рисунке:

Вход в пользовательскую поисковую систему

После того, как вы войдете в свою учетную запись Google, вам появится новая панель, которая будет выглядеть примерно так:

Создание нового CSE

Вы можете включить веб-сайты, которые вы хотите включить в результаты поиска, выбрать язык своей поисковой системы и настроить ее имя. По завершении вы будете перенаправлены на эту страницу:

Создано CSE

Использование CSE API в Python
Теперь, чтобы использовать вашу поисковую систему в Python, вам нужны две вещи: Во-первых, вам нужно получить свой идентификатор поисковой системы, вы можете легко найти его в панели управления CSE:

Идентификатор поисковой системы на панели управления

Во-вторых, вы должны сгенерировать новый ключ API, перейти на страницу Custom Search JSON API и нажать на кнопку «Получить ключ», там появится новое окно, вам нужно создать новый проект (вы можете назвать его как хотите) и нажать кнопку «Далее», после чего у вас будет ключ API, вот мой результат:

Ключ API CSE готов к использованию

Наконец, если вы хотите искать во всем Интернете, вам нужно включить его на панели управления:

Включение функции поиска по всему Интернету в CSEТеперь у вас есть все необходимое для использования CSE API в вашем коде Python, откройте новый файл Python и следуйте за ним. Мы будем использовать библиотеку запросов для удобства. Вы можете установить его с помощью этой команды:

pip3 install requests
Давайте инициализируем наши требования CSE:

import requests

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "<INSERT_YOUR_API_KEY_HERE>"
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "<INSERT_YOUR_SEARCH_ENGINE_ID_HERE>"
Мы сделаем простой поисковый запрос «python» для демонстрационных целей. Давайте создадим URL-адрес API, который мы запросим:

# the search query you want
query = "python"
# using the first page
page = 1
# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
start = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
Здесь мы создаем URL-адрес, который мы будем запрашивать. По умолчанию API CSE возвращает первые десять результатов поиска. Например, изменение номера страницы на 2 приведет к тому, что параметр start API будет установлен равным 11, поэтому он вернет результат второй страницы и так далее.

Выполнение запроса API и использование метода json() запросов для автоматического синтаксического анализа возвращенных данных JSON в словарь Python:

# make the API request
data = requests.get(url).json()
Теперь эти данные представляют собой словарь, содержащий множество тегов результатов. Нас интересуют только «предметы», которые являются результатами поиска. По умолчанию CSE возвращает десять результатов поиска. Давайте повторим их:

# get the result items
search_items = data.get("items")
# iterate over 10 results found
for i, search_item in enumerate(search_items, start=1):
    try:
        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
    except KeyError:
        long_description = "N/A"
    # get the page title
    title = search_item.get("title")
    # page snippet
    snippet = search_item.get("snippet")
    # alternatively, you can get the HTML snippet (bolded keywords)
    html_snippet = search_item.get("htmlSnippet")
    # extract the page url
    link = search_item.get("link")
    # print the results
    print("="*10, f"Result #{i+start-1}", "="*10)
    print("Title:", title)
    print("Description:", snippet)
    print("Long description:", long_description)
    print("URL:", link, "\n")
Мы извлекаем заголовок, длинное описание, фрагмент (т.е. описание) и ссылку на результирующую страницу. Проверьте результат:

========== Result #1 ==========
Title: Welcome to Python.org
Description: The official home of the Python Programming Language.
Long description: The official home of the Python Programming Language
URL: https://www.python.org/

========== Result #2 ==========
Title: The Python Tutorial — Python 3.8.2 documentation
Description: It has efficient high-level data structures and a simple but effective approach to 
object-oriented programming. Python's elegant syntax and dynamic typing,
together ...
Long description: N/A
URL: https://docs.python.org/3/tutorial/

========== Result #3 ==========
Title: Download Python | Python.org
Description: Looking for Python with a different OS? Python for Windows, Linux/UNIX, Mac OS     
X, Other. Want to help test development versions of Python? Prereleases ...
Long description: The official home of the Python Programming Language
URL: https://www.python.org/downloads/
Это потрясающе, я сократил вывод только до трех результатов поиска, но в вашем случае он напечатает десять результатов.

Заключение
Вы можете указать различные параметры запроса для настройки поиска. Вы также можете распечатать словарь данных, чтобы увидеть другие метаданные, такие как общие результаты, время поиска и даже метатеги каждой страницы. Ознакомьтесь с документацией CSE для получения дополнительной информации.

По умолчанию он ограничен 100 поисковыми запросами в день для свободного доступа. Если вы считаете, что этого недостаточно для вашего приложения, рассмотрите возможность регистрации для выставления счетов в консоли API.

Отличным вариантом использования этого API является получение рейтинга Google определенной страницы по определенному ключевому слову. Проверьте этот учебник, в котором я покажу вам, как!

Теперь вы можете интегрировать методы поиска в свои приложения, и я надеюсь, что этот учебник был полезен и прост в использовании. Если вам это нравится, пожалуйста, не стесняйтесь поделиться им!

Есть и другие учебники по API Google. Вот некоторые из них, если вы хотите проверить их:

Как извлечь данные Google Trends в Python.
Как использовать API Google Диска в Python.
Как извлечь данные YouTube с помощью API YouTube в Python.
Как использовать API Gmail в Python.