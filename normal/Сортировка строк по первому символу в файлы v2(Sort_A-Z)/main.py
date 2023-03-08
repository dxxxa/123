#!/usr/bin/python
# -*- coding: cp1251 -*-

#
# https://ru.stackoverflow.com/questions/1193403/%D0%A1%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D1%81%D1%82%D1%80%D0%BE%D0%BA-%D0%B2-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%BC-%D1%84%D0%B0%D0%B9%D0%BB%D0%B5?ysclid=l6dntdmveq996744519


from random import choices
from tqdm.auto import tqdm
import os
import shutil


# Создание Класса LetterFile
class LetterFile:  # Ключевое слово class(создать класс) за которым следует наименование класса(LetterFile).
    #  Слово self это способ описания любого объекта
    def __init__(self, letter, max_lines):  # метод __init__ — это конструкторметод, вызывается при создании объекта класса, self для обращения в переменным и методам объекта
        self.letter = letter  # Атрибут объекта
        self.number = 0  # Атрибут объекта
        self.line_count = 0  # Атрибут объекта
        self.max_lines = max_lines  # Атрибут объекта
        #os.chdir(path_sort)  # нужен?
        self.create()

    def create(self):  # Метод объекта
        self.open('w')

    def open(self, mode='w+'):  # Метод объекта
        self.file = open(self.letter + "(" + str(self.number) + ")" + '.txt', mode)

    def close(self):  # Метод объекта
        self.file.close()

    def append(self, line):  # Метод объекта
        self.file.write(line)
        self.line_count += 1
        if self.line_count >= self.max_lines:
            self.close()
            self.number += 1
            self.line_count = 0
            self.open()


# Генератор [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
def get_big_letters():
    # Функция ord() обратная chr().   >>> ord('A') # 65   >>> chr(65) # 'A'
    for ch in range(ord('A'), ord('Z') + 1):  # Функция ord() вернет число/позицию в таблице Unicode для символов 'A-Z'
        # Ключевое слово yield используется в функциях так же, как и return – для возвращения результата работы.
        # Разница заключается в том, что yield возвращает генератор.
        yield chr(ch)  # Функция chr() вернет строку, представляющую символ, из таблицы Unicode


# Генератор [abcdefghijklmnopqrstuvwxyz]
def get_small_letters():
    # Функция ord() обратная chr().   >>> ord('a') # 97      >>> chr(97) # 'a'
    for ch1 in range(ord('a'), ord('z') + 1):  # Функция ord() вернет число/позицию в таблице Unicode для символов 'a-z'
        # Ключевое слово yield используется в функциях так же, как и return – для возвращения результата работы.
        # Разница заключается в том, что yield возвращает генератор.
        yield chr(ch1)  # Функция chr() вернет строку, представляющую символ, из таблицы Unicode


# Генератор [0123456789]
def digits():
    # Функция ord() обратная chr().   >>> ord('0') # 48   >>> chr(48) # '0'
    for ch2 in range(ord('0'), ord('9') + 1):  # Функция ord() вернет число/позицию в таблице Unicode для символов '0-9'
        # Ключевое слово yield используется в функциях так же, как и return – для возвращения результата работы.
        # Разница заключается в том, что yield возвращает генератор.
        yield chr(ch2)  # Функция chr() вернет строку, представляющую символ, из таблицы Unicode


input_file_name = 'data.txt'
# input_file_rows = 15_000_000
max_lines = 300000_000  # Максимальное количество строк в файле
# str_len = 15  # Максимальное количество символов в строке
alphabet0 = list(get_big_letters())  # Генератор [ABCDEFGHIJKLMNOPQRSTUVWXYZ] переводим в список
alphabet1 = list(get_small_letters())  # Генератор [abcdefghijklmnopqrstuvwxyz] переводим в список
alphabet2 = list(digits())  # Генератор [0123456789] переводим в список
print("\nBig_Letters:  [", *alphabet0, "]"
      "\nSmall_Letters:[", *alphabet1, "]"
      "\nNumbers:      [", *alphabet2, "]"
      "\n#####################################")

# print('[0] Generating input File ### Генерация Файла')
# with open(input_file_name, 'w') as f:
#    for i in tqdm(range(input_file_rows)):
#        s = ''.join(choices(alphabet, k=str_len))
#        f.write(s)
#        f.write('\n')

path = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\"  # Каталог текстовых файлов
path_data = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\data.txt"  # Путь к файлу сортировки data.txt
path_sort = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\Sort"  # Каталог сортировки с файлами 0-9.txt & A-Z.txt

line_count = 0

# input("Press Enter to continue1...")
# print("Текущая деректория:", os.getcwd())
# os.chdir(path_sort)

if os.path.exists(path_data):  # os.path.exists(path_data) Проверяет существует ли файл "C:\\Users\\path_data\\text.txt"
    print("Файл data.txt найден")
    files = {}  # Фигурные скобки: представляют тип данных словаря(dict), а словарь состоит из групп значений пар ключей
                # dicts = [
                #    {'id': 123, 'name': 'L'},
                #    {'id': 234, 'name': 'K'},
                #    {'id': 345, 'name': 'P'}
                # ]
                # print(dicts[0]['name'])
                # 'L'

    #os.mkdir(path_sort)  # Создает директорию "C:\\Users\\path_sort"

    #directory_folder = r"C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\test"
    #folder_path = os.path.dirname(directory_folder)  # Путь к папке с файлом
    #if not os.path.exists(folder_path):  # Если пути не существует создаем его
    #    os.makedirs(folder_path)

    print('[1] Create Files')
    os.chdir(path_sort)  # Функция chdir() модуля os изменяет текущий рабочий каталог на path_sort ("C:\\Users\\path_sort")

    for ch in alphabet0:  # Список Генератора [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
        f = LetterFile(ch, max_lines)  # Передает A-Z в класс(LetterFile)
        files[ch] = f

    for ch1 in alphabet1:  # Список Генератора [abcdefghijklmnopqrstuvwxyz]
        f = LetterFile(ch1, max_lines)  # Передает a-z в класс(LetterFile)
        files[ch1] = f

    for ch2 in alphabet2:  # Список Генератора [0123456789]
        f = LetterFile(ch2, max_lines)  # Передает 0-9 в класс(LetterFile)
        files[ch2] = f

    print('[2] Process input File')
    os.chdir("..")  # Функция chdir() модуля os изменяет текущий рабочий каталог на ".." (предыдущий) ("C:\\Users")

    try:
        er = 0
        with open(input_file_name) as fr:
        #with open(input_file_name, encoding='ascii', errors='ignore') as fr:
            try:
            #    file = open('ok123.txt', 'r')
            except FileNotFoundError as e:
            #    print(e)

            i = 0  # Для счетчика строк с Symbol
            for s in tqdm(fr.readlines()):
                try:
                    fw = files[s[0].upper()]  # Метод string upper() преобразует все символы нижнего регистра в строке в символы верхнего регистра
                except:
                    i += 1  # Счетчик ошибок
                    my_file = open("Symbol.txt", "a")  # Запись ошибок ошибок
                    my_file.write(s)
                    my_file.close()
                fw.append(s)
            print("Error: Строк с символом!!!", i)
        print('[3] Closing Files')
        os.chdir(path_sort)  # Функция chdir() модуля os изменяет текущий рабочий каталог на path_sort ("C:\\Users\\path_sort")

        for ch in alphabet0:
            f = files[ch]
            f.close()

        for ch1 in alphabet1:
            f = files[ch1]
            f.close()

        for ch2 in alphabet2:
            f = files[ch2]
            f.close()
    except:
        # получим объект файла
        # file1 = open("C:\\Users\\nUser\\Desktop\\Sort_A-Z\\data.txt", "r")
        # while True:
        #    line = file1.readline()  # считываем строку
        #    if not line:  # прерываем цикл, если строка пустая
        #        break
        #    print(line.strip())  # выводим строку
        # file1.close  # закрываем файл

        print("[Error!]Удаление каталога Sort и файлов.txt")  # ИСПРАВИТЬ !!! Процесс не может получить доступ к файлу, так как этот файл занят другим процессом: 'C:\\Users\\nUser\\Desktop\\Sort_A-Z\\Sort\\0(0).txt
        # shutil.rmtree(path_sort)  # Функция rmtree() модуля shutil рекурсивно удаляет все дерево каталогов path_sort.



    print('[4] Counting rows Files')
    # input("(Press Enter to continue...)")
    print("=====================================")
    os.chdir(path)  # Функция chdir() модуля os изменяет текущий рабочий каталог на ".." (предыдущий) ("C:\\Users")

    with open('data.txt') as f:
        n = 0
        for line in f:
            n += 1
    # print("Data.txt = ", n)
    # line_count_d = line_count - n
    # abc = print(f"Всего строк - Data.txt {line_count_d}")
    # print("=====================================")

    os.chdir(path_sort)  # Функция chdir() модуля os изменяет текущий рабочий каталог на path_sort ("C:\\Users\\path_sort")
    # Вывести список всех файлов каталога и количество строк в них
    for file in os.listdir(path_sort):  # Функция listdir() модуля os возвращает список, содержащий имена файлов и директорий в каталоге, заданном путем path.
        if file.endswith(".txt"):  # Паттерн поиска файлов по расширению
            if (file == 'data.txt'):  # Если имя файла data.txt
                continue  # то пропускет его
            else:  # Иначе
                local_count = 0
                # Вариант подсчета строк без загрузки файла в память целиком
                with open(file) as f:
                    quantity = sum(1 for line in f)

                print(f'{os.path.join(path, file)} - {quantity} строк')
                line_count += quantity
    print("=====================================")
    print("Data.txt = ", n)
    print(f"Всего строк - {line_count}")

else:
    print("Файл data.txt не найден")
