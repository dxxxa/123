# [How to Download Files in Python](https://www.thepythoncode.com/article/download-files-python)
To download a file using Python:
- `pip3 install -r requirements.txt`
-
    ```
    python download.py https://download.winzip.com/gl/nkln/winzip24-downwz.exe
    ```
    This will start downloading the file and **outputs** something like this:
    ```
    Downloading winzip24-downwz.exe:   6%|█████▏                                                                         | 779k/11.8M [00:03<00:55, 210kB/s]
    ```
##
# [[] / []]()
Загрузка файлов из Интернета является одной из наиболее распространенных повседневных задач, выполняемых в Интернете. Это важно в связи с тем, что множество успешных программ позволяет своим пользователям скачивать файлы из интернета.

В этом учебнике вы узнаете, как можно загружать файлы по протоколу HTTP в Python с помощью библиотеки запросов.

Связанные с: Как использовать хэш-алгоритмы в Python с помощью hashlib.

Приступим к установке необходимых зависимостей:

pip3 install requests tqdm
Мы собираемся использовать модуль tqdm здесь, чтобы распечатать красивый индикатор выполнения в процессе загрузки.

Откройте новый файл Python и импортируйте:

from tqdm import tqdm
import requests
import cgi
import sys
Мы получим URL-адрес файла из аргументов командной строки:

# the url of file you want to download, passed from command line arguments
url = sys.argv[1]
Теперь метод, который мы собираемся использовать для загрузки контента из Интернета, - это requests.get(),но проблема в том, что он загружает файл немедленно, и мы этого не хотим, так как он застрянет на больших файлах, и память будет заполнена. К счастью для нас, есть атрибут, который мы можем установить в значение True, который является параметром потока:

# read 1024 bytes every time 
buffer_size = 1024
# download the body of response by chunk, not immediately
response = requests.get(url, stream=True)
Теперь загружаются только заголовки ответов, а соединение остается открытым, что позволяет нам контролировать рабочий процесс с помощью метода iter_content(). Прежде чем мы увидим его в действии, нам сначала нужно получить общий размер файла и имя файла:

# get the total file size
file_size = int(response.headers.get("Content-Length", 0))
# get the default filename
default_filename = url.split("/")[-1]
# get the content disposition header
content_disposition = response.headers.get("Content-Disposition")
if content_disposition:
    # parse the header using cgi
    value, params = cgi.parse_header(content_disposition)
    # extract filename from content disposition
    filename = params.get("filename", default_filename)
else:
    # if content dispotion is not available, just use default from URL
    filename = default_filename
Мы получаем размер файла в байтах из заголовка ответа Content-Length, мы также получаем имя файла в заголовке Content-Disposition, но нам нужно разобрать его с помощью функции cgi.parse_header().

Давайте загрузим файл сейчас:

# progress bar, changing the unit to bytes instead of iteration (default by tqdm)
progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for data in progress.iterable:
        # write data read to the file
        f.write(data)
        # update the progress bar manually
        progress.update(len(data))
iter_content() перебирает данные ответа, это позволяет избежать считывания содержимого сразу в память для больших ответов, мы указали buffer_size как количество байтов, которые он должен считывать в память в каждом цикле.

Затем мы обернули итерацию объектом tqdm, который напечатает причудливый индикатор выполнения. Мы также изменили единицу измерения tqdm по умолчанию с итерации на байты.

После этого в каждой итерации мы читаем кусок данных и записываем его в открытый файл, а также обновляем индикатор выполнения.

Вот мой результат после попытки загрузить файл, вы можете выбрать любой файл, который вы хотите, просто убедитесь, что он заканчивается расширением файла (.exe, .pdf и т. Д.):

C:\file-downloader>python download.py https://download.virtualbox.org/virtualbox/6.1.18/VirtualBox-6.1.18-142142-Win.exe
Downloading VirtualBox-6.1.18-142142-Win.exe:   8%|██▍                             | 7.84M/103M [00:06<01:14, 1.35MB/s]
Это работает!

Хорошо, мы закончили, как вы можете видеть, загрузка файлов на Python довольно проста с использованием мощных библиотек, таких как запросы, теперь вы можете использовать это в своих приложениях Python, удачи!

Вот несколько идей, которые вы можете реализовать:

Загрузка всех изображений с веб-страницы.
Скрипт Python для загрузки сжатых архивных файлов из Интернета и их автоматического извлечения.
Кстати, если вы хотите скачать торрент-файлы, проверьте этот туториал.