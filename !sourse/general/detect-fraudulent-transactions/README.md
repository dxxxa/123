# [Detecting Fraudulent Transactions in a Streaming Application using Kafka in Python](https://www.thepythoncode.com/article/detect-fraudulent-transactions-with-apache-kafka-in-python)
Check the original repo [here](https://github.com/bassemmarji/Kafka_Fraud_Detector).
##
# [[] / []]()
По мере масштабирования и миграции систем борьба с мошенниками стала первостепенной задачей, которую лучше всего решать с помощью технологий обработки потоков в режиме реального времени.

Для целей этого урока мы создадим с нуля систему обнаружения мошенничества в режиме реального времени, где мы будем генерировать поток фиктивных транзакций и синхронно анализировать их, чтобы обнаружить, какие из них являются мошенническими.

Необходимые условия
В соответствии с нашими требованиями нам нужна надежная, масштабируемая и отказоустойчивая платформа потоковой передачи событий, которая хранит наши входные события или транзакции и результаты процесса. Apache Kafka — это распределенная потоковая платформа с открытым исходным кодом, которая отвечает именно этой потребности.

Apache Kafka можно скачать с его официального сайта, установка и запуск Apache Kafka на вашей операционной системе выходит за рамки этого учебника. Тем не менее, вы можете проверить это руководство, которое показывает, как установить его на Ubuntu (или любой дистрибутив на основе Debian).

После того, как все настроено, вы можете проверить следующее:

Экземпляр Zookeeper работает на TCP-порту 2181.
Экземпляр Kafka запущен и привязан к TCP-порту 9092.
Если вышеупомянутые элементы управления выполнены, то теперь у вас есть кластер Kafka с одним узлом.

Создание скелета приложения
Теперь мы можем начать создавать наше приложение для обнаружения мошенничества в режиме реального времени, используя API для потребителей и производителей Kafka.

Наша заявка будет состоять из:

Генератор транзакций на одном конце, который производит фиктивные транзакции для имитации потока событий.
Детектор мошенничества, с другой стороны, чтобы отфильтровать транзакции, которые выглядят подозрительно.
Следующая блок-схема процесса демонстрирует наш дизайн:

Блок-схема детектора мошеннических транзакций

Давайте перейдем прямо к настройке. Конечно, вам нужен Python 3, установленный в вашей системе. Я буду использовать виртуальную среду, где я устанавливаю необходимые библиотеки, и это, несомненно, лучший подход для выбора:

Создайте виртуальную среду и активируйте ее:
$ python -m venv fraud-detector
$ source fraud-detector/bin/activate
Создайте требования к файлу.txt и добавьте к нему следующие строки:
Kafka-python==2.0.2
Flask==1.1.2
Установите библиотеки:
$ pip install -r requirements.txt
В конце этого учебника структура папок будет выглядеть следующим образом:

Окончательная структура проектаОчистив это, давайте теперь начнем писать фактический код.

Во-первых, давайте инициализируем наши параметры в settings.py файле:

# URL for our broker used for connecting to the Kafka cluster
KAFKA_BROKER_URL   = "localhost:9092"
# name of the topic hosting the transactions to be processed and requiring processing
TRANSACTIONS_TOPIC = "queuing.transactions"
# these 2 variables will control the amount of transactions automatically generated
TRANSACTIONS_PER_SECOND = float("2.0")
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND
# name of the topic hosting the legitimate transactions
LEGIT_TOPIC = "queuing.legit"
# name of the topic hosting the suspicious transactions
FRAUD_TOPIC = "queuing.fraud"
Примечание: Для краткости я жестко закодировал параметры конфигурации в settings.py, но рекомендуется хранить эти параметры в отдельном файле (например, .env)

Во-вторых, давайте создадим файл Python с именем transactions.py для создания рандомизированных транзакций на лету:

from random import choices, randint
from string import ascii_letters, digits

account_chars: str = digits + ascii_letters

def _random_account_id() -> str:
    """Return a random account number made of 12 characters"""
    return "".join(choices(account_chars,k=12))

def _random_amount() -> float:
    """Return a random amount between 1.00 and 1000.00"""
    return randint(100,1000000)/100

def create_random_transaction() -> dict:
    """Create a fake randomised transaction."""
    return {
        "source":_random_account_id()
       ,"target":_random_account_id()
       ,"amount":_random_amount()
       ,"currency":"EUR"
    }
В-третьих, давайте построим наш генератор транзакций, который будет использоваться для создания потока транзакций. Файл Python producer.py будет играть роль генератора транзакций и будет хранить опубликованные транзакции в теме под названием queuing.transactions, ниже приведен код producer.py:

import os
import json
from time import sleep
from kafka import KafkaProducer
# import initialization parameters
from settings import *
from transactions import create_random_transaction


if __name__ == "__main__":
   producer = KafkaProducer(bootstrap_servers = KAFKA_BROKER_URL
                            #Encode all values as JSON
                           ,value_serializer = lambda value: json.dumps(value).encode()
                           ,)
   while True:
       transaction: dict = create_random_transaction()
       producer.send(TRANSACTIONS_TOPIC, value= transaction)
       print(transaction) #DEBUG
       sleep(SLEEP_TIME)
Чтобы убедиться, что вы на правильном пути, давайте протестируем программу producer.py. Для этого откройте окно терминала и введите следующую команду:

$ python producer.py
Примечание: Перед выполнением теста убедитесь, что сервер Kafka запущен.

Вы должны увидеть результат, подобный следующему:

Сгенерированные поддельные транзакцииВ-четвертых, после того, как мы гарантировали, что наша продюсерская программа запущена и работает, давайте перейдем к созданию механизма обнаружения мошенничества для обработки потока транзакций и выявления мошеннических.

Мы разработаем две версии этой программы:

Версия 1 detector.py: Эта программа будет отфильтровывать транзакции в очереди на основе определенных критериев или набора критериев и выводит результаты в две отдельные темы: одна для законных транзакций LEGIT_TOPIC, а другая FRAUD_TOPIC для мошеннических, которые соответствуют критериям, которые мы выбрали.
Эта программа основана на потребительском API Kafka Python, этот API позволяет потребителям подписываться на определенные темы Kafka, и Kafka будет автоматически транслировать им сообщения, пока эти сообщения публикуются.

Ниже приведен код для detector.py:

import os
import json
from kafka import KafkaConsumer, KafkaProducer
from settings import *

def is_suspicious(transaction: dict) -> bool:
    """Simple condition to determine whether a transaction is suspicious."""
    return transaction["amount"] >= 900

if __name__ == "__main__":
   consumer = KafkaConsumer(
       TRANSACTIONS_TOPIC
      ,bootstrap_servers=KAFKA_BROKER_URL
      ,value_deserializer = lambda value: json.loads(value)
      ,
   )

   for message in consumer:
       transaction: dict = message.value
       topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
       print(topic,transaction) #DEBUG
Для простоты я выбрал базовое условие функции is_suspicious(), которая основана на простом предикате (то есть, если сумма транзакции больше или равна 900, то это подозрительно). Однако в реальных сценариях может быть задействовано множество параметров, среди которых:

Инициатор учитывает транзакцию, будь то активная, неактивная или неактивная.
Местоположение транзакции, инициированной организацией, предположительно закрытой в течение периода блокировки.
Эти сценарии составят ядро решения по борьбе с мошенничеством и должны быть тщательно разработаны для обеспечения гибкости и оперативности этого решения.

Давайте теперь протестируем как producer.py, так и detector.py, откроем новое окно терминала и введем следующее:

$ python producer.py
Одновременно откройте другое окно и введите:

$ python detector.py
Примечание: Перед выполнением теста убедитесь, что сервер Kafka запущен.

Вы увидите результат, аналогичный этому, на detector.py:

Обнаруженные мошеннические транзакцииОтладочная печать, включенная в программу, выведет транзакции на консоль и укажет целевую очередь на основе условия, которое мы указали и связали с суммой транзакции.

Версия 2 appdetector.py: Это расширенная версия сценария detector.py, который позволит передавать транзакции в Интернет с помощью микрофреймворка Flask.
В этом коде используются следующие технологии:

Flask: микро веб-фреймворк на Python.
События, отправленные сервером (SSE): тип механизма принудительной отправки сервера, при котором клиент подписывается на поток обновлений, генерируемый сервером, и всякий раз, когда происходит новое событие, клиенту отправляется уведомление.
Jinja2: современный шаблонизатор, широко используемый в экосистеме Python. Flask поддерживает Jinja2 по умолчанию.
Ниже приведен appdetector.py:

from flask import Flask, Response, stream_with_context, render_template, json, url_for

from kafka import KafkaConsumer
from settings import *

# create the flask object app
app = Flask(__name__)

def stream_template(template_name, **context):
    print('template name =',template_name)
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

def is_suspicious(transaction: dict) -> bool:
    """Determine whether a transaction is suspicious."""
    return transaction["amount"] >= 900

# this router will render the template named index.html and will pass the following parameters to it:
# title and Kafka stream
@app.route('/')
def index():
    def g():
        consumer = KafkaConsumer(
            TRANSACTIONS_TOPIC
            , bootstrap_servers=KAFKA_BROKER_URL
            , value_deserializer=lambda value: json.loads(value)
            ,
        )
        for message in consumer:
            transaction: dict = message.value
            topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
            print(topic, transaction)  # DEBUG
            yield topic, transaction

    return Response(stream_template('index.html', title='Fraud Detector / Kafka',data=g()))

if __name__ == "__main__":
   app.run(host="localhost" , debug=True)
Далее мы определим индекс шаблона.html HTML-файл, который использовался функцией маршрута index() и находится в папке templates:

<!doctype html>
<title> Send Javascript with template demo </title>
<html>
<head>
</head>
<body>
    <div class="container">
        <h1>{{title}}</h1>
    </div>
    <div id="data"></div>
    {% for topic, transaction in data: %}
    <script>
        var topic = "{{ topic }}";
        var transaction = "{{ transaction }}";
        if (topic.search("fraud") > 0) {
            topic = topic.fontcolor("red")
        } else {
            topic = topic.fontcolor("green")
        }
        document.getElementById('data').innerHTML += "<br>" + topic + " " + transaction;
    </script>
    {% endfor %}
</body>
</html>
индекс.html содержит Javascript, позволяющий выполнять итерацию по всему принятому потоку и отображать транзакции по мере их получения.

Теперь, чтобы запустить его, убедитесь, что producer.py запущен, а затем:

$ python appdetector.py
Он должен запустить локальный сервер на порту 5000, перейти в ваш браузер и получить доступ к http://localhost:5000, где запущен экземпляр Flask, вы увидите непрерывную потоковую передачу законных и мошеннических транзакций, как показано на следующем экране:

Фильтрация непрерывных транзакцийВы можете проверить полный код здесь.