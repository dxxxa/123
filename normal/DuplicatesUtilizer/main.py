# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html

# Python program to find SHA256 hash string of a file

import os
import time
import shutil
import hashlib
from pathlib import Path
from colorama import Fore, Back, Style

# file_log = "C://Users//nUser/Desktop/filelog.txt"
file_source = "D:\Распред\[.Leak's_dBase]\\Netease Password Database 201603 plaintext & MD5"
destination_of_checked = "D:/Checked/"
destination_of_duplicates = "D:/Duplicates/"


# convert bytes to MB / GB / etc
def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


# return the file size
def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def alotcheck_sha():
    for files in os.listdir(file_source):  # Функция listdir() возвращает список, содержащий имена файлов и директорий
        file_path = os.path.join(file_source, files)  # Конкатенацию пути(file_source) и компонентов(file)
        print("#########################################################################"
              "\nPath:", file_path,
              "\nSize:", file_size(file_path))

        # вычисляет хэш-значение SHA256 файла
        filename = file_path
        sha256_hash = hashlib.sha256()  # для создания хеш-объекта для алгоритма хеширования SHA-256
        with open(filename, "rb") as f:  # rb - Открывает файл в бинарном режиме только для чтения
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            print("Sha256: ", sha256_hash.hexdigest())
            shax = str(sha256_hash.hexdigest())

        with open('filelog.txt') as file_log:
            if shax in file_log.read():
                print(Fore.RED + "\nreMove:", files, Style.RESET_ALL)
                filelog = open("filelog_dupl.txt", "a+", encoding="utf-8")
                filelog.write(shax + "    " + str(filename) + "    " + str(file_size(file_path)) + "\n")
                filelog.close()

                for file in Path(file_source).glob(files):
                    shutil.move(os.path.join(file_source, file), destination_of_duplicates)

            else:
                print(Fore.GREEN + "\nADDing:", files, Style.RESET_ALL)
                filelog = open("filelog.txt", "a+", encoding="utf-8")
                filelog.write(shax + "    " + str(filename) + "    " + str(file_size(file_path)) + "\n")
                filelog.close()

                for file in Path(file_source).glob(files):
                    shutil.move(os.path.join(file_source, file), destination_of_checked)


if __name__ == "__main__":
    start = time.time()
    alotcheck_sha()
    filelog = open("filelog.txt", "a+", encoding="utf-8")
    filelog.write("################################################################\n" * 3)
    filelog.close()
    end = time.time()
    print("\nОбщее время работы:", ('%.3f' % (end - start)), "sec")
