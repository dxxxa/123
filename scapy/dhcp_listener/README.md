# [How to Make a DHCP Listener using Scapy in Python](https://www.thepythoncode.com/article/dhcp-listener-using-scapy-in-python)
to run this:
- `pip3 install -r requirements.txt`
-   
    ```
    $ python3 dhcp_listener.py
    ```
##
# [[] / []]()
Протокол DHCP (Dynamic Host Configuration Protocol) — это сетевой протокол, который предоставляет клиентам, подключенным к сети, получение сведений о конфигурации TCP/IP (таких как частный IP-адрес) от DHCP-сервера.

DHCP-сервер (может быть точкой доступа, маршрутизатором или настроенным на сервере) динамически назначает IP-адрес и другие параметры конфигурации каждому устройству, подключенному к сети.

Протокол DHCP использует протокол UDP для выполнения обмена данными между сервером и клиентами. Он реализован с двумя номерами портов: UDP порт 67 для сервера и UDP порт 68 для клиента.

В этом уроке мы сделаем простой прослушиватель DHCP, используя библиотеку Scapy на Python. Другими словами, мы сможем прослушивать DHCP-пакеты в сети и извлекать ценную информацию всякий раз, когда устройство подключается к сети, в которой мы находимся.

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Чтобы начать, давайте установим Scapy:

$ pip install scapy
Если у вас возникли проблемы с установкой Scapy, я предлагаю вам следовать этому руководству, если вы находитесь в Ubuntu или другом подобном дистрибутиве или Windows 10 здесь.

Как вы, возможно, уже знаете, функция sniff() в Scapy отвечает за перехват любого типа пакетов, которые можно отслеживать. К счастью, чтобы удалить другие пакеты, которые нас не интересуют, мы просто используем параметр фильтра в функции sniff():

from scapy.all import *
import time


def listen_dhcp():
    # Make sure it is DHCP with the filter options
    sniff(prn=print_packet, filter='udp and (port 67 or port 68)')
В функции listen_dhcp() мы передаем функцию print_packet(), которую мы определим как обратный вызов, выполняемый всякий раз, когда пакет перехватывается и сопоставляется фильтром.

Мы сопоставляем UDP-пакеты с портом 67 или 68 в их атрибутах для фильтрации DHCP.

Определим функцию print_packet():

def print_packet(packet):
    # initialize these variables to None at first
    target_mac, requested_ip, hostname, vendor_id = [None] * 4
    # get the MAC address of the requester
    if packet.haslayer(Ether):
        target_mac = packet.getlayer(Ether).src
    # get the DHCP options
    dhcp_options = packet[DHCP].options
    for item in dhcp_options:
        try:
            label, value = item
        except ValueError:
            continue
        if label == 'requested_addr':
            # get the requested IP
            requested_ip = value
        elif label == 'hostname':
            # get the hostname of the device
            hostname = value.decode()
        elif label == 'vendor_class_id':
            # get the vendor ID
            vendor_id = value.decode()
    if target_mac and vendor_id and hostname and requested_ip:
        # if all variables are not None, print the device details
        time_now = time.strftime("[%Y-%m-%d - %H:%M:%S]")
        print(f"{time_now} : {target_mac}  -  {hostname} / {vendor_id} requested {requested_ip}")
Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Во-первых, мы извлекаем MAC-адрес из атрибута src уровня пакетов Ether.

Во-вторых, если в пакет включены параметры DHCP, мы перебираем их и извлекаем requested_addr (который является запрошенным IP-адресом), имя хоста (имя хоста запрашивающей стороны) и vendor_class_id (идентификатор клиента поставщика DHCP). После этого получаем текущее время и распечатываем детали. Начнем нюхать:

if __name__ == "__main__":
    listen_dhcp()
Перед запуском сценария убедитесь, что вы подключены к собственной сети в целях тестирования, а затем подключитесь к сети с помощью другого устройства и просмотрите выходные данные. Вот мой результат, когда я попытался подключиться к трем разным устройствам:

[2022-04-05 - 09:42:07] : d8:12:65:be:88:af  -  DESKTOP-PSU2DCJ / MSFT 5.0 requested 192.168.43.124
[2022-04-05 - 09:42:24] : 1c:b7:96:ab:ec:f0  -  HUAWEI_P30-9e8b07efe8a355 / HUAWEI:android:ELE requested 192.168.43.4        
[2022-04-05 - 09:58:29] : 48:13:7e:fe:a5:e3  -  android-a5c29949fa129cde / dhcpcd-5.5.6 requested 192.168.43.66
Заключение
Замечательно! Теперь у вас есть быстрый прослушиватель DHCP в Python, который вы можете расширить, я предлагаю вам распечатать переменную dhcp_options в функции print_packet(), чтобы увидеть, как выглядит этот объект.

Полный код можно найти здесь.

Наконец, у нас есть электронная книга Ethical Hacking with Python, где мы создаем 24 хакерских инструмента и скрипта с нуля с помощью Python! Обязательно проверьте это здесь, если вы заинтересованы.