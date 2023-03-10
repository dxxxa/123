# [How to Get Google Page Ranking in Python](https://www.thepythoncode.com/article/get-google-page-ranking-by-keyword-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Setup CSE API and retrieve `API_KEY` and `SEARCH_ENGINE_ID` as shown in [this tutorial](https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python) and replace them in `page_ranking.py` script.
- For instance, to get the page rank of `thepythoncode.com` of the keyword "google custom search engine api python":
    ```
    python page_ranking.py thepythoncode.com "google custom search engine api python"
    ```
    **Output:**
    ```
    [*] Going for page: 1
    [+] thepythoncode.com is found on rank #3 for keyword: 'google custom search engine api python'
    [+] Title: How to Use Google Custom Search Engine API in Python - Python ...
    [+] Snippet: 10 results ... Learning how to create your own Google Custom Search Engine and use its 
    Application Programming Interface (API) in Python.
    [+] URL: https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python 
    ```
##
# [[] / []]()
Google Custom Search Engine (CSE) - это поисковая система, которая позволяет разработчикам включать поиск в свои приложения, будь то настольное приложение, веб-сайт или мобильное приложение.

Возможность отслеживать свой рейтинг в Google - это удобный инструмент, особенно когда вы являетесь владельцем веб-сайта, и вы хотите отслеживать рейтинг своей страницы, когда пишете статью или редактируете ее.

В этом уроке мы создадим скрипт Python, который сможет получить ранжирование страниц вашего домена с помощью CSE API. Прежде чем мы углубимся в это, мне нужно убедиться, что у вас есть настройка CSE API и готовность к работе, если это не так, пожалуйста, ознакомьтесь с руководством, чтобы начать работу с Пользовательским API поисковой системы в Python.

После того, как вы запустили свою поисковую систему, продолжайте и устанавливайте запросы, чтобы мы могли легко выполнять HTTP-запросы:

pip3 install requests
Откройте новый Python и следуйте за ним. Начнем с импорта модулей и определения наших переменных:

import requests
import urllib.parse as p

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "<INSERT_YOUR_API_KEY_HERE>"
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "<INSERT_YOUR_SEARCH_ENGINE_ID_HERE>"
# target domain you want to track
target_domain = "thepythoncode.com"
# target keywords
query = "google custom search engine api python"
Опять же, пожалуйста, проверьте этот учебник, в котором я покажу вам, как получить API_KEY и SEARCH_ENGINE_ID. target_domain - это домен, который вы хотите найти, а запрос - целевое ключевое слово. Например, если вы хотите отслеживать stackoverflow.com по ключевым словам «преобразовать строку в int python», то вы помещаете их в target_domain и запрос соответственно.

Теперь CSE позволяет нам видеть первые 10 страниц, каждая страница поиска имеет 10 результатов, поэтому всего 100 URL-адресов для проверки, приведенный ниже блок кода отвечает за итерацию по каждой странице и поиск доменного имени в результатах:

for page in range(1, 11):
    print("[*] Going for page:", page)
    # calculating start 
    start = (page - 1) * 10 + 1
    # make API request
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data = requests.get(url).json()
    search_items = data.get("items")
    # a boolean that indicates whether `target_domain` is found
    found = False
    for i, search_item in enumerate(search_items, start=1):
        # get the page title
        title = search_item.get("title")
        # page snippet
        snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        link = search_item.get("link")
        # extract the domain name from the URL
        domain_name = p.urlparse(link).netloc
        if domain_name.endswith(target_domain):
            # get the page rank
            rank = i + start - 1
            print(f"[+] {target_domain} is found on rank #{rank} for keyword: '{query}'")
            print("[+] Title:", title)
            print("[+] Snippet:", snippet)
            print("[+] URL:", link)
            # target domain is found, exit out of the program
            found = True
            break
    if found:
        break
Поэтому после того, как мы делаем запрос API к каждой странице, мы перебираем результат и извлекаем доменное имя с помощью функции urllib.parse.urlparse() и смотрим, соответствует ли оно нашему target_domain, причина, по которой мы используем функцию endswith() вместо двойных равных (==), заключается в том, что мы не хотим пропускать URL-адреса, которые начинаются с www или других поддоменов.

Скрипт сделан, вот мой вывод выполнения (после замены моего ключа API и идентификатора поисковой системы, конечно):

[*] Going for page: 1
[+] thepythoncode.com is found on rank #3 for keyword: 'google custom search engine api python'
[+] Title: How to Use Google Custom Search Engine API in Python - Python ...
[+] Snippet: 10 results ... Learning how to create your own Google Custom Search Engine and use its
Application Programming Interface (API) in Python.
[+] URL: https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python
Удивительно, этот сайт занимает третье место по этому ключевому слову, вот еще один пример запуска:

[*] Going for page: 1
[*] Going for page: 2
[+] thepythoncode.com is found on rank #13 for keyword: 'make a bitly url shortener in python'
[+] Title: How to Make a URL Shortener in Python - Python Code
[+] Snippet: Learn how to use Bitly and Cuttly APIs to shorten long URLs programmatically
using requests library in Python.
[+] URL: https://www.thepythoncode.com/article/make-url-shortener-in-python
На этот раз он перешел на 2-ю страницу, так как не нашел его на первой странице. Как упоминалось ранее, он пройдет весь путь до страницы 10 и остановится.

Заключение
Хорошо, у вас есть сценарий, я призываю вас добавить к нему и настроить его. Например, заставьте его принимать несколько ключевых слов для вашего сайта и делайте пользовательские оповещения, чтобы уведомлять вас всякий раз, когда позиция меняется (идет вниз или вверх), удачи!