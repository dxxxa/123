# [How to Automate your VPS or Dedicated Server Management in Python](https://www.thepythoncode.com/article/automate-veesp-server-management-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Edit `automate.py` and run the code line by line.
- This tutorial introduces you to web APIs, feel free to make your own scripts of your own needs.
##
# [[] / []]()
Веб-API - это интерфейсы прикладного программирования через Интернет, к которым можно получить доступ с помощью протокола HTTP. Хостинг-провайдеры серверов, такие как Veesp, предоставляют программный доступ для получения и публикации данных для управления нашими серверами и услугами, которые они предоставляют.

В этом уроке вы узнаете, как автоматизировать задачи Veesp VPS в Python с помощью библиотеки запросов, хорошо, давайте начнем.

Во-первых, давайте установим библиотеку запросов:

pip3 install requests
После того, как вы создадите свою собственную учетную запись, вы можете заказать дешевый VPS с некоторыми долларами, вот список доступных услуг:

Доступные услуги Veesp

Я выбрал Linux SSD VPS здесь, не стесняйтесь выбирать любой, который вам нравится, и я использовал опцию песочницы в следующем списке:

Veesp Linux SSD VPSПосле оплаты и правильной активации вашего VPS вы можете следить за этим, открыть новый файл Python или интерактивную оболочку (предпочтительно) и следовать дальше:

import requests
from pprint import pprint
Я использую pprint только для красивой печати результатов API.

Определите кортеж, содержащий реальные учетные данные для проверки подлинности в учетной записи Veesp:

# email and password
auth = ("email@example.com", "ffffffff")
Вам нужно будет передать этот кортеж аутентификации в каждый вызов API, который вы делаете.

Давайте начнем с получения данных об учетной записи:

# get the HTTP Response
res = requests.get("https://secure.veesp.com/api/details", auth=auth)

# get the account details
account_details = res.json()

pprint(account_details)
Функция requests.get() отправляет HTTP GET запрос на этот URL с вашей аутентификацией, here - мой результат (со скрытой конфиденциальной информацией, конечно):

{'client': {'address1': '',
            'city': '',
            'companyname': '',
            'country': 'US',
            'email': 'email@example.com',
            'firstname': 'John Doe',
            'host': '0.0.0.0',
            'id': '29401',
            'ip': '0.0.0.0',
            'lastlogin': '2019-11-06 11:18:04',
            'lastname': '',
            'newsletter': [''],
            'phonenumber': '',
            'postcode': '',
            'privacypolicy': [''],
            'state': ''}}
Давайте посмотрим на наш сервис, который мы только что купили:

# get the bought services
services = requests.get('https://secure.veesp.com/api/service', auth=auth).json()
pprint(services)
Это приведет к следующему:

{'services': [{'id': '32723',
   'domain': 'test',
   'total': '4.000',
   'status': 'Active',
   'billingcycle': 'Monthly',
   'next_due': '2019-12-06',
   'category': 'Linux SSD VPS',
   'category_url': 'vps',
   'name': 'SSD Sandbox'}]}
Потрясающе, так что это ежемесячный Linux SSD VPS с общей стоимостью 4$.

Вы также можете просмотреть параметры обновления виртуальной машины и автоматически сделать запрос на обновление, всегда обращаясь к их официальной документации для получения дополнительной информации.

Давайте перечислим все виртуальные машины, которыми мы владеем:

# list all bought VMs
all_vms = requests.get("https://secure.veesp.com/api/service/32723/vms", auth=auth).json()
pprint(all_vms)
32723 - это мой идентификатор службы, как показано выше, поэтому вы должны отредактировать его с помощью своего собственного идентификатора.

Это выведет что-то вроде этого:

{'vms': {'18867': {'bandwidth': 100,
                   'burstmem': -512,
                   'cpus': '1',
                   'disk': 10,
                   'id': '18867',
                   'ip': ['hiddenip', ' 2a00:1838:37:3bd::ae42'],
                   'ipv6subnets': ['2a00:1838:37:3bd::/64'],
                   'label': 'test',
                   'memory': 512,
                   'pae': 0,
                   'password': 'hiddenpassword',
                   'pxe': 0,
                   'state': 'online',
                   'template': 'linux-debian-10-x86_64-min-gen2-v1',
                   'template_label': 'Debian Buster 10 64 bit',
                   'usage': {'bandwidth': {'free': 100,
                                           'percent': '0',
                                           'total': 100,
                                           'used': 0},
                             'disk': {'free': 10,
                                      'percent': '0',
                                      'total': 10,
                                      'used': 0},
                             'memory': {'free': 0,
                                        'percent': '0',
                                        'total': 0,
                                        'used': 0}}}}}
I've hid the real IP address and password of my VPS, but you can see I chose a linux debian distro with 10GB SSD disk, 512GB of memory and 1CPU, etc.

Now let's stop the VPS:

# stop a VM automatically
stopped = requests.post("https://secure.veesp.com/api/service/32723/vms/18867/stop", auth=auth).json()
print(stopped)
18867 is my VM ID, you should use your own ID of course.

Note that I'm using requests.post() function here instead, this function sends HTTP POST request to that URL.

The above code outputs:

{'status': True}
Great, that means it successfully stopped the VPS, let's see it in the Veesp dashboard:

Offline VPS

Let's start it again:

# start it again
started = requests.post("https://secure.veesp.com/api/service/32723/vms/18867/start", auth=auth).json()
print(started)
Выпуск:

{'status': True}
Это круто, теперь вы можете использовать SSH-доступ к нему, так как он онлайн, как показано на панели инструментов:

Онлайн VPS

В заключение, вы можете сделать много интересных вещей с этим API, а не только те, которые видны в этом учебнике, проверьте их официальный веб-сайт и документацию по API для получения дополнительных функций. Я надеюсь, что этот учебник поможет вам узнать о веб-API и их преимуществах автоматизации различных задач, а не только VPS и выделенных серверов.