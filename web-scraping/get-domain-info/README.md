# [How to Get Domain Name Information in Python](https://www.thepythoncode.com/article/extracting-domain-name-information-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Use `validate_domains.py` code to validate domains
- Use `get_domain_info.py` code to get various domain information from WHOIS
##
# [[] / []]()
Доменное имя — это строка, идентифицирующая сетевой домен; он представляет собой IP-ресурс, такой как сервер, на котором размещен веб-сайт, или просто компьютер, имеющий доступ к Интернету.

Проще говоря, то, что мы знаем как доменное имя, - это адрес вашего сайта, который люди вводят в URL-адрес браузера для посещения.

В этом руководстве мы будем использовать библиотеку whois в Python для проверки доменных имен и получения различной информации о домене, такой как дата создания и истечения срока действия, регистратор доменов, адрес и страна владельца и многое другое.

Если вы хотите извлечь информацию DNS о конкретном домене, то этот учебник для вас.

Чтобы начать работу, давайте установим библиотеку:

pip3 install python-whois
WHOIS — это протокол запросов и ответов, который часто используется для запросов баз данных, в которых хранятся зарегистрированные доменные имена. Он хранит и доставляет контент в удобочитаемом формате. Библиотека whois просто запрашивает сервер WHOIS напрямую, а не проходит через промежуточную веб-службу.

В Linux также есть простая команда whois для извлечения информации о домене, но поскольку мы разработчики Python, то мы будем использовать Python для этого.

Проверка доменных имен
В этом разделе мы будем использовать whois, чтобы определить, существует ли доменное имя и зарегистрировано ли оно, это делает следующая функция:

import whois # pip install python-whois

def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)
Функция whois.whois() вызывает исключение для доменов, которые не существуют и могут возвращаться без создания каких-либо исключений, даже если домен не зарегистрирован, поэтому мы проверяем, существует ли domain_name, давайте протестируем эту функцию:

# list of registered & non registered domains to test our function
domains = [
    "thepythoncode.com",
    "google.com",
    "github.com",
    "unknownrandomdomain.com",
    "notregistered.co"
]
# iterate over domains
for domain in domains:
    print(domain, "is registered" if is_registered(domain) else "is not registered")
Мы определили некоторые известные домены и другие, которые не существуют. Вот выходные данные:

thepythoncode.com is registered
google.com is registered
github.com is registered
unknownrandomdomain.com is not registered
notregistered.co is not registered
Удивительно, в следующем разделе мы увидим, как получить различную полезную информацию о доменных именах.

Получение информации о домене WHOIS
Использовать эту библиотеку довольно просто, мы просто передаем доменное имя функции whois.whois():

import whois

# test with Google domain name
domain_name = "google.com"
if is_registered(domain_name):
    whois_info = whois.whois(domain_name)
Теперь, чтобы получить регистратора доменов (компанию, которая управляет резервированием доменных имен), мы просто обратимся к регистратору атрибутов:

    # print the registrar
    print("Domain registrar:", whois_info.registrar)
Получение сервера WHOIS:

    # print the WHOIS server
    print("WHOIS server:", whois_info.whois_server)
Дата создания и истечения срока действия домена:

    # get the creation time
    print("Domain creation date:", whois_info.creation_date)
    # get expiration date
    print("Expiration date:", whois_info.expiration_date)
Выпуск:

Domain registrar: MarkMonitor Inc.
WHOIS server: whois.markmonitor.com        
Domain creation date: 1997-09-15 04:00:00  
Expiration date: 2028-09-14 04:00:00 
Чтобы увидеть другую различную информацию WHOIS, такую как серверы имен, страна, город, штат, адрес и т. Д., Просто распечатайте whois_info:

    # print all other info
    print(whois_info)
Заключение
Вот оно! Вы только что узнали самый простой и быстрый способ получить информацию о доменном имени в Python. Проверьте репозиторий python-whois Github.

Вам интересно узнать больше об этическом взломе и создании инструментов для защиты от киберугроз? Наша электронная книга «Этический взлом с Python» - идеальный ресурс для вас! Это всеобъемлющее руководство охватывает создание инструментов в различных разделах, включая сбор информации, вредоносные программы и манипуляции с сетевыми пакетами. Вы узнаете, как создавать такие инструменты, как обратная оболочка, инструменты для взлома паролей и многое другое (более 35 инструментов для пентестинга).

С пошаговыми инструкциями и четкими объяснениями, эта электронная книга идеально подходит как для начинающих, так и для опытных профессионалов, желающих расширить свои знания в области этического взлома с помощью Python. Не упустите возможность стать экспертом в области кибербезопасности – получите свою копию уже сегодня!

Узнайте также: Как создать сканер поддоменов в Python.