# https://pythonru.com/biblioteki/vvedenie-v-postgresql-s-python-psycopg2?ysclid=ld2cntijfn578484899

import hashlib
import psycopg2
from psycopg2 import Error

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import psycopg2.extras

from config import *


if __name__ == '__main__':

    print("\nSQL SHA256 Files Manager")
    user_master = input("\nEnter Master Password:").encode()
    if hashlib.sha256(user_master).hexdigest() == MASTER_PWD_HASH:


        # Выбор действий
        print("0. Info PostgreSQL")
        print("01. Отображение ВСЕХ баз данных на СЕРВЕРе PostgreSQL")
        print("1. Создание базы данных")
        print("001.Удаление БД PostgreSQL")
        print("20. Отображение ВСЕХ таблиц Сервера")
        print("200. Отображение таблиц ...")
        print("2. Отображение таблиц БД")
        print("21. Отображение ВСЕХ таблиц БД")
        print("3. Создание таблицы")
        print("4. Удаление таблицы")
        print("5. Выполнение CRUD-операций (SQL-запрос вставки данных в таблицу)")  # CREATE, READ, UPDATE и DELETE
        print("6. Выполнение CRUD-операций (SQL-запрос обновления таблицы)")  # CREATE, READ, UPDATE и DELETE
        print("7. Выполнение CRUD-операций (SQL-запрос удаление строки в таблице)\n")  # CREATE, READ, UPDATE и DELETE

        userChoice = input("Enter Option: ")
        if userChoice == "0":
            try:    # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,  # пароль указанный при установке PostgreSQL
                                              host=DB_HOST,
                                              port=DB_PORT)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # Распечатать сведения о PostgreSQL
                print("Информация о сервере PostgreSQL\n", connection.get_dsn_parameters(), "\n")  # свойства соединения
                # Выполнение SQL-запроса
                cursor.execute("SELECT version();")  # execute - для выполнения любой операции или запроса к базе данных
                # Получить результат
                record = cursor.fetchone()  # Результаты запроса получают с помощью fetchone(), fetchmany(), fetchall()
                print("Вы подключены к - ", record, "\n")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "01":  # Отображение ВСЕХ БД СЕРВЕРА PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                show_table_query = ("""SELECT datname FROM pg_database
                                       WHERE datistemplate = 'false'""")

                # Выполнение команды: это отобразит таблицы
                cursor.execute(show_table_query)
                for table in cursor.fetchall():
                    print(table)
                connection.commit()
                print("Таблицы успешно отображены в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        if userChoice == "1":
            try:
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,  # пароль указанный при установке PostgreSQL
                                              host=DB_HOST,
                                              port=DB_PORT)
            # Создание базы данных
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных
                sql_create_database = 'create database ' + input("\nEnter Name dBase:")
                cursor.execute(sql_create_database)  # execute - для выполнения любой операции или запроса к базе данных
            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "001":  # Удаление БД PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT)

                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для удаления таблицы
                delete_table_query = 'DROP database ' + input("\nEnter Name dBase:") + ";"

                # Выполнение команды: это удаляет таблицу
                cursor.execute(delete_table_query)
                connection.commit()
                print("Таблица успешно удалена в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                print("Соединение с PostgreSQL закрыто")

        elif userChoice == "20":  # Отображение ВСЕХ таблиц СЕРВЕРА PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для отображения таблиц БД
                show_table_query = ("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")

                # Выполнение команды: это отобразит таблицы
                cursor.execute(show_table_query)
                for table in cursor.fetchall():
                    print(table)
                connection.commit()
                print("Таблицы успешно отображены в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "200":  # Отображение ВСЕХ таблиц СЕРВЕРА PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для отображения таблиц БД
                show_table_query = ("""SELECT table_name FROM information_schema.tables""")

                # Выполнение команды: это отобразит таблицы
                cursor.execute(show_table_query)
                for table in cursor.fetchall():
                    print(table)
                connection.commit()
                print("Таблицы успешно отображены в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "2":  # Отображение таблиц БД PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для отображения таблиц БД
                show_table_query = ("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")

                # Выполнение команды: это отобразит таблицы
                cursor.execute(show_table_query)
                for table in cursor.fetchall():
                    print(table)
                connection.commit()
                print("Таблицы успешно отображены в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "21":  # Отображение ВСЕХ таблиц БД PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для отображения ВСЕХ таблиц БД
                show_table_query = ("""SELECT table_name FROM information_schema.tables""")

                # Выполнение команды: это отобразит таблицы
                cursor.execute(show_table_query)
                for table in cursor.fetchall():
                    print(table)
                connection.commit()
                print("Таблицы успешно отображены в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "3":  # Создание таблицы PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для создания новой таблицы
                create_table_query = '''CREATE TABLE unique_files
                                          (ID SERIAL PRIMARY KEY     NOT NULL,
                                          DATEADDED           DATE    NOT NULL,
                                          DATEOFCHANGE           DATE    NOT NULL,
                                          SHA256           VARCHAR(64)    NOT NULL,
                                          FILENAME           TEXT    NOT NULL,
                                          EXTENSION           TEXT    NOT NULL,
                                          SIZE           TEXT    NOT NULL,
                                          FILEPATH           TEXT    NOT NULL,
                                          COMMENT           TEXT    NOT NULL); '''

                # Выполнение команды: это создает новую таблицу
                cursor.execute(create_table_query)
                connection.commit()
                print("Таблица успешно создана в PostgreSQL")

                create_table_query = '''CREATE TABLE duplicates_files
                                          (ID SERIAL PRIMARY KEY     NOT NULL,
                                          DATEADDED           DATE    NOT NULL,
                                          DATEOFCHANGE           DATE    NOT NULL,
                                          SHA256           VARCHAR(64)    NOT NULL,
                                          FILENAME           TEXT    NOT NULL,
                                          EXTENSION           TEXT    NOT NULL,
                                          SIZE           TEXT    NOT NULL,
                                          FILEPATH           TEXT    NOT NULL,
                                          COMMENT           TEXT    NOT NULL); '''

                # Выполнение команды: это создает новую таблицу
                cursor.execute(create_table_query)
                connection.commit()
                print("Таблица успешно создана в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                print("Соединение с PostgreSQL закрыто")

        elif userChoice == "4":  # Удаление таблицы PostgreSQL из Python
            try:
                # пытаемся подключиться к базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()  # Курсор для выполнения операций с базой данных

                # SQL-запрос для удаления таблицы
                delete_table_query = '''DROP TABLE ''' + input("\nEnter Name Table:")

                # Выполнение команды: это удаляет таблицу
                cursor.execute(delete_table_query)
                connection.commit()
                print("Таблица успешно удалена в PostgreSQL")

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                print("Соединение с PostgreSQL закрыто")

        elif userChoice == "5":  # Выполнение CRUD-операций
            try:
                # Подключиться к существующей базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()
                # Выполнение SQL-запроса для вставки данных в таблицу
                insert_query = """ INSERT INTO unique_files (ID, DATEADDED, DATEOFCHANGE, SHA256, FILENAME, EXTENSION, SIZE, FILEPATH, COMMENT) 
                VALUES (5, '1992-09-06', '2023-01-19', '70d28042cd1ba8ef59c8760fd336ff7b3144063214eff769359b1f7cd2c15c1d', 'FILENAME', 'EXTENSION', 'SIZE', 'FILEPATH', 'COMMENT')"""

                id =1
                dateadded =2
                dateofchange =3
                sha256 =4
                filename =5
                extension =6
                size =7
                filepath =8
                comment =9
                insert_query = "INSERT INTO RecordONE (dateadded, dateofchange, sha256, filename, extension, size, filepath, comment) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (dateadded, dateofchange, sha256, filename, extension, size, filepath, comment)
                cursor.execute(insert_query)
                connection.commit()
                print("1 запись успешно вставлена")
                # Получить результат
                cursor.execute("SELECT * from unique_files")
                record = cursor.fetchall()
                print("Результат", record)

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "6":  # Выполнение CRUD-операций
            try:
                # Подключиться к существующей базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()
                # Выполнение SQL-запроса для обновления таблицы
                update_query = """Update unique_files set price = 1500 where id = 1"""
                cursor.execute(update_query)
                connection.commit()
                count = cursor.rowcount
                print(count, "Запись успешно удалена")
                # Получить результат
                cursor.execute("SELECT * from unique_files")
                print("Результат", cursor.fetchall())

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        elif userChoice == "7":  # Выполнение CRUD-операций
            try:
                # Подключиться к существующей базе данных
                connection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)

                cursor = connection.cursor()
                # Выполнение SQL-запроса для удаления таблицы
                delete_query = """Delete from unique_files where id = 4"""
                cursor.execute(delete_query)
                connection.commit()
                count = cursor.rowcount
                print(count, "Запись успешно удалена")
                # Получить результат
                cursor.execute("SELECT * from unique_files")
                print("Результат", cursor.fetchall())

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")



        elif userChoice == "777":  # Выполнение CRUD-операций
            try:
                # Подключиться к существующей базе данных
                postgresConnection = psycopg2.connect(user=DB_UserNAME,
                                              password=DB_PWD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)


                # Name of the table
                tableName = "unique_files"

                # Obtain a dictionary cursor from the connection object
                cursorObject = postgresConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # Execute the stored function/procedure
                print("Runnning the function ExpireOrders()...")
                cursorObject.execute("select ExpireOrders()")
                cursorObject.execute("select * from unique_files")
                rows = cursorObject.fetchall()

                print("Orders and their status after expiring them through stored function/procedure:")

                for row in rows:
                    print("%d %s %s %s" % (row["ID"], row["DATEADDED"], row["SHA256"], row["FILENAME"]))
                    #print("%d %s %s %s" % (row["ID"], row["DATEADDED"], row["SHA256"], row["FILENAME"], row["EXTENSION"], row["SIZE,"], row["FILEPATH"], row["COMMENT"]))

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

        else:
            print("Invalid Option!")

        #connection.commit()
        #connection.close()

    else:
        print("Wrong Master Password!")
