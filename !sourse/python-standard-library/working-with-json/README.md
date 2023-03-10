# [How to Work with JSON Files in Python](https://www.thepythoncode.com/article/working-with-json-files-in-python)
To run `example.py`, you have to install `requests` library:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
JSON (JavaScript Object Notation) - это легкий формат файлов обмена данными открытого стандарта, который использует читаемый человеком текст для передачи данных.

Хотя из названия можно сделать вывод, что это формат данных Javascript. Ну, не совсем так, JSON - это текстовый формат, который полностью независим от языка и использует соглашения, знакомые большинству популярных языков программирования, таких как Python.

В этом учебнике вы будете использовать Python для:

Сохранение данных JSON
Загрузка данных JSON
К счастью для нас, Python имеет встроенный модуль json, которого достаточно для нашей работы, давайте начнем!

Сохранение данных JSON
Словари Python очень похожи на формат JSON, на самом деле, вы можете сохранить словарь в очень нескольких строках кода:

import json

# example dictionary to save as JSON
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@doe.com",
    "salary": 1499.9, # just to demonstrate we can use floats as well
    "age": 17,
    "is_real": False, # also booleans!
    "titles": ["The Unknown", "Anonymous"] # also lists!
}

# save JSON file
# 1st option
with open("data1.json", "w") as f:
    json.dump(data, f)
Как только вы выполните приведенный выше код, вы заметите, что файл data1.json появился в вашем рабочем каталоге. Мы открыли файл в режиме записи и использовали функцию json.dump() для сериализации словаря Python в виде потока в формате JSON в открытый файл.

Полученный файл будет выглядеть примерно так:

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@doe.com",
    "salary": 1499.9,
    "age": 17,
    "is_real": false,
    "titles": [
        "The Unknown",
        "Anonymous"
    ]
}
Это один из способов сохранения в формате JSON, вы также можете использовать функцию json.dumps():

# 2nd option
with open("data2.json", "w") as f:
    f.write(json.dumps(data, indent=4))
Функция json.dumps() возвращает словарь в виде проанализированной строки JSON, вам может понадобиться эта строка для другого использования, мы просто сохранили ее в файл, чтобы вы знали, что она существует.

Обратите внимание, что на этот раз я добавил indent=4 в качестве параметра в функцию json.dumps(), это будет красиво печатать элементы массива JSON и члены объекта, если вы используете отступ = 0, он будет печатать только новые строки, а если это None (по умолчанию), то он сбрасывается в одну строку (не читается человеком). Ключевое слово T he indent существует как в функциях dump(), так и в функциях dumps().

Обработка символов, отличных от ASCII
Если ваши данные содержат символы, отличные от ASCII, и вам не нужны экземпляры Юникода в вашем JSON-файле (например, \u0623), то вы должны передать ensure_ascii=False в функцию json.dump():

unicode_data = {
    "first_name": "أحمد",
    "last_name": "علي"
}

with open("data_unicode.json", "w", encoding="utf-8") as f:
    json.dump(unicode_data, f, ensure_ascii=False)
Результирующий файл:

{"first_name": "أحمد", "last_name": "علي"}
Загрузка данных JSON
Десериализовать файлы JSON и загрузить их в Python довольно просто, приведенный ниже код загружает ранее сохраненный JSON-файл:

# read a JSON file
# 1st option
file_name = "data1.json"
with open(file_name) as f:
    data = json.load(f)
    
print(data)
Функция json.load() автоматически вернет словарь Python, что облегчит нашу работу с файлами JSON, вот вывод:

{'first_name': 'John', 'last_name': 'Doe', 'email': 'john@doe.com', 'salary': 1499.9, 'age': 17, 'is_real': False, 'titles': ['The Unknown', 'Anonymous']}
Аналогично, вы также можете использовать функцию json.loads() для чтения строки вместо этого:

# 2nd option
file_name = "data2.json"
with open(file_name) as f:
    data = json.loads(f.read())

print(data)
Итак, мы сначала прочитали содержимое файла с помощью метода read(), а затем передали его в функцию json.loads() для его синтаксического анализа.

Пример простой игрушки из реального мира
В этом разделе мы будем использовать запрос API к удаленному веб-серверу и сохранять полученные данные в JSON-файл, вот полный код для этого:

import requests
import json


# make API request and parse JSON automatically
data = requests.get("https://jsonplaceholder.typicode.com/users").json()
# save all data in a single JSON file
file_name = "user_data.json"
with open(file_name, "w") as f:
    json.dump(data, f, indent=4)
    print(file_name, "saved successfully!")

# or you can save each entry into a file
for user in data:
    # iterate over `data` list
    file_name = f"user_{user['id']}.json"
    with open(file_name, "w") as f:
        json.dump(user, f, indent=4)
        print(file_name, "saved successfully!")


# load 2nd user for instance
file_name = "user_2.json"
with open(file_name) as f:
    user_data = json.load(f)
    
print(user_data)
print("Username:", user_data["username"])
Заметка: Чтобы запустить приведенный выше код, вам нужно установить библиотеку запросов через: pip install requests

Заключение
Теперь вы знаете, как использовать функции dump(), dumps(),, load() и loads() в модуле json, и у вас есть возможность работать с данными JSON в Python.

Как разработчику, вам, вероятно, придется часто взаимодействовать с ним, вы будете сталкиваться с JSON много раз, особенно при работе с REST API, как мы показали в примере, или при сборе данных из Интернета.

Каждый код в этом учебнике включен в полную кодовую страницу, проверьте это!

Хотите узнать больше?
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python, удачи!