# [How to List all Files and Directories in FTP Server using Python](https://www.thepythoncode.com/article/list-files-and-directories-in-ftp-server-in-python)
##
# [[] / []]()
FTP (File Transfer Protocol) является стандартным сетевым протоколом, который позволяет компьютерам передавать файлы по сети. В этом уроке вы узнаете, как вы можете подключиться к FTP-серверу и перечислить все файлы и каталоги на нем, вы также познакомитесь со встроенным модулем ftplib Python и некоторыми из его методов.

ftplib поставляется с предустановленным Python, поэтому, если у вас есть Python, установленный на вашем компьютере, вы готовы к работе. Откройте новый файл Python и следуйте за ним, давайте импортируем необходимый модуль для учебника:

import ftplib
import os
from datetime import datetime
На обычном FTP-сервере вам нужны учетные данные (имя пользователя и пароль), чтобы правильно войти в один из них, но для этого урока мы будем использовать FTP-сервер Эдинбургского университета, который позволяет пользователям анонимно входить в систему:

FTP_HOST = "ftp.ed.ac.uk"
FTP_USER = "anonymous"
FTP_PASS = ""
Ниже приведены служебные функции, которые помогут нам позже распечатать наш список файлов и каталогов:

# some utility functions that we gonna need
def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024

def get_datetime_format(date_time):
    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human readable date time string
    return date_time.strftime("%Y/%m/%d %H:%M:%S")
Функция get_size_format() была взята из этого учебника, она в основном преобразует размер файлов из байтов в более удобочитаемый формат, такой как 1,3 МБ, 103,5 КБ и т. Д. Функция get_datetime_format() также преобразует дату-время в более читаемый формат.

Теперь подключимся к нашему серверу с помощью клиентского класса FTP():

# initialize FTP session
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
При написании кода этого учебника я столкнулся с некоторыми проблемами при работе с нелатинскими символами, так как Python использует ISO-8859-1 в качестве кодировки по умолчанию, в результате давайте изменим кодировку на UTF-8:

# force UTF-8 encoding
ftp.encoding = "utf-8"
Теперь, когда мы находимся внутри сервера, давайте распечатаем приветственное сообщение, которое отправляется сервером после подключения:

# print the welcome message
print(ftp.getwelcome())
Вот выходные данные для этого сервера:

         Welcome to the University of Edinburgh Anonymous FTP server        
 ===========================================================================

  When requested for a username enter 'ftp' or 'anonymous'.  If you have    
  problems, try using a dash (-) as the first character of your password.   
  If you still have problems or wish to make a comment then send email to   
  ftpmaster@ed.ac.uk.

  All transfers are logged.
220 FTP Server
Давайте начнем вызывать некоторые команды, первый метод, который мы будем использовать, это cwd(), который изменяет текущий рабочий каталог, поскольку мы находимся в корневом каталоге, давайте перейдем к некоторому каталогу, в котором есть некоторые файлы внутри:

# change the current working directory to 'pub' folder and 'maps' subfolder
ftp.cwd("pub/maps")
Список файлов и каталогов:

# LIST a directory
print("*"*50, "LIST", "*"*50)
ftp.dir()
Вот часть выходных данных:

************************************************** LIST **************************************************
-rw-r--r--   1 1407     bin         25175 Jul  8  1991 JIPS-map.910704-1.ps.Z
-rw-r--r--   1 1407     bin         25714 Jul 30  1991 JIPS-map.910730-1.ps.Z
-rw-r--r--   1 1407     bin         25980 Aug  2  1991 JIPS-map.910802-1.ps.Z
-rw-r--r--   1 1407     bin         26812 Aug  7  1991 JIPS-map.910806-1.ps.Z
-rw-r--r--   1 1407     bin         26673 Oct 11  1991 JIPS-map.911011-1.ps.Z
...<SNIPPED>...
Очень похоже на вывод, предоставляемый командой ls. Однако для этого используется команда LIST FTP, которая к настоящему времени устарела. Кроме того, как вы, возможно, уже заметили, он не возвращает никакого значения, он просто выводит на экран каталоги и файлы в текущем рабочем каталоге.

Другой альтернативой является использование команды NLST:

# NLST command
print("*"*50, "NLST", "*"*50)
print("{:20} {}".format("File Name", "File Size"))
for file_name in ftp.nlst():
    file_size = "N/A"
    try:
        ftp.cwd(file_name)
    except Exception as e:
        ftp.voidcmd("TYPE I")
        file_size = get_size_format(ftp.size(file_name))
    print(f"{file_name:20} {file_size}")
Выпуск:

************************************************** NLST **************************************************
File Name            File Size
backbone.t3-ps.Z     23.39KB
backbone.t1t3-ps.Z   24.56KB
ripe-map06-netnums.ps.Z 29.54KB
edlana4bw.ps.Z       63.34KB
...<SNIPPED>...
Но, как вы можете видеть, команда NLST возвращает только имена файлов и каталогов, ничего больше, мы хотим что-то, что предоставляет нам список имен, а также их метаданные, такие как разрешения, размер, дата последнего изменения и т. Д.

Здесь мы используем команду MLSD, которая приходит на помощь:

print("*"*50, "MLSD", "*"*50)
# using the MLSD command
print("{:30} {:19} {:6} {:5} {:4} {:4} {:4} {}".format("File Name", "Last Modified", "Size",
                                                    "Perm","Type", "GRP", "MODE", "OWNER"))
for file_data in ftp.mlsd():
    # extract returning data
    file_name, meta = file_data
    # i.e directory, file or link, etc
    file_type = meta.get("type")
    if file_type == "file":
        # if it is a file, change type of transfer data to IMAGE/binary
        ftp.voidcmd("TYPE I")
        # get the file size in bytes
        file_size = ftp.size(file_name)
        # convert it to human readable format (i.e in 'KB', 'MB', etc)
        file_size = get_size_format(file_size)
    else:
        # not a file, may be a directory or other types
        file_size = "N/A"
    # date of last modification of the file
    last_modified = get_datetime_format(meta.get("modify"))
    # file permissions
    permission = meta.get("perm")
    
    # get the file unique id
    unique_id = meta.get("unique")
    # user group
    unix_group = meta.get("unix.group")
    # file mode, unix permissions 
    unix_mode = meta.get("unix.mode")
    # owner of the file
    unix_owner = meta.get("unix.owner")
    # print all
    print(f"{file_name:30} {last_modified} {file_size:7} {permission:5} {file_type:4} {unix_group:4} {unix_mode:4} {unix_owner}")
Мы использовали метод mlsd(), который вызывает команду MLSD FTP, он возвращает кортеж, содержащий имя файла и метаданные файла, мы извлекли все и распечатали их на экране. Обратите внимание, что я использовал команду TYPE I для изменения типа передачи в двоичное изображение, это потому, что size() вызовет исключение, если это не так.

Мы также использовали нашу ранее определенную функцию get_datetime_format() для преобразования даты, возвращенной FTP-сервером, в более удобочитаемый формат, вот усеченный вывод приведенного выше рецепта:

************************************************** MLSD **************************************************
File Name                      Last Modified       Size   Perm  Type GRP  MODE OWNER
backbone.t3-ps.Z               1991/07/30 11:28:13 23.39KB adfr  file 1    0644 1407
backbone.t1t3-ps.Z             1991/07/30 11:28:41 24.56KB adfr  file 1    0644 1407
ripe-map06-netnums.ps.Z        1991/07/08 09:57:23 29.54KB adfr  file 1    0644 1407
edlana4bw.ps.Z                 1992/06/17 13:30:40 63.34KB adfr  file 2005 0644 1407
...<SNIPPED>...
Команда MLSD является текущим стандартом FTP форматирования списков каталогов, она была введена в RFC 3659.

Наконец, после работы с FTP-сервером, пришло время выйти и закрыть соединение:

# quit and close the connection
ftp.quit()
Хорошо, вот и все для учебника. Вы не должны использовать команду LIST (используя метод dir() в Python) сейчас, MLSD - это путь, хотя некоторые FTP-серверы все еще не поддерживают MLSD, команда NLST по-прежнему является альтернативой.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python, удачи!

Связанные с: Как загружать и загружать файлы на FTP-сервере с помощью Python.