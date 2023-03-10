# [How to Make a Process Monitor in Python](https://www.thepythoncode.com/article/make-process-monitor-python)
to run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python3 process_monitor.py --help
    ```
    **Output:**
    ```
    usage: process_monitor.py [-h] [-c COLUMNS] [-s SORT_BY] [--descending] [-n N]

    Process Viewer & Monitor

    optional arguments:
    -h, --help            show this help message and exit
    -c COLUMNS, --columns COLUMNS
                            Columns to show, available are name,create_time,cores,
                            cpu_usage,status,nice,memory_usage,read_bytes,write_by
                            tes,n_threads,username. Default is name,cpu_usage,memo
                            ry_usage,read_bytes,write_bytes,status,create_time,nic
                            e,n_threads,cores.
    -s SORT_BY, --sort-by SORT_BY
                            Column to sort by, default is memory_usage .
    --descending          Whether to sort in descending order.
    -n N                  Number of processes to show, will show all if 0 is
                            specified, default is 25 .

    ```
## Examples:
- Showing 10 processes sorted by create_time in ascending order:
```
python3 process_monitor.py --sort-by create_time -n 10
```
**Output:**
```
             name  cpu_usage memory_usage read_bytes write_bytes    status          create_time  nice  n_threads  cores
pid
1         systemd        0.0     187.92MB   242.47MB     27.64MB  sleeping  2019-09-09 10:56:21     0          1      4
19   kworker/1:0H        0.0        0.00B      0.00B       0.00B      idle  2019-09-09 10:56:21   -20          1      1
17    ksoftirqd/1        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
16    migration/1        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
15     watchdog/1        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
13        cpuhp/0        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
12     watchdog/0        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
11    migration/0        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
14        cpuhp/1        0.0        0.00B      0.00B       0.00B  sleeping  2019-09-09 10:56:21     0          1      1
9       rcu_sched        0.0        0.00B      0.00B       0.00B      idle  2019-09-09 10:56:21     0          1      4
```
- Showing 20 processes with only name, cpu_usage, memory_usage and status as columns, sorted by memory_usage in descending order:
```
python3 process_monitor.py --columns name,cpu_usage,memory_usage,status -n 20 --sort-by memory_usage --descending
```
**Output:**
```
                name  cpu_usage memory_usage    status
pid
1312          mysqld        0.0     144.63MB  sleeping
915      gnome-shell        0.0      81.00MB  sleeping
3214         python3        0.0      58.12MB   running
1660   rtorrent main        0.0      35.84MB  sleeping
2466   rtorrent main        0.0      24.02MB  sleeping
3186             php        0.0      19.58MB  sleeping
737             Xorg        0.0      15.52MB  sleeping
1452         apache2        0.0      12.18MB  sleeping
872      teamviewerd        0.0      11.53MB  sleeping
974        gsd-color        0.0       8.65MB  sleeping
553   NetworkManager        0.0       7.71MB  sleeping
1045          colord        0.0       7.16MB  sleeping
982     gsd-keyboard        0.0       6.23MB  sleeping
969    gsd-clipboard        0.0       6.09MB  sleeping
548     ModemManager        0.0       5.68MB  sleeping
986   gsd-media-keys        0.0       4.94MB  sleeping
1001       gsd-power        0.0       4.72MB  sleeping
962    gsd-xsettings        0.0       4.59MB  sleeping
1023       gsd-wacom        0.0       4.40MB  sleeping
961      packagekitd        0.0       4.31MB  sleeping
```

##
# [[] / []]()
Мониторинг процессов операционной системы позволяет нам отслеживать и отображать активность процесса в режиме реального времени. Вэтом уроке вы узнаете, как получить информацию о запущенных процессах в операционной системе с помощью Python и построить вокруг него диспетчер задач!

Теперь вы, возможно, думаете о создании чего-то вроде этого:

Диспетчер задач Windows

Ну, не совсем так, мы собираемся сделать версию для командной строки этого, окончательный вывод скрипта будет таким:

Монитор процессов Python

Однако, если вы программист с графическим интерфейсом, вы можете сделать это намного лучше с помощью собственного дизайна и конкурировать с диспетчером задач Windows!

Связанные с: Как обрабатывать файлы в Python с помощью модуля ОС.

Хорошо, теперь давайте перейдем к созданию этого. Во-первых, давайте установим зависимости:

pip3 install psutil pandas
Откройте новый файл Python и импортируйте необходимые модули:

import psutil
from datetime import datetime
import pandas as pd
import time
import os
Мы будем использовать psutil, так как это кроссплатформенная библиотека для получения информации о запущенных процессах в Python.

Причина, по которой нам нужны панды здесь, заключается в том, что после получения информации о процессах нам нужно будет сортировать по столбцам и печатать табличным способом.

Теперь нам нужен способ извлечения всех процессов в цикле. К счастью для нас, есть функция psutil.process_iter(), которая возвращает генератор, создающий экземпляр процесса для всех запущенных процессов в операционной системе.

Давайте построим основную функцию, которая возвращает всю информацию о процессе, то есть будет хранить все процессы в списке словарей, чтобы позже можно было легко преобразовать ее в фрейм данных:

def get_processes_info():
    # the list the contain all process dictionaries
    processes = []
Запустим цикл и пересмотрим генератор:

    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
Как вы, возможно, заметили, я исключил PID 0, который является процессом простоя системы, который предназначен для Windows NT, в любом случае у него нет полезной информации.

Process.oneshot() помогает нам эффективно извлекать информацию о процессе (более быстрым способом), мы уже получили pid, давайте получим имя процесса:

            # get the name of the file executed
            name = process.name()
Извлекая время, когда процесс был создан в метке времени, в результате мы преобразуем в правильный объект Python datetime:

            # get the time the process was spawned
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())
Давайте получим загрузку ЦП процесса, а также количество ядер, которые могут выполнить этот процесс:

            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            # get the CPU usage percentage
            cpu_usage = process.cpu_percent()
Примечание: метод cpu_affinity() работает только для Linux, Windows и FreeBSD, поэтому, если вы используете другую ОС, такую как MacOS, вы должны прокомментировать приведенный выше код.

Причина, по которой я обернул process.cpu_affinity() в блок try/except, заключается в том, что иногда это вызовет psutil. AccessDenied для системных процессов (убедитесь, что вы запускаете Python от имени администратора).

Метод process.cpu_percent() возвращает плавающую точку, представляющую текущую загрузку ЦП процесса в процентах. Он сравнивает время процесса с временем процессора системы, прошедшим с момента последнего вызова, возвращаясь немедленно. Это означает, что при первом вызове он вернет 0,0.

Получение статуса процесса, будь то запущенный, спящий и т.д.:

            # get the status of the process (running, idle, etc.)
            status = process.status()
Приоритет процесса:

            try:
                # get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0
Использование памяти:

            try:
                # get the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
Общее количество записанных и прочитанных байтов с помощью этого процесса:

            # total process read and written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
Всего порожденных потоков:

            # get the number of total threads spawned by this process
            n_threads = process.num_threads()
Наконец, пользователь, который породил этот процесс:

            # get the username of user spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"
Давайте добавим всю эту информацию в наш список и выйдем из цикла и вернем ее:

        processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'username': username,
        })

    return processes
Обратите внимание, что в каждом процессе нет информации об использовании сети, потому что psutil не предоставляет эту информацию. Если вы хотите получить его, проверьте этот учебник, чтобы получить сетевое использование в каждом процессе, объединив библиотеки Scapy и psutil.

Как упоминалось ранее, мы идемnna преобразовать список процессов в , в результате чего следующая функция принимает предыдущий список процессов и преобразует его в кадр данных:pandas.DataFrame

def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    df.set_index('pid', inplace=True)
    # sort rows by the column passed as argument
    df.sort_values(sort_by, inplace=True, ascending=not descending)
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    # reorder and define used columns
    df = df[columns.split(",")]
    return df
Приведенная выше функция не только преобразует этот список в кадр данных, но и выполняет многие другие действия:

Он задает индекс каждой строки в кадре данных в качестве идентификатора процесса (поскольку это уникальный идентификатор).
Он сортирует строки по столбцу sort_by, которые будут переданы в виде аргументов командной строки (мы углубимся в это).
Поскольку нам нужен хороший способ печати байтов, он применяет функцию get_size(которую мы объявим через мгновение), которая преобразует кучу больших чисел в формат байтов (например, 54,4 МБ, 103,3 КБ и т. Д.).
Он также форматирует create_time как читаемую дату.
Вот функция get_size():

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
Теперь давайте выполним разбор аргументов командной строки:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process Viewer & Monitor")
    parser.add_argument("-c", "--columns", help="""Columns to show,
                                                available are name,create_time,cores,cpu_usage,status,nice,memory_usage,read_bytes,write_bytes,n_threads,username.
                                                Default is name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores.""",
                        default="name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores")
    parser.add_argument("-s", "--sort-by", dest="sort_by", help="Column to sort by, default is memory_usage .", default="memory_usage")
    parser.add_argument("--descending", action="store_true", help="Whether to sort in descending order.")
    parser.add_argument("-n", help="Number of processes to show, will show all if 0 is specified, default is 25 .", default=25)
    parser.add_argument("-u", "--live-update", action="store_true", help="Whether to keep the program on and updating process information each second")

    # parse arguments
    args = parser.parse_args()
    columns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    n = int(args.n)
    live_update = args.live_update
Если вы не знакомы со встроенным модулем Python argparse, он позволяет нам легко анализировать аргументы, передаваемые из командной строки (т.е. терминала).

Мы добавили кучу аргументов, таких как столбцы для отображения, sort_by столбец, по которому мы будем сортировать в кадре данных, количество процессов для отображения и live_update который отвечает за то, хотите ли вы поддерживать работу программы и постоянно обновлять и печатать информацию о процессе каждый раз (например, верхняя команда в Linux).

Наконец, давайте вызовем функции, которые мы сделали, и покажем кадр данных:

    # print the processes for the first time
    processes = get_processes_info()
    df = construct_dataframe(processes)
    if n == 0:
        print(df.to_string())
    elif n > 0:
        print(df.head(n).to_string())
    # print continuously
    while live_update:
        # get all process info
        processes = get_processes_info()
        df = construct_dataframe(processes)
        # clear the screen depending on your OS
        os.system("cls") if "nt" in os.name else os.system("clear")
        if n == 0:
            print(df.to_string())
        elif n > 0:
            print(df.head(n).to_string())
        time.sleep(0.7)
Здесь я использую метод head(), который печатает первые n строк.

Теперь, чтобы выполнить это, вы должны запустить его от имени администратора, чтобы получить информацию о системных процессах, а также, вот пример выходных данных из моего linux box:

root@rockikz:~/pythonscripts# python3 process_monitor.py --columns name,cpu_usage,memory_usage,status -n 20 --sort-by memory_usage --descending
                name  cpu_usage memory_usage    status
pid
1312          mysqld        0.0     144.63MB  sleeping
915      gnome-shell        0.0      81.00MB  sleeping
3214         python3        0.0      58.12MB   running
1660   rtorrent main        0.0      35.84MB  sleeping
2466   rtorrent main        0.0      24.02MB  sleeping
3186             php        0.0      19.58MB  sleeping
737             Xorg        0.0      15.52MB  sleeping
1452         apache2        0.0      12.18MB  sleeping
872      teamviewerd        0.0      11.53MB  sleeping
974        gsd-color        0.0       8.65MB  sleeping
553   NetworkManager        0.0       7.71MB  sleeping
1045          colord        0.0       7.16MB  sleeping
982     gsd-keyboard        0.0       6.23MB  sleeping
969    gsd-clipboard        0.0       6.09MB  sleeping
548     ModemManager        0.0       5.68MB  sleeping
986   gsd-media-keys        0.0       4.94MB  sleeping
1001       gsd-power        0.0       4.72MB  sleeping
962    gsd-xsettings        0.0       4.59MB  sleeping
1023       gsd-wacom        0.0       4.40MB  sleeping
961      packagekitd        0.0       4.31MB  sleeping
И вот мы поехали! Мы закончили с этим, как обсуждалось выше, вы можете сделать версию этого графического интерфейса с кнопками для закрытия, приостановки и возобновления процесса, поскольку для этого уже есть доступные функции (process.kill(), process.suspend() и process.resume()).

Существует также другая информация, которую вы можете получить, которая не обсуждается здесь, введите help(psutil. Процесс) для всех доступных полей и методов, или проверьте их официальную документацию.

Проверьте полный код здесь.

Кроме того, вы можете использовать psutil для получения общей информации о системе и оборудовании.