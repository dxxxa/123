# [How to Build a CRUD App with Flask and SQLAlchemy in Python](https://www.thepythoncode.com/article/building-crud-app-with-flask-and-sqlalchemy)
##
# [[] / []]()
Приложение CRUD — это веб-приложение, которое позволяет создавать, читать, обновлять и удалять вещи. Это распространенная задача в веб-разработке и очень полезна для изучения того, как создавать веб-приложения.

В этом учебнике вы узнаете, как создать приложение CRUD в Flask, и в результате получится рабочий бэкэнд для веб-приложения книжного магазина. Мы определим сервисы для обработки операций CRUD; Запросы GET, POST, PUT и DELETE для API книжного магазина RESTful. Есть вторая часть учебника, где мы завершаем сборку приложения, добавляя код интерфейса с помощью Jinja2 и Bootstrap; проверьте это здесь.

Создание приложения книжного магазина полезно для обучения, потому что это реальный пример, а не игрушечный проект. Код будет основан на Flask и расширении Flask-SQLAlchemy.

Flask - это микрофреймворк для создания веб-приложений с использованием Python. Это очень легкий фреймворк, который прост в освоении и использовании. Легкий вес не означает, что Flask не является мощным. Расширения Flask можно использовать всякий раз, когда хотите использовать в приложении что-то вроде ORM (Object Relational Mapping). В этом учебнике я использовал расширение Flask-SQLAlchemy для создания базы данных и таблицы для хранения книг.

SQLAlchemy - это библиотека Python ORM (Object Relational Mapping), которая упрощает работу с базами данных.

Содержание:

Проектирование базы данных
Структурирование API
Установка зависимостей
Создание модели базы данных
Настройка приложения Flask
Настройка запросов GET
Добавление данных в SQLAlchemy
Запуск приложения Flask
Удаление книги
Добавление новой книги
Обновление книги
Заключение
Проектирование базы данных
Перед созданием базы данных необходимо определить схему базы данных и таблицы. Схема — это структура метаданных базы данных, а таблицы — это фактические данные, которые мы хотим сохранить.

Дизайн этого проекта прост: у нас есть одна таблица под названием книги, в которой хранятся поля книг: ISBN (книги), название, автор и цена.

Эти поля будут храниться в базе данных через SQLAlchemy ORM. API Flask будет использовать эти поля в качестве модели данных для операций CRUD.

Ниже приведена UML-схема, показывающая функции, используемые в API, которые будут зависеть от схемы базы данных:

Приложение Flask вызывало функции в зависимости от таблицы Book. (Разработано Plantuml)

Как мы видим, Flask API имеет пять функций, которые полагаются на таблицу Book. Вы увидите, как эти функции будут вызывать соответствующие методы из SQLAlchemy. Давайте сначала посмотрим, как мы структурируем функции API. Эти функции будут вызваны API Flask и украшены декоратором @app.route. Сопоставления для каждого из них показаны ниже:

get_books(), чтобы перечислить все книги, которые сопоставляются с URL-адресом /book/list с помощью запроса GET.
get_book(isbn), чтобы получить указанную книгу, определенную параметром URL isbn, который мы передаем функции. Эта функция сопоставляется с URL-адресом /book/<isbn> с помощью запроса GET.
create_book(), чтобы добавить новую книгу в базу данных. Эта функция сопоставляется с URL-адресом /book с помощью запроса POST.
update_book(isbn) для обновления указанной книги, которая сопоставляется с URL-адресом /book/<isbn> с помощью запроса PUT.
delete_book(isbn) удалить выбранную книгу, которая сопоставляется с /book/<isbn> URL-адресом с помощью запроса DELETE.
Структурирование API
Чтобы следовать этому проекту, вы можете создать один файл и сбросить в него код. Вы также можете создать несколько файлов и импортировать код из этих файлов, чтобы разделить проблемы, или, в конечном счете, вы можете проверить эту страницу, чтобы получить код для каждого файла.

Я предпочитаю структурировать код API в нескольких файлах. Причина в том, что это помогает вам поддерживать код организованным, а также помогает вам поддерживать код в чистоте.

Давайте создадим папку с именем bookshop. Внутри этой папки структура этого проекта отображается следующим образом:

├── app
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── bookshop.py
├── config.py
Я попытался сделать структуру как можно более минимальной без чертежей, что, я думаю, было бы излишним для этого небольшого приложения. Вот разбивка каждого файла:

bookshop.py является основным файлом, содержащим API Flask.
config.py имеет конфигурацию для API.
app/__init__.py — это файл, содержащий экземпляры базы данных и приложения.
app/models.py содержит схему базы данных и ORM.
app/routes.py содержит функции API, которые будет вызывать API.
Начнем с файла app/models.py для создания базы данных.

Установка зависимостей
Перед созданием модели БД установим Flask и расширение Flask-SQLAlchemy.

Давайте также установим ядро СУБД. В этом учебнике вы будете использовать MySQL, но не стесняйтесь использовать любое другое ядро СУБД. SQLAlchemy поддерживает MySQL, SQLite, Postgres и многое другое. Для MySQL мы устанавливаем библиотеку PyMySQL:

$ pip install flask flask-sqlalchemy PyMySQL
Создание модели базы данных
Определим модель базы данных в файле app/models.py следующим образом:

from . import db

class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def to_json(self):
        return {
            'isbn': self.isbn,
            'author': self.author,
            'title': self.title,
            'price': self.price
        }
В этом файле мы определили имя таблицы как книги, а поля как:

isbn: первичный ключ таблицы.
автор: автор книги, обязательное строковое поле и не может быть NULL. Он ограничен 100 символами.
title: название книги, обязательное поле и имеет длину 100 символов.
price: цена книги, которая является плавающим полем и может быть NULL.
Функция to_json() используется здесь для преобразования объекта Book в объект JSON, который может быть возвращен клиенту в браузере. Мы увидим лучший способ сделать это в следующих разделах.

Обратите внимание, что класс Book является подклассом базы данных. Класс модели. Этот экземпляр БД определяется в файле app/__init__.py следующим образом:

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Настройка приложения Flask
Теперь, когда у нас есть модель базы данных, давайте настроим приложение Flask для расширения SQLAlchemy.

Рекомендуется настроить приложение для определения родительского класса Config, который будет содержать стандартные конфигурации для всех сред. Затем создайте экземпляр дочернего класса конфигурации для своих сред. В нашем случае мы создадим три среды: разработку, тестирование и производство.

Давайте посмотрим на это в действии:

#config.py
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
Таким образом, класс Config содержит глобальные конфигурации для приложения, а именно:

SQLALCHEMY_TRACK_MODIFICATIONS установлено значение False, чтобы отключить систему отслеживания изменений. Это хорошая практика, чтобы избежать накладных расходов на отслеживание изменений от Flask-SQLAlchemy к библиотеке SQLAlchemy.
init_app() — статический метод, используемый для инициализации конфигураций приложений.
У нас есть три дочерних класса для каждой среды, следующих за этим родительским классом Config. Каждая среда определяет конфигурации, подходящие для этой среды.

И, наконец, у нас есть словарь конфигурации, который сопоставляет имя среды с классом конфигурации. Среда по умолчанию — это среда разработки, которую мы будем использовать в этом учебнике.

В классе DevelopmentConfig атрибут DEBUG имеет значение True, так как мы хотим видеть отладочные сообщения в браузере, если в API есть ошибка.

Кроме того, он имеет атрибут SQLALCHEMY_DATABASE_URI, установленный для URL-адреса базы данных, который мы определяем для подключения к базе данных.

В нашем случае мы устанавливаем URL-адрес базы данных переменной среды DEV_DATABASE_URL , которая является URL-адресом базы данных MySQL. Выполните следующую команду на терминале, чтобы определить этот env var:

$ export DEV_DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/flaskapp
где <имя пользователя> и <пароль> — учетные данные для базы данных MySQL, а flaskapp — имя базы данных. Не стесняйтесь заменять любое из значений на свое собственное.

Если вы используете Windows, вы можете использовать команду SET вместо экспорта:

$ SET DEV_DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/flaskapp
Если вы работаете с другим ядром СУБД, вы можете изменить DEV_DATABASE_URL на соответствующий URL-адрес для этой базы данных. Например, если вы используете SQLite, вы можете настроить его на sqlite:///<path_to_db>.

Теперь давайте импортируем конфигурационный словарь и начнем создавать приложение Flask. Теперь файл app/__init__.py выглядит следующим образом:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    return app
Функция create_app() используется для создания экземпляра приложения на основе среды, который передается в качестве аргумента функции через параметр config_name.

Метод app.config.from_object() используется для загрузки конфигурации из словаря конфигурации. Затем эта конфигурация используется для инициализации приложения. Наконец, база данных экземпляра SQLAlchemy инициализируется экземпляром приложения.

Давайте настроим первые конечные точки для API, запросы GET.

Настройка запросов GET
Добавим функции запроса GET в файл app/routes.py:

import os
from . import create_app
from .models import Book
from flask import jsonify

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/book/list", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])

@app.route("/book/<int:isbn>", methods=["GET"])
def get_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    return jsonify(book.to_json())
Функция create_app() создает экземпляр приложения, а затем использует декоратор app.route() для регистрации конечных точек. Внутри метода get_books() мы запрашиваем базу данных для всех книг с помощью Book.query.all(), а затем возвращаем JSON-представление всех книг с помощью функции jsonify(); это вспомогательная функция, которая сериализует объекты Python в JSON.

Теперь давайте добавим некоторые данные через SQLAlchemy перед запуском приложения.

Добавление данных в SQLAlchemy
Одним из способов добавления данных в базу данных является открытие интерактивной оболочки Flask, а затем создание нового экземпляра модели Book.

Прежде чем мы это сделаем, давайте настроим переменную среды приложения flask с помощью этой команды:

$ export FLASK_APP=bookshop.py
Если вы используете Windows, вместо этого используйте SET:

$ SET FLASK_APP=bookshop.py
и тогда мы можем запустить:

$ flask shell
Эта команда открывает интерактивный сеанс для выполнения команд Python. Это помогает отлаживать и тестировать код.

Теперь мы внутри оболочки. Давайте импортируем экземпляр db и модель Book:

>>> from app import db
>>> db
<SQLAlchemy engine=mysql+pymysql://root:***@localhost:3306/flaskapp?charset=utf8>
>>> from app.models import Book
>>> Book
<class 'app.models.Book'>
С предположением, что база данных flaskapp уже создана на вашем компьютере. Создадим таблицу Book в базе данных, а затем определим новую книгу:

>>> db.create_all()
>>> book = Book(author="Ezz", title="Cleaner Python", price=0.0)
>>> book
<app.models.Book object at 0x7f404a052e50>
>>> db.session.add(book)
>>> db.session.commit()
Итак, теперь таблица Book была создана с db.create_all(), который делает все таблицы, которые являются подклассами db. Модель.

Переменная book добавляется в базу данных с помощью db.session.add(). Обратите внимание, что добавление объекта book в базу данных не означает, что вы можете запрашивать его. Он еще не привязан к базе данных. Вот почему нам нужно запустить db.session.commit(), чтобы сохранить изменения, которые мы внесли в базу данных.

Создадим еще одну книгу:

>>> book2 = Book(author="Ahmed", title="Python", price=10.99)
>>> db.session.add(book2)
>>> db.session.commit()
Итак, теперь у нас есть две книги в нашем книжном магазине. Этого будет достаточно, чтобы продемонстрировать листинг и игру с API.

Закроем оболочку с помощью CTRL+C (или CMD+C) и вернемся к нашему терминалу для запуска приложения.

Запуск приложения Flask
Вы можете запустить приложение, выполнив на терминале следующую команду:

$ export FLASK_APP=bookshop.py
$ flask run
На Окнах:

$ SET FLASK_APP=bookshop.py
$ flask run
Первая команда определяет переменную среды FLASK_APP, указывающую на файл bookshop.py. Если вы уже определили FLASK_APP, вы не должны повторяться. Вы обнаружите ожидаемую ошибку при запуске колбы. Этот файл пуст. Давайте исправим это и импортируем переменную приложения из файла:bookshop.pyapp/routes.py

from app.routes import app
Теперь можно запустить приложение и предоставить конечные точки API на http://localhost:5000/book/list.

В этом случае вы найдете следующий ответ JSON:

[
  {
    "author": "Ezz", 
    "isbn": 1, 
    "price": 0.0, 
    "title": "Cleaner Python"
  }, 
  {
    "author": "Ahmed", 
    "isbn": 2, 
    "price": 10.99, 
    "title": "Python"
  }
]
И когда вы вызовете эту конечную точку http://localhost:5000/book/1, вы получите первую книгу:

{
  "author": "Ezz", 
  "isbn": 1, 
  "price": 0.0, 
  "title": "Cleaner Python"
}
Заменив 1 на ISBN книги, вы получите ответ, связанный с книгой, которую вы запросили.

Удаление книги
Запрос DELETE аналогичен тому, что мы сделали для запроса GET. Давайте снова откроем файл app/routes.py и добавим следующий фрагмент:

from . import db
# ...

@app.route("/book/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'result': True})
Здесь мы используем db.session.delete(book) для удаления книги из базы данных, а затем фиксируем это изменение с помощью db.session.commit().

Вы можете задаться вопросом, как протестировать эту конечную точку, если маршрут DELETE совпадает с маршрутом GET. Чтобы удалить книгу, вы можете использовать curl или любую клиентскую программу API, такую как Postman, и выбрать метод DELETE, поскольку по умолчанию он будет рассматривать запрос как запрос GET.

Например, если вы хотите удалить вторую книгу, вы можете использовать следующую команду:

$ curl http://localhost:5000/book/2 -X DELETE
{
  "result": true
}
Который успешно возвращает ответ JSON с ключом результата, равным True, как и ожидалось.

Вы можете снова вызвать конечную точку GET, чтобы проверить, прошла ли вторая книга, просмотрев URL-адрес: http://localhost:5000/book/list или с помощью команды curl:

$ curl http://localhost:5000/book/list
[
  {
    "author": "Ezz", 
    "isbn": 1, 
    "price": 0.0, 
    "title": "Cleaner Python"
  }
]
Который дает список только из одной книги; первый.

Добавление новой книги
Мы также можем добавить новую книгу в базу данных, вызвав функцию метода POST.

from flask import request
...

@app.route('/book', methods=['POST'])
def create_book():
    if not request.json:
        abort(400)
    book = Book(
        title=request.json.get('title'),
        author=request.json.get('author'),
        price=request.json.get('price')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_json()), 201
Чтобы протестировать добавление новой книги, давайте снова воспользуемся программой curl:

$ curl -H "Content-Type: application/json" -X POST -d '{"title": "Learning", "author": "Ibrahim", "price": "3.44"}' http://localhost:5000/book
{
  "author": "Ibrahim", 
  "isbn": 3, 
  "price": 3.44, 
  "title": "Learning"
}
Конечно, мы также можем добавлять новые книги, используя оболочку колбы. Проблема с этим подходом заключается в том, что необходимо импортировать экземпляры db и Book. Чтобы избежать этого, теперь файл bookshop.py будет выглядеть следующим образом (после добавления в него фрагмента):

from app import db
from app.routes import app
from app.models import Book

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book)
Декоратор @app.shell_context_processor используется для регистрации функции, которая будет вызываться для вставки переменных в сеанс оболочки.

Функция make_shell_context() возвращает словарь, содержащий экземпляры db и Book, которые нам нужно добавить в сеанс оболочки, чтобы использовать их в оболочке без необходимости их импорта.

Обновление книги
Обновление книги похоже на добавление новой, за исключением того, что мы используем метод PUT вместо POST.

Добавим в файл app/routes.py следующее:

@app.route('/book/<int:isbn>', methods=['PUT'])
def update_book(isbn):
    if not request.json:
        abort(400)
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.price = request.json.get('price', book.price)
    db.session.commit()
    return jsonify(book.to_json())
Чтобы протестировать обновление книги, давайте используем curl:

$ curl http://localhost:5000/book/3 -X PUT -H "Content-Type: application/json" -d '{"author": "Ahmed", "title": "Python for Beginners", "price": 12.99}'
{
  "author": "Ahmed", 
  "isbn": 3, 
  "price": 12.99, 
  "title": "Python for Beginners"
}
Заключение
В этом учебнике рассматривалось создание RESTful API, который взаимодействует с приложением CRUD с помощью Flask и SQLAlchemy через реальное приложение.

Мы видели, как использовать SQLAlchemy для подключения к базе данных, как создать модель, как сопоставить модель с таблицей, как создать маршрут, как использовать программу curl для вызова и тестирования API и как использовать оболочку flask для отладки вашего приложения.

Мы также рассмотрели, как читать, создавать, обновлять и удалять книгу из приложения книжного магазина CRUD.

Вы можете получить полный код для этого учебника на этой странице.

Если вы хотите сделать графический пользовательский интерфейс вокруг приложения, то проверьте вторую часть учебника, где мы создаем хороший интерфейс с использованием Jinja2 и Bootstrap.