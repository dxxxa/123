# [How to Get Geographic Locations in Python](https://www.thepythoncode.com/article/get-geolocation-in-python)
##
# [[] / []]()
Геокодирование — это процесс преобразования описания местоположения (например, физического адреса или названия места) в пару широты и долготы на поверхности Земли для этого места.

Это также относится к преобразованию географических координат в описание местоположения (например, адрес); это часто называют обратным геокодированием. В этом уроке мы узнаем, как сделать и то, и другое с помощью библиотеки GeoPy на Python.

Однако, если вы хотите геолоцировать IP-адреса, то этот учебник для вас.

GeoPy - это клиент Python, который предоставляет несколько популярных веб-сервисов геокодирования; это позволяет разработчикам Python легко находить координаты адреса, города или страны, и наоборот.

Чтобы начать работу, давайте установим его:

pip3 install geopy
GeoPy предоставляет множество оболочек сервиса геокодирования, таких как OpenStreetMap Nominatim, Google Geocoding API V3, Bing Maps и многое другое. В этом уроке мы будем придерживаться OpenStreetMap Nominatim.

Вот что мы рассмотрим:

Получение широты и долготы по адресу (геокодирование)
Получение адреса из широты и долготы (обратное геокодирование)
Получение широты и долготы по адресу (геокодирование)
В этом разделе мы будем использовать OpenStreetMap Nominatim API для получения широты и долготы по физическому адресу, городу или любому названию местоположения.

Давайте сначала импортируем библиотеку:

from geopy.geocoders import Nominatim
import time
from pprint import pprint
Обратите внимание, что мы выбрали геокодер Nominatim, теперь создавая его новый экземпляр:

# instantiate a new Nominatim client
app = Nominatim(user_agent="tutorial")
Теперь попробуем получить географические данные по адресу:

# get location raw data
location = app.geocode("Nairobi, Kenya").raw
# print raw data
pprint(location)
Выпуск:

{'boundingbox': ['-1.444471', '-1.163332', '36.6509378', '37.1038871'],
 'class': 'place',
 'display_name': 'Nairobi, Kenya',
 'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
 'importance': 0.845026759433763,
 'lat': '-1.2832533',
 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
            'https://osm.org/copyright',
 'lon': '36.8172449',
 'osm_id': 9185096,
 'osm_type': 'relation',
 'place_id': 273942566,
 'type': 'city'}
Удивительно, у нас есть атрибут широта в lat (в котором мы можем получить доступ по местоположению['lat']) и долгота в атрибуте lon, у нас также есть доступ к ограничительной рамке адреса в атрибуте boundingbox.

Как видите, API Nominatim не требует полного адреса (который состоит из улицы, номера дома и города), вы также можете передавать бизнес-адреса и точки ваших интересов, он поддерживает это!

Однако, если вы вызываете эту функцию неоднократно (например, перебираете список адресов), вы столкнетесь с ошибкой тайм-аута, и это потому, что если вы читаете политику использования Nominatim, она требует, чтобы вы использовали максимум 1 запрос в секунду, и это абсолютно приемлемо, поскольку это бесплатная служба.

В результате следующая функция соблюдает это требование и спит в течение одной секунды, прежде чем сделать запрос:

def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)
Поэтому всякий раз, когда возникает ошибка тайм-аута, мы перехватываем ее и вызываем функцию рекурсивно, и эта функция будет спать еще секунду и, надеюсь, извлекает результат:

address = "Makai Road, Masaki, Dar es Salaam, Tanzania"
location = get_location_by_address(address)
latitude = location["lat"]
longitude = location["lon"]
print(f"{latitude}, {longitude}")
# print all returned data
pprint(location)
Выпуск:

-6.7460493, 39.2750804
{'boundingbox': ['-6.7467061', '-6.7454602', '39.2741806', '39.2760514'],
 'class': 'highway',
 'display_name': 'Makai Road, Masaki, Msasani, Dar es-Salaam, Dar es Salaam, '
                 'Coastal Zone, 2585, Tanzania',
 'importance': 0.82,
 'lat': '-6.7460493',
 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
            'https://osm.org/copyright',
 'lon': '39.2750804',
 'osm_id': 23347726,
 'osm_type': 'way',
 'place_id': 89652779,
 'type': 'residential'}
Получение адреса из широты и долготы (обратное геокодирование)
Теперь, чтобы получить адрес, город, страну и другую информацию, только из широты и долготы, мы просто используем метод reverse() вместо geocode(),который принимает координаты (широту и долготу) в виде строки, разделенной запятой.

Следующая функция меняет координаты наряду с политикой использования Nominatim:

def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)
Таким образом, эта функция ожидает широту и долготу в качестве параметров и возвращает необработанные географические данные, вот пример использования:

# define your coordinates
latitude = 36.723
longitude = 3.188
# get the address info
address = get_address_by_location(latitude, longitude)
# print all returned data
pprint(address)
Выпуск:

{'address': {'country': 'Algeria',
             'country_code': 'dz',
             'county': 'Dar El Beida District',
             'postcode': '16110',
             'state': 'Algiers',
             'town': 'Bab Ezzouar'},
 'boundingbox': ['36.7231765', '36.7242661', '3.1866439', '3.1903998'],
 'display_name': 'Bab Ezzouar, Dar El Beida District, Algiers, 16110, Algeria',
 'lat': '36.72380363740118',
 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
            'https://osm.org/copyright',
 'lon': '3.188236679492425',
 'osm_id': 42812185,
 'osm_type': 'way',
 'place_id': 98075368}
Таким образом, это вернет все адресные данные, включая штат, город, почтовый индекс, районы и многое другое. Если вы хотите вернуть эту информацию на определенном языке, вы можете задать для параметра language нужный язык или установить для него значение False для языка по умолчанию для этого конкретного местоположения.

Заключение
Как всегда, мы видели только простые примеры того, что может сделать GeoPy, я настоятельно рекомендую вам прочитать документацию, если вы заинтересованы в более продвинутых утилитах.