# [How to Get Hardware and System Information in Python](https://www.thepythoncode.com/article/get-hardware-system-information-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python3 sys_info.py
    ```
##
# [[] / []]()
Как разработчику Python, удобно использовать сторонние библиотеки, которые выполняют работу, которую вы действительно хотите, вместо того, чтобы каждый раз изобретать велосипед. В этом уроке вы будете знакомы с psutil, который представляет собойбиблиотеку c ross-платформы для мониторинга процессов и системы на Python, а также встроенный платформенный модуль для извлечения информации о вашей системе и оборудовании на Python.

В конце концов, я покажу вам, как вы можете печатать информацию о графическом процессоре (если она у вас есть, конечно).

Существуют довольно популярные инструменты для извлечения системной и аппаратной информации в Linux, такие как lshw, uname и hostnamectl. Тем не менее, мы будем использовать библиотеку psutil в Python, чтобы она могла работать на всех операционных системах и получать практически одинаковые результаты.

Вот оглавление этого учебника:

Информация о системе
Информация о процессоре
Использование памяти
Использование диска
Информация о сети
Информация о графическом процессоре
Связанные с: Как манипулировать IP-адресами в Python с помощью модуля ipaddress.

Прежде чем мы углубимся в это, вам нужно установить psutil:

pip3 install psutil
Откройте новый файл Python и приступим к импорту необходимых модулей:

import psutil
import platform
from datetime import datetime
Сделаем функцию, которая преобразует большое количество байтов в масштабированный формат (например, в кило, мега, гига и т.д.):

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
System Information
We gonna need the platform module here:

print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")
Получение даты и времени загрузки компьютера:

# Boot Time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
Информация о процессоре
Давайте получим некоторую информацию о процессоре, такую как общее количество ядер, использование и т. Д.:

# let's print CPU information
print("="*40, "CPU Info", "="*40)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")
Функция psutil cpu_count() возвращает количество ядер, тогда как функция cpu_freq() возвращает частоту процессора в виде именованного значения, включая текущую, минимальную и максимальную частоту, выраженную в МГц, вы можете установить percpu=True для получения частоты процессора.

cpu_percent() метод возвращает плавающую точку, представляющую текущую загрузку ЦП в процентах, установка интервала в 1 (секунды) будет сравнивать системное время ЦП, прошедшее до и после секунды, мы устанавливаем percpu в значение True, чтобы получить загрузку ЦП каждого ядра.

Использование памяти
# Memory Information
print("="*40, "Memory Information", "="*40)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")
метод virtual_memory() возвращает статистику об использовании системной памяти в виде именованного шаблона, включая такие поля, как общий объем доступной физической памяти), доступный (доступная память, т.е. неиспользованная), использованный и процент (т.е. процент). swap_memory() то же самое, но для памяти подкачки.

Мы использовали ранее определенную функцию get_size() для печати значений в масштабе, так как эти статистические данные выражены в байтах.

Использование диска
# Disk Information
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")
Как и ожидалось, функция disk_usage() возвращает статистику использования диска в виде именованного шаблона, включая общее, используемое и свободное пространство, выраженное в байтах.

Информация о сети
# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
Функция net_if_addrs() возвращает адреса, связанные с каждой сетевой картой, установленной в системе. Для получения подробной информации об использовании сети ознакомьтесь с этим учебником, посвященным мониторингу использования сети с помощью psutil.

Хорошо, вот результат вывода моей личной машины Linux:

======================================== System Information ========================================
System: Linux
Node Name: rockikz
Release: 4.17.0-kali1-amd64
Version: #1 SMP Debian 4.17.8-1kali1 (2018-07-24)
Machine: x86_64
Processor:
======================================== Boot Time ========================================
Boot Time: 2019/8/21 9:37:26
======================================== CPU Info ========================================
Physical cores: 4
Total cores: 4
Max Frequency: 3500.00Mhz
Min Frequency: 1600.00Mhz
Current Frequency: 1661.76Mhz
CPU Usage Per Core:
Core 0: 0.0%
Core 1: 0.0%
Core 2: 11.1%
Core 3: 0.0%
Total CPU Usage: 3.0%
======================================== Memory Information ========================================
Total: 3.82GB
Available: 2.98GB
Used: 564.29MB
Percentage: 21.9%
==================== SWAP ====================
Total: 0.00B
Free: 0.00B
Used: 0.00B
Percentage: 0%
======================================== Disk Information ========================================
Partitions and Usage:
=== Device: /dev/sda1 ===
  Mountpoint: /
  File system type: ext4
  Total Size: 451.57GB
  Used: 384.29GB
  Free: 44.28GB
  Percentage: 89.7%
Total read: 2.38GB
Total write: 2.45GB
======================================== Network Information ========================================
=== Interface: lo ===
  IP Address: 127.0.0.1
  Netmask: 255.0.0.0
  Broadcast IP: None
=== Interface: lo ===
=== Interface: lo ===
  MAC Address: 00:00:00:00:00:00
  Netmask: None
  Broadcast MAC: None
=== Interface: wlan0 ===
  IP Address: 192.168.1.101
  Netmask: 255.255.255.0
  Broadcast IP: 192.168.1.255
=== Interface: wlan0 ===
=== Interface: wlan0 ===
  MAC Address: 64:70:02:07:40:50
  Netmask: None
  Broadcast MAC: ff:ff:ff:ff:ff:ff
=== Interface: eth0 ===
  MAC Address: d0:27:88:c6:06:47
  Netmask: None
  Broadcast MAC: ff:ff:ff:ff:ff:ff
Total Bytes Sent: 123.68MB
Total Bytes Received: 577.94MB
Если вы используете ноутбук, вы можете использовать psutil.sensors_battery() для получения информации о батарее.

Кроме того, если вы являетесь пользователем Linux, вы можете использовать psutil.sensors_fan() для получения RPM вентилятора (оборотов в минуту), а также psutil.sensors_temperatures() для получения температуры различных устройств.

Информация о графическом процессоре
psutil не предоставляет нам информацию о графическом процессоре. Поэтому нам нужно установить GPUtil:

pip3 install gputil
GPUtil - это модуль Python для получения статуса графического процессора только для графических процессоров NVIDIA, он находит все графические процессоры на компьютере, определяет их доступность и возвращает упорядоченный список доступных графических процессоров. Для этого требуется установленная последняя версия драйвера NVIDIA.

Кроме того, нам нужно установить табличный модуль, который позволит нам печатать информацию GPU табличным способом:

pip3 install tabulate
Следующие строки кода печатают все графические процессоры на вашем компьютере вместе с их деталями:

# GPU information
import GPUtil
from tabulate import tabulate
print("="*40, "GPU Details", "="*40)
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))

print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")))
Вот выходные данные в моей машине:

======================================== GPU Details ========================================
  id  name              load    free memory    used memory    total memory    temperature    uuid
----  ----------------  ------  -------------  -------------  --------------  -------------  ----------------------------------------
   0  GeForce GTX 1050  2.0%    3976.0MB       120.0MB        4096.0MB        52.0 °C        GPU-c9b08d82-f1e2-40b6-fd20-543a4186d6ce
Заключение
Отлично, теперь вы можете интегрировать эту информацию в свои приложения и утилиты для мониторинга Python! Ознакомьтесь с документацией библиотек, которые мы использовали в этом учебнике:

платформа — доступ к идентифицирующим данным базовой платформы
Официальная документация psutil
Документация GPUtil
Вы также можете использовать psutil для мониторинга процессов операционной системы, таких как использование ЦП и памяти каждого процесса и т. Д.