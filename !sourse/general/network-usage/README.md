# [How to Make a Network Usage Monitor in Python](https://www.thepythoncode.com/article/make-a-network-usage-monitor-in-python)
To run the scripts:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Вы когда-нибудь хотели создать программу, которая отслеживает использование сети вашей машиной? В этом уроке мы создадим три скрипта Python, которые отслеживают общее использование сети, использование сети для каждого сетевого интерфейса и использование сети для каждого системного процесса:

Общая загрузка сети
Использование сети на сетевой интерфейс
Использование сети для каждого процесса
Чтобы начать работу, давайте установим необходимые библиотеки:

$ pip install psutil scapy pandas
psutil - это кроссплатформенная библиотека для получения информации о запущенных процессах и системной и аппаратной информации в Python, мы будем использовать ее для получения сетевой статистики, а также установленных соединений.

1. Общее использование сети
Начиная с простейшей программы; Давайте импортируем psutil и сделаем функцию, которая печатает байты в хорошем формате:

import psutil
import time

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
Далее мы будем использовать функцию psutil.net_io_counters(), которая возвращает статистику ввода и вывода сети:

# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
Теперь давайте введем цикл, который получает ту же статистику, но после задержки, чтобы мы могли рассчитать скорость загрузки и выгрузки:

while True:
    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the stats again
    io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    # print the total download/upload along with current speeds
    print(f"Upload: {get_size(io_2.bytes_sent)}   "
          f", Download: {get_size(io_2.bytes_recv)}   "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
    # update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
Мы просто вычитаем старую сетевую статистику из новой статистики, чтобы получить скорость, мы также включим общую загруженную и загруженную статистику. Поскольку мы хотим, чтобы печать обновлялась в одной строке, а не печаталась в нескольких строках, мы передаем возвращаемый символ "\r" в конечный параметр в функции print(), чтобы вернуться в начало той же строки после печати. Давайте запустим его:

$ python network_usage.py
Выходные данные будут обновляться каждую секунду:

Upload: 19.96MB   , Download: 114.03MB   , Upload Speed: 4.25KB/s   , Download Speed: 207.00B/s 
И все! Мы успешно сделали быстрый скрипт, чтобы получить общую загрузку и использование загрузок вместе со скоростью. В следующем разделе мы сделаем то же самое, но покажем использование для каждого интерфейса, это полезно, если вы подключены к нескольким сетям с помощью нескольких сетевых адаптеров.

2. Использование сети для каждого сетевого интерфейса
В этом разделе мы используем тот же метод, что и раньше, но мы устанавливаем для pernic значение True:

import psutil
import time
import os
import pandas as pd

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

# get the network I/O stats from psutil on each network interface
# by setting `pernic` to `True`
io = psutil.net_io_counters(pernic=True)
Теперь введем цикл while:

while True:
    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the network I/O stats again per interface 
    io_2 = psutil.net_io_counters(pernic=True)
    # initialize the data to gather (a list of dicts)
    data = []
    for iface, iface_io in io.items():
        # new - old stats gets us the speed
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
        })
    # update the I/O stats for the next iteration
    io = io_2
    # construct a Pandas DataFrame to print stats in a cool tabular style
    df = pd.DataFrame(data)
    # sort values per column, feel free to change the column
    df.sort_values("Download", inplace=True, ascending=False)
    # clear the screen based on your OS
    os.system("cls") if "nt" in os.name else os.system("clear")
    # print the stats
    print(df.to_string())
На этот раз psutil.net_io_counters() возвращает словарь каждого интерфейса и соответствующую ему сетевую статистику. Внутри цикла while мы перебираем этот словарь и выполняем те же вычисления, что и раньше.

Поскольку у нас есть несколько строк, мы используем панд для печати статистики в табличной форме и используем команду cls в Windows или clear в Linux или macOS, чтобы очистить экран перед печатью обновленных результатов.

Чтобы напечатать весь кадр данных панды, мы просто вызываем метод to_string() внутри функции print(), и он выполнит эту работу. Давайте запустим его:

$ pip install network_usage_per_interface.py
Вот выходные данные:

Использование сети на интерфейс

3. Использование сети для каждого процесса
К сожалению, psutil имеет возможность отслеживать только общее использование сети или использование сети для каждого сетевого интерфейса. Чтобы иметь возможность отслеживать использование каждого процесса, мы должны использовать еще одну библиотеку, и это Scapy.

Scapy - это мощный инструмент для управления пакетами, который предоставляет нам возможность перехватывать исходящие и входящие пакеты в нашей машине. Ознакомьтесь с нашими учебными пособиями, если вы хотите узнать больше об его использовании.

На этот раз мы будем использовать библиотеку psutil для получения текущих сетевых подключений и извлечения портов источника и назначения, а также идентификатора процесса (PID), который отвечает за соединение.

Затем мы сопоставляем эту информацию при поиске пакетов с помощью Scapy и помещаем статистику трафика в соответствующий PID. Давайте начнем:

from scapy.all import *
import psutil
from collections import defaultdict
import os
from threading import Thread
import pandas as pd

# get the all network adapter's MAC addresses
all_macs = {iface.mac for iface in ifaces.values()}
# A dictionary to map each connection to its correponding process ID (PID)
connection2pid = {}
# A dictionary to map each process ID (PID) to total Upload (0) and Download (1) traffic
pid2traffic = defaultdict(lambda: [0, 0])
# the global Pandas DataFrame that's used to track previous traffic stats
global_df = None
# global boolean for status of the program
is_program_running = True

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
После импорта необходимых библиотек мы инициализируем наши глобальные переменные, которые будут использоваться в наших будущих функциях:

all_macs - это набор Python, который содержит MAC-адреса всех сетевых интерфейсов в нашей машине.
connection2pid — это словарь Python, который сопоставляет каждое соединение (представленное в виде портов источника и назначения на уровне TCP/UDP).
pid2traffic — это еще один словарь, который сопоставляет каждый идентификатор процесса (PID) со списком из двух значений, представляющих трафик загрузки и загрузки.
global_df — это кадр данных Pandas, который используется для хранения предыдущих данных о трафике (чтобы мы могли рассчитать использование).
is_program_running — это просто логическое значение, то есть при установке значения False программа останавливается и завершает работу.
Если вы не знакомы со Scapy, то для того, чтобы иметь возможность перехватывать пакеты, мы должны использовать функцию sniff(), предоставляемую этой библиотекой. Эта функция принимает несколько параметров, одним из важных из которых является обратный вызов, который вызывается при захвате пакета. Прежде чем мы вызовем sniff(), давайте сделаем наш обратный звонок:

def process_packet(packet):
    global pid2traffic
    try:
        # get the packet source & destination IP addresses and ports
        packet_connection = (packet.sport, packet.dport)
    except (AttributeError, IndexError):
        # sometimes the packet does not have TCP/UDP layers, we just ignore these packets
        pass
    else:
        # get the PID responsible for this connection from our `connection2pid` global dictionary
        packet_pid = connection2pid.get(packet_connection)
        if packet_pid:
            if packet.src in all_macs:
                # the source MAC address of the packet is our MAC address
                # so it's an outgoing packet, meaning it's upload
                pid2traffic[packet_pid][0] += len(packet)
            else:
                # incoming packet, download
                pid2traffic[packet_pid][1] += len(packet)
Связанные с: Как сделать АТАКУ SYN Flooding в Python.

Обратный вызов process_packet() принимает пакет в качестве аргумента. Если в пакете есть уровни TCP или UDP, он извлекает исходный и конечный порты и пытается использовать словарь connection2pid, чтобы получить PID, отвечающий за это соединение. Если он находит его, и если исходный MAC-адрес является одним из MAC-адресов машины, то он добавляет размер пакета к трафику загрузки. В противном случае он добавляет его к трафику загрузки.

Далее сделаем функцию, отвечающую за получение соединений:

def get_connections():
    """A function that keeps listening for connections on this machine 
    and adds them to `connection2pid` global variable"""
    global connection2pid
    while is_program_running:
        # using psutil, we can grab each connection's source and destination ports
        # and their process ID
        for c in psutil.net_connections():
            if c.laddr and c.raddr and c.pid:
                # if local address, remote address and PID are in the connection
                # add them to our global dictionary
                connection2pid[(c.laddr.port, c.raddr.port)] = c.pid
                connection2pid[(c.raddr.port, c.laddr.port)] = c.pid
        # sleep for a second, feel free to adjust this
        time.sleep(1)
Указанная выше функция отвечает за заполнение глобальной переменной connection2pid, которая используется в функции process_packet(). Конечно, соединения могут быть сделаны в любую секунду, поэтому мы продолжаем прослушивать соединения каждую секунду или около того в цикле.

Далее, написав функцию, которая вычисляет использование сети и выводит собранные нами данные:

def print_pid2traffic():
    global global_df
    # initialize the list of processes
    processes = []
    for pid, traffic in pid2traffic.items():
        # `pid` is an integer that represents the process ID
        # `traffic` is a list of two values: total Upload and Download size in bytes
        try:
            # get the process object from psutil
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            # if process is not found, simply continue to the next PID for now
            continue
        # get the name of the process, such as chrome.exe, etc.
        name = p.name()
        # get the time the process was spawned
        try:
            create_time = datetime.fromtimestamp(p.create_time())
        except OSError:
            # system processes, using boot time instead
            create_time = datetime.fromtimestamp(psutil.boot_time())
        # construct our dictionary that stores process info
        process = {
            "pid": pid, "name": name, "create_time": create_time, "Upload": traffic[0],
            "Download": traffic[1],
        }
        try:
            # calculate the upload and download speeds by simply subtracting the old stats from the new stats
            process["Upload Speed"] = traffic[0] - global_df.at[pid, "Upload"]
            process["Download Speed"] = traffic[1] - global_df.at[pid, "Download"]
        except (KeyError, AttributeError):
            # If it's the first time running this function, then the speed is the current traffic
            # You can think of it as if old traffic is 0
            process["Upload Speed"] = traffic[0]
            process["Download Speed"] = traffic[1]
        # append the process to our processes list
        processes.append(process)
    # construct our Pandas DataFrame
    df = pd.DataFrame(processes)
    try:
        # set the PID as the index of the dataframe
        df = df.set_index("pid")
        # sort by column, feel free to edit this column
        df.sort_values("Download", inplace=True, ascending=False)
    except KeyError as e:
        # when dataframe is empty
        pass
    # make another copy of the dataframe just for fancy printing
    printing_df = df.copy()
    try:
        # apply the function get_size to scale the stats like '532.6KB/s', etc.
        printing_df["Download"] = printing_df["Download"].apply(get_size)
        printing_df["Upload"] = printing_df["Upload"].apply(get_size)
        printing_df["Download Speed"] = printing_df["Download Speed"].apply(get_size).apply(lambda s: f"{s}/s")
        printing_df["Upload Speed"] = printing_df["Upload Speed"].apply(get_size).apply(lambda s: f"{s}/s")
    except KeyError as e:
        # when dataframe is empty again
        pass
    # clear the screen based on your OS
    os.system("cls") if "nt" in os.name else os.system("clear")
    # print our dataframe
    print(printing_df.to_string())
    # update the global df to our dataframe
    global_df = df
Приведенная выше функция выполняет итерацию по словарю pid2traffic и пытается получить объект процесса с помощью psutil, чтобы он мог получить имя и время создания процесса с помощью методов name() и create_time() соответственно.

После того, как мы создадим наш словарь процессов, в котором содержится большая часть необходимой нам информации о процессе, включая общее использование, мы используем global_df, чтобы получить предыдущее общее использование, а затем рассчитать текущую скорость загрузки и загрузки, используя это. После этого мы добавляем этот процесс в наш список процессов и преобразуем его в кадр данных pandas для его печати.

Прежде чем мы напечатаем кадр данных, мы можем сделать некоторые изменения, такие как сортировка по использованию «Скачать», а также применить функцию утилиты get_size() для печати байтов в хорошем масштабируемом формате.

Сделаем еще одну функцию, которая каждую секунду вызывает вышеуказанную функцию:

def print_stats():
    """Simple function that keeps printing the stats"""
    while is_program_running:
        time.sleep(1)
        print_pid2traffic()
Итак, теперь у нас есть две функции, которые продолжают работать в отдельных потоках, одна из которых - выше print_stats(), а вторая - get_connections(). Сделаем основной код:

if __name__ == "__main__":
    # start the printing thread
    printing_thread = Thread(target=print_stats)
    printing_thread.start()
    # start the get_connections() function to update the current connections of this machine
    connections_thread = Thread(target=get_connections)
    connections_thread.start()
Наконец, давайте начнем sniffing с помощью функции sniff() Scapy:

    # start sniffing
    print("Started sniffing")
    sniff(prn=process_packet, store=False)
    # setting the global variable to False to exit the program
    is_program_running = False   
Мы передаем нашу ранее определенную функцию process_packet() аргументу prn и устанавливаем для хранилища значение False, чтобы не хранить захваченные пакеты в памяти.

Мы просто устанавливаем для is_program_running значение False всякий раз, когда выходим из функции sniff() по какой-либо причине (включая нажатие CTRL + C). Давайте запустим нашу программу сейчас:

$ python network_usage_per_process.py
Вот выходные данные:

Использование сети для каждого процесса

В учебнике по мониторингу процесса мы включили много столбцов (но не использование сети) в наш монитор, не стесняйтесь добавлять их сюда, если хотите.

Заметка: Этот код может содержать проблемы и ошибки, вы можете комментировать или предлагать любые изменения, если вы обнаружите какую-либо проблему.

Заключение
Отлично, теперь у вас есть три программы для мониторинга использования сети, не стесняйтесь редактировать и использовать код по своему усмотрению, например, обновлять UPDATE_DELAY или изменять столбец сортировки, или что-то еще.

Кроме того, вы можете многое сделать с psutil, вы можете сделать монитор процесса или извлечь различную системную и аппаратную информацию на своей машине, проверьте учебники, если вам интересно, как это сделать.