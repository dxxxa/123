# [How to Build a WiFi Scanner in Python using Scapy](https://www.thepythoncode.com/article/building-wifi-scanner-in-python-scapy)
To run this:
- `pip3 install -r requirements.txt`
- Scan nearby networks using `wlan0mon` interface:
    ```
    python wifi_scanner.py wlan0mon
    ```
##
# [[] / []]()
Вы когда-нибудь хотели создать инструмент для отображения близлежащих беспроводных сетей вместе с их MAC-адресом и какой-либо другой полезной информацией? Ну, в этом уроке мы собираемся построить сканер Wi-Fi, используя библиотеку Scapy на Python.

Если вы находитесь в этой области некоторое время, вы, возможно, видели утилиту airodump-ng, которая нюхает, захватывает и декодирует кадры 802.11 для отображения близлежащих беспроводных сетей в хорошем формате, в этом уроке мы сделаем аналогичное.

Связанные с: Как извлечь сохраненные пароли WiFi в Python.

Начало работы
Чтобы начать, вам нужно установить Scapy, я клонировал версию разработки, вы также можете установить ее с помощью pip:

pip3 install scapy
Или вы можете клонировать текущую версию разработки в Github:

git clone https://github.com/secdev/scapy.git
cd scapy
sudo python setup.py install
Заметка: В этом учебнике предполагается, что вы используете любую среду на базе Unix, также предлагается использовать Kali Linux.

После этого мы будем использовать панд только для печати в хорошем формате (вы можете изменить это очевидно):

pip3 install pandas
Теперь код этого учебника не будет работать, если вы не включите режим монитора в своем сетевом интерфейсе, пожалуйста, установите aircrack-ng (поставляется предустановленным на Kali) и выполните следующую команду:

Включение режима монитора с помощью airmon-ng

Теперь вы можете проверить имя интерфейса с помощью iwconfig:

Проверка имени интерфейса с помощью iwconfig

Как видите, наш интерфейс теперь находится в режиме монитора и имеет название "wlan0mon".

Вы также можете использовать сам iwconfig для переключения сетевой карты в режим монитора:

sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
ПОЛУЧИТЕ СКИДКУ -10%: Создайте 24 этических хакерских скрипта и инструмента с помощью python EBook
Написание кода
Давайте начнем, откроем новый файл Python и импортируем необходимые модули:

from scapy.all import *
from threading import Thread
import pandas
import time
import os
Затем нам нужно инициализировать пустой фрейм данных, в котором хранятся наши сети:

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)
Поэтому я установил BSSID (MAC-адрес точки доступа) в качестве индекса каждой строки, так как он уникален для каждого устройства.

Если вы знакомы со Scapy, то вы точно знаете, что мы собираемся использовать функцию sniff(), которая принимает функцию обратного вызова, которая выполняется всякий раз, когда пакет перехватывается, давайте реализуем эту функцию:

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
Связанные с: Как сделать изменение MAC-адреса в Python

Этот обратный вызов гарантирует, что на взломанном пакете есть слой маяка, если это так, то он извлечет BSSID, SSID (имя точки доступа), сигнал и некоторую статистику. Класс Dot11Beacon от Scapy имеет удивительную функцию network_stats(), которая извлекает некоторую полезную информацию из сети, такую как канал, скорости и тип шифрования. Наконец, мы добавляем эту информацию в фрейм данных с BSSID в качестве индекса.

Вы столкнетесь с некоторыми сетями, которые не имеют SSID (ssid равен «»), это показатель того, что это скрытая сеть. В скрытых сетях точка доступа оставляет информационное поле пустым, чтобы скрыть обнаружение имени сети, вы все равно найдете их с помощью сценария этого учебника, но без имени сети.

Теперь нам нужен способ визуализации этого фрейма данных. Поскольку мы собираемся использовать функцию sniff() (которая блокирует и начинает нюхать в основном потоке), нам нужно использовать отдельный поток для печати содержимого сетевого фрейма данных, приведенный ниже код делает это:

def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)
К основному коду сейчас:

if __name__ == "__main__":
    # interface name, check using iwconfig
    interface = "wlan0mon"
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)
Узнайте также: Как сделать АТАКУ SYN Flooding в Python.

Смена каналов
Теперь, если вы выполните это, вы заметите, что не все близлежащие сети доступны. Это потому, что мы слушаем только на одном канале WLAN. Мы можем использовать команду iwconfig для изменения канала. Вот функция Python для него:

def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)
Например, если вы хотите перейти на канал 2, команда будет следующей:

iwconfig wlan0mon channel 2
Отлично, так что это будет менять каналы постепенно от 1 до 14 каждые 0,5 секунды, порождая поток демона, который запускает эту функцию:

    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
Заметка: Каналы 12 и 13 разрешены в режиме низкого энергопотребления, в то время как канал 14 запрещен и разрешен только в Японии.

Обратите внимание, что мы устанавливаем для атрибута daemon потока значение True, поэтому этот поток будет завершаться всякий раз, когда программа завершает работу. Дополнительные сведения о потоках демонов см. в этом учебнике.

Проверьте полный код здесь.

Вот скриншот моего исполнения:

Пример выполнения сканера Wi-Fi с помощью Scapy в Python

 
Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python EBook
Заключение
Хорошо, в этом уроке мы написали простой сканер Wi-Fi с использованием библиотеки Scapy, который обнюхивает и декодирует кадры маяков, которые каждый раз передаются точками доступа. Они служат для объявления о наличии беспроводной сети.

Наконец, у нас есть электронная книга Ethical Hacking with Python, где мы создаем более 20 скриптов хакерских инструментов с нуля с использованием Python. Обязательно проверьте это, если вы заинтересованы!