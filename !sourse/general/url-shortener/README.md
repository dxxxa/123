# [How to Make a URL Shortener in Python](https://www.thepythoncode.com/article/make-url-shortener-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Edit your account credentials for both `bitly_shortener.py` and `cuttly_shortener.py` and run the scripts along with URL you want to shorten, example:
    ```
    python bitly_shortener.py https://www.thepythoncode.com/article/make-url-shortener-in-python
    ```
##
# [[] / []]()
Сокращение URL-адресов - это инструмент, который берет длинный URL-адрес и превращает его в короткий, который перенаправляет на нужную страницу. Сокращения URL-адресов оказываются полезными во многих случаях, таких как отслеживание количества кликов или требование к пользователю вводить только небольшое количество символов, так как длинные URL-адреса трудно запомнить.

В этом уроке мы будем использовать API Bitly и Cuttly для автоматического сокращения URL-адресов в Python. Не стесняйтесь переходить к вашему любимому провайдеру:

Битовый API
Каттли API
В этом учебнике мы не будем использовать оболочки API. В результате нам понадобится библиотека запросов для удобства. Давайте установим его:

pip3 install requests
Битовый API
Bitly - это служба сокращения URL-адресов и платформа управления ссылками. Он позволяет отслеживать клики с различной информацией о кликах. Чтобы начать работу с Bitly API. Во-первых, вам нужно зарегистрировать новую учетную запись. Это бесплатно, и если у вас уже есть один, просто используйте его.

После создания учетной записи Bitly нам необходимо получить идентификатор учетной записи для доступа к API. Нажмите на свой профиль в правом верхнем углу и нажмите Настройки учетной записи:

Перейдите в Настройки учетной записи в Bitly

После этого возьмите имя учетной записи, которое нам понадобится в коде, как показано на следующем рисунке:

Получить битовое имя учетной записи

Хорошо, это все, что нам нужно; Начнем с кодирования:

import requests

# account credentials
username = "o_3v0ulxxxxx"
password = "your_password_here"
имя пользователя - это имя учетной записи, которое я только что показал вам, как его получить, пароль - это фактический пароль вашей учетной записи Bitly, поэтому вы должны заменить их своими учетными данными.

Если вы внимательно прочитаете документацию Bitly API, вы увидите, что нам нужен маркер доступа для выполнения вызовов API, чтобы получить сокращенный URL-адрес, поэтому давайте создадим новый маркер доступа:

# get the access token
auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
if auth_res.status_code == 200:
    # if response is OK, get the access token
    access_token = auth_res.content.decode()
    print("[!] Got access token:", access_token)
else:
    print("[!] Cannot get access token, exiting...")
    exit()
Мы использовали метод requests.post(), чтобы сделать POST-запрос к конечной точке /oauth/access_token и получить маркер доступа. Мы передали параметр auth, чтобы добавить учетные данные нашей учетной записи в заголовки запроса.

Теперь у нас есть токен доступа, прежде чем мы углубимся в сокращение URL-адресов, нам сначала нужно получить UID группы, связанный с нашей учетной записью Bitly:

# construct the request headers with authorization
headers = {"Authorization": f"Bearer {access_token}"}

# get the group UID associated with our account
groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
if groups_res.status_code == 200:
    # if response is OK, get the GUID
    groups_data = groups_res.json()['groups'][0]
    guid = groups_data['guid']
else:
    print("[!] Cannot get GUID, exiting...")
    exit()
Теперь, когда у нас есть guid, давайте сделаем наш запрос, чтобы сократить пример URL:

# the URL you want to shorten
url = "https://www.thepythoncode.com/topic/using-apis-in-python"
# make the POST request to get shortened URL for `url`
shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": url}, headers=headers)
if shorten_res.status_code == 200:
    # if response is OK, get the shortened URL
    link = shorten_res.json().get("link")
    print("Shortened URL:", link)
Мы отправляем запрос POST на конечную точку /v4/shorten, чтобы сократить наш URL-адрес, мы передали group_guid нашей учетной записи и URL-адрес, который мы хотим сократить в качестве тела запроса.

Мы использовали параметр json вместо данных в методе requests.post() для автоматического кодирования нашего словаря Python в формат JSON и отправки его с Content-Type как application/json, затем мы добавили заголовки, чтобы содержать маркер авторизации, который мы захватили ранее. Вот мой вывод:

Shortened URL: https://bit.ly/32dtJ00
Отлично, мы успешно сократили наш URL с Bitly! Вот их официальная документация.

Каттли API
Другой альтернативой является использование Cuttly API. Довольно легко создать новую учетную запись и использовать ее API. После того, как вы зарегистрировали учетную запись, перейдите в «Ваша учетная запись» и нажмите «Изменить учетную запись»:

Каттли Редактировать Аккаунт

После этого вы увидите данные своей учетной записи, перейдите и нажмите на ключ Change API, чтобы получить новый ключ API (чтобы мы могли делать запросы API):

Изменение ключа API в Cuttly

Чтобы сократить ваш URL-адрес с помощью Cuttly, это довольно просто:

import requests

api_key = "64d1303e4ba02f1ebba4699bc871413f0510a"
# the URL you want to shorten
url = "https://www.thepythoncode.com/topic/using-apis-in-python"
# preferred name in the URL
api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
# or
# api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}&name=some_unique_name"
# make the request
data = requests.get(api_url).json()["url"]
if data["status"] == 7:
    # OK, get shortened URL
    shortened_url = data["shortLink"]
    print("Shortened URL:", shortened_url)
else:
    print("[!] Error Shortening URL:", data)
Просто замените ключ API в api_key и URL-адрес, который вы хотите сократить, и вы готовы к работе. Вот мой вывод:

Shortened URL: https://cutt.ly/mpAOd1b
Обратите внимание, что вы можете указать уникальное имя, и результат будет примерно таким: https://cutt.ly/some_unique_name, вы можете сделать это, просто добавив параметр name в запрос GET в URL-адресе.

Узнайте больше о документации По Каттли.

Заключение
Отлично, теперь вы знаете, как сократить свои URL-адреса, используя как Bitly, так и Cuttly shorteners! Обратите внимание, что эти поставщики предоставляют больше конечных точек для кликов, статистики и многого другого. Вы должны проверить их документацию для получения более подробной информации.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!