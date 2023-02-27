# [Simple Network Scanner](https://www.thepythoncode.com/article/building-network-scanner-using-scapy)
to run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python3 network_scanner.py
    ```
##
# [[] / []]()
Сетевой сканер является важным элементом как для сетевого администратора, так и для тестера проникновения. Это позволяет пользователю сопоставить сеть, чтобы найти устройства, подключенные к той же сети.

Из этого туториала Вы узнаете, как построить простой сетевой сканер с помощью библиотеки Scapy на Python.

СВЯЗАННЫЕ С: Как извлечь сохраненные пароли WiFi в Python.

Я предполагаю, что у вас уже установлен он, если это не так, не стесняйтесь проверять эти учебники:

Как установить Scapy на Windows
Как установить Scapy на Ubuntu
Вы также можете обратиться к официальной документации Scapy.

Возвращаясь к сути, есть много способов сканирования компьютеров в одной сети, но мы собираемся использовать один из популярных способов, который использует ARP-запросы.

Во-первых, нам нужно будет импортировать основные методы из scapy:

from scapy.all import ARP, Ether, srp
Во-вторых, нам нужно будет сделать ARP-запрос, как показано на следующем рисунке:

Запрос ARP

Сетевой сканер отправит ARP-запрос, указывающий, у кого есть какой-то конкретный IP-адрес, скажем, «192.168.1.1», владелец этого IP-адреса (цель) автоматически ответит, сказав, что он «192.168.1.1», с этим ответом MAC-адрес также будет включен в пакет, это позволяет нам успешно извлекать IP- и MAC-адреса всех пользователей сети одновременно, когда мы отправляем широковещательный пакет (отправка пакета на все устройства в сети).

Обратите внимание, что вы можете изменить MAC-адрес вашего компьютера, поэтому имейте это в виду при получении MAC-адресов, так как они могут меняться от одного раза к другому, если вы находитесь в общедоступной сети.

Ответ ARP показан на следующем рисунке:

Ответ ARP

Итак, давайте создадим эти пакеты:

target_ip = "192.168.1.1/24"
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp
ПОЛУЧИТЕ СКИДКУ -10%: Создайте 24 этических хакерских скрипта и инструмента с помощью python EBook

Примечание: Если вы не знакомы с обозначением «/24» или «/16» после IP-адреса, это в основном диапазон IP-адресов здесь, например, «192.168.1.1/24» - это диапазон от «192.168.1.0» до «192.168.1.255», пожалуйста, прочитайте больше о CIDR Notation.

Теперь мы создали эти пакеты, нам нужно отправить их с помощью функции srp(), которая отправляет и принимает пакеты на уровне 2, мы устанавливаем тайм-аут 3, чтобы скрипт не застрял:

result = srp(packet, timeout=3)[0]
результат теперь список пар, который имеет формат (sent_packet, received_packet), давайте переберем их:

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
Теперь все, что нам нужно сделать, это распечатать этот список, который мы только что заполнили:

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
Полный код:

from scapy.all import ARP, Ether, srp

target_ip = "192.168.1.1/24"
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
Получить сейчас: Этический взлом с помощью электронной книги Python

Вот скриншот моего результата в моей личной сети:

Скриншот результата

Хорошо, мы закончили с этим учебником. Посмотрите, как вы можете расширить это и сделать его более удобным для замены других инструментов сканирования.

Если вы хотите сканировать близлежащие сети, ознакомьтесь с этим туториалом.

И помните, не копируйте и не вставляйте. Напишите его самостоятельно, чтобы правильно понять!

Наконец, у нас есть Ethical Hacking with Python EBook, где мы создаем более 35 хакерских инструментов и скриптов с нуля с использованием Python. Проверьте это здесь, если вам интересно!