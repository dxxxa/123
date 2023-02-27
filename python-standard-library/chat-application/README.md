# [How to Make a Chat Application in Python](https://www.thepythoncode.com/article/make-a-chat-room-application-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Run `server.py` first to initialize the server.
- Run one or more `client.py` instances and chat!
- If you want to run `client.py` from another machine, make sure you change `SERVER_HOST` in `client.py` to the server's IP address.
##
# [[] / []]()
Комната чата — это интерфейс, который позволяет двум или более людям общаться и отправлять сообщения всем в комнате. В этом учебнике вы узнаете, как создать простой сервер чата и позволить нескольким клиентам подключаться к нему с помощью сокетов в Python.

Мы собираемся использовать модуль сокета, который поставляется со встроенным Python и предоставляет нам операции сокетами, которые широко используются в Интернете, так как они стоят за любым подключением к любой сети.

Чтобы начать работу и изменить цвет текста, нам понадобится пакет colorama для назначения цвета печати каждому клиенту в чате:

pip3 install colorama
Поскольку мы используем сокеты, то нам нужен серверный и клиентский код, начнем с серверной части.

Код сервера
В нашей архитектуре вся работа сервера заключается в выполнении двух основных операций:

Прослушивание предстоящих клиентских подключений, если подключен новый клиент, мы добавляем его в нашу коллекцию клиентских сокетов.
Запустите новый поток для каждого подключенного клиента, который будет прослушивать предстоящие сообщения, отправленные клиентом, и транслировать их всем другим клиентам.
Приведенный ниже код создает TCP-сокет и привязывает его к адресу сервера, а затем прослушивает предстоящие подключения:

import socket
from threading import Thread

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
Обратите внимание, что я использовал «0.0.0.0» в качестве IP-адреса сервера. это означает все IPv4-адреса на локальном компьютере. Вы можете задаться вопросом, почему мы просто не используем localhost или "127.0.0.1"? Ну, если сервер имеет два IP-адреса, скажем, «192.168.1.2» в сети и «10.0.0.1» в другой, то сервер прослушивает обе сети.

Мы еще не принимаем соединения, так как мы не вызывали метод accept(), приведенный ниже код завершает рецепт серверного кода:

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
Как упоминалось ранее, мы добавляем подключенный клиентский сокет в коллекцию наших сокетов, а затем запускаем новый поток и устанавливаем его как поток демона (см. в этом учебнике для получения дополнительной информации о потоках демонов), который выполняет нашу определенную функцию listen_for_client(), которая, учитывая клиентский сокет, ожидает отправки сообщения с помощью метода recv(), если это так, то он отправляет его всем другим подключенным клиентам.

Наконец, давайте закроем все сокеты:

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
Хорошо, это все для серверного кода, давайте углубимся в клиентский код.

Код клиента
Клиент выполняет три основные операции:

Подключается к серверу.
Продолжайте прослушивать сообщения, поступающие с сервера (должен быть клиент, отправивший сообщение на сервер, а сервер широковещал его) и распечатайте его на консоли.
Ожидание ввода пользователем сообщений для отправки на сервер.
Вот код для первой операции:

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
В качестве побочной операции мы также устанавливаем цвет для каждого клиента, вы увидите его в выходных данных. Кроме того, давайте установим имя для каждого клиента, чтобы мы могли различать клиентов:

# prompt the client for a name
name = input("Enter your name: ")
Приведенный ниже код отвечает за вторую операцию; продолжайте прослушивать сообщения с сервера и печатайте их на консоли:

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
Мы также хотим, чтобы он был в отдельном потоке в качестве потока демона, чтобы мы могли делать другие вещи во время прослушивания сообщений.

Теперь давайте выполним последнее задание; ожидание ввода пользователем сообщений, а затем отправка их на сервер:

while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()
Мы добавляем цвет клиента, имя и текущую дату-время к отправляемому сообщению, отправляем сообщение методом send() и делаем способ выйти из проблемы, просто введя символ 'q' вместо сообщения.

Демонстрация
Хорошо, теперь, когда мы закончили оба рецепта кода, давайте сделаем демонстрацию. Во-первых, давайте запустим один и только один экземпляр сервера:

Сервер прослушивает предстоящие клиентские подключения

Удивительно, сервер прослушивает предстоящие клиентские подключения, давайте попробуем запустить один экземпляр клиента:

Первый подключенный клиентТеперь клиент подключен к серверу и запрашивает имя пользователя, чтобы убедиться, что он подключен, вернитесь к консоли сервера, и вы увидите, что он действительно подключен:

Клиент подключен к серверуОбратите внимание, что на данный момент мы находимся на адресу localhost (127.0.0.1), так как это одна и та же машина, но если вы хотите подключиться с других машин в той же сети, вы также можете сделать это, просто убедитесь, что изменили код клиента с 127.0.0.1 на частный IP-адрес сервера.SERVER_HOST

Давайте запустим другой клиент, чтобы мы могли общаться:

Второй клиент подключен и общается в чате

Удивительно, как вы можете видеть, каждый клиент имеет цвет, поэтому мы можем различать пользователей, давайте запустим третий клиент для удовольствия:

Три клиента в чате

Заключение
Отлично, теперь каждое сообщение, отправленное от конкретного клиента, отправляется всем остальным клиентам. Обратите внимание, что цвета изменяются при повторном выполнении сценария client.py.

Пожалуйста, проверьте полный код, чтобы вы могли легко запустить их самостоятельно!

Я призываю вас добавить больше функций в эту программу. Например, вы можете сделать уведомление всем пользователям при подключении нового клиента!

Дополнительные учебники по сокетам Python см. в следующих разделах:

Как передавать файлы в сети с помощью сокетов в Python.
Как создать обратную оболочку в Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую!