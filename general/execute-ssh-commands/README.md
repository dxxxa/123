# [How to Execute BASH Commands in a Remote Machine in Python](https://www.thepythoncode.com/article/executing-bash-commands-remotely-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To execute certain commands, edit `execute_commands.py` on your needs and then execute.
- To execute an entire BASH script (.sh) named `script.sh` for instance on `192.168.1.101` with `test` as username and `abc123` as password:
    ```
    python execute_bash.py 192.168.1.101 -u root -p inventedpassword123 -b script.sh
    ```
##
# [[] / []]()
Вы когда-нибудь хотели быстро выполнять определенные команды на своей машине Linux удаленно? или вы хотите регулярно выполнять некоторые строки кода на своем сервере для автоматизации работы? В этом учебнике вы узнаете, как вы можете написать простой скрипт Python для удаленного выполнения команд оболочки на вашем компьютере Linux.

СВЯЗАННЫЕ С: Как перебор SSH-серверов в Python.

Мы будем использовать библиотеку paramiko; давайте установим его:

pip3 install paramiko
Определение некоторых учетных данных подключения:

import paramiko

hostname = "192.168.1.101"
username = "test"
password = "abc123"
В приведенном выше коде я определил имя хоста, имя пользователя и пароль, это мое локальное окно Linux, вам нужно отредактировать эти переменные для вашего случая, или вы можете сделать анализ аргументов командной строки с помощью модуля argparse, как мы обычно делаем в таких задачах.

Обратите внимание, что подключение к SSH с использованием таких учетных данных небезопасно. Можно настроить демон прослушивателя SSH на прием только открытых ключей проверки подлинности вместо использования пароля. Однако в демонстрационных целях мы будем использовать пароль.

Выполнение команд оболочки
Теперь давайте создадим список команд, которые вы хотите выполнить на этой удаленной машине:

commands = [
    "pwd",
    "id",
    "uname -a",
    "df -h"
]
В этом случае простые команды выводят полезную информацию об операционной системе.

Приведенный ниже код отвечает за запуск SSH-клиента и подключение к серверу:

# initialize the SSH client
client = paramiko.SSHClient()
# add to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=hostname, username=username, password=password)
except:
    print("[!] Cannot connect to the SSH Server")
    exit()
Теперь давайте переберем только что определенные нами команды и выполним их одну за другой:

# execute the commands
for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)
Вот мои результаты:

================================================== pwd ==================================================
/home/test

================================================== id ==================================================
uid=1000(test) gid=0(root) groups=0(root),27(sudo)

================================================== uname -a ==================================================
Linux rockikz 4.17.0-kali1-amd64 #1 SMP Debian 4.17.8-1kali1 (2018-07-24) x86_64 GNU/Linux

================================================== df -h ==================================================
Filesystem      Size  Used Avail Use% Mounted on
udev            1.9G     0  1.9G   0% /dev
tmpfs           392M  6.2M  386M   2% /run
/dev/sda1       452G  410G   19G  96% /
tmpfs           2.0G     0  2.0G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           392M   12K  392M   1% /run/user/131
tmpfs           392M     0  392M   0% /run/user/1000
Удивительно, эти команды были успешно выполнены на моей машине Linux!

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python EBook

Выполнение скриптов
Теперь, когда вы знаете, как вы можете выполнять команды одну за другой, давайте углубимся немного глубже и выполним целые сценарии оболочки (.sh).

Рассмотрим этот скрипт (названный «script.sh»):

cd Desktop
mkdir test_folder
cd test_folder
echo "$PATH" > path.txt
После SSH-соединения, вместо итерации команд, теперь мы читаем содержимое этого скрипта и выполняем его:

# read the BASH script content from the file
bash_script = open("script.sh").read()
# execute the BASH script
stdin, stdout, stderr = client.exec_command(bash_script)
# read the standard output and print it
print(stdout.read().decode())
# print errors if there are any
err = stderr.read().decode()
if err:
    print(err)
# close the connection
client.close()
exec_command() выполняет сценарий с использованием оболочки по умолчанию (BASH, SH или любой другой) и возвращает стандартный ввод, стандартный вывод и стандартную ошибку соответственно. Мы будем читать из stdout и stderr, если таковые имеются, а затем закроем соединение SSH.

После выполнения приведенного выше кода в Desktop был создан новый файл test_folder и внутри которого содержалась глобальная переменная $PATH:

Результаты после выполнения скрипта на Python

ПОЛУЧИТЕ СКИДКУ -10%: Создайте 24 этических хакерских скрипта и инструмента с помощью python EBook
Заключение
Как видите, это полезно для многих сценариев. Например, вы можете управлять своими серверами только путем удаленного выполнения скриптов Python; Вы можете делать все, что захотите!

И, кстати, если вы хотите выполнять более сложные задания на удаленном сервере, вы можете вместо этого заглянуть в Ansible.

Вы также можете использовать библиотеку Fabric, так как это высокоуровневая библиотека Python, предназначенная только для удаленного выполнения команд оболочки через SSH. Он построен поверх Invoke и Paramiko.

Не стесняйтесь редактировать код по своему усмотрению; Например, может потребоваться синтаксический анализ аргументов командной строки с помощью argparse.