# [How to Build an English Dictionary App with Django in Python](https://www.thepythoncode.com/article/build-dictionary-app-with-django-and-pydictionary-api-python)
##
# [[] / []]()
Словарь - это приложение, которое позволяет пользователям искать конкретное слово и предоставляет значения слова и его синоним и антоним взамен.

В этом уроке вы узнаете, как создать словарь английского языка с помощью фреймворка Django и PyDictionary API на Python. Чтобы следовать этому руководству, необходимо иметь базовое понимание HTML и начальной загрузки, которые будут использоваться для внешнего интерфейса приложения.

Прежде чем мы будем использовать фреймворк Django и PyDictionary API, давайте познакомимся с этими двумя, Django - это фреймворк, используемый для создания веб-приложений, а PyDictionary - это API, который используется для получения значений слов, синонимов, антонимов и переводов.

API PyDictionary не работает в автономном режиме; нужно быть в сети, чтобы делать успешные запросы к API.

Ниже приведено оглавление:

Создание виртуальной среды
Установка Django и PyDictionary
Создание проекта и приложения
Регистрация приложения в Settings.py файле
Настройка URL-адресов приложения
Создание представлений
Создание HTML-шаблонов
Реализация функции поиска слов
Тестирование функциональности
Заключение
Создание виртуальной среды
Давайте, прежде всего, создадим виртуальную среду для этого проекта, назовем его проектом, это не условность; вы можете назвать его как угодно; используйте следующую команду:

$ python -m venv project
Теперь активируйте виртуальную среду с помощью следующей команды:

$ .\project\Scripts\activate
Установка Django и PyDictionary
Затем мы установим необходимые библиотеки внутри активированной виртуальной среды, фреймворка Django и PyDictionary, как показано ниже:

$ pip install django PyDictionary
Создание проекта и приложения
Теперь, когда Django успешно установлен, давайте создадим проект Django с помощью встроенной команды Django django-admin startproject, выполните эту команду в вашем терминале:

$ django-admin startproject djangodictionary
Приведенная выше команда создаст папку под названием djangodictionary, мы будем работать внутри этой папки. Теперь cd в папку djangodictionary и давайте создадим приложение Django. Выполните следующую команду:

$ python manage.py startapp dictionary
После успешной установки Django и создания нового проекта, давайте посмотрим, была ли установка успешной, выполните следующую команду:

$ python manage.py runserver
manage.py представляет собой файл скрипта, который используется для выполнения административных команд Django в терминале, таких как runerver, startproject, startapp и т. Д. Сценарий manage.py создается после выполнения команды django-admin startproject.

Убедитесь, что вы получили следующие выходные данные:

python manage.py runerver

Скопируйте http://127.0.0.1:8000/ в свой браузер, если вы получите следующий вывод, то вы успешно установили Django:

Django успешно установлен

Регистрация приложения в Settings.py файле
В Django каждое приложение, которое мы создаем, должно быть зарегистрировано перед его использованием, теперь внутри папки djangodictionary есть файл под названием settings.py, этот файл используется для настройки параметров для всего проекта:

Регистрация приложения в settings.py файле

Откройте файл settings.py и прокрутите вниз до списка INSTALLED_APPS, чтобы список теперь выглядел следующим образом:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # external installed app
    # registering the dictionary app
    'dictionary',
]
Настройка URL-адресов приложения
Давайте теперь настроим наши URL-адреса, в Django у нас есть два файла urls.py, первый поставляется с Django и используется для регистрации всех URL-адресов приложений, и он находится в корневой папке проекта, в то время как второй urls.py файл создается внутри папки приложения программистом, в нашем случае он будет создан внутри папки словаря.

Прежде всего, давайте зарегистрируем URL-адреса нашего приложения и откроем файл urls.py в корневой папке проекта:

Настройка URL-адресов приложения

Откройте файл urls.py и убедитесь, что он выглядит следующим образом

# importing the django's in-built admin url
from django.contrib import admin
# importing path and include from django's in-built urls
from django.urls import path, include

# defining the list for urls
urlpatterns = [
    path('admin/', admin.site.urls),
    # registering dictionary app urls in project
    path('', include('dictionary.urls')),
]
Теперь, когда мы зарегистрировали URL-адреса приложения словаря, давайте создадим их внутри папки словаря, создадим файл urls.py:

Настройка URL-адресов приложения

Откройте файл urls.py в приложении словаря и добавьте следующее:

# from current folder, we are importing the two views, HomeView & SearchView
from . import views
# importing path from django's in-built urls
from django.urls import path

# defining the list for urls
urlpatterns = [
    path('', views.homeView, name='home'),#this is the home url
    path('search', views.searchView, name='search'),#this is the search url
]
Создание представлений
HomeView и searchView еще не созданы, давайте теперь создадим их. Внутри папки словаря находится файл views.py:

Создание представлений приложения

Откройте этот файл и сделайте так, чтобы он выглядел следующим образом:

# importing the render function from django.shortcuts
# the render function renders templates
from django.shortcuts import render

# this is the view that will render the index page
def homeView(request):
    return render(request, 'dictionary/index.html')

# this is the view that will render search page
def searchView(request):
    return render(request, 'dictionary/search.html')
В следующем разделе мы создадим индекс.html и поиск.html внутри папки словаря.

Создание HTML-шаблонов
Теперь давайте немного отойдем от Django и создадим базовый интерфейс словарного приложения. Очевидно, что мы будем использовать HTML для содержимого приложения и bootstrap для стилизации контента.

В папке словаря создайте папку с именем templates, а внутри этой папки templates создайте другую папку под названием dictionary, здесь Django найдет все HTML-файлы.

Мы создадим три HTML-файла, а именно index.html, search.html и base.html, два файла index.html и search.html унаследуют от base.html. Наследование шаблонов является одной из функций, которые приходят с Django, и это пригодится, потому что мы не будем повторяться.

Теперь давайте создадим эти три HTML-файла:

Создание HTML-файлов

Откройте файл base.html и добавьте следующее:

<!DOCTYPE html>
<html lang="en">
 
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dictionary</title>
    <!-- CSS only -->
    <!-- we are getting bootstrap5 from the CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
 
<body>
    <div class="container mt-4">
        <div class="row">
 
            <div class="mt-4 p-5 bg-success text-white rounded mb-3">
                <h1>ThePythonCode.com Dictionary</h1>
            </div>
 
            <div class="col-md-12">
                {% block content %}
                <!-- here we will inject the content of every page that 
                    inherits from the base page -->
                {% endblock %}
            </div>
        </div>
    </div>
</body>
 
</html>
Базовый шаблон HTML и Bootstrap. индекс.html будет наследовать от файла base.html, поэтому добавьте в index следующее.html:

<!-- the index page is inheriting from the base page -->
<!-- the extends tags are used for inheriting from the base page -->
{% extends 'dictionary/base.html' %}

<!-- the block content tags for containing content of the page -->
{%  block content %}

<form action="search">
    <div class="input-group">
        <input type="text" required class="form-control" name="search" placeholder="Search your favorite word.......">
        <div class="input-group-append">
            <button class="btn btn-success" type="submit">
                Search
            </button>
        </div>
    </div>

</form>

{% endblock %}
Зайдя так далеко, мы еще не почувствовали наше приложение, поэтому давайте протестируем его, запустив сервер:

$ python manage.py runserver
После запуска сервера, зайдите в браузер и обновите страницу http://127.0.0.1:8000/, вы сможете получить следующую страницу:

ThePythonCode.com Страница словаря

Реализация функции поиска слов
Теперь, когда домашняя индексная страница работает успешно, давайте вернемся к Django, на этот раз мы хотим реализовать функциональность поисковых слов через searchView.

Откройте файл views.py в папке словаря и отредактируйте searchView():

# importing the render function from django.shortcuts
# the render function renders templates
from django.shortcuts import render
# importing the PyDictionary library
from PyDictionary import PyDictionary


# this is the view that will render the index page
def homeView(request):
    return render(request, 'dictionary/index.html')


# this is the view that will render search page
def searchView(request):
    # capturing the word from the form via the name search
    word = request.GET.get('search')
    # creating a dictionary object
    dictionary = PyDictionary()
    # passing a word to the dictionary object
    meanings = dictionary.meaning(word)
    # getting a synonym and antonym  
    synonyms = dictionary.synonym(word)
    antonyms = dictionary.antonym(word)
    # bundling all the variables in the context  
    context = {
            'word': word,
            'meanings':meanings,
            'synonyms':synonyms,
            'antonoyms':antonyms
        }
    return render(request, 'dictionary/search.html', context)
Мы используем PyDictionary, чтобы получить значение, синоним и антоним данного слова, затем мы создаем контекстный словарь, который мы будем использовать в поиске.html.

Откройте поиск.html и добавьте ниже:

<!-- the search page inherits from the base -->
{% extends 'dictionary/base.html' %}

{% block content %}
<!-- this will display the searched word -->
<h4>{{ word }}</h4>

<!-- this will display the word meaning -->
<p>{{ meanings }}</p>

<hr>
<!-- this will display the antonym for the word if its available-->
<p><b>Antonyms</b>:{{ antonym }}</p>
<hr>
<!-- this will display the synonym for the word if its available-->
<p><b>Synonyms</b>:{{ synonym }}</p>

{% endblock %}
Тестирование функциональности
Теперь, когда нам удалось реализовать функциональность поиска слов в функции searchView(), давайте протестируем наш поиск по первому слову. Скопируйте http://127.0.0.1:8000 в браузере, чтобы получить вывод ниже:

Тестирование функциональности поисковых слов

Убедитесь, что сервер запущен, если нет, то повторно выполните следующую команду:

$ python manage.py runserver
Теперь, когда приложение запущено, мы найдем слово «программирование», введем слово в поле ввода и нажмем кнопку поиска. После завершения поиска вы будете перенаправлены на страницу поиска, где отображаются все результаты, как показано ниже:

Тестирование функциональности поисковых слов

Заключение
Вот и все для этого урока, мы теперь надеемся, что вы знаете, как поиграть с фреймворком Django и Api PyDictionary.

Обратите внимание, что в этом уроке мы только что рассмотрели несколько основных вещей, рассматривая более продвинутые вещи, которые вы могли бы создать, используя эти два, Django и PyDictionary.