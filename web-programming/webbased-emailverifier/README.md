# [How to Build an Email Address Verifier App using Django in Python](https://www.thepythoncode.com/article/build-an-email-verifier-app-using-django-in-python)
##
# [[] / []]()
Проверка адреса электронной почты — это процесс, который включает в себя подтверждение подлинности или легитимности адреса электронной почты. В настоящее время компании интегрируют проверку электронной почты в свои повседневные операции, и это оказалось более эффективным, поскольку помогает им сохранять только адреса электронной почты клиентов, которые являются действительными и доступными.

В Интернете есть тонны услуг по проверке адресов электронной почты, но все это обходится дорого, но хорошая новость заключается в том, что вы можете бесплатно создать свой собственный инструмент для этой задачи с помощью пакетов Django и email-validator. В этой статье вы узнаете, как создать свой собственный веб-верификатор адресов электронной почты с нуля, поэтому с учетом сказанного, давайте погрузимся в него!

К концу этой статьи вы сможете создать приложение, которое выглядит следующим образом:

Верификатор электронной почты

Вот оглавление:

Начало работы
Создание основного проекта и приложения
Регистрация приложения в settings.py файле
Создание основного представления для приложения в файле views.py
Настройка URL-адресов для приложения
Создание и рендеринг шаблонов
Проверка адресов электронной почты
Заключение
Начало работы
Начнем с создания виртуальной среды для проекта; мы будем использовать эту команду:

$ python -m venv project
Чтобы активировать виртуальную среду, используйте:

$ .\project\Scripts\activate
Создав и активировав виртуальную среду, установим в ней необходимые зависимости для данного проекта; мы установим их за один раз, поэтому используйте:

$ pip install django email-validator
Создание основного проекта и приложения
Теперь, когда о настройке среды проекта позаботились, мы должны создать основной проект Django, теперь запустите:

$ django-admin startproject webbased_emailverifier
Затем cd в папку webbased_emailverifier с этой командой:

$ cd webbased_emailverifier
В папке webbased_emailverifier выполните следующую команду:

$ python manage.py startapp verifier
Это создаст приложение верификатора. После всего этого убедитесь, что у вас есть следующая структура папок для проекта:



Папка верификатора - это приложение, папка webbased_emailverifier - основной проект, а файл manage.py - это скрипт, который помогает нам выполнять административные команды Django, такие как startapp, runserver и т. Д.

Прежде чем двигаться дальше, давайте проверим, был ли Django установлен успешно, чтобы запустить локальный сервер Django, выполните команду:

$ python manage.py runserver
Если сервер работает успешно, вставьте URL-адрес http://127.0.0.1:8000/ в веб-браузере и убедитесь, что вы получили этот вывод в браузере:



Это означает, что Django был успешно установлен, и мы готовы продолжить.

Регистрация приложения в settings.py файле
Наше приложение верификатора еще не известно основному проекту, поэтому мы должны его зарегистрировать. Для этого откройте файл settings.py, расположенный внутри webbased_emailverifier:



И прокрутите вниз, пока не найдете список INSTALLED_APP, и отредактируйте его так, чтобы он выглядел следующим образом:



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # the newly created application
    'verifier',
]
Файл settings.py является важным файлом для проекта, так как он отвечает за все конфигурации проекта, поэтому будьте очень осторожны при его редактировании, потому что одна испорченная строка кода может сломать весь проект.

Создание основного представления для приложения в файле views.py
Теперь мы создадим представление для приложения и откроем файл views.py, который находится внутри папки verifier:



Файл views.py обрабатывает всю логику приложения, например захват и проверку данных из форм, выполнение вызовов API-запросов и проверку подлинности пользователей.

Откройте его и вставьте следующие строки кода:

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('This is the Index page!!')
В фрагменте кода мы импортируем функцию HttpResponse() из django.http, эта функция предназначена только для повторения ответов в браузере пользователю. Вы узнаете больше о функции render() далее в статье.

Настройка URL-адресов для приложения
Теперь давайте создадим URL-адреса для приложения. Создайте файл urls.py в папке верификатора следующим образом:



Этот файл предназначен для регистрации представлений приложения; убедитесь, что вы назвали его urls.py иначе; это условность Джанго.

Откройте его и вставьте следующий код:

# from the current folder import views
from views import index
# importing path from django.urls
from django.urls import path

# this is the list of the app's views
# if the app has several views then it will have several paths
urlpatterns = [
    path('', index, name='home'),
]
В файл мы импортируем представление index() из views.py файла. После импорта мы создаем список под названием urlpatterns list, который будет содержать URL-путь, и если приложение имеет несколько представлений, то urlpatterns будет содержать несколько URL-путей. Если вы заметили, функция path() принимает три аргумента: фактический путь в виде пустой строки, представление и имя представления.

Теперь давайте сделаем URL приложения известным проекту, откроем папку webbased_emailverifier и откроем файл urls.py:

Здесь стоит упомянуть, что файл urls.py приложения не совпадает с файлом urls.py проекта. Файл urls.py в папке verifier предназначен для регистрации всех представлений приложения, а файл urls.py в папке webbased_emailverifier предназначен для регистрации URL-адресов всех приложений. Если проект имеет, например, пять приложений, то URL-адреса всех этих приложений будут зарегистрированы в urls.py файле проекта.

Откройте его и вставьте следующий код:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # this points to admin.site urls
    path('admin/', admin.site.urls),
    # this points to verifier urls
    path('', include('verifier.urls')),
]
Давайте немного разберем код, чтобы мы были на одной странице. Мы создаем список urlpatterns с двумя функциями path(), первая из которых указывает на URL-адреса сайтов администратора по умолчанию, а вторая — на URL-адреса приложений верификатора с помощью функции include().

Пришло время проверить, работают ли все конфигурации, которые мы сделали. Убедитесь, что сервер запущен; на всякий случай, если он остановился, перезапустите его. Теперь в своем веб-браузере перейдите по этому URL-адресу http://127.0.0.1:8000/; Выходные данные будут выглядеть следующим образом:



Кажется, что все работает отлично.

Создание и рендеринг шаблонов
Теперь мы переключим наше внимание на построение фронтенд-части приложения. Мы будем использовать HTML и Bootstrap5 для стилизации. Создадим шаблоны для приложения внутри папки verifier.

Создайте папку с именем templates, и внутри этой папки templates создайте другую папку под названием verifier, это способ Django делать вещи.

Это приложение будет иметь две базы шаблонов.html и индекс.html, и они будут расположены внутри вновь созданной папки верификатора:



Прежде всего, откройте базу.html и вставьте следующий код:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web-based Email Verifier</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="background-color:rgb(248, 244, 244)">
    {% block content %}

    {% endblock %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
Это html-файл шаблона, в который Bootstrap5 CSS и JavaScript добавлены через теги link и script соответственно. JavaScript добавит интерактивность во внешний интерфейс.

Шаблон index.html унаследует все от базового.html шаблона, это удобно, так как экономит наше время, потому что мы не будем повторять код, тем самым делая его чистым. Откройте шаблон index.html и вставьте следующий код:

<!-- extends is for inheriting from the base.html -->
{% extends 'verifier/base.html' %}
{% block content %}
<div class="row justify-content-center my-5">
          <div class="col-md-5 mt-4">
              <div class="card">
                  <h3 class="card-header">Email Verifier</h3>
                  <div class="card-body">
                    <form action="." method="POST">
                      {% csrf_token %}
                      <div class="input-group">
                        <input type="text" required class="form-control" name="email-address" placeholder="Enter an email address to verify it">
                        <div class="input-group-append">
                          <button class="btn btn-primary fw-bold" type="submit">
                            Verify
                          </button>
                        </div>
                      </div>
                    </form>
                      <hr>
                      {% if messages %}
                          {% for message in messages %}
                            {% if message.tags == 'success' %}
                              <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                                  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                </svg> {{ email }} is a valid email address!!!!!
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                              </div>
                            {% elif message.tags == 'warning' %}
                              <div class="alert alert-danger alert-dismissible fade show" role="alert">
				{{ email }}
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
                                  <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                                </svg> {{ message }} 
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                              </div>
                            {% endif %}       
                          {% endfor %}
                      {% endif %}
                  </div>
              </div>
          </div>
        </div>
</div>
{% endblock %}
Для наследования шаблона индекса.html от шаблона base.html мы используем:

{% extends 'verifier/base.html' %}
Этот шаблон предназначен для отображения результатов проверки формы и адреса электронной почты. Внутри формы у нас есть следующий код:

{% csrf_token %}
Поскольку форма использует метод POST, мы используем csrf_token, чтобы защитить ее во время отправки от любой формы вредоносной атаки.

Создав все шаблоны, пришло время отобразить их в браузере, открыть файл views.py и отредактировать функцию index() так, чтобы она выглядела так:

def index(request):
    return render(request, 'verifier/index.html')
Здесь мы заменили функцию HttpResponse() функцией render(), эта функция предназначена для шаблонов рендеринга, и она принимает два аргумента, запрос и фактический шаблон.

Теперь давайте рассмотрим первый взгляд на приложение. Снова посетите URL-адрес по умолчанию, и если вы обновите страницу, вы получите следующий результат:



Поздравляем с разработкой интерфейса приложения!

Проверка адресов электронной почты
В этой заключительной части статьи мы реализуем функциональность проверки адреса электронной почты. Для этого откройте файл views.py и сделайте его следующим образом:

from django.shortcuts import render
# this displays flash messages or notifications
from django.contrib import messages
# importing validate_email and EmailNotValidError
from email_validator import validate_email, EmailNotValidError

# Create your views here.
def index(request):
    # checking if the method is POST
    if request.method == 'POST':
        # getting the email from the form input
        email = request.POST.get('email-address')
        # this is the context
        context = {
                'email': email
            }
        # the try statement for verify/validating the email
        try:
            # validating the actual email address using the validate_email function
            email_object = validate_email(email)
            # creating the message and storing it
            messages.success(request, f'{email} is a valid email address!!')
            # rendering the results to the index page
            return render(request, 'verifier/index.html', context)
        # the except statement will capture EmailNotValidError error 
        except EmailNotValidError as e:
            # creating the message and storing it
            messages.warning(request, f'{e}')
            # rendering the error to the index page
            return render(request, 'verifier/index.html', context)
    # this will render when there is no request POST or after every POST request  
    return render(request, 'verifier/index.html')
В фрагменте кода мы импортируем функцию render(), как обычно, мы также импортируем встроенные сообщения Django из django.contrib, это для отображения флэш-сообщений или уведомлений, и, наконец, мы импортируем validate_email и EmailNotValidError из email_validator. Согласно документации email-validator, в ней говорится, что библиотека проверяет, что строка имеет вид name@example.com.

В функции index() мы проверяем, является ли отправленный запрос POST. Если это так, то мы получаем электронное письмо из данных формы с помощью запроса. POST.get('email-address'), адрес электронной почты - это имя, указанное для ввода электронной почты в форме.

После помещения электронной почты в контекст у нас есть блок try/except, в операторе try мы проверяем адрес электронной почты с помощью функции validate_email(), после успешной проверки создаем сообщение об успешном завершении и вызываем функцию render(). В блоке except мы просто ловим EmailNotValidError, мы также создаем сообщение, но на этот раз оно имеет предупреждение типа, и мы снова вызываем функцию render().

До или после запроса POST мы по-прежнему хотим отобразить форму, чтобы функция render() после блока try/except сделала это за нас.

Давайте попробуем приложение, предоставим действительный адрес электронной почты и проверим его, нажав кнопку проверки; Выходные данные, которые вы получите, будут следующими:



На этот раз попробуйте ввести любой недопустимый адрес электронной почты, который не имеет символа @; Результат будет следующим:



Введите адрес электронной почты еще раз с недопустимыми символами, например, адрес электронной почты этой формы first..last@example.com; Вот выходные данные, которые будет выдавать приложение:



Наконец, введите адрес электронной почты с неполным доменным именем, например, name@example; Вот выходные данные, которые вы получите:



Если вы заметили, все оповещения имеют кнопку закрытия. Нажатие этой кнопки приводит к исчезновению оповещений; это возможно благодаря JavaScript, который мы включили в шаблон base.html и в шаблон index.html у нас есть операторы if чуть ниже формы для фильтрации оповещений. Каждое оповещение имеет значок; для иконок мы используем теги svg.

Примечание: Приложение может поймать много ошибок; эта статья не исчерпала их всех, но вы можете попробовать самостоятельно разобраться, что это такое.

Заключение
Вот и все из этой статьи; мы надеемся, что вы многому научились и что полученные знания будут применены в ваших будущих проектах Django. В этой статье вы узнаете о процессе создания веб-верификатора адресов электронной почты с использованием платформы Django и пакета email-validator. Это может быть полезным инструментом в бизнесе для предотвращения злоупотребления адресами электронной почты и обеспечения использования только действительных адресов электронной почты.

Вы можете получить файлы проекта здесь.

Вот некоторые другие учебники Django:

Как создать блог с помощью Django в Python
Как создать приложение Todo с помощью Django в Python
Как построить систему аутентификации в Django
Как создать приложение погоды с помощью Django в Python
Как создать приложение CRUD с помощью Django в Python
Как создать приложение словаря английского языка с помощью Django на Python