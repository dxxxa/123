# [How to Use Github API in Python](https://www.thepythoncode.com/article/using-github-api-in-python)
To be able to execute this:
`pip3 install -r requirements.txt`
##
# [[] / []]()
GitHub - это служба хостинга репозитория Git, которая добавляет множество своих собственных функций, таких как графический веб-интерфейс для управления репозиториями, контроль доступа и некоторые другие функции, такие как вики, организации, gists и многое другое.

Как вы, возможно, уже знаете, есть тонна данных, которые нужно захватить. В дополнение к использованию GitHub API v3 в Python, вам также может быть интересно узнать, как использовать API Google Диска в Python для автоматизации задач, связанных с Google Диском. Или, возможно, вам нужно использовать API Gmail в Python для автоматизации задач, связанных с вашей учетной записью Gmail.

Из этого туториала Вы узнаете, как использовать GitHub API v3 в Python с помощью запросов или библиотек PyGithub.

Содержание:

Получение пользовательских данных
Получение репозиториев пользователя
Извлечение частных репозиториев вошедшего в систему пользователя
Загрузка файлов в репозиторий
Поиск репозиториев
Управление файлами в репозитории
Заключение
Чтобы начать работу, давайте установим зависимости:

$ pip3 install PyGithub requests
Связанные с: Как извлечь данные YouTube с помощью API YouTube в Python.

Получение пользовательских данных
Поскольку использовать Api Github версии 3 довольно просто, вы можете сделать простой запрос GET к определенному URL-адресу и получить результаты:

import requests
from pprint import pprint

# github username
username = "x4nth055"
# url to request
url = f"https://api.github.com/users/{username}"
# make the request and return the json
user_data = requests.get(url).json()
# pretty print JSON data
pprint(user_data)
Здесь я использовал свой аккаунт; вот часть возвращенного JSON (вы также можете увидеть его в браузере):

{'avatar_url': 'https://avatars3.githubusercontent.com/u/37851086?v=4',
 'bio': None,
 'blog': 'https://www.thepythoncode.com',
 'company': None,
 'created_at': '2018-03-27T21:49:04Z',
 'email': None,
 'events_url': 'https://api.github.com/users/x4nth055/events{/privacy}',
 'followers': 93,
 'followers_url': 'https://api.github.com/users/x4nth055/followers',
 'following': 41,
 'following_url': 'https://api.github.com/users/x4nth055/following{/other_user}',
 'gists_url': 'https://api.github.com/users/x4nth055/gists{/gist_id}',
 'gravatar_id': '',
 'hireable': True,
 'html_url': 'https://github.com/x4nth055',
 'id': 37851086,
 'login': 'x4nth055',
 'name': 'Rockikz',
<..SNIPPED..>
Много данных, поэтому использование одной только библиотеки запросов не будет удобным для извлечения этой тонны данных вручную. В результате на помощь приходит ПиГитуб.

Связанные с: Веб-перехватчики в Python с Помощью Flask.

Получение репозиториев пользователя
Давайте получим все общедоступные репозитории этого пользователя, используя библиотеку PyGithub, которую мы только что установили:

import base64
from github import Github
from pprint import pprint

# Github username
username = "x4nth055"
# pygithub object
g = Github()
# get that user by username
user = g.get_user(username)

for repo in user.get_repos():
    print(repo)
Вот мой вывод:

Repository(full_name="x4nth055/aind2-rnn")
Repository(full_name="x4nth055/awesome-algeria")
Repository(full_name="x4nth055/emotion-recognition-using-speech")
Repository(full_name="x4nth055/emotion-recognition-using-text")
Repository(full_name="x4nth055/food-reviews-sentiment-analysis")
Repository(full_name="x4nth055/hrk")
Repository(full_name="x4nth055/lp_simplex")
Repository(full_name="x4nth055/price-prediction")
Repository(full_name="x4nth055/product_recommendation")
Repository(full_name="x4nth055/pythoncode-tutorials")
Repository(full_name="x4nth055/sentiment_analysis_naive_bayes")
Итак, я сделал простую функцию для извлечения полезной информации из этого объекта Repository:

def print_repo(repo):
    # repository full name
    print("Full name:", repo.full_name)
    # repository description
    print("Description:", repo.description)
    # the date of when the repo was created
    print("Date created:", repo.created_at)
    # the date of the last git push
    print("Date of last push:", repo.pushed_at)
    # home website (if available)
    print("Home Page:", repo.homepage)
    # programming language
    print("Language:", repo.language)
    # number of forks
    print("Number of forks:", repo.forks)
    # number of stars
    print("Number of stars:", repo.stargazers_count)
    print("-"*50)
    # repository content (files & directories)
    print("Contents:")
    for content in repo.get_contents(""):
        print(content)
    try:
        # repo license
        print("License:", base64.b64decode(repo.get_license().content.encode()).decode())
    except:
        pass
Объект репозитория имеет множество других полей. Я предлагаю вам использовать dir(repo), чтобы получить поля, которые вы хотите напечатать. Давайте снова повторим репозитории и воспользуемся функцией, которую мы только что написали:

# iterate over all public repositories
for repo in user.get_repos():
    print_repo(repo)
    print("="*100)
Это приведет к печати некоторой информации о каждом публичном репозитории этого пользователя:

====================================================================================================
Full name: x4nth055/pythoncode-tutorials
Description: The Python Code Tutorials
Date created: 2019-07-29 12:35:40
Date of last push: 2020-04-02 15:12:38
Home Page: https://www.thepythoncode.com
Language: Python
Number of forks: 154
Number of stars: 150
--------------------------------------------------
Contents:
ContentFile(path="LICENSE")
ContentFile(path="README.md")
ContentFile(path="ethical-hacking")
ContentFile(path="general")
ContentFile(path="images")
ContentFile(path="machine-learning")
ContentFile(path="python-standard-library")
ContentFile(path="scapy")
ContentFile(path="web-scraping")
License: MIT License
<..SNIPPED..>
Я урезал весь вывод, так как он вернет все репозитории и их информацию; вы можете видеть, что мы использовали метод repo.get_contents("") для извлечения всех файлов и папок этого репозитория, PyGithub анализирует его в объект ContentFile, используйте dir(content), чтобы увидеть другие полезные поля.

Извлечение частных репозиториев вошедшего в систему пользователя
Кроме того, если у вас есть частные репозитории, вы можете получить к ним доступ, аутентифицировав свою учетную запись (используя правильные учетные данные) с помощью PyGithub следующим образом:

username = "username"
password = "password"

# authenticate to github
g = Github(username, password)
# get the authenticated user
user = g.get_user()
for repo in user.get_repos():
    print_repo(repo)
GitHub также предлагает использовать аутентифицированные запросы, так как это вызовет исключение RateLimitExceededException, если вы используете общедоступный (без аутентификации) и превышаете небольшое количество запросов.

Загрузка файлов в репозиторий
Вы также можете скачать любой файл из любого репозитория, который вы хотите. Для этого я редактирую функцию print_repo() для поиска файлов Python в данном репозитории. Если найдено, мы делаем соответствующее имя файла и записываем его содержимое, используя атрибут content.decoded_content. Вот отредактированная версия функции print_repo():

# make a directory to save the Python files
if not os.path.exists("python-files"):
    os.mkdir("python-files")

def print_repo(repo):
    # repository full name
    print("Full name:", repo.full_name)
    # repository description
    print("Description:", repo.description)
    # the date of when the repo was created
    print("Date created:", repo.created_at)
    # the date of the last git push
    print("Date of last push:", repo.pushed_at)
    # home website (if available)
    print("Home Page:", repo.homepage)
    # programming language
    print("Language:", repo.language)
    # number of forks
    print("Number of forks:", repo.forks)
    # number of stars
    print("Number of stars:", repo.stargazers_count)
    print("-"*50)
    # repository content (files & directories)
    print("Contents:")
    try:
        for content in repo.get_contents(""):
            # check if it's a Python file
            if content.path.endswith(".py"):
                # save the file
                filename = os.path.join("python-files", f"{repo.full_name.replace('/', '-')}-{content.path}")
                with open(filename, "wb") as f:
                    f.write(content.decoded_content)
            print(content)
        # repo license
        print("License:", base64.b64decode(repo.get_license().content.encode()).decode())
    except Exception as e:
        print("Error:", e)
После того, как вы снова запустите код (вы можете получитьполный код всего учебника здесь), вы заметите папку с именем python-files, которая содержит файлы Python из разных репозиториев этого пользователя:

Загруженные файлы из репозитория GitHubУзнайте также: Как сделать сокращение URL-адреса в Python.

Поиск репозиториев
GitHub API довольно богат; Вы можете искать репозитории по определенному запросу так же, как вы это делаете на веб-сайте:

# search repositories by name
for repo in g.search_repositories("pythoncode tutorials"):
    # print repository details
    print_repo(repo)
Это вернет 9 репозиториев и их информацию.

Вы также можете выполнять поиск по языку программирования или теме:

# search by programming language
for i, repo in enumerate(g.search_repositories("language:python")):
    print_repo(repo)
    print("="*100)
    if i == 9:
        break
Чтобы найти определенную тему, вы просто помещаете что-то вроде «тема: машинное обучение» в метод search_repositories().

Читайте также: Как извлечь данные Википедии на Python.

Управление файлами в репозитории
Если вы используете версию с проверкой подлинности, вы также можете легко создавать, обновлять и удалять файлы с помощью API:

# searching for my repository
repo = g.search_repositories("pythoncode tutorials")[0]

# create a file and commit n push
repo.create_file("test.txt", "commit message", "content of the file")

# delete that created file
contents = repo.get_contents("test.txt")
repo.delete_file(contents.path, "remove test.txt", contents.sha)
Приведенный выше код является простым вариантом использования; Я искал конкретный репозиторий, я добавил новый файл и назвал его test.txt, я поместил в него некоторый контент и сделал фиксацию. После этого я схватил содержимое этого нового файла и удалил его (и он также будет считаться фиксацией git).

И, конечно же, после выполнения вышеуказанных строк кода были созданы и протолкнуты коммиты:

Коммиты GithubЗаключение
Мы только что поцарапали поверхность GitHub API, есть много других функций и методов, которые вы можете использовать, и, очевидно, мы не можем охватить их все. Вот некоторые полезные из них, которые вы можете протестировать самостоятельно:

g.get_organization(login): возвращает объект Organization, представляющий организацию GitHub.
g.get_gist(id): возвращает объект Gist, представляющий gist в GitHub.
g.search_code(query): возвращает разбиение на страницы списка объектов ContentFile, представляющих соответствующие файлы в нескольких репозиториях.
g.search_topics(query): возвращает список объектов Topic с разбивкой на страницы, представляющих раздел GitHub.
g.search_commits(query): возвращает список объектов Commit с разбивкой на страницы, в котором он представляет фиксацию в GitHub.
Их гораздо больше; пожалуйста, используйте dir(g) для получения других методов. Обратитесь к документации PyGithub или API GitHub для получения подробной информации.