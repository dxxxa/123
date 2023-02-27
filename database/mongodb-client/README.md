# [How to Use MongoDB Database in Python](https://www.thepythoncode.com/article/introduction-to-mongodb-in-python)
##
# [[] / []]()
MongoDB — это кроссплатформенная документоориентированная база данных. Он классифицируется как база данных NoSQL, поскольку он хранит данные в гибких, JSON-подобных документах, что означает, что поля могут варьироваться от документа к другому, а структура данных может быть изменена с течением времени.

В отличие от реляционных баз данных, таких как MySQL, которые хранят данные в таблицах, MongoDB хранит данные в коллекциях в формате BSON, который является двоичной сериализацией JSON, расшифровывается как «Binary JSON», все, что вы можете сделать с JSON, вы можете сделать это и с BSON, но с дополнительными расширениями, которые не являются частью JSON, такими как типы данных Date и BinData.

Связанные с: Как работать с файлами JSON в Python.

Существует множество причин для выбора MongoDB вместо баз данных SQL, в том числе:

Максимально эффективное использование облачных вычислений и хранения данных
Гибкость
Ускорение разработки
Это распределенная база данных, поэтому высокая доступность, горизонтальное масштабирование и географическое распределение встроены и просты в использовании.
Вот что мы рассмотрим в этом уроке:

Начало работы
Подключение к базе данных MongoDB
Листинговые базы данных
Доступ к базе данных
Перечисление всех коллекций в базе данных
Вставка документов
Получение документов
Удаление документа
Удаление коллекции
Удаление базы данных
Начало работы
Во-первых, вам нужно будет установить MongoDB на свою машину, я настоятельно рекомендую вам проверить официальное руководство по установке MongoDB, вам нужно следовать процедуре для вашей операционной системы.

Во-вторых, вам нужно установить драйвер MongoDB Python: pymongo:

pip3 install pymongo
Если вы просто устанавливаете pymongo через pip, то вам хорошо идти, последняя версия pymongo поддерживает все версии баз данных MongoDB.

Наконец, вам нужно запустить демон MongoDB с помощью следующей команды:

$ mongod
Подключение к базе данных MongoDB
После установки MongoDB и запуска демона Mongo с помощью команды mongod за подключение к базе данных отвечает приведенный ниже код:

from pymongo import MongoClient
from pprint import pprint

# connect to the MongoDB server
client = MongoClient()
# or explicitly
# client = MongoClient("localhost", 27017)
Передача параметров без параметров аналогична указанию localhost в качестве хоста и порта по умолчанию 27017 MongoDB. Обратите внимание, что это еще не установит никакого соединения, это будет сделано только после того, как вы выполните какую-либо операцию (например, получение информации о сервере).

If you want to get some information about the server, you can using client.server_info() method.

Listing Databases
Let's get all the databases available in our MongoDB server:

# list all database names
print("Available databases:", client.list_database_names())
This will only output the names for the databases, you can use client.list_databases() method if you want to get some information about databases such as size taken on disk, here is my output:

Available databases: ['admin', 'config', 'db', 'local', 'mydb']
Don't worry if you don't have the same output as mine, I had MongoDB for a while and for sure, I made a lot of work there.

Accessing a Database
To access a specific database, we can either by accessing it as an attribute or Python's dictionary-style:

# access the database "python", this will create the actual database
# if it doesn't exist
database = client["python"]
# or this:
# database = client.python
Note that the database does not exist, it'll be created automatically once we create a collection (like a table in SQL) and insert a document.

Listing All Collections with a Database
Collection is the term for a table in MongoDB. To get all the collections inside this database, we simply use database.list_collection_names() method:

# list all collections
print("Available collections:", database.list_collection_names())
Here is my output:

[]
Not very surprising, since this is a new database, we haven't created any collection yet. You can also use database.list_collections() method to get each collection along with some information.

Inserting Documents
A document in MongoDB is like a row in relational databases. For demonstration, let's make books collection and insert books in it:

# get books collection (or create one)
books = database["books"]
# insert a single book
result = books.insert_one({
    "name": "Invent Your Own Computer Games with Python, 4E",
    "author": "Al Sweigart",
    "price": 17.99,
    "url": "https://amzn.to/2zxN2W2"
})
We have retrieved books collection (or create it if it doesn't exist) and used books.insert_one() method to insert a single document, we simply passed a Python dictionary.

Let's get the ID of the inserted element:

print("One book inserted:", result.inserted_id)
Output:

One book inserted: 5ee79b10c6bd9552e204a625
A great feature about MongoDB, it automatically generates a unique ID for each element inserted, we'll see it again later on.

Now what if we want to insert multiple documents in a time ? We simply use insert_many() method instead of insert_one():

# insert many books
books_data = [
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
result = books.insert_many(books_data)
print("Many books inserted, Ids:", result.inserted_ids)
We have inserted 3 documents in one go, notice the last book doesn't have a url field and MongoDB doesn't complain about it, because it's allowed!

Here is my output:

Many books inserted, Ids: [ObjectId('5ee79c4fc6bd9552e204a62c'), ObjectId('5ee79c4fc6bd9552e204a62d'), ObjectId('5ee79c4fc6bd9552e204a62e')]
Fetching Documents
The amazing thing about MongoDB is that we can filter documents using a Python dictionary, let's get a single book by a specific author:

# get a single book by a specific author
eric_book = books.find_one({"author": "Eric Matthes"})
pprint(eric_book)
Output:

{'_id': ObjectId('5ee79c10c6bd9552e204a627'),
 'author': 'Eric Matthes',
 'name': 'Python Crash Course: A Hands-On, Project-Based Introduction to '
         'Programming',
 'price': 22.97,
 'url': 'https://amzn.to/2yQfQZl'}
The output is a Python dictionary as well, let's get all books of Al Sweigart:

# get all books by a specific author
sweigart_books = books.find({"author": "Al Sweigart"})
print("Al Sweigart's books:")
pprint(list(sweigart_books))
Notice I wrapped the result in a list() function to retrieve it as a list of dictionaries, that's because find() method returns a pymongo.cursor.Cursor() instance, in which you can iterate over it using a for loop, or wrap it using list() function. Here is the expected output:

[{'_id': ObjectId('5ee79b10c6bd9552e204a625'),
  'author': 'Al Sweigart',
  'name': 'Invent Your Own Computer Games with Python, 4E',
  'price': 17.99,
  'url': 'https://amzn.to/2zxN2W2'},
 {'_id': ObjectId('5ee79c10c6bd9552e204a626'),
  'author': 'Al Sweigart',
  'name': 'Automate the Boring Stuff with Python: Practical Programming for '
          'Total Beginners',
  'price': 17.76,
  'url': 'https://amzn.to/2YAncdY'},
 {'_id': ObjectId('5ee79c34c6bd9552e204a629'),
  'author': 'Al Sweigart',
  'name': 'Automate the Boring Stuff with Python: Practical Programming for '
          'Total Beginners',
  'price': 17.76,
  'url': 'https://amzn.to/2YAncdY'},
 {'_id': ObjectId('5ee79c4fc6bd9552e204a62c'),
  'author': 'Al Sweigart',
  'name': 'Automate the Boring Stuff with Python: Practical Programming for '
          'Total Beginners',
  'price': 17.76,
  'url': 'https://amzn.to/2YAncdY'}]
Finally, if you want to get all the documents without any filter, you can simply pass an empty dictionary to find() method:

# get all documents in books collection
all_books = books.find({})
print("All books:")
pprint(list(all_books))
Deleting a Document
To delete a specific document, you simply use delete_one() method, here is an example:

# delete a specific document by a JSON query
result = books.delete_one({"author": "Albert Lukaszewski"})
Even if there is more than one document using that filter, it will still delete a single document. If you want to delete all the documents using that filter, you use delete_many() method:

# delete all books by Al Sweigart
result = books.delete_many({"author": "Al Sweigart"})
Удаление коллекции
Чтобы удалить коллекцию в MongoDB, у вас есть два варианта:

# drop this collection
database.drop_collection("books")
# or this:
# books.drop()
Это приведет к удалению коллекции книг.

Удаление базы данных
# drop this entire database
client.drop_database("python")
# close the connection
client.close()
drop_database() делает то, что предполагает его имя, он удаляет базу данных, получившую имя в аргументах.

Наконец, мы закрываем соединение с помощью метода close().

Заключение
Теперь вы знаете основные функциональные возможности MongoDB и его драйвера Python, pymongo. Я призываю вас поиграть с ним, чтобы ознакомиться с базой данных, она такая же гибкая, как язык Python!

Связанные с: Как использовать базу данных MySQL в Python.