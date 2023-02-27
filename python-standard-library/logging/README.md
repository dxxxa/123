# [Logging in Python](https://www.thepythoncode.com/article/logging-in-python)
##
# [[] / []]()
Ведение журнала позволяет программистам и разработчикам программного обеспечения отслеживать события, которые происходят в их программном обеспечении, оно может не только отслеживать фактическое событие, но и когда оно произошло и в какой функции и даже в какой строке.

Ведение журнала создает подробный набор событий, происходящих в приложении. Например, если где-то в приложении есть ошибка, вы можете легко найти причину проблемы, если в коде правильно настроена регистрация.

Полезные журналы не только помогают нам отлаживать наши ошибки, но и могут оказать нам огромную помощь при попытке понять, что на самом деле делает конкретный код. В этом учебнике вы узнаете, как использовать встроенный модуль ведения журнала в Python.

Вам может быть интересно, почему мы не должны использовать только известную функцию print()? Ну, вы должны использовать его только на небольших скриптах Python, но для более крупных сложных программ он быстро станет беспорядочным, и вы обязательно должны использовать ведение журнала.

Ведение журнала — это более простой способ отслеживать, что делает ваш код. Почти каждое приложение производственного уровня использует этот метод, чтобы отслеживать, какие этапы проходят их приложения.

Модуль ведения журнала
Модуль ведения журнала встроен в стандартную библиотеку Python и является мощным готовым к использованию инструментом для программистов Python, чтобы быстро приступить к ведению журнала. Это также удобный способ, и он используется большинством сторонних библиотек Python.

Модуль ведения журнала поставляется с 5 стандартными уровнями ведения журнала, указывающими на серьезность событий, каждый из которых имеет соответствующий метод, который можно использовать для регистрации событий на этом уровне, в следующей таблице показаны все уровни ведения журнала, а также их числовые значения и когда мы его используем:

Уровень	Числовое значение	Когда он используется
 DEBUG	 10	Подробная информация, например, попытка найти ошибки в вашей программе.
 INFO	 20	Информационные сообщения, которые подтверждают, что все работает по назначению.
 WARNING	 30	Указывая на то, что произошло что-то неожиданное, сообщая о какой-то потенциальной проблеме или предупреждении о деректации.
 ERROR	 40	Указывает, что программное обеспечение не смогло выполнить определенную функцию, но все же позволяет приложению продолжать работать.
 CRITICAL	 50	Серьезная ошибка, которая приведет к остановке работы программы.
Следующая ячейка кода выполняет простое ведение журнала сообщений со всеми уровнями консоли:

import logging

# make a debug message
logging.debug("This is a simple debug log")
# make an info message
logging.info("This is a simple info log")
# make a warning message
logging.warning("This is a simple warning log")
# make an error message
logging.error("This is a simple error log")
# make a critical message
logging.critical("This is a simple critical log")
Выпуск:

WARNING:root:This is a simple warning log
ERROR:root:This is a simple error log
CRITICAL:root:This is a simple critical log
Удивительно, поэтому форматом ведения журнала по умолчанию является уровень, имя регистратора (root по умолчанию) и сообщение. В последующих разделах мы увидим, как изменить этот формат, чтобы добавить больше полезной информации.

Вам может быть интересно, почему сообщения DEBUG и INFO не регистрировались? Ну, это потому, что уровень ведения журнала по умолчанию — ПРЕДУПРЕЖДЕНИЕ:

# just mapping logging level integers into strings for convenience
logging_levels = {
    logging.DEBUG: "DEBUG", # 10
    logging.INFO: "INFO", # 20
    logging.WARNING: "WARNING", # 30
    logging.ERROR: "ERROR", # 40
    logging.CRITICAL: "CRITICAL", # 50
}

# get the current logging level
print("Current logging level:", logging_levels.get(logging.root.level))
Выпуск:

Current logging level: WARNING
Таким образом, используя этот уровень, модуль ведения журнала регистрирует сообщения с уровнем WARNING или выше, единственными сообщениями, которые проходят, являются ПРЕДУПРЕЖДЕНИЕ, ОШИБКА и КРИТИЧЕСКИЙ. Если вы установите для него значение INFO, то INFO, WARNING, ERROR и CRITICAL сообщения будут проходить и так далее.

Следующая строка кода выводит формат ведения журнала по умолчанию:

# get the current logging format
print("Current logging format:", logging.BASIC_FORMAT)
Выпуск:

Current logging format: %(levelname)s:%(name)s:%(message)s
Правильно, поэтому форматом по умолчанию является имя уровня, имя регистратора и фактическое сообщение.

Основные конфигурации
Модуль ведения журнала предоставляет нам полезный метод basicConfig(), который позволяет нам изменять пару параметров во время нашего процесса ведения журнала, он принимает кучу полезных параметров, вот наиболее часто используемые:

имя файла: указывает имя файла для входа, поэтому он будет входить в файл, а не в консоль.
filemode: задает режим открытия файла, по умолчанию используется значение 'a', что означает добавление, 'w' для записи и т.д.
level: Установите уровень корневого средства ведения журнала на указанный уровень, который является ведением журнала. ОТЛАДКА, logging.INFO, ведение журнала. ПРЕДУПРЕЖДЕНИЕ, ведение журнала. ОШИБКА и ведение журнала. КРИТИЧЕСКИЙ.
format: указанная строка формата для средства ведения журнала.
datefmt: формат даты/даты и времени.
обработчики: если указано, это должна быть итерация обработчиков ведения журнала, которые будут добавлены в корневой обработчик.
Изменение уровня ведения журнала
Вы можете легко изменить уровень серьезности с помощью метода basicConfig():

import logging

# make a basic logging configuration
# here we set the level of logging to DEBUG
logging.basicConfig(
    level=logging.DEBUG
)

# make a debug message
logging.debug("This is a simple debug log")
# make an info message
logging.info("This is a simple info log")
# make a warning message
logging.warning("This is a simple warning log")
# make an error message
logging.error("This is a simple error log")
# make a critical message
logging.critical("This is a simple critical log")
И действительно, теперь все сообщения будут доходить:

DEBUG:root:This is a simple debug log
INFO:root:This is a simple info log        
WARNING:root:This is a simple warning log  
ERROR:root:This is a simple error log      
CRITICAL:root:This is a simple critical log
Изменение формата ведения журнала
Мы можем изменить формат ведения журнала, установив для параметра format значение метода basicConfig():

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("This is an info message!")
Выпуск:

2020-10-10 19:26:19,908 - INFO - This is an info message!
Замечательно! Теперь у нас есть дата-время в нашем сообщении журнала. Обратите внимание, что мы использовали атрибут %(asctime)s для получения даты и времени, %(levelname)s для получения имени уровня и %(message)s для получения фактического сообщения журнала.

Есть много других атрибутов, вот некоторые из самых важных:

%(funcName)s: имя функции, содержащей вызов журнала.
%(lineno)d: номер исходной строки, в которой был выдан вызов журнала (если имеется).
%(модуль)s: Имя модуля.
%(name)s: имя фактического средства ведения журнала, используемого для регистрации вызова.
%(process)d: идентификатор процесса (при наличии).
Пожалуйста, проверьте эту ссылку, чтобы получить все доступные атрибуты LogRecord.

Если вы хотите изменить формат даты, то вам также следует изменить параметр datefmt:

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="[%Y-%m-%d] %H:%M:%S",
)

logging.info("This is an info message!")
Коды форматов одинаковы для методов time.strftime() и time.strptime(), список можно найти здесь.

Выпуск:

[2020-10-10] 19:33:23 - INFO - This is an info message!
Удивительно, теперь давайте испачкаем руки на примере!

Пример
Приведенный ниже рецепт является хорошим примером использования модуля ведения журнала в Python:

import logging
import math

logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler('logs.log', 'a', 'utf-8')],
                    format="%(asctime)s %(levelname)-6s - %(funcName)-8s - %(filename)s - %(lineno)-3d - %(message)s",
                    datefmt="[%Y-%m-%d] %H:%M:%S - ",
                    )

logging.info("This is an info log")

def square_root(x):
    logging.debug(f"Getting the square root of {x}") 
    try:
        result = math.sqrt(x)
    except ValueError:
        logging.exception("Cannot get square root of a negative number")
        # or
        # logging.error("Cannot get square root of a negative number", exc_info=True)
        return None
    logging.info(f"The square root of {x} is {result:.5f}")
    return result

square_root(5)
square_root(-5)
В этом примере мы использовали параметр handlers для передачи списка обработчиков ведения журнала, мы указали FileHandler, который ведет журналы в журналы.log файл с режимом добавления и кодировкой UTF-8.

После выполнения приведенного выше кода, вот результирующий файл logs.log:

[2020-10-10] 19:44:49 -  INFO   - <module> - logger_file.py - 10  - This is an info log
[2020-10-10] 19:44:49 -  DEBUG  - square_root - logger_file.py - 13  - Getting the square root of 5
[2020-10-10] 19:44:49 -  INFO   - square_root - logger_file.py - 21  - The square root of 5 is 2.23607
[2020-10-10] 19:44:49 -  DEBUG  - square_root - logger_file.py - 13  - Getting the square root of -5
[2020-10-10] 19:44:49 -  ERROR  - square_root - logger_file.py - 17  - Cannot get square root of a negative number
Traceback (most recent call last):
  File "c:/pythoncode-tutorials/python-standard-library/logging/logger_file.py", line 15, in square_root
    result = math.sqrt(x)
ValueError: math domain error
Удивительно, мы указали имя функции, а также номер строки события, обратите внимание, когда ведение журнала не находится в функции, токен <module> будет индикатором того, что он находится на уровне модуля (не в какой-либо функции).

Функция toy square_root(), которую мы использовали, перехватывает ValueError, который возникает всякий раз, когда мы передаем отрицательное значение, мы использовали функцию logging.exception() для включения трассировки ошибок в файл журнала, это то же самое, что и использование функции logging.error() с exc_info задано значение True.

Использование обработчиков
До сих пор мы использовали ведение журнала на уровне модулей, но что, если мы хотим использовать несколько регистраторов для разных целей? Вот где обработчики вступают в игру.

Мы используем обработчики журналов, когда хотим настроить наши собственные регистраторы и отправить журналы в несколько мест. Мы можем использовать обработчики для отправки сообщений журнала в стандартный вывод, файл или даже по протоколу HTTP.

В следующем примере извлекается объект средства ведения журнала с помощью метода logging.getLogger() и добавляется к нему обработчик:

import logging

# return a logger with the specified name & creating it if necessary
logger = logging.getLogger(__name__)

# create a logger handler, in this case: file handler
file_handler = logging.FileHandler("file.log")
# set the level of logging to INFO
file_handler.setLevel(logging.INFO)

# create a logger formatter
logging_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# add the format to the logger handler
file_handler.setFormatter(logging_format)

# add the handler to the logger
logger.addHandler(file_handler)

# use the logger as previously
logger.critical("This is a critical message!")
Мы также устанавливаем модуль форматирования для обработчика файлов с помощью метода setFormatter(), вот выходные данные файла.log файла:

2020-10-10 20:00:16,019 - CRITICAL - This is a critical message!
Заключение
Удивительно, теперь, надеюсь, вы начнете использовать вход в свои программы Python вместо обычной функции print(), я настоятельно рекомендую вам проверить учебник из документации Python для получения более подробной информации.

В качестве упражнения я предлагаю вам проверить приведенный ниже код учебников и добавить операторы ведения журнала в тех местах, где, по вашему мнению, это полезно:

Как передавать файлы в сети с помощью сокетов в Python.
Как создать обратную оболочку в Python.
Извлечение и отправка веб-форм из URL-адреса с помощью Python.
Как читать электронные письма в Python
Узнайте также: Как использовать регулярные выражения в Python.