import os
import time
import datetime

import pathlib
import hashlib

import psycopg2
from psycopg2 import Error

import shutil
from colorama import Fore, Style


#source = "E:\[.Leak's_dBase]\Collection #1-5 & Antipublic"
destination_of_unique = "E:\\Unique"
#destination_of_duplicates = "E:\\Duplicates"
source = "E:\\BreachCompilation2"
destination_of_duplicates = "E:\\Duplicates"

MASTER_PWD_HASH = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"

DB_HOST = "127.0.0.1"
DB_PORT = "5432"

DB_UserNAME = "postgres"  # ИМЯ ПОЛЬЗОВАТЕЛЯ # "postgres" by default
DB_PWD = "Qwerty123456!"  # ПАРОЛЬ ОТ БАЗЫ ДАННЫХ

DB_NAME = "qqq"  # ИМЯ БАЗЫ ДАННЫХ
DB_TABLE_NAME = 'qqqtable'  # ИМЯ ТАБЛИЦЫ БД # Ex: 'public."Table"'
SALT = b""  # Можно помещать сюда любую двоичную строку Ex: b". Y\x20\xBF\x045\xAC"


# convert bytes to MB / GB / etc
def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


# return the file size
def file_size_x(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


# Creating TABLEs PostgreSQL из Python
def option0():
    print("\nCreate TABLEs (unique_files/duplicates_files) PostgreSQL")
    try:
        # Connection to DATA BASE
        connection = psycopg2.connect(user=DB_UserNAME,
                                      password=DB_PWD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)

        cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

        # SQL-запрос для создания таблицы unique_files
        query_create_table = '''CREATE TABLE unique_files
                                      (ID SERIAL PRIMARY KEY     NOT NULL,
                                      SHA256           VARCHAR(64)    NOT NULL,
                                      NAME           TEXT    NOT NULL,
                                      SIZE           TEXT    NOT NULL,
                                      PATH           TEXT    NOT NULL,
                                      COMMENT           TEXT    NOT NULL,
                                      EXTENSION           TEXT    NOT NULL,
                                      DATEMODIFICATION           DATE    NOT NULL,
                                      DATECREATION          DATE    NOT NULL,
                                      DATEADDED           DATE    NOT NULL); '''

        # Выполнение команды: создает новую таблицу unique_files
        cursor.execute(query_create_table)
        connection.commit()
        print("!Completed CREATE TABLE unique_files!")

        # SQL-запрос для создания таблицы duplicates_files
        query_create_table = '''CREATE TABLE duplicates_files
                                      (ID SERIAL PRIMARY KEY     NOT NULL,
                                      SHA256           VARCHAR(64)    NOT NULL,
                                      NAME           TEXT    NOT NULL,
                                      SIZE           TEXT    NOT NULL,
                                      PATH           TEXT    NOT NULL,
                                      COMMENT           TEXT    NOT NULL,
                                      EXTENSION           TEXT    NOT NULL,
                                      DATEMODIFICATION           DATE    NOT NULL,
                                      DATECREATION          DATE    NOT NULL,
                                      DATEADDED           DATE    NOT NULL); '''

        # Выполнение команды: создает новую таблицу duplicates_files
        cursor.execute(query_create_table)
        connection.commit()
        print("!Completed CREATE TABLE duplicates_files!")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        print("Соединение с PostgreSQL закрыто")


def option1():
    print("\n1. SQL HASH(SHA256) Files Manager")
    user_master = input("Enter Master Password: ").encode()
    if hashlib.sha256(user_master).hexdigest() == MASTER_PWD_HASH:
        comment = input("Comment to file_source: ")
        start = time.time()

        for src_dir, dirs, files in os.walk(source):

            dst_of_unique = src_dir.replace(source, destination_of_unique, 1)
            #print(dst_of_unique)
            if not os.path.exists(dst_of_unique):
                os.makedirs(dst_of_unique)

            dst_of_duplicates = src_dir.replace(source, destination_of_duplicates, 1)
            #print(dst_of_duplicates)
            if not os.path.exists(dst_of_duplicates):
                os.makedirs(dst_of_duplicates)

            for file_name in files:
                file_source = src_dir
                file_path = os.path.join(src_dir, file_name)  # Path+FileName Source

                print("Path_Source:", file_source)
                print("File_Name:", file_name)
                print("File_Path:", file_path)

                dst_file_of_unique = os.path.join(dst_of_unique, file_name)  # Path+FileName Unique

                dst_file_of_duplicates = os.path.join(dst_of_duplicates, file_name)  # Path+FileName Duplicates

                # function to return the file hash(sha256)
                sha256_hash = hashlib.sha256()  # для создания хеш-объекта для алгоритма хеширования SHA-256
                with open(file_path, "rb") as f:  # rb - Открывает файл в бинарном режиме только для чтения
                    # Read and update hash string value in blocks of 4K
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                    file_hash = sha256_hash.hexdigest()
                    print("Sha256:", file_hash)

                # function to return the file extension
                file_extension = pathlib.Path(file_path).suffix
                print("File_Extension:", file_extension)

                # function to return the file size
                file_size = file_size_x(file_path)
                print("File_Size:", file_size)

                # function to return the file Date/Time modification
                file_time_modification = os.path.getmtime(file_path)
                file_date_modification = datetime.datetime.fromtimestamp(file_time_modification)  # convert time into DateTime
                print("Date/Time Modified:", file_date_modification)

                # function to return the file Date/Time creation
                file_time_creation = os.path.getctime(file_path)
                file_date_creation = datetime.datetime.fromtimestamp(file_time_creation)  # convert time into DateTime
                print("Date/Time Created:", file_date_creation)

                # function to return the present Date/Time
                present_date_time = datetime.datetime.now()
                print("Date/Time Present:", present_date_time)

                # Переменные для DATA BASE
                sha256 = file_hash
                name = file_name
                size = file_size
                path = file_path
                path_unique = dst_file_of_unique
                path_duplicates = dst_file_of_duplicates
                comment = comment
                extension = file_extension
                datemodification = file_date_modification
                datecreation = file_date_creation
                dateadded = present_date_time

                try:
                    # Connection to DATA BASE
                    connection = psycopg2.connect(user=DB_UserNAME,
                                                  password=DB_PWD,
                                                  host=DB_HOST,
                                                  port=DB_PORT,
                                                  database=DB_NAME)

                    cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                    # Выполнение SQL-запроса для поиска file_hash в столбце sha256 таблицы unique_files
                    query_checking = """SELECT * FROM unique_files WHERE sha256 = %s"""
                    cursor.execute(query_checking, (sha256,))
                    records = cursor.fetchall()

                    print("\nSearch for hash records...")
                    i = 0
                    for row in records:
                        if True:
                            i += 1
                            print("ID:", row[0],
                                  "Sha256:", row[1],
                                  "Name:", row[2],
                                  "Size:", row[3],
                                  "Path:", row[4],
                                  "Comment:", row[5], end="\n\n")

                    if i == 0:
                        # Data recording into Unique
                        query_insert_unique = "INSERT INTO unique_files (sha256, name, size, path, comment, extension, datemodification, datecreation, dateadded) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query_insert_unique, (sha256, name, size, path, comment, extension, datemodification, datecreation, dateadded))
                        connection.commit()
                        print(Fore.GREEN + "!Data recording into Unique!", Style.RESET_ALL)

                        # Получить результат
                        # cursor.execute("SELECT * from unique_files")
                        # record = cursor.fetchall()
                        # print("Результат", record)

                        # reMOVE file into Unique
                        if os.path.exists(dst_file_of_unique):
                            os.remove(dst_file_of_unique)
                        shutil.move(file_path, dst_of_unique)
                        print(Fore.GREEN + "!File reMOVE    into Unique!", Style.RESET_ALL)

                    else:
                        # Data recording into Duplicates
                        query_insert_duplicates = "INSERT INTO duplicates_files (sha256, name, size, path, comment, extension, datemodification, datecreation, dateadded) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query_insert_duplicates, (sha256, name, size, path, comment, extension, datemodification, datecreation, dateadded))
                        connection.commit()
                        print(Fore.RED + "!Data recording into Duplicates!", Style.RESET_ALL)

                        # Получить результат
                        # cursor.execute("SELECT * from unique_files")
                        # record = cursor.fetchall()
                        # print("Результат", record)

                        # reMOVE file into Duplicates
                        if os.path.exists(dst_file_of_duplicates):
                            os.remove(dst_file_of_duplicates)
                        shutil.move(file_path, dst_of_duplicates)
                        print(Fore.RED + "!File reMOVE    into Duplicates!", Style.RESET_ALL)

                    cursor.close()
                    connection.commit()
                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("\n#####################################"
                              "\n!!!Соединение с PostgreSQL закрыто!!!"
                              "\n#####################################")

        end = time.time()
        print("\nОбщее время работы:", ('%.3f' % (end - start)), "sec")
    else:
        print("Wrong Master Password!")


def option2():
    print("\n2. Search for HASH")
    search_hash = input("Enter SHA256 (64 Symbol): ")

    try:
        # Connection to DATA BASE
        connection = psycopg2.connect(user=DB_UserNAME,
                                      password=DB_PWD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)

        cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

        # Выполнение SQL-запроса для поиска search_hash в столбце sha256 таблицы unique_files
        query_search_unique = """SELECT * FROM unique_files WHERE sha256 = %s"""
        cursor.execute(query_search_unique, (search_hash,))
        records = cursor.fetchall()

        print("\nSearch for hash records into ...Unique")
        for row in records:
            print(Fore.GREEN +
                  "ID:", row[0],
                  "Sha256:", row[1],
                  "Name:", row[2],
                  "Size:", row[3],
                  "Path:", row[4],
                  "Comment:", row[5],
                  Style.RESET_ALL, end="\n")

        # Выполнение SQL-запроса для поиска search_hash в столбце sha256 таблицы duplicates_files
        query_search_duplicates = """SELECT * FROM duplicates_files WHERE sha256 = %s"""
        cursor.execute(query_search_duplicates, (search_hash,))
        records = cursor.fetchall()

        print("\nSearch for hash records into ...Duplicates")
        for row in records:
            print(Fore.RED +
                  "ID:", row[0],
                  "Sha256:", row[1],
                  "Name:", row[2],
                  "Size:", row[3],
                  "Path:", row[4],
                  "Comment:", row[5],
                  Style.RESET_ALL, end="\n")

        print("\n     !!!Search  completed!!!     ")
        cursor.close()
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\n#####################################"
                  "\n!!!Соединение с PostgreSQL закрыто!!!"
                  "\n#####################################")


def option3():
    print("\nOption 3")


def option4():
    print("\n1. SQL HASH(SHA256) Files Manager !!!NO ADDing dBase!!!")
    user_master = input("Enter Master Password: ").encode()
    if hashlib.sha256(user_master).hexdigest() == MASTER_PWD_HASH:
        start = time.time()

        for src_dir, dirs, files in os.walk(source):

            dst_of_unique = src_dir.replace(source, destination_of_unique, 1)
            #print(dst_of_unique)
            if not os.path.exists(dst_of_unique):
                os.makedirs(dst_of_unique)

            dst_of_duplicates = src_dir.replace(source, destination_of_duplicates, 1)
            #print(dst_of_duplicates)
            if not os.path.exists(dst_of_duplicates):
                os.makedirs(dst_of_duplicates)

            for file_name in files:
                file_source = src_dir
                file_path = os.path.join(src_dir, file_name)  # Path+FileName Source

                print("Path_Source:", file_source)
                print("File_Name:", file_name)
                print("File_Path:", file_path)

                dst_file_of_unique = os.path.join(dst_of_unique, file_name)  # Path+FileName Unique

                dst_file_of_duplicates = os.path.join(dst_of_duplicates, file_name)  # Path+FileName Duplicates

                # function to return the file hash(sha256)
                sha256_hash = hashlib.sha256()  # для создания хеш-объекта для алгоритма хеширования SHA-256
                with open(file_path, "rb") as f:  # rb - Открывает файл в бинарном режиме только для чтения
                    # Read and update hash string value in blocks of 4K
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                    file_hash = sha256_hash.hexdigest()
                    print("Sha256:", file_hash)

                # function to return the file extension
                file_extension = pathlib.Path(file_path).suffix
                print("File_Extension:", file_extension)

                # function to return the file size
                file_size = file_size_x(file_path)
                print("File_Size:", file_size)

                # function to return the file Date/Time modification
                file_time_modification = os.path.getmtime(file_path)
                file_date_modification = datetime.datetime.fromtimestamp(file_time_modification)  # convert time into DateTime
                print("Date/Time Modified:", file_date_modification)

                # function to return the file Date/Time creation
                file_time_creation = os.path.getctime(file_path)
                file_date_creation = datetime.datetime.fromtimestamp(file_time_creation)  # convert time into DateTime
                print("Date/Time Created:", file_date_creation)

                # function to return the present Date/Time
                present_date_time = datetime.datetime.now()
                print("Date/Time Present:", present_date_time)

                # Переменные для DATA BASE
                sha256 = file_hash

                try:
                    # Connection to DATA BASE
                    connection = psycopg2.connect(user=DB_UserNAME,
                                                  password=DB_PWD,
                                                  host=DB_HOST,
                                                  port=DB_PORT,
                                                  database=DB_NAME)

                    cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                    # Выполнение SQL-запроса для поиска file_hash в столбце sha256 таблицы unique_files
                    query_checking = """SELECT * FROM unique_files WHERE sha256 = %s"""
                    cursor.execute(query_checking, (sha256,))
                    records = cursor.fetchall()

                    print("\nSearch for hash records...")
                    i = 0
                    for row in records:
                        if True:
                            i += 1
                            print("ID:", row[0],
                                  "Sha256:", row[1],
                                  "Name:", row[2],
                                  "Size:", row[3],
                                  "Path:", row[4],
                                  "Comment:", row[5], end="\n\n")

                    if i == 0:
                        print(Fore.GREEN + "!SHA256 Unique!", Style.RESET_ALL)

                    else:
                        print(Fore.RED + "!SHA256 Duplicate!", Style.RESET_ALL)

                        # reMOVE file into Duplicates
                        if os.path.exists(dst_file_of_duplicates):
                            os.remove(dst_file_of_duplicates)
                        shutil.move(file_path, dst_of_duplicates)
                        print(Fore.RED + "!File reMOVE    into Duplicates!", Style.RESET_ALL)

                    cursor.close()
                    connection.commit()
                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("\n#####################################"
                              "\n!!!Соединение с PostgreSQL закрыто!!!"
                              "\n#####################################")

        end = time.time()
        print("\nОбщее время работы:", ('%.3f' % (end - start)), "sec")
    else:
        print("Wrong Master Password!")


if __name__ == '__main__':
    # printing the heading
    print("File Hash Manager (SQL & SHA256)")

    # using the while loop to print menu list
    while True:
        print("\nMENU")
        print("0. Create TABLEs / ")
        print("1. HASH Manager +ADDing dBase / ")
        print("2. Search for HASH / Поиск указанного хзша в бд")
        print("3. Option 3")
        print("4. Checking HASH for a match / Проверка на совпадение с БД (только перенос дублей без записи в бд)")
        print("5. Exit")
        choice = int(input("\nEnter the Choice: "))

        # using if-elif-else statement to pick different options
        if choice == 0:
            option0()

        elif choice == 1:
            option1()

        elif choice == 2:
            option2()

        elif choice == 3:
            option3()

        elif choice == 4:
            option4()

        elif choice == 5:
            print('Thanks message before exiting')
            exit()

        else:
            print("Please Provide a valid Input!")
            print('Invalid option. Please enter a number between 0 and 5.')
