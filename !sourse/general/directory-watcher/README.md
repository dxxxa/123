# [How to Create a Watchdog in Python](https://www.thepythoncode.com/article/create-a-watchdog-in-python)
To run this:
- `pip3 install -r requirements.txt`
- `python3 controller.py --help`
**Output:**
```
usage: controller.py [-h] [-d WATCH_DELAY] [-r] [-p PATTERN] [--watch-directories] path

Watchdog script for watching for files & directories' changes

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  -d WATCH_DELAY, --watch-delay WATCH_DELAY
                        Watch delay, default is 1
  -r, --recursive       Whether to recursively watch for the path's children, default is False
  -p PATTERN, --pattern PATTERN
                        Pattern of files to watch, default is .txt,.trc,.log
  --watch-directories   Whether to watch directories, default is True
```
- For example, watching the path `E:\watchdog` recursively for log and text files:
    ```
    python controller.py E:\watchdog --recursive -p .txt,.log
    ```
##
# [[] / []]()
В разработке программного обеспечения ведение журнала приложений играет ключевую роль. Как бы мы ни хотели, чтобы наше программное обеспечение было идеальным, проблемы всегда будут возникать, поэтому важно иметь надежный мониторинг и ведение журнала, чтобы контролировать и управлять неизбежным хаосом.

В настоящее время инженеры по поддержке приложений должны иметь возможность легко получать доступ и анализировать огромные объемы данных журналов, генерируемых их приложениями и инфраструктурой. При возникновении проблемы они не могут позволить себе ждать минуту или две, пока запрос не вернет результаты. Им нужна скорость, независимо от объема данных, которые они собирают и запрашивают.

Из этого туториала Вы узнаете, как создать сторожевого пса на Python; мы объясним, как обнаружить изменения в определенном каталоге (предположим, что в каталоге размещены журналы ваших приложений). Всякий раз, когда происходит изменение, измененные или вновь созданные файлы предопределенных типов будут своевременно обработаны для извлечения строк, соответствующих заданным шаблонам.

С другой стороны, все строки в этих файлах, которые не соответствуют указанным шаблонам, считаются выбросами и отбрасываются в нашем анализе.

Мы будем использовать библиотеки watchdog и pygtail для обнаружения происходящих изменений, есть также версия Flask, Redis и SocketIO, где веб-приложение GUI создается для той же цели, вы всегда можете обратиться к нему здесь.

Блок-схема процесса
process-flowchart-of-watchdog-tutorial-in-pythonЧтобы начать работу, давайте установим требования:

$ pip3 install Pygtail==0.11.1 watchdog==2.1.1
Во-первых, давайте определим параметры конфигурации для нашего приложения в течение config.py:

# Application configuration File
################################
# Directory To Watch, If not specified, the following value will be considered explicitly.
WATCH_DIRECTORY = "C:\\SCRIPTS"
# Delay Between Watch Cycles In Seconds
WATCH_DELAY = 1
# Check The WATCH_DIRECTORY and its children
WATCH_RECURSIVELY = False
# whether to watch for directory events
DO_WATCH_DIRECTORIES = True
# Patterns of the files to watch
WATCH_PATTERN = '.txt,.trc,.log'
LOG_FILES_EXTENSIONS = ('.txt', '.log', '.trc')
# Patterns for observations
EXCEPTION_PATTERN = ['EXCEPTION', 'FATAL', 'ERROR']
Параметры в config.py будут по умолчанию, позже, в скрипте, мы можем переопределить их, если захотим.

Далее, давайте определим механизм проверки, этот механизм будет использовать модули pygtail и re для того, чтобы точно определить наблюдения на основе параметра, EXCEPTION_PATTERN мы только что определили в config.py:

import datetime
from pygtail import Pygtail

# Loading the package called re from the RegEx Module in order to work with Regular Expressions
import re

class FileChecker:
    def __init__(self, exceptionPattern):
        self.exceptionPattern = exceptionPattern

    def checkForException(self, event, path):
        # Get current date and time according to the specified format.
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        # Read the lines of the file (specified in the path) that have not been read yet
        # Meaning by that it will start from the point where it was last stopped.
        for num, line in enumerate(Pygtail(path), 1):
            # Remove leading and trailing whitespaces including newlines.
            line = line.strip()
            # Return all non-overlapping matches of the values specified in the Exception Pattern.
            # The line is scanned from left to right and matches are returned in the oder found.
            if line and any(re.findall('|'.join(self.exceptionPattern), line, flags=re.I | re.X)):
                # Observation Detected
                type = 'observation'
                msg = f"{now} -- {event.event_type} -- File = {path} -- Observation: {line}"
                yield type, msg
            elif line:
                # No Observation Detected
                type = 'msg'
                msg = f"{now} -- {event.event_type} -- File = {path}"
                yield type, msg
Метод checkForException(), определенный в приведенном выше коде, будет принимать события, отправленные классом наблюдателя сторожевого модуля (см. позже).

Эти события будут инициированы для любого изменения файла в данном каталоге, объект события имеет 3 атрибута:

event_type: тип события в виде строки (изменено, создано, перемещено или удалено).
is_directory: логическое значение, указывающее, было ли событие вызвано для каталога.
src_path: исходный путь к объекту файловой системы, вызвавшему событие.
Теперь давайте определим наши controller.py, сначала импортируем библиотеки:

# The Observer watches for any file change and then dispatches the respective events to an event handler.
from watchdog.observers import Observer
# The event handler will be notified when an event occurs.
from watchdog.events import FileSystemEventHandler
import time
import config
import os
from checker import FileChecker
import datetime
from colorama import Fore, init

init()

GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESET
RED = Fore.RED
YELLOW = Fore.YELLOW

event2color = {
    "created": GREEN,
    "modified": BLUE,
    "deleted": RED,
    "moved": YELLOW,
}

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)
Мы будем использовать colorama, чтобы различать различные события с цветами текста, для получения дополнительной информации о colorama, ознакомьтесь с этим руководством.

Далее давайте определим наш обработчик событий:

# Class that inherits from FileSystemEventHandler for handling the events sent by the Observer
class LogHandler(FileSystemEventHandler):

    def __init__(self, watchPattern, exceptionPattern, doWatchDirectories):
        self.watchPattern = watchPattern
        self.exceptionPattern = exceptionPattern
        self.doWatchDirectories = doWatchDirectories
        # Instantiate the checker
        self.fc = FileChecker(self.exceptionPattern)

    def on_any_event(self, event):
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        # print("event happened:", event)
        # To Observe files only not directories
        if not event.is_directory:
            # To cater for the on_move event
            path = event.src_path
            if hasattr(event, 'dest_path'):
                path = event.dest_path
            # Ensure that the file extension is among the pre-defined ones.
            if path.endswith(self.watchPattern):
                msg = f"{now} -- {event.event_type} -- File: {path}"
                if event.event_type in ('modified', 'created', 'moved'):
                    # check for exceptions in log files
                    if path.endswith(config.LOG_FILES_EXTENSIONS):
                        for type, msg in self.fc.checkForException(event=event, path=path):
                            print_with_color(msg, color=event2color[event.event_type])
                    else:
                        print_with_color(msg, color=event2color[event.event_type])
                else:
                    print_with_color(msg, color=event2color[event.event_type])
        elif self.doWatchDirectories:
            msg = f"{now} -- {event.event_type} -- Folder: {event.src_path}"
            print_with_color(msg, color=event2color[event.event_type])

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass
Класс LogHandler наследует от класса с именем FileSystemEventHandler библиотеки сторожевого приложения и в основном перезаписывает свой метод on_any_event().

Ниже приведены некоторые полезные методы, если этот класс:

on_any_event(): Вызывается на любое мероприятие.
on_created(): вызывается при создании файла или каталога.
on_modified(): вызывается при изменении файла или переименовании каталога.
on_deleted(): вызывается при удалении файла или каталога.
on_moved(): вызывается при перемещении файла или каталога.
Код, выделенный для метода on_any_event(), будет:

Наблюдение за файлами и каталогами.
Убедитесь, что расширение файла, являющегося объектом события, является одним из предопределенных в переменной WATCH_PATTERN в config.py
Создайте сообщение, иллюстрирующее событие или наблюдение, если оно обнаружено.
Теперь давайте напишем наш класс LogWatcher:

class LogWatcher:
    # Initialize the observer
    observer = None
    # Initialize the stop signal variable
    stop_signal = 0
    # The observer is the class that watches for any file system change and then dispatches the event to the event handler.
    def __init__(self, watchDirectory, watchDelay, watchRecursively, watchPattern, doWatchDirectories, exceptionPattern, sessionid, namespace):
        # Initialize variables in relation
        self.watchDirectory = watchDirectory
        self.watchDelay = watchDelay
        self.watchRecursively = watchRecursively
        self.watchPattern = watchPattern
        self.doWatchDirectories = doWatchDirectories
        self.exceptionPattern = exceptionPattern
        self.namespace = namespace
        self.sessionid = sessionid

        # Create an instance of watchdog.observer
        self.observer = Observer()
        # The event handler is an object that will be notified when something happens to the file system.
        self.event_handler = LogHandler(watchPattern, exceptionPattern, self.doWatchDirectories)

    def schedule(self):
        print("Observer Scheduled:", self.observer.name)
        # Call the schedule function via the Observer instance attaching the event
        self.observer.schedule(
            self.event_handler, self.watchDirectory, recursive=self.watchRecursively)

    def start(self):
        print("Observer Started:", self.observer.name)
        self.schedule()
        # Start the observer thread and wait for it to generate events
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Started On: {now} - Related To Session: {self.sessionid}"
        print(msg)

        msg = (
            f"Watching {'Recursively' if self.watchRecursively else 'Non-Recursively'}: {self.watchPattern}"
            f" -- Folder: {self.watchDirectory} -- Every: {self.watchDelay}(sec) -- For Patterns: {self.exceptionPattern}"
        )
        print(msg)
        self.observer.start()

    def run(self):
        print("Observer is running:", self.observer.name)
        self.start()
        try:
            while True:
                time.sleep(self.watchDelay)

                if self.stop_signal == 1:
                    print(
                        f"Observer stopped: {self.observer.name}  stop signal:{self.stop_signal}")
                    self.stop()
                    break
        except:
            self.stop()
        self.observer.join()

    def stop(self):
        print("Observer Stopped:", self.observer.name)

        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Stopped On: {now} - Related To Session: {self.sessionid}"
        print(msg)
        self.observer.stop()
        self.observer.join()

    def info(self):
        info = {
            'observerName': self.observer.name,
            'watchDirectory': self.watchDirectory,
            'watchDelay': self.watchDelay,
            'watchRecursively': self.watchRecursively,
            'watchPattern': self.watchPattern,
        }
        return info
Вот что мы сделали в классе LogWatcher:

Создайте экземпляр класса потока watchdog.observer, наблюдатель следит за любым изменением файловой системы, а затем отправляет соответствующее событие в обработчик событий.
Создайте экземпляр обработчика событий LogHandler, который наследует от FileSystemEventHandler. Обработчик событий уведомляется о любых изменениях.
Назначьте расписание нашему наблюдателю и определите другие входные параметры, такие как каталог для просмотра, режим просмотра и другие. Обратите внимание, что при установке для рекурсивного параметра значения True необходимо убедиться в наличии достаточных прав доступа к вложенным папкам.
Наконец, давайте создадим аргументы командной строки вокруг кода с помощью argparse:

def is_dir_path(path):
    """Utility function to check whether a path is an actual directory"""
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Watchdog script for watching for files & directories' changes")
    parser.add_argument("path",
                        default=config.WATCH_DIRECTORY,
                        type=is_dir_path,
                        )
    parser.add_argument("-d", "--watch-delay",
                        help=f"Watch delay, default is {config.WATCH_DELAY}",
                        default=config.WATCH_DELAY,
                        type=int,
                        )
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        help=f"Whether to recursively watch for the path's children, default is {config.WATCH_RECURSIVELY}",
                        default=config.WATCH_RECURSIVELY,
                        )
    parser.add_argument("-p", "--pattern",
                        help=f"Pattern of files to watch, default is {config.WATCH_PATTERN}",
                        default=config.WATCH_PATTERN,
                        )
    parser.add_argument("--watch-directories",
                        action="store_true",
                        help=f"Whether to watch directories, default is {config.DO_WATCH_DIRECTORIES}",
                        default=config.DO_WATCH_DIRECTORIES,
                        )
    # parse the arguments
    args = parser.parse_args()
    # define & launch the log watcher
    log_watcher = LogWatcher(
        watchDirectory=args.path,
        watchDelay=args.watch_delay,
        watchRecursively=args.recursive,
        watchPattern=tuple(args.pattern.split(",")),
        doWatchDirectories=args.watch_directories,
        exceptionPattern=config.EXCEPTION_PATTERN,
    )
    log_watcher.run()
Мы определили is_dir_path(), чтобы убедиться, что введенный путь является допустимым каталогом. Воспользуемся скриптом:

Запуск сторожевого скрипта с pythonЯ перешел следить за всем, что происходит в каталоге, включая подпапки, я также указал шаблон , для просмотра текстовых и графических файлов.--recursiveE:\watchdog.txt,.log,.jpg,.png

Затем я создал папку и начал писать в текстовый файл, затем переместил изображение и удалил его, сторожевой пес ловит все!

Обратите внимание, что вы можете переопределить параметры в config.py или передать параметры здесь.

Заключение
Я надеюсь, что эта статья помогла вам после того, как мы подробно изучили доступные функции сторожевых и пигтейловых библиотек.

Стоит отметить, что, расширяя описанные функциональные возможности, вы можете связать механизм оповещения или воспроизвести звук всякий раз, когда в одном из ваших файлов журнала возникает фатальная ошибка. При этом при точном обнаружении наблюдения настроенный рабочий процесс или оповещение запускается автоматически.

Вы можете расширить функции, разработанные в этом учебнике, добавив механизм оповещения, основанный на шаблонах, найденных в отслеживаемых файлах; это может быть достигнуто с помощью нескольких механизмов, таких как:

Отправка оповещения по электронной почте с помощью встроенной библиотеки smtplib Python.
Генерация звукового сигнала в Python с помощью библиотеки Simpleaudio.
Отправка уведомлений в Slack с помощью библиотеки knockknock.