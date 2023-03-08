# Removing_duplicate_files.py # Удаление дубликатов файлов
# https://bestprogrammer.ru/programmirovanie-i-razrabotka/udalenie-dublikatov-fajlov-s-pomoshhyu-python

from tkinter.filedialog import askdirectory

# Importing required libraries. # Импорт библиотек
from tkinter import Tk  # Для возможности выбрать папку (диалоговое окно)
import os  # Для удаления дубликатов, предоставляя функции для извлечения содержимого файлов, удаления файлов и т. д.
import hashlib  # Для использования хеш-функцию md5
from pathlib import Path

# We don't want the GUI window of tkinter to be appearing on our screen
Tk().withdraw()  # Открывает диалоговое окно на экране

# Dialog box for selecting a folder.
file_path = askdirectory(title="Select a folder")  # Окно выбора папки

# Listing out all the files inside our root folder.
list_of_files = os.walk(file_path)  # Перечисление всех файлов в нашей корневой папке

# In order to detect the duplicate files we are going to define an empty dictionary.
unique_files = dict()

for root, folders, files in list_of_files:
    # Running a for loop on all the files
    for file in files:
        # Finding complete file path
        file_path = Path(os.path.join(root, file))
        # Converting all the content of our file into md5 hash.
        Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        print(file_path, Hash_file)
        # If file hash has already been added we'll simply delete that file
        if Hash_file not in unique_files:
            unique_files[Hash_file] = file_path
        else:
            os.remove(file_path)
            print(f"{file_path} has been deleted")