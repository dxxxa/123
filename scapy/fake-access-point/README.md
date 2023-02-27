# [Fake Access Point Generator](https://www.thepythoncode.com/article/create-fake-access-points-scapy)
to run this:
- Linux Machine.
- USB WLAN Stick.
- aircrack-ng.
- Turn the network interface to Monitor mode using the command:
    ```
    airmon-ng start wlan0
    ```
- `pip3 install -r requirements.txt`.
- 
    ```
    python3 fake_access_point.py --help
    ```
    **Output**:
    ```
    usage: fake_access_point.py [-h] [-n N_AP] interface

    Fake Access Point Generator

    positional arguments:
    interface             The interface to send beacon frames with, must be in
                            monitor mode

    optional arguments:
    -h, --help            show this help message and exit
    -n N_AP, --access-points N_AP
                            Number of access points to be generated
    ```
##
# [[] / []]()
Вы когда-нибудь задумывались, как ваш ноутбук или мобильный телефон узнает, какие беспроводные сети доступны поблизости? На самом деле это просто. Беспроводные точки доступа постоянно отправляют кадры маяков на все близлежащие беспроводные устройства; эти кадры содержат информацию о точке доступа, такую как SSID (имя), тип шифрования, MAC-адрес и т. Д.

В этом уроке вы узнаете, как отправлять кадры маяков в воздух, используя библиотеку Scapy на Python, чтобы успешно создавать поддельные точки доступа!

Необходимые пакеты для установки для этого учебника:

$ pip3 install faker scapy
Чтобы убедиться, что Scapy установлен правильно, перейдите к этому руководству или проверьте официальную документацию scapy для полной установки для всех сред.

Настоятельно рекомендуется следовать вместе со средой Kali Linux, так как она предоставляет предустановленные утилиты, необходимые в этом учебнике.

Прежде чем мы углубимся в захватывающий код, вам нужно включить режим монитора в вашей сетевой интерфейсной карте:

Вы должны убедиться, что вы находитесь в системе на базе Unix.
Установите утилиту aircrack-ng:
$ apt-get install aircrack-ng
Заметка: Утилита aircrack-ng поставляется с предустановленной Kali Linux, поэтому вы не должны выполнять эту команду, если вы находитесь на Kali.

Включите режим монитора с помощью команды airmon-ng:
root@rockikz:~# airmon-ng check kill

Killing these processes:

  PID Name
  735 wpa_supplicant
root@rockikz:~# airmon-ng start wlan0

PHY    Interface    Driver     Chipset

phy0   wlan0        ath9k_htc  Atheros Communications, Inc. TP-Link TL-WN821N v3 / TL-WN822N v2 802.11n [Atheros AR7010+AR9287]

               (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
               (mac80211 station mode vif disabled for [phy0]wlan0)
Примечание: Мой USB WLAN-накопитель называется wlan0 в моем случае, вы должны выполнить команду ifconfig и увидеть правильное имя сетевого интерфейса.

Хорошо, теперь у вас все готово, давайте начнем с простого рецепта:

from scapy.all import *

# interface to use to send beacon frames, must be in monitor mode
iface = "wlan0mon"
# generate a random MAC address (built-in in scapy)
sender_mac = RandMAC()
# SSID (name of access point)
ssid = "Test"
# 802.11 frame
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)
# beacon layer
beacon = Dot11Beacon()
# putting ssid in the frame
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
# stack all the layers and add a RadioTap
frame = RadioTap()/dot11/beacon/essid
# send the frame in layer 2 every 100 milliseconds forever
# using the `iface` interface
sendp(frame, inter=0.1, iface=iface, loop=1)
Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Приведенный выше код выполняет следующие действия:

Мы генерируем случайный MAC-адрес, устанавливаем имя точки доступа, которую мы хотим создать, а затем создаем кадр 802.11. Поля:

type=0: указывает, что это фрейм управления.
subtype=8: указывает, что этот кадр управления является кадром маяка.
addr1: относится к MAC-адресу назначения, другими словами, MAC-адресу получателя. Здесь мы используем адрес трансляции ("ff:ff:ff:ff:ff:ff:ff"). Если вы хотите, чтобы эта поддельная точка доступа отображалась только на целевом устройстве, вы можете использовать MAC-адрес цели.
addr2: исходный MAC-адрес, MAC-адрес отправителя.
addr3: MAC-адрес точки доступа.
Связанные с: Как сделать изменение MAC-адреса в Python

Поэтому мы должны использовать один и тот же MAC-адрес addr2 и addr3, потому что отправитель является точкой доступа!

Мы создаем нашу рамку маяка с SSID Infos, затем складываем их все вместе и отправляем их с помощью функции sendp() Scapy.

После того, как мы настроим наш интерфейс в режим монитора и выполним скрипт, мы должны увидеть что-то подобное в списке доступных точек доступа Wi-Fi:

Поддельная точка доступа

Теперь давайте станем немного более причудливыми и создадим много поддельных точек доступа одновременно:

from scapy.all import *
from threading import Thread
from faker import Faker

def send_beacon(ssid, mac, infinite=True):
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    # ESS+privacy to appear as secured on some devices
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap()/dot11/beacon/essid
    sendp(frame, inter=0.1, loop=1, iface=iface, verbose=0)

if __name__ == "__main__":
    # number of access points
    n_ap = 5
    iface = "wlan0mon"
    # generate random SSIDs and MACs
    faker = Faker()
    ssids_macs = [ (faker.name(), faker.mac_address()) for i in range(n_ap) ]
    for ssid, mac in ssids_macs:
        Thread(target=send_beacon, args=(ssid, mac)).start()
Все, что я здесь сделал, это обернул предыдущие строки кода в функцию, сгенерировал случайные MAC-адреса и SSID с помощью пакета faker, а затем запустил отдельный поток для каждой точки доступа. Как только вы выполните скрипт, интерфейс будет отправлять пять маяков каждые 100 миллисекунд (по крайней мере, в теории). Это приведет к появлению пяти поддельных точек доступа. Взгляните:

Поддельные точки доступа

Вот как это выглядит на ОС Android:

Поддельные точки доступа

Если вы не знаете, как использовать потоки, ознакомьтесь с этим руководством.

Это удивительно. Обратите внимание, что подключение к одной из этих точек доступа не удастся, так как они не являются реальными точками доступа, а просто иллюзией!

Наконец, у нас есть электронная книга Ethical Hacking with Python, где мы создаем 24 хакерских инструмента и скрипта! Обязательно проверьте это, если вы заинтересованы.

СВЯЗАННЫЕ С: Как сделать DNS Spoof атаку с помощью Scapy в Python.