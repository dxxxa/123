# [How to Use Pickle for Object Serialization in Python](https://www.thepythoncode.com/article/object-serialization-saving-and-loading-objects-using-pickle-python)
##
# [[] / []]()
Сериализация объектов — это процесс преобразования структур данных или состояния объекта в формат, который может быть сохранен в файле или передан и реконструирован позже. В этом учебнике вы узнаете, как использовать встроенный модуль pickle для сериализации и десериализации объектов в Python.

Сериализацию в Python часто называют маринованием. Маринование — это просто процесс, при котором иерархия объектов Python преобразуется в байтовый поток, а отмена выбора — это обратная операция.

СВЯЗАННЫЕ С: Как сжимать и распаковывать файлы в Python.

Давайте начнем с выбора основных структур данных Python:

import pickle

# define any Python data structure including lists, sets, tuples, dicts, etc.
l = list(range(10000))
Я использовал здесь список, который содержит 10000 элементов только в демонстрационных целях, вы можете использовать любой объект Python, приведенный ниже код сохранит этот список в файл:

# save it to a file
with open("list.pickle", "wb") as file:
    pickle.dump(l, file)
pickle.dump(obj, file) записывает маринованное представление obj (в данном случае список) в открытый файл (в режиме записи и байтов "wb"), загрузим этот объект еще раз:

# load it again
with open("list.pickle", "rb") as file:
    unpickled_l = pickle.load(file)
pickle.load(file) считывает и возвращает объект из данных pickle, хранящихся в файле (открывается в режиме чтения и байтов "rb"), сравнивая исходный и невыбранный объект:

print("unpickled_l == l: ", unpickled_l == l)
print("unpickled l is l: ", unpickled_l is l)
Выпуск:

unpickled_l == l:  True
unpickled l is l:  False
Имеет смысл, значения списка все те же (равны), но он не идентичен, другими словами, невыбранный список имеет другое место в памяти, поэтому это буквально копия исходного объекта.

Можно также сохранять и загружать экземпляры объектов пользовательских классов. Например, давайте определим простой класс Person:

class Person:
    def __init__(self, first_name, last_name, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"<Person name={self.first_name} {self.last_name}, age={self.age}, gender={self.gender}>"

p = Person("John", "Doe", 99, "Male")
Давайте сделаем тот же процесс снова:

# save the object
with open("person.pickle", "wb") as file:
    pickle.dump(p, file)

# load the object
with open("person.pickle", "rb") as file:
    p2 = pickle.load(file)

print(p)
print(p2)
Это приводит к следующему:

<Person name=John Doe, age=99, gender=Male>
<Person name=John Doe, age=99, gender=Male>
Как правило, если требуется отменить пикирование определяемого пользователем конкретного объекта, необходимо реализовать его класс в текущей области, в противном случае возникнет ошибка.

Например, если вы распакуете массив NumPy (или любые другие определенные объекты, которые находятся в установленных модулях), Python автоматически импортирует модуль NumPy и загрузит объект для вас.

Можно также использовать функцию pickle.dumps(obj), которая возвращает маринованное представление объекта в виде байтового объекта, чтобы его можно было зашифровать, передать или что-то еще. Приведенный ниже код рассеивает и расстегивает предыдущий объект с помощью функций pickle.dumps(obj) и pickle.loads(data):

# get the dumped bytes
dumped_p = pickle.dumps(p)
print(dumped_p)

# write them to a file
with open("person.pickle", "wb") as file:
    file.write(dumped_p)

# load it
with open("person.pickle", "rb") as file:
    p2 = pickle.loads(file.read())
Взгляните на повторное представление байтов этого объекта:

b'\x80\x03c__main__\nPerson\nq\x00)\x81q\x01}q\x02(X\n\x00\x00\x00first_nameq\x03X\x04\x00\x00\x00Johnq\x04X\t\x00\x00\x00last_nameq\x05X\x03\x00\x00\x00Doeq\x06X\x03\x00\x00\x00ageq\x07KcX\x06\x00\x00\x00genderq\x08X\x04\x00\x00\x00Maleq\tub.'
Да, это верно, не читается человеком, это потому, что он в двоичном формате.

Наконец, вот список объектов, которые вы можете мариновать и снимать:

Нет.
Логические переменные (True и False).
Целые числа, числа с плавающей запятой и комплексные числа.
Строки, байты, массивы байтов.
Кортежи, списки, наборы и словари, содержащие только маринованные объекты.
Функции, определенные на верхнем уровне модуля (с использованием def, а не лямбда).
Встроенные функции, определенные на верхнем уровне модуля (например, max, min, bool и т.д.).
Классы, определенные на верхнем уровне модуля.
Смотрите официальную документацию по Python для получения дополнительной информации.