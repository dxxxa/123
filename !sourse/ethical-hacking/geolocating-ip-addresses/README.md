# [How to Geolocate IP addresses in Python](https://www.thepythoncode.com/article/geolocate-ip-addresses-with-ipinfo-in-python)
##
# [[] / []]()
IP-геолокация для сбора информации является очень распространенной задачей в информационной безопасности. Он используется для сбора информации о пользователе, обращающемся к системе, такой как страна, город, адрес и, возможно, даже широта и долгота.

В этом уроке мы собираемся выполнить IP-геолокацию с помощью Python. Существует множество способов выполнения такой задачи, но наиболее распространенным является использование сервиса IPinfo.

Если вы хотите следить за этим, вы должны пойти дальше и зарегистрировать учетную запись на IPinfo. Стоит отметить, что бесплатная версия сервиса ограничена 50 000 запросов в месяц, так что этого нам более чем достаточно. После регистрации вы переходите на панель мониторинга и получаете маркер доступа.

Чтобы использовать ipinfo.io в Python, нам нужно сначала установить его оболочку:

$ pip install ipinfo
Откройте новый файл Python с именем get_ip_info.py и добавьте следующий код:

import ipinfo
import sys
# get the ip address from the command line
try:
    ip_address = sys.argv[1]
except IndexError:
    ip_address = None
# access token for ipinfo.io
access_token = '<put_your_access_token_here>'
# create a client object with the access token
handler = ipinfo.getHandler(access_token)
# get the ip info
details = handler.getDetails(ip_address)
# print the ip info
for key, value in details.all.items():
    print(f"{key}: {value}")
Довольно просто, мы создаем обработчик с маркером доступа, а затем используем метод getDetails() для получения местоположения IP-адреса. Убедитесь, что вы заменили access_token маркером доступа, найденным на панели мониторинга. Вы можете нажать «Копировать в буфер обмена», чтобы скопировать маркер доступа:

Копирование маркера доступа на панели мониторинга IPinfo

Давайте запустим его на примере:

$ python get_ip_info.py 142.93.95.0 
ip: 142.93.95.0
city: Santa Clara
region: California
country: US
loc: 37.3483,-121.9844
org: AS14061 DigitalOcean, LLC
postal: 95051
timezone: America/Los_Angeles
country_name: United States
latitude: 37.3483
longitude: -121.9844
Если вы не передаете ip-адрес, сценарий будет использовать IP-адрес компьютера, на котором он запущен. Это полезно, если требуется запустить сценарий с удаленного компьютера.