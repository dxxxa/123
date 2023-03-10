# [Daemon Threads in Python](https://www.thepythoncode.com/article/daemon-threads-in-python)
##
# [[] / []]()
В этом уроке вы узнаете, что такое потоки демонов в Python и как их настроить, вы должны иметь базовые знания о потоках для последующих действий в этом учебнике.

Поток демона — это поток, который умирает всякий раз, когда умирает основной поток, его также называют неблокирующим потоком. Обычно основной поток должен ждать завершения других потоков, чтобы выйти из программы, но если вы установите флаг демона, вы можете позволить потоку выполнять свою работу и забыть о нем, а когда программа завершит работу, она будет убита автоматически.

Это полезно для многих сценариев, предположим, что вы выполняете некоторые задачи веб-парсинга, и вы хотите создать поток, который предупреждает вас по электронной почте всякий раз, когда новый элемент вставляется в тот конкретный веб-сайт, который вы очищаете.

В другом примере может потребоваться создать поток, который отслеживает файлы журналов в вашей программе и предупреждает вас о возникновении критической ошибки.

В конце учебника мы поделимся с вами некоторыми учебниками, которые мы сочли полезными для использования потоков демонов.

Теперь, когда вы знаете, что такое поток демона, и вы знаете, что он полезен, давайте возьмем демонстрационный пример, следующий код инициирует поток, отличный от демона, и запускает его, а затем мы заканчиваем основной поток:

import threading
import time

def func():
    while True:
        print(f"[{threading.current_thread().name}] Printing this message every 2 seconds")
        time.sleep(2)

# initiate the thread to call the above function
normal_thread = threading.Thread(target=func, name="normal_thread")
# start the thread
normal_thread.start()
# sleep for 4 seconds and end the main thread
time.sleep(4)
# the main thread ends
Функция func() должна выполняться вечно, так как мы устанавливаем True в качестве условия цикла while. После того, как мы запустили этот поток, мы делаем простой спящий режим в основном потоке и выходим из программы.

Однако, если вы запустите его, вы увидите, что программа продолжает работать и не позволит вам выйти (только если вы закроете окно):

[normal_thread] Printing this message every 2 seconds
[normal_thread] Printing this message every 2 seconds
[normal_thread] Printing this message every 2 seconds
[normal_thread] Printing this message every 2 seconds
[normal_thread] Printing this message every 2 seconds
...goes forever
Таким образом, поток, не являющийся демоном, заставляет программу отказываться выходить, пока она не будет завершена.

На этот раз в следующем примере инициируется поток демона:

import threading
import time

def func_1():
    while True:
        print(f"[{threading.current_thread().name}] Printing this message every 2 seconds")
        time.sleep(2)

# initiate the thread with daemon set to True
daemon_thread = threading.Thread(target=func_1, name="daemon-thread", daemon=True)
# or
# daemon_thread.daemon = True
# or
# daemon_thread.setDaemon(True)
daemon_thread.start()
# sleep for 10 seconds and end the main thread
time.sleep(4)
# the main thread ends
Теперь мы передаем daemon=True в многопоточность. Класс Thread, чтобы указать, что это поток демона, вы также можете получить доступ к атрибуту daemon True или использовать метод setDaemon(True).

Выполним программу:

[daemon-thread] Printing this message every 2 seconds
[daemon-thread] Printing this message every 2 seconds
На этот раз, как только основной поток заканчивает свою работу, поток демона также автоматически убивается и выходит из программы.

Реальные примеры
Ниже приведены некоторые из учебников, в которых мы использовали потоки демонов для выполнения наших задач:

Создание кейлоггера на Python: поток демона для отправки кейлогов на нашу электронную почту или сохранения в файл.
Создание сканера портов в Python: несколько потоков демона для поиска портов.
Перебор FTP-серверов с Python: несколько потоков демонов для попытки входа в FTP.
Создание приложения чата на Python: поток демона, который прослушивает предстоящие сообщения из сети и печатает их на консоли.