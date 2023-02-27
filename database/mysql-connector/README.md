# [How to Use MySQL Database in Python](https://www.thepythoncode.com/article/using-mysql-database-in-python)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Подключение к базе данных MySQL
Создание базы данных
Создание таблицы
Вставка данных в таблицу
Извлечение данных из таблицы
Связанные с: Как использовать базу данных MongoDB в Python.

Чтобы начать, во-первых, вам нужно иметь экземпляр сервера MySQL, запущенный на вашем компьютере, если вы используете Windows, я предлагаю вам установить XAMPP. Если вы используете компьютер Linux (Ubuntu или аналогичный), проверьте этот учебник. Если вы используете macOS, run через этот учебник, чтобы установить MySQL.

Во-вторых, давайте установим библиотеку Python коннектора MySQL, а также табличный модуль:

pip3 install mysql-connector-python tabulate
Мы будем использовать табличный модуль опционально для вывода извлеченных данных аналогично обычным клиентам MySQL.

Подключение к базе данных MySQL
Давайте импортируем коннектор MySQL и подключим его к нашей базе данных:

import mysql.connector as mysql
from tabulate import tabulate

# insert MySQL Database information here
HOST = "localhost"
DATABASE = ""
USER = "root"
PASSWORD = ""

# connect to the database
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
# get server information
print(db_connection.get_server_info())
Мы использовали метод mysql.connector.connect() для подключения к базе данных, он принимает 4 аргумента:

host: Я указал "localhost" в качестве хоста, что означает, что мы подключаемся к нашему локальному серверу MySQL (установленному на нашей машине). Однако, если вы хотите подключиться к удаленному серверу MySQL, вам нужно сделать некоторые настройки, ознакомьтесь с этим учебником, в котором я покажу вам, как настроить ваш сервер MySQL для приема удаленных подключений.
database: Это имя базы данных, которую вы хотите подключить, установка базы данных на пустую строку будет подключаться только к MySQL, а не к фактической базе данных, поэтому мы будем обрабатывать создание нашей базы данных вручную.
user: root является пользователем по умолчанию в MySQL, вы, конечно, можете использовать другой.
password: Это пароль пользователя, по умолчанию это пустая строка для пользователя root (конечно, это только для разработки).
После этого мы вызвали метод get_server_info() для информации о сервере печати, вот выходные данные до сих пор:

5.5.5-10.1.32-MariaDB
Если вы получили информацию о своем сервере, то все прошло нормально.

Давайте посмотрим, в какой базе данных мы находимся:

# get the db cursor
cursor = db_connection.cursor()
# get database information
cursor.execute("select database();")
database_name = cursor.fetchone()
print("[+] You are connected to the database:", database_name)
Обратите внимание, что прежде чем мы выполним какую-либо команду MySQL, нам нужно создать курсор. Курсор — это временная рабочая область, создаваемая в экземпляре сервера MySQL при выполнении инструкции SQL.

Вот мой вывод:

[+] You are connected to the database: (None,)
Конечно, мы не подключены к какой-либо базе данных, прежде чем мы это сделаем, давайте сначала создадим ее.

Создание базы данных
Поскольку мы не находимся ни в одной базе данных, нам нужно создать ее:

# create a new database called library
cursor.execute("create database if not exists library")
Это так же просто, как выполнить обычную команду MySQL, мы используем «если не существует», поэтому, если вы запустите код еще раз, вы не получите ошибку «База данных существует». Давайте поработаем над этой базой данных сейчас:

# use that database 
cursor.execute("use library")
print("[+] Changed to `library` database")
Создание таблицы
Чтобы создать таблицу, все, что нам нужно сделать, это передать правильную команду SQL методу cursor.execute():

# create a table
cursor.execute("""create table if not exists book (
    `id` integer primary key auto_increment not null,
    `name` varchar(255) not null,
    `author` varchar(255) not null,
    `price` float not null,
    `url` varchar(255)
    )""")
print("[+] Table `book` created")
Мы только что создали таблицу книг, которая имеет 5 столбцов, просто для демонстрации, notice я использовал тройные двойные кавычки, чтобы мы могли легко переходить к новым строкам.

Вставка данных в таблицу
Чтобы вставить данные в таблицу, нам нужен источник данных, вы можете вставить очищенные данные в базу данных или некоторые данные в локальный файл, каким бы ни был источник, для этого урока мы вставим из обычного словаря Python, просто для удобства:

# insert some books
books = [
    {
        "name": "Automate the Boring Stuff with Python: Practical Programming for Total Beginners",
        "author": "Al Sweigart",
        "price": 17.76,
        "url": "https://amzn.to/2YAncdY"
    },
    {
        "name": "Python Crash Course: A Hands-On, Project-Based Introduction to Programming",
        "author": "Eric Matthes",
        "price": 22.97,
        "url": "https://amzn.to/2yQfQZl"
    },
    {
        "name": "MySQL for Python",
        "author": "Albert Lukaszewski",
        "price": 49.99,
    }
]
# iterate over books list
for book in books:
    id = book.get("id")
    name = book.get("name")
    author = book.get("author")
    price = book.get("price")
    url = book.get("url")
    # insert each book as a row in MySQL
    cursor.execute("""insert into book (id, name, author, price, url) values (
        %s, %s, %s, %s, %s
    )
    """, params=(id, name, author, price, url))
    print(f"[+] Inserted the book: {name}")
So we have inserted a couple of books here, notice we used "%s" to replace the actual data fields passed in params parameter, this is due to many reasons including SQL injection prevention and performance.

Вот мой вывод:

[+] Inserted the book: Automate the Boring Stuff with Python: Practical Programming for Total Beginners
[+] Inserted the book: Python Crash Course: A Hands-On, Project-Based Introduction to Programming
[+] Inserted the book: MySQL for Python
Если вы перейдете сейчас к своему клиенту MySQL, будь то PhpMyAdmin или в командной строке, вы не найдете эти новые вставленные книги, это потому, что нам нужно зафиксировать:

# commit insertion
db_connection.commit()
Основной причиной использования фиксации является завершение текущей транзакции (в данном случае вставка 3 книг) и внесение всех изменений в транзакцию постоянными.

Противоположностью фиксации является откат, это в основном означает отмену всех изменений, сделанных текущей транзакцией (в данном случае не вставляя 3 книги), вы можете использовать db_connection.rollback() для этого, если хотите.

Для получения дополнительной информации о транзакциях ознакомьтесь с документацией MySQL об этом.

Извлечение данных из таблицы
Теперь давайте получим данные, которые мы только что вставили из фактической базы данных:

# fetch the database
cursor.execute("select * from book")
# get all selected rows
rows = cursor.fetchall()
# print all rows in a tabular format
print(tabulate(rows, headers=cursor.column_names))
Мы выполнили команду select и захватили все строки с помощью метода cursor.fetchall(), если вы хотите получить только первую, вы также можете использовать метод fetchone().

Затем печатаем все возвращенные строки в табличном формате с помощью табличного модуля, проверяем мой вывод:

  id  name                                                                              author                price  url
----  --------------------------------------------------------------------------------  ------------------  -------  -----------------------
   1  Automate the Boring Stuff with Python: Practical Programming for Total Beginners  Al Sweigart           17.76  https://amzn.to/2YAncdY
   2  Python Crash Course: A Hands-On, Project-Based Introduction to Programming        Eric Matthes          22.97  https://amzn.to/2yQfQZl
   3  MySQL for Python                                                                  Albert Lukaszewski    49.99
Наконец, давайте закроем соединение:

# close the cursor
cursor.close()
# close the DB connection
db_connection.close()
Заключение
Вот он, библиотека коннектора MySQL позволяет разработчикам Python выполнять команды SQL, вы можете следовать той же процедуре для других команд, таких как UPDATE и DELETE.

Проверьте полный код для этого учебника.