# [Making a Port Scanner using sockets in Python](https://www.thepythoncode.com/article/make-port-scanner-python)
To run simple port scanner:   
```
python simple_port_scanner.py
```
To run fast port scanner:
```
python fast_port_scanner --help
```
**Output:**
```
usage: fast_port_scanner.py [-h] [--ports PORT_RANGE] host

Simple port scanner

positional arguments:
host                  Host to scan.

optional arguments:
-h, --help            show this help message and exit
--ports PORT_RANGE, -p PORT_RANGE
                        Port range to scan, default is 1-65535 (all ports)
```
For example, if you want to scan the ports from 1 to 1024 of your router (**192.168.1.1**):
```
python3 fast_port_scanner.py 192.168.1.1 --ports 1-1024
```
##
# [[] / []]()
Сканирование портов — это метод сканирования для определения того, какие порты на сетевом устройстве открыты, будь то сервер, маршрутизатор или обычная машина. Сканер портов — это просто сценарий или программа, которая предназначена для проверки хоста на наличие открытых портов.

В этом учебнике вы сможете создать свой собственный сканер портов на Python, используя библиотеку сокетов. Основная идея этого простого сканера портов заключается в попытке подключения к определенному хосту (веб-сайту, серверу или любому устройству, подключенному к Интернету / сети) через список портов. Если соединение установлено успешно, это означает, что порт открыт.

Например, когда вы загрузили эту веб-страницу, вы установили соединение с этим веб-сайтом через порт 80. Аналогично, этот сценарий будет пытаться подключиться к хосту, но на нескольких портах. Эти виды инструментов полезны для хакеров и тестеров на проникновение, поэтому не используйте этот инструмент на хосте, на тестирование которого у вас нет разрешения!

Содержание:

Простой сканер портов
Быстрый (резьбовой) сканер портов
Заключение
GET: Создайте 24 этических хакерских скрипта и инструмента с помощью электронной книги Python

Опционально необходимо установить модуль colorama для печати в цветах:

pip3 install colorama
Простой сканер портов
Во-первых, давайте начнем с создания простого сканера портов. Давайте импортируем модуль сокета:

import socket # for connecting
from colorama import init, Fore

# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
Примечание: модуль сокета уже установлен на вашей машине, это встроенный модуль в стандартной библиотеке Python, поэтому вам не нужно ничего устанавливать.

Модуль сокета предоставляет нам операции с сокетами, функции для задач, связанных с сетью, и т. Д. Они широко используются в интернете, так как стоят за любым подключением к любой сети. Любое сетевое взаимодействие проходит через сокет. Более подробная информация приведена в официальной документации по Python.

Мы будем использовать здесь colorama только для печати зелеными цветами всякий раз, когда порт открыт, и серым, когда он закрыт.

Определим функцию, которая отвечает за определение того, открыт ли порт:

def is_port_open(host, port):
    """
    determine whether `host` has the `port` open
    """
    # creates a new socket
    s = socket.socket()
    try:
        # tries to connect to host using that port
        s.connect((host, port))
        # make timeout if you want it a little faster ( less accuracy )
        # s.settimeout(0.2)
    except:
        # cannot connect, port is closed
        # return false
        return False
    else:
        # the connection was established, port is open!
        return True
Функция s.connect((host, port)) пытается подключить сокет к удаленному адресу с помощью кортежа (host, port), она вызовет исключение, когда не сможет подключиться к этому хосту, поэтому мы обернули эту строку кода в блок try-except, поэтому всякий раз, когда возникает исключение, это указывает на то, что порт фактически закрыт, в противном случае он открыт.

Теперь давайте воспользуемся приведенной выше функцией и проведем итерацию по диапазону портов:

# get the host from the user
host = input("Enter the host:")
# iterate over ports, from 1 to 1024
for port in range(1, 1025):
    if is_port_open(host, port):
        print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
    else:
        print(f"{GRAY}[!] {host}:{port} is closed    {RESET}", end="\r")
Приведенный выше код будет сканировать порты в диапазоне от 1 до 1024, вы можете изменить диапазон на 65535, если хотите, но это займет больше времени.

Когда вы попытаетесь запустить его, вы сразу заметите, что скрипт довольно медленный. Ну, нам это сойдет с рук, если мы установим тайм-аут в 200 миллисекунд или около того (используя метод settimeout(0.2)). Тем не менее, это на самом деле может снизить точность разведки, особенно когда ваша задержка довольно высока. В результате нам нужен лучший способ ускорить это.

Читайте также: Как использовать Shodan API в Python.

Быстрый (резьбовой) сканер портов
Теперь давайте выведем наш простой сканер портов на более высокий уровень. В этом разделе мы напишем многопоточный сканер портов, который может сканировать 200 или более портов одновременно.

Приведенный ниже код на самом деле является той же функцией, которую мы видели ранее, которая отвечает за сканирование одного порта. Поскольку мы используем потоки, нам нужно использовать блокировку, чтобы только одна нить могла печатать одновременно. В противном случае вывод будет испорчен, и мы не будем читать ничего полезного:

import argparse
import socket # for connecting
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

# number of threads, feel free to tune this parameter as you wish
N_THREADS = 200
# thread queue
q = Queue()
print_lock = Lock()

def port_scan(port):
    """
    Scan a port on the global variable `host`
    """
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()
Так что на этот раз функция ничего не возвращает; мы просто хотим распечатать, открыт ли порт (не стесняйтесь изменять его, хотя).

Мы использовали класс Queue() из встроенного модуля очереди, который поможет нам с использованием портов, две следующие функции предназначены для создания и заполнения очереди номерами портов и использования потоков для их использования:

def scan_thread():
    global q
    while True:
        # get the port number from the queue
        worker = q.get()
        # scan that port number
        port_scan(worker)
        # tells the queue that the scanning for that port 
        # is done
        q.task_done()


def main(host, ports):
    global q
    for t in range(N_THREADS):
        # for each thread, start it
        t = Thread(target=scan_thread)
        # when we set daemon to true, that thread will end when the main thread ends
        t.daemon = True
        # start the daemon thread
        t.start()
    for worker in ports:
        # for each port, put that port into the queue
        # to start scanning
        q.put(worker)
    # wait the threads ( port scanners ) to finish
    q.join()
Связанные с: Этический взлом с python EBook

Задача функции scan_thread() состоит в том, чтобы получить номера портов из очереди и отсканировать ее, а затем добавить к выполненным задачам, тогда как функция main() отвечает за заполнение очереди номерами портов и порождение N_THREADS потоков для их использования.

Обратите внимание, что q.get() будет блокироваться до тех пор, пока в очереди не будет доступен один элемент. q.put() помещает один элемент в очередь, а q.join() ожидает завершения всех потоков демона (очистка очереди).

Наконец, давайте сделаем простой парсер аргументов, чтобы мы могли передать диапазон номеров хоста и портов из командной строки:

if __name__ == "__main__":
    # parse some parameters passed
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]

    main(host, ports)
Вот скриншот того, когда я пытался сканировать свой домашний маршрутизатор:Сканер быстрых портов с использованием Python

Заключение
Замечательно! Он завершил сканирование 5000 портов менее чем за 2 секунды! Вы можете использовать диапазон по умолчанию (от 1 до 65535), который займет несколько секунд.

Если вы видите, что сканер зависает на одном порту, это признак того, что вам нужно уменьшить количество потоков. Если сервер, который вы исследуете, имеет высокий пинг, вы должны уменьшить N_THREADS до 100, 50 или даже ниже, попробуйте поэкспериментировать с этим параметром.

Сканирование портов оказывается полезным во многих случаях. Авторизованный тестер проникновения может использовать этот инструмент, чтобы увидеть, какие порты открыты, и выявить наличие потенциальных устройств безопасности, таких как брандмауэры, а также проверить сетевую безопасность и прочность устройства.

Это также популярный инструмент разведки для хакеров, которые ищут слабые места, чтобы получить доступ к целевой машине.

Большинство тестеров проникновения часто используют Nmap для сканирования портов, так как он не просто обеспечивает сканирование портов, но показывает запущенные службы и операционные системы, а также гораздо более продвинутые методы.