# [How to Transfer Files in the Network using Sockets in Python](https://www.thepythoncode.com/article/send-receive-files-using-sockets-python)
To run this:
- `pip3 install -r requirements.txt`.
- ### For the server ( the receiver ):
    - 
        ```
        python3 receiver.py
        ```
- ### For the client ( the sender ):
    - 
        ```
        C:\> python sender.py --help
        usage: sender.py [-h] [-p PORT] file host

        Simple File Sender

        positional arguments:
        file                  File name to send
        host                  The host/IP address of the receiver

        optional arguments:
        -h, --help            show this help message and exit
        -p PORT, --port PORT  Port to use, default is 5001
        ```
        For instance, if you want to send `data.csv` to `192.168.1.101`:
        ```
        python3 sender.py data.csv 192.168.1.101
        ```
##
# [[] / []]()
Передача файлов — это процесс копирования или перемещения файла с одного компьютера на другой по сети или подключению к Интернету. В этом уроке мы шаг за шагом расскажем о том, как вы можете написать клиент-серверные скрипты Python, которые обрабатывают это.

Основная идея состоит в том, чтобы создать сервер, который прослушивает определенный порт; этот сервер будет отвечать за получение файлов (вы также можете заставить сервер отправлять файлы). С другой стороны, клиент попытается подключиться к серверу и отправить файл любого типа.

Мы будем использовать модуль сокета, который поставляется со встроенным Python и предоставляет нам операции сокетами, которые широко используются в Интернете, так как они стоят за любым подключением к любой сети.

Обратите внимание, что существуют более надежные способы передачи файлов с помощью таких инструментов, как rsync или scp. Тем не менее, целью этого учебника является передача файлов с помощью языка программирования Python и без какого-либо стороннего инструмента.

Связанные с: Как организовать файлы по расширению в Python.

Во-первых, нам нужно будет установить библиотеку tqdm, которая позволит нам печатать причудливые индикаторы выполнения:

pip3 install tqdm
Код клиента
Начнем с клиента, отправителя:

import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
Нам нужно указать IP-адрес, порт сервера, к которому мы хотим подключиться, и имя файла, который мы хотим отправить.

# the ip address or hostname of the server, the receiver
host = "192.168.1.101"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "data.csv"
# get the file size
filesize = os.path.getsize(filename)
Имя файла должно существовать в текущем каталоге, или вы можете использовать абсолютный путь к этому файлу где-то на вашем компьютере. Это файл, который вы хотите отправить.

os.path.getsize(имя_файла) получает размер этого файла в байтах; Это здорово, так как он нужен нам для отображения индикаторов выполнения в клиенте и на сервере.

Создадим TCP-сокет:

# create the client socket
s = socket.socket()
Подключение к серверу:

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
Метод connect() ожидает, что адрес пары (хост, порт) соединит сокет с этим удаленным адресом. Как только соединение установлено, мы отправляем имя и размер файла:

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
Я использовал SEPARATOR здесь для разделения полей данных; это просто нежелательное сообщение, мы можем просто использовать send() дважды, но мы можем не захотеть этого делать в любом случае. функция encode() кодирует строку, которую мы передали в кодировку 'utf-8' (это необходимо).

Теперь нам нужно отправить файл, и когда мы отправляем файл, мы будем печатать хорошие индикаторы выполнения с помощью библиотеки tqdm:

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
По сути, то, что мы здесь делаем, это открываем файл как прочитанный в двоичном виде («rb»), считываем куски из файла (в данном случае 4096 байт или 4 КБ) и отправляем их в сокет с помощью функции sendall(), а затем мы обновляем индикатор выполнения каждый раз, как только это закончится, мы закрываем этот сокет.

Связанные с: Как создать приложение чата на Python.

Код сервера
Хорошо, так что мы закончили с клиентом. Давайте углубимся в сервер, поэтому откройте новый пустой файл Python и:

import socket
import tqdm
import os
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
Я инициализировал некоторые параметры, которые мы собираемся использовать. Обратите внимание, что я использовал «0.0.0.0» в качестве IP-адреса сервера. Это означает все IPv4-адреса, которые находятся на локальном компьютере. Вы можете задаться вопросом, почему мы просто не используем наш локальный IP-адрес или «localhost» или «127.0.0.1»? Ну, если сервер имеет два IP-адреса, скажем, «192.168.1.101» в сети и «10.0.1.1» в другой, и сервер прослушивает «0.0.0.0», он будет доступен на обоих этих IP-адресах.

Кроме того, вы можете использовать свой общедоступный или частный IP-адрес, в зависимости от ваших клиентов. Если подключенные клиенты находятся в вашей локальной сети, вы должны использовать свой частный IP-адрес (вы можете проверить его с помощью команды ipconfig в Windows или команды ifconfig в Mac OS / Linux), но если вы ожидаете клиентов из Интернета, вы обязательно должны использовать свой публичный адрес.

Кроме того, убедитесь, что на сервере используется тот же порт, что и на клиенте.

Давайте создадим наш TCP-сокет:

# create the server socket
# TCP socket
s = socket.socket()
Теперь это отличается от клиента; нам нужно привязать только что созданный сокет к нашему SERVER_HOST и SERVER_PORT:

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
После этого мы будем прослушивать соединения:

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
Как только клиент подключается к нашему серверу, нам нужно принять это соединение:

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
Помните, что когда клиент подключен, он отправит имя и размер файла. Давайте получим их:

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
Как упоминалось ранее, полученные данные объединяются с именем файла и размером файла, и мы можем легко извлечь их, разделив их строкой SEPARATOR.

После этого нам нужно удалить абсолютный путь к файлу, потому что отправитель отправил файл со своим собственным путем к файлу, который может отличаться от нашего, функция os.path.basename() возвращает конечный компонент пути.

Теперь нам нужно получить файл:

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
Не совсем отличается от клиентского кода. Тем не менее, мы открываем файл как запись в двоичном виде ("wb") здесь и используем метод recv(BUFFER_SIZE) для получения BUFFER_SIZE байтов из клиентского сокета и записи его в файл. Как только это будет завершено, мы закроем клиентские и серверные сокеты.

Узнайте также: Как перечислить все файлы и каталоги на FTP-сервере с помощью Python

Хорошо, позвольте мне попробовать это в моей собственной частной сети:

C:\> python receiver.py

[*] Listening as 0.0.0.0:5001
Мне нужно зайти в мой Linux box и отправить пример файла:

root@rockikz:~/tools# python3 sender.py
[+] Connecting to 192.168.1.101:5001
[+] Connected.
Sending data.npy:   9%|███████▊                                                                            | 45.5M/487M [00:14<02:01, 3.80MB/s]
Давайте посмотрим на сервер сейчас:

[+] ('192.168.1.101', 47618) is connected.
Receiving data.npy:  33%|███████████████████▍                                       | 160M/487M [01:04<04:15, 1.34MB/s]
Заключение
Отлично, мы закончили! Работает!

Если вы хотите запустить серверный код на удаленной машине, а не в локальной сети, убедитесь, что вы разрешаете порт на брандмауэре. Если это виртуальная машина в облаке, убедитесь, что вы разрешили ее через ufw:

$ ufw allow 5001
Это скажет брандмауэру разрешить этот порт для удаленной связи. Если сервер находится в вашем доме, то вам нужно включить порт в настройках маршрутизатора.

Теперь вы можете расширить этот код для своих нужд. Вот несколько примеров, которые вы можете реализовать:

Предоставление серверу возможности получать несколько файлов от нескольких клиентов одновременно с помощью потоков.
Сжатие файлов перед их отправкой, что может помочь увеличить продолжительность передачи. Если целевые файлы, которые вы хотите отправить, являются изображениями, вы можете оптимизировать изображения, сжимая их, или, если они являются pdf-документами, вы также можете сжимать PDF-файлы.
Шифрование файла перед его отправкой, чтобы никто не мог перехватить и прочитать этот файл, этот учебник поможет.
Проверка правильности отправки файла путем проверки контрольных сумм обоих файлов (исходного файла отправителя и отправленного файла в получателе). В этом случае для этого вам понадобятся безопасные алгоритмы хеширования.
Добавление комнаты чата, чтобы вы могли как общаться, так и передавать файлы.