# [How to Download Torrent Files in Python](https://www.thepythoncode.com/article/download-torrent-files-in-python)
To run this:
- Install [qBittorrent client](https://www.qbittorrent.org/download.php) for your operating system.
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Вы когда-нибудь хотели скачать файлы в торренте программным путем? Ну, в этом уроке вы узнаете, как вы можете загружать файлы в торренте с помощью Python.

Мы будем использовать qBittorrent здесь, это потому, что для него есть классная оболочка Python, которая облегчает все для нас.

Для начала работы необходимо загрузить и установить официальный клиент qBittorent для вашей операционной системы, а затем установить модуль оболочки Python с помощью следующей команды:

pip3 install python-qbittorrent
Теперь, прежде чем мы углубимся в код, нам нужно установить некоторые конфигурации, после установки клиента qBittorent вам нужно включить веб-интерфейс qBittorrent, выполнив следующие шаги:

Как только у вас все будет установлено, запустите qBittorrent. В строке меню выберите Инструменты > Параметры qBittorrent WEB UI.
Когда появится новое окно, выберите параметр Веб-интерфейс.
Установите флажок "Веб-интерфейс пользователя (пульт дистанционного управления)".
Вы можете выбрать порт (по умолчанию 8080).
Установите имя пользователя и пароль (по умолчанию admin:adminadmin).
Следующее изображение должно прояснить все:

Включение веб-интерфейса qBittorrentТеперь, когда мы включили веб-интерфейс, вы можете зайти в браузер и увидеть веб-версию qBittorrent, используя адрес «127.0.0.1:8080». Вы увидите небольшую страницу входа в систему следующим образом:

запрос на вход в веб-интерфейс qBittorrent

Поместите учетные данные, которые вы установили в конфигурацию, а затем войдите в систему, теперь вы должны быть готовы увидеть веб-интерфейс qBittorrent:

Версия веб-интерфейса qBittorrentЕсли вы здесь, то поздравляем! Теперь вы готовы использовать Python для загрузки торрент-файлов, открытия нового файла Python (или интерактивной оболочки Python) и импорта модуля qBittorrent:

from qbittorrent import Client
Теперь давайте подключимся и войдите в веб-интерфейс:

# connect to the qbittorent Web UI
qb = Client("http://127.0.0.1:8080/")

# put the credentials (as you configured)
qb.login("admin", "adminadmin")
Я выбрал этот торрент-файл для этого урока, пожалуйста, не стесняйтесь использовать любой торрент-файл, который вы хотите (просто поместите его в свой текущий рабочий каталог и измените имя):

# open the torrent file of the file you wanna download
torrent_file = open("debian-10.2.0-amd64-netinst.iso.torrent", "rb")
Заметка: Если вы не уверены, что делает функция open(), проверьте этот учебник.

Начнем скачивать:

# start downloading
qb.download_from_file(torrent_file)
Если вы выполняете эту ячейку за ячейкой в интерактивном окне, вы сразу увидите, что новый торрент-файл появляется как в веб-интерфейсе, так и в клиенте рабочего стола qBittorrent, как показано на следующем рисунке:

Начать загрузку торрент-файла

Удивительно, вы можете использовать параметр savepath для сохранения результирующего файла по пути, который вы действительно хотите:

# you can specify the save path for downloads
qb.download_from_file(torrent_file, savepath="/the/path/you/want/to/save")
Вы также можете использовать метод download_from_link(), который принимает URL-адрес магнита, который вы хотите загрузить:

# this magnet is not valid, replace with yours
magnet_link = "magnet:?xt=urn:btih:e334ab9ddd91c10938a7....."
qb.download_from_link(magnet_link)
Вы также можете делать различные вещи, например, давайте приостановим все торренты в клиенте:

# pause all downloads
qb.pause_all()
Или вы можете возобновить их:

# resume them
qb.resume_all()
Или даже перечислить их и показать некоторую полезную информацию:

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

# return list of torrents
torrents = qb.torrents()

for torrent in torrents:
    print("Torrent name:", torrent["name"])
    print("hash:", torrent["hash"])
    print("Seeds:", torrent["num_seeds"])
    print("File size:", get_size_format(torrent["total_size"]))
    print("Download speed:", get_size_format(torrent["dlspeed"]) + "/s")
Вот мой вывод:

Torrent name: debian-10.2.0-amd64-netinst.iso
hash: 86d4c80024a469be4c50bc5a102cf71780310074
Seeds: 70
File size: 335.00MB
Download speed: 606.15KB/s
Вы также можете приостановить и возобновить определенные торрент-файлы, используя их хэш-значение, эта оболочка богата полезными методами, пожалуйста, проверьте их полную документацию по методу API и репозиторий GitHub.

Хорошо, вот и все для этого урока. Это сделает вас открытым для многих классных задач, вот пример вызова:

Получение всех ссылок на сайт и извлечение только торрент-файлов, а затем загрузка файлов только с .torrent расширениями и после этого, запуск их для загрузки в qBittorrent, довольно аккуратно, верно? Дерзайте.
Кстати, если вы хотите использовать оболочку Python для клиента uTorrent, этот репозиторий может помочь.

Хотите узнать больше?
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python, удачи!