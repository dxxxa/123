# [How to Download and Upload Files in FTP Server using Python](https://www.thepythoncode.com/article/download-and-upload-files-in-ftp-server-using-python)
- To upload a file to a FTP server, consider editing `ftp_file_uploader.py` on your needs and run it.
- To download a file, same in `ftp_file_downloader.py`
##
# [[] / []]()
Одной из основных особенностей FTP-сервера является возможность хранения и извлечения файлов. В этом учебнике вы узнаете, как можно загружать и загружать файлы на FTP-сервер с помощью Python.

Мы будем использовать встроенный модуль ftplib Python, мы собираемся использовать тестовый FTP-сервер для этого учебника, он называется DLPTEST, давайте определим его информацию:

import ftplib

FTP_HOST = "ftp.dlptest.com"
FTP_USER = "dlpuser@dlptest.com"
FTP_PASS = "SzMf7rTE4pCrf9dV286GuNe4N"
Пароль может меняться время от времени. Убедитесь, что вы посещаете их веб-сайт для получения правильных учетных данных, подключаясь к этому серверу:

# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"
Загрузка файлов
Чтобы загрузить файл, нам нужно будет использовать метод ftp.storbinary(), приведенный ниже код обрабатывает это:

# local file name you want to upload
filename = "some_file.txt"
with open(filename, "rb") as file:
    # use FTP's STOR command to upload the file
    ftp.storbinary(f"STOR {filename}", file)
Мы открыли файл в режиме "rb", что означает, что мы читаем локальный файл в двоичном режиме.

После этого мы использовали команду STOR FTP, которая хранит файл в двоичном режиме, он передает этот файл на новый порт. Обратите внимание, что файл должен существовать в локальном рабочем каталоге, иначе это не сработает.

Этот тестовый сервер удалит файл через 30 минут,чтобы убедиться, что файл успешно загружен, нам нужно перечислить все файлы и каталоги с помощью метода ftp.dir():

# list current files & directories
ftp.dir()
Конечно, файл есть:

drwxr-xr-x    2 dlptest9   dlptest9        40960 Apr 11 07:04 .
drwxr-xr-x    2 dlptest9   dlptest9        40960 Apr 11 07:04 ..
-rw-r--r--    1 dlptest9   dlptest9          172 Apr 11 07:00 357299070163503-2020-04-11-11-59.txt
-rw-r--r--    1 dlptest9   dlptest9          171 Apr 11 07:01 357299070163503-2020-04-11-12-00.txt
-rw-r--r--    1 dlptest9   dlptest9          171 Apr 11 07:02 357299070163503-2020-04-11-12-01.txt
-rw-r--r--    1 dlptest9   dlptest9          171 Apr 11 07:03 357299070163503-2020-04-11-12-02.txt
-rw-r--r--    1 dlptest9   dlptest9           20 Apr 11 07:04 some_file.txt
-rw-r--r--    1 dlptest9   dlptest9           24 Apr 11 07:00 syslogtest_be.txt
Загрузка файлов
Теперь давайте попробуем загрузить тот же файл еще раз:

# the name of file you want to download from the FTP server
filename = "some_file.txt"
with open(filename, "wb") as file:
    # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {filename}", file.write)
На этот раз мы открываем локальный файл в режиме «wb», так как мы собираемся записать файл с сервера на локальную машину.

Мы используем команду RETR, которая загружает копию файла на сервер, мы предоставляем имя файла, которое мы хотим загрузить в качестве первого аргумента для команды, и сервер отправит нам копию файла.

Метод ftp.retrbinary() принимает метод, вызываемый при хранении файла на локальном компьютере, в качестве второго аргумента.

Если вы удалили этот файл и выполнили приведенный выше код, вы увидите, что файл появится снова; мы успешно скачали файл!

Наконец, вы должны выйти и закрыть FTP-соединение:

# quit and close the connection
ftp.quit()
Хорошо, мы закончили с учебником, я разделил код для загрузки и загрузки скриптов, проверьте их здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python, удачи!

Связанные с: Как перечислить все файлы и каталоги на FTP-сервере с помощью Python.