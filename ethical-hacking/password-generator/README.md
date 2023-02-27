# [How to Make a Password Generator in Python](https://www.thepythoncode.com/article/make-a-password-generator-in-python)
##
# [[] / []]()
Генераторы паролей — это инструменты, которые позволяют пользователю создавать случайные и настраиваемые надежные пароли на основе предпочтений.

В этом уроке мы создадим инструмент командной строки на Python для генерации паролей. Мы будем использовать модуль argparse, чтобы упростить анализ аргументов командной строки, предоставленных пользователем. Давайте начнем.

Импорт
Давайте импортируем некоторые модули. Для этой программы нам просто нужен класс ArgumentParser из argparse и модули random и secrets. Мы также получаем строковый модуль, который просто имеет несколько коллекций букв и цифр. Нам не нужно устанавливать какие-либо из них, потому что они поставляются с Python:

from argparse import ArgumentParser
import secrets
import random
import string
Если вы не уверены, как работают случайные и секретные модули. Ознакомьтесь с этим учебником, в котором рассматривается создание случайных данных с помощью этих модулей.

Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Настройка средства синтаксического анализа аргументов
Теперь мы продолжим настройку парсера аргументов. Для этого мы создаем новый экземпляр класса ArgumentParser для нашей переменной parser. Мы даем парсеру имя и описание. Эта информация появится, если пользователь предоставит аргумент -h при запуске нашей программы, он также сообщит им доступные аргументы:

# Setting up the Argument Parser
parser = ArgumentParser(
    prog='Password Generator.',
    description='Generate any number of passwords with this tool.'
)
Мы продолжаем добавлять аргументы в синтаксический анализатор. Первые четыре будут номером каждого типа символов; числа, строчные, прописные и специальные символы, мы также устанавливаем тип этих аргументов как int:

# Adding the arguments to the parser
parser.add_argument("-n", "--numbers", default=0, help="Number of digits in the PW", type=int)
parser.add_argument("-l", "--lowercase", default=0, help="Number of lowercase chars in the PW", type=int)
parser.add_argument("-u", "--uppercase", default=0, help="Number of uppercase chars in the PW", type=int)
parser.add_argument("-s", "--special-chars", default=0, help="Number of special chars in the PW", type=int)
Далее, если пользователь хочет вместо этого передать общее количество символов пароля и не хочет указывать точное количество каждого типа символов, то аргумент -t или --total-length обрабатывает это:

# add total pw length argument
parser.add_argument("-t", "--total-length", type=int, 
                    help="The total password length. If passed, it will ignore -n, -l, -u and -s, " \
                    "and generate completely random passwords with the specified length")
Следующими двумя аргументами являются выходной файл, в котором мы храним пароли, и количество паролей для генерации. Сумма будет целым, а выходной файл — строкой (по умолчанию):

# The amount is a number so we check it to be of type int.
parser.add_argument("-a", "--amount", default=1, type=int)
parser.add_argument("-o", "--output-file")
И последнее, но не менее важное: мы анализируем командную строку для этих аргументов с помощью метода parse_args() класса ArgumentParser. Если мы не вызовем этот метод, синтаксический анализатор ничего не проверит и не вызовет никаких исключений:

# Parsing the command line arguments.
args = parser.parse_args()
Цикл паролей
Продолжаем с основной частью программы: циклом паролей. Здесь мы генерируем количество паролей, указанных пользователем.

Нам нужно определить список паролей, который будет содержать все сгенерированные пароли:

# list of passwords
passwords = []
# Looping through the amount of passwords.
for _ in range(args.amount):
В цикле for мы сначала проверяем, передается ли total_length. Если это так, то мы напрямую генерируем случайный пароль, используя указанную длину:

    if args.total_length:
        # generate random password with the length
        # of total_length based on all available characters
        passwords.append("".join(
            [secrets.choice(string.digits + string.ascii_letters + string.punctuation) \
                for _ in range(args.total_length)]))
Мы используем модуль секретов вместо случайного, чтобы мы могли генерировать криптографически надежные случайные пароли, подробнее в этом уроке.

В противном случае мы составляем список паролей, который сначала будет содержать все возможные буквы, а затем строку пароля:

    else:
        password = []
Теперь добавим возможные буквы, цифры и специальные символы в список паролей. Для каждого из типов мы проверяем, передан ли он парсеру. Получаем соответствующие буквы из строкового модуля:

        # If / how many numbers the password should contain  
        for _ in range(args.numbers):
            password.append(secrets.choice(string.digits))

        # If / how many uppercase characters the password should contain   
        for _ in range(args.uppercase):
            password.append(secrets.choice(string.ascii_uppercase))
        
        # If / how many lowercase characters the password should contain   
        for _ in range(args.lowercase):
            password.append(secrets.choice(string.ascii_lowercase))

        # If / how many special characters the password should contain   
        for _ in range(args.special_chars):
            password.append(secrets.choice(string.punctuation))
Затем мы используем функцию random.shuffle(), чтобы перепутать список. Это делается на месте:

        # Shuffle the list with all the possible letters, numbers and symbols.
        random.shuffle(password)
После этого мы соединяем результирующие символы с пустой строкой "", чтобы у нас была строковая версия:

        # Get the letters of the string up to the length argument and then join them.
        password = ''.join(password)
И последнее, но не менее важное: мы добавляем этот пароль в список паролей.

        # append this password to the overall list of password.
        passwords.append(password)
Опять же, если вы не знаете, как работает случайный модуль, ознакомьтесь с этим учебником, который охватывает генерацию случайных данных с помощью этого модуля.

Сохранение паролей
После цикла ввода пароля мы проверяем, указал ли пользователь выходной файл. Если это так, мы просто открываем файл (который будет сделан, если его не существует) и пишем список паролей:

# Store the password to a .txt file.
if args.output_file:
    with open(args.output_file, 'w') as f:
        f.write('\n'.join(passwords))
Во всех случаях мы распечатываем пароли.

print('\n'.join(passwords))
Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Примеры
Теперь воспользуемся скриптом для генерации различных комбинаций паролей. Во-первых, давайте распечатаем справку:

$ python password_generator.py --help
usage: Password Generator. [-h] [-n NUMBERS] [-l LOWERCASE] [-u UPPERCASE] [-s SPECIAL_CHARS] [-t TOTAL_LENGTH]
                           [-a AMOUNT] [-o OUTPUT_FILE]

Generate any number of passwords with this tool.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBERS, --numbers NUMBERS
                        Number of digits in the PW
  -l LOWERCASE, --lowercase LOWERCASE
                        Number of lowercase chars in the PW
  -u UPPERCASE, --uppercase UPPERCASE
                        Number of uppercase chars in the PW
  -s SPECIAL_CHARS, --special-chars SPECIAL_CHARS
                        Number of special chars in the PW
  -t TOTAL_LENGTH, --total-length TOTAL_LENGTH
                        The total password length. If passed, it will ignore -n, -l, -u and -s, and generate completely   
                        random passwords with the specified length
  -a AMOUNT, --amount AMOUNT
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
Многое для освещения, начиная с параметра --total-length или -t:

$ python password_generator.py --total-length 12
uQPxL'bkBV>#
Это сгенерировало пароль длиной 12 и содержит все возможные символы. Хорошо, давайте сгенерируем 10 различных паролей, как это:

$ python password_generator.py --total-length 12 --amount 10
&8I-%5r>2&W&
k&DW<kC/obbr
=/'e-I?M&,Q!
YZF:Lt{*?m#.
VTJO%dKrb9w6
E7}D|IU}^{E~
b:|F%#iTxLsp
&Yswgw&|W*xp
$M`ui`&v92cA
G3e9fXb3u'lc
Замечательно! Сгенерируем пароль с 5 строчными буквами, 2 прописными буквами, 3 цифрами и одним специальным символом, в общей сложности 11 символов:

$ python password_generator.py -l 5 -u 2 -n 3 -s 1
1'n3GqxoiS3
Итак, генерация 5 разных паролей на основе одного и того же правила:

$ python password_generator.py -l 5 -u 2 -n 3 -s 1 -a 5
Xs7iM%x2ia2
ap6xTC0n3.c
]Rx2dDf78xx
c11=jozGsO5
Uxi^fG914gi
Это здорово! Мы также можем генерировать случайные контакты из 6 цифр:

$ python password_generator.py -n 6 -a 5 
743582
810063
627433
801039
118201
Добавление 4 символов верхнего регистра и сохранение в файл с именем keys.txt:

$ python password_generator.py -n 6 -u 4 -a 5 --output-file keys.txt
75A7K66G2H
H33DPK1658
7443ROVD92
8U2HS2R922
T0Q2ET2842
Новый ключ.txt файл появится в текущем рабочем каталоге, который содержит эти пароли, вы можете сгенерировать столько паролей, сколько сможете:

$ python password_generator.py -n 6 -u 4 -a 5000 --output-file keys.txt
Заключение
Отлично! Вы успешно создали генератор паролей с помощью кода Python! Посмотрите, как вы можете добавить больше функций в эту программу!

Для длинных списков может потребоваться не печатать результаты в консоли, поэтому можно опустить последнюю строку кода, который выводит созданные пароли на консоль.