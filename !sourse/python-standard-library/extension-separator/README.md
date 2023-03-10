# [How to Organize Files by Extension in Python](https://www.thepythoncode.com/article/organize-files-by-extension-with-python)
##
# [[] / []]()
Организация файлов на вашем компьютере может быть утомительной задачей, особенно когда вы делаете это вручную, некоторые папки (например, папка «Загрузки») на вашем компьютере слишком грязные, что вы даже не можете там искать. В этом уроке вы будете участвовать в Python, чтобы организовать файлы по расширению в любой папке на вашем компьютере.

Без лишних слов, давайте начнем. Нам не нужна какая-либо библиотека для установки, так как мы будем использовать стандартную библиотеку Python. Импорт их:

import os
import glob
import shutil
Мы будем использовать функцию shutil.move() из модуля shutil для перемещения файлов, и нам также нужен glob, чтобы получить список совпадающих файлов с помощью regex. Мы также используем модуль OS для обработки имен файлов.

Поскольку мы собираемся упорядочить файлы по расширению, имеет смысл поместить файлы одного типа (например, mp3, wav) в одну папку (например, «аудио»), ниже словарь Python сопоставляет каждое расширение с типом, не стесняйтесь редактировать по вашим потребностям:

# dictionary mapping each extension with its corresponding folder
# For example, 'jpg', 'png', 'ico', 'gif', 'svg' files will be moved to 'images' folder
# feel free to change based on your needs
extensions = {
    "jpg": "images",
    "png": "images",
    "ico": "images",
    "gif": "images",
    "svg": "images",
    "sql": "sql",
    "exe": "programs",
    "msi": "programs",
    "pdf": "pdf",
    "xlsx": "excel",
    "csv": "excel",
    "rar": "archive",
    "zip": "archive",
    "gz": "archive",
    "tar": "archive",
    "docx": "word",
    "torrent": "torrent",
    "txt": "text",
    "ipynb": "python",
    "py": "python",
    "pptx": "powerpoint",
    "ppt": "powerpoint",
    "mp3": "audio",
    "wav": "audio",
    "mp4": "video",
    "m3u8": "video",
    "webm": "video",
    "ts": "video",
    "json": "json",
    "css": "web",
    "js": "web",
    "html": "web",
    "apk": "apk",
    "sqlite3": "sqlite3",
}
Например, файлы mp4 и m3u8 будут перемещены в папку с именем video, файлы JSON будут иметь свою собственную папку и т. Д. Это далеко не полный список расширений, поэтому вам придется добавить больше в вашем случае.

Теперь перейдем к коду:

    path = r"E:\Downloads"
    # setting verbose to 1 (or True) will show all file moves
    # setting verbose to 0 (or False) will show basic necessary info
    verbose = 0
    for extension, folder_name in extensions.items():
        # get all the files matching the extension
        files = glob.glob(os.path.join(path, f"*.{extension}"))
        print(f"[*] Found {len(files)} files with {extension} extension")
        if not os.path.isdir(os.path.join(path, folder_name)) and files:
            # create the folder if it does not exist before
            print(f"[+] Making {folder_name} folder")
            os.mkdir(os.path.join(path, folder_name))
        for file in files:
            # for each file in that extension, move it to the correponding folder
            basename = os.path.basename(file)
            dst = os.path.join(path, folder_name, basename)
            if verbose:
                print(f"[*] Moving {file} to {dst}")
            shutil.move(file, dst)
Мы перебираем наш словарь, который сопоставляет каждое расширение с типом файлов, мы получаем список файлов каждого расширения и перемещаем их в соответствующую папку. Мы также создаем папку с помощью функции os.mkdir(), если она не существует ранее.

Переменная path — это путь к папке, которую вы хотите упорядочить, вы можете использовать модули sys или argparse для передачи пути к папке в аргументах командной строки.

Это часть моей папки «Загрузки»:

перед организациейСлишком грязные, файлы с разными типами, и если я хочу искать конкретный файл, но не знаю точного имени, мне нужно будет много прокручивать.

Давайте запустим его:

$ python extension_separator.py
Выпуск:

[*] Found 17 files with jpg extension
[+] Making images folder
[*] Found 6 files with png extension
[*] Found 0 files with ico extension
[*] Found 0 files with gif extension
[*] Found 0 files with svg extension
[*] Found 3 files with sql extension
[+] Making sql folder
[*] Found 0 files with exe extension
[*] Found 3 files with msi extension
[+] Making programs folder
[*] Found 38 files with pdf extension
[+] Making pdf folder
[*] Found 7 files with xlsx extension
[+] Making excel folder
[*] Found 9 files with csv extension
[*] Found 2 files with rar extension
[+] Making archive folder
[*] Found 9 files with zip extension
[*] Found 2 files with gz extension
[*] Found 0 files with tar extension
[*] Found 5 files with docx extension
[+] Making word folder
[*] Found 11 files with torrent extension
[+] Making torrent folder
[*] Found 2 files with txt extension
[+] Making text folder
[*] Found 5 files with ipynb extension
[+] Making python folder
[*] Found 4 files with py extension
[*] Found 0 files with pptx extension
[*] Found 0 files with ppt extension
[*] Found 0 files with mp3 extension
[*] Found 0 files with wav extension
[*] Found 1 files with mp4 extension
[+] Making video folder
[*] Found 0 files with m3u8 extension
[*] Found 1 files with webm extension
[*] Found 0 files with ts extension
[*] Found 11 files with json extension
[+] Making json folder
[*] Found 0 files with css extension
[*] Found 0 files with js extension
[*] Found 0 files with html extension
[*] Found 0 files with apk extension
[*] Found 0 files with sqlite3 extension
Если вы установите для параметра подробное значение 1, вы получите все движущиеся файлы в выходных данных. Это папка после запуска скрипта Python:

Папка после упорядочиванияЗаключение
Теперь я знаю, что если я хочу искать файл, я просто перехожу к его типу и найду его там, или, если я хочу удалить бесполезные файлы, теперь это намного проще.

Хорошо, вот и все для этого урока, я надеюсь, что это был полезный и удобный код для вас, чтобы организовать свои папки!

Проверьте полный код здесь.