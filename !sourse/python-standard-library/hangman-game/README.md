# [How to Make a Hangman Game in Python](https://www.thepythoncode.com/article/make-a-hangman-game-in-python)
##
# [[] / []]()
Одним из самых популярных базовых проектов для новых программистов является игра под названием «Палач». Это игра в угадывание слов, где за каждую ошибку, допущенную игроком, будет нарисована фигура человека, висящая на виселице. Это довольно крутой проект в качестве приложения основ, которые вы только что изучили.

В этом уроке мы узнаем, как создать простую игру Hangman с использованием Python с нуля с базовым использованием некоторых встроенных модулей. С учетом сказанного, давайте начнем.

Содержание
Извлечение игровых слов
Создание класса Палача
Функция __init__
Создание функций для догадки
Проверка угаданных букв
Запуск игры с помощью main()
Извлечение игровых слов
Давайте начнем с того, что получим слова для палача. Я посмотрел на некоторых сайтах в Интернете, чтобы получить слова, которые используются для игры в палача, скопировать их в текстовый файл и назвать его словами.txt. Вы можете получить доступ к шахте здесь.

Создание класса Палача
Создайте файл Python с именем hangman.py и внутри него импортируйте os, random и ascii_letters из строкового модуля. Под ним создайте класс Hangman():

# /*hangman.py

from string import ascii_letters
import os
import random

class Hangman:
    
    def greet_user(self):
        print("Hangman\n")
Функция __init__
Над нашей функцией greet_user() добавим функцию __init__() в наш класс. Первое, что мы добавляем, это secret_word и guessed_word, где мы получаем доступ к словам.txt, выбираем секретное слово и передаем его secret_word в то время как guessed_word действует как пробелы в буквах слова, которое угадывает игрок (секретное слово).

class Hangman:

    def __init__(self):
        with open("./words.txt", "r") as file:
            words = file.read().split("\n")
            self.secret_word = random.choice(words)
            self.guessed_word = "*" * len(self.secret_word)

    def greet_user(self):
        print("Hangman\n")
Мы также добавляем количество incorrect_guess_limit (которое составляет 6, так как стикмен имеет 6 частей тела), количество incorrect_guesses, список букв wrong_guesses, gallow_pieces для виселицы и man_pieces:

class Hangman:

    def __init__(self):
        with open("./words.txt", "r") as file:
            words = file.read().split("\n")
            self.secret_word = random.choice(words)
            self.guessed_word = "*" * len(self.secret_word)

        self.incorrect_guess_limit = 6
        self.incorrect_guesses = 0
        self.wrong_guesses = []
        self.gallow_pieces = [
            "------",
            "|    |",
            "|    ",
            "|  ",
            "|   ",
            "|"
        ]
        self.gallow = "\n".join(self.gallow_pieces)
        self.man_pieces = [
            " \\",
            "/",
            " \\",
            " |",
            "/",
            "O",
        ]
    
    def greet_user(self):
        print("Hangman\n")
Создание функций для догадки
Давайте сначала создадим функцию, которая печатает все неправильные угадывания букв игрока. В начале игры он будет пустым и будет заполняться до тех пор, пока игрок не начнет догадываться об ошибках. Это помогает игроку увидеть, какие буквы уже устранены, и избежать того, чтобы игрок тратил ход на букву, которая уже вычеркнута из возможных букв:

    def show_list_of_wrong_guesses(self):
        print(f"Wrong guesses: {', '.join(self.wrong_guesses)}\n\n")
Следующая функция, которую мы создаем, — это функция, которая принимает угадывания букв. Он также проверяет, является ли данное предположение буквой, а не цифрой или символом. Если значение угадывания является буквой, оно вернет букву, а если нет, то распечатает сообщение «Недопустимый ввод» и снова попросит игрока ввести угадывание буквы. Помните, что ранее мы импортировали ascii_letters и собираемся использовать его для проверки персонажа, отправленного игроком:

    def take_guess(self) -> str:
        while True:
            guess = input("Guess a letter:\n>>> ")
            if len(guess) == 1 and guess in ascii_letters:
                break
            else:
                print("Invalid input")
        return guess
Давайте также создадим еще одну функцию для проверки, если игрок уже достиг неправильного предела угадывания:

    def is_out_of_guesses(self) -> bool:
        return self.incorrect_guesses == self.incorrect_guess_limit
Проверка угаданных букв
Создадим еще одну функцию внутри класса, которая проверяет букву, заданную из функции take_guess().

    def check_guess(self, guess_letter: str):
        if guess_letter in self.secret_word:
            self._correct_guess(guess_letter)
        else:
            self._wrong_guess(guess_letter)
Нам нужны еще две функции для перечисления значения угадывания, чтобы исправить догадки или неправильные догадки.

Давайте сначала получим функцию с именем _correct_guess(), которая принимает guess_letter в качестве аргумента.

    def _correct_guess(self, guess_letter: str):
        index_positions = [index for index, item in enumerate(self.secret_word) if item == guess_letter]
        for i in index_positions:
            self.guessed_word = self.guessed_word[0:i] + guess_letter + self.guessed_word[i+1:]
Index_positions проверяет каждую букву на self.secret_word одну за другой (перечисляя элементы и индексы), и каждый раз, когда элемент имеет одно и то же значение с guess_letter, индекс элемента будет указан в списке index_positions. Это связано с тем, что некоторые слова содержат одну и ту же букву два или более раз, такие слова, как «дверь», которая имеет 2 «о», «зубы», которые имеют 2 «t» и 2 «e», и «деление», которое имеет 3 «i».

Для каждого индекса, который у нас есть в index_positions мы добавим guess_letter на self.guessed_word, позиционированный указанным индексом, и добавим другие пустые символы перед этим индексом. Допустим, наше секретное слово – «разделение». Значение self.guessed_word будет следующим:

self.guessed_word = "********"
Допустим, игрок вводит букву «i». Его новое значение будет следующим:

self.guessed_word = "*i*i*i**"
Теперь создайте другую функцию и назовите ее _wrong_guess которая также принимает guess_letter в качестве аргумента:

    def _wrong_guess(self, guess_letter: str):
        row = 2
        if self.incorrect_guesses > 0 and self.incorrect_guesses < 4:
            row = 3
        elif self.incorrect_guesses >= 4:
            row = 4

        self.gallow_pieces[row] = self.gallow_pieces[row] + self.man_pieces.pop()
        self.gallow = "\n".join(self.gallow_pieces)

        if guess_letter not in self.wrong_guesses:
            self.wrong_guesses.append(guess_letter)
        self.incorrect_guesses += 1
Переменная первой строки сообщает строку в виселице, в которую будет помещен «кусок человека», когда пользователь угадал неправильную букву. Так каждая из частей человека будет притягиваться к виселице.

Для первой ошибки он добавляет «голову человека» в строку 3 (индекс 2) в массиве self.gallow_pieces. Переменная второй строки предназначена для 2-го, 3-го и 4-го неправильных догадок, где левая рука, туловище и правая рука будут добавлены в строку 4 (индекс 3) в массиве self.gallow_pieces. А третья строка переменной предназначена для 5-й и 6-й ошибок, левая и правая ноги будут добавлены в строку 5 (индекс 4) в массиве self.gallow_pieces.

Массив self.man_pieces содержит «человеческие части», которые должны быть добавлены к «виселицам». Self.man_pieces расположен в обратном порядке, поэтому вызов метода .pop() принимает каждый кусок человека (от головы до ног) в надлежащем порядке, который будет добавлен в виселицу.

После того, как часть тела была добавлена, мы добавим guess_letter в self.wrong_guesses и увеличим self.incorrect_guesses на 1.

Запуск игры с помощью main()
Последнее, что мы добавляем, это функция main(), которая запускает всю игру. Эта функция управляет правилами игры:

def main():
    hangman = Hangman()
    while True:
        # greet user and explain mechanics
        os.system('cls' if os.name=='nt' else 'clear')
        hangman.greet_user()
        # show gallow and the hidden word
        print(hangman.gallow, "\n")
        print("Secret word: ", hangman.guessed_word)
        # show the list of wrong guesses
        hangman.show_list_of_wrong_guesses()
        if hangman.is_out_of_guesses():
            print(f"Secret word is: {hangman.secret_word}")
            print("You lost")
            break
        elif hangman.guessed_word == hangman.secret_word:
            print("YOU WIN!!!")
            break
        else:
            # take user guess
            guess = hangman.take_guess()
            # check guess
            hangman.check_guess(guess)

if __name__ == "__main__":
    main()
И все готово! Теперь вы можете играть в hangman в своем терминале, перейдя в каталог программы и запустив python hangman.py. Ниже приведены некоторые из снимков игры:

Запуск игры:

запуск игры

Недопустимое угадывание персонажа:

недопустимое угадывание символовИграя в игру:

играя в игруПравильно угадал загадочное слово:

правильно угадал загадочное словоТеперь мы знаем, как создать игру Hangman с помощью основ Python с помощью встроенных модулей. Теперь мы можем весело играть и улучшать нашу способность угадывать слова с помощью этой игры. Надеюсь, вам понравился этот туториал. Спасибо, что учились со мной и отличного путешествия!