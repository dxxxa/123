# [How to Make a Simple Math Quiz Game in Python](https://www.thepythoncode.com/article/make-a-simple-math-quiz-game-in-python)
To run this:
- `pip install -r requirements.txt`
- 
    ```
    $ python simple_math_game.py

    Round down to one Number after the Comma.
    When asked to press enter to continue, type stop to stop.

    5 ** 4 = 625
    Correct!
    Points:  1
    Press "Enter" to continue

    9 ** 18 = 190
    Wrong!
    Solution: 150094635296999121
    Points:  0
    Press "Enter" to continue   

    7 - 17 = -10
    Correct!
    Points:  1
    Press "Enter" to continue
    stop
    ```
##
# [[] / []]()
В этом уроке мы сделаем простую математическую игру на консоли с модулем PyInputPlus. Основными особенностями этой простой игры являются добавление очков (например, счет), несколько типов уравнений (таких как сложение, вычитание, умножение и деление) и возможность остановить игру.

Чтобы начать, поскольку PyInputPlus не является встроенным модулем, мы должны установить его:

$ pip install PyInputPlus
Импорт PyInputPlus и случайных:

# Imports
import pyinputplus as pyip
from random import choice
Настройка переменных
Мы продолжаем настраивать некоторые переменные для использования позже.

Список questionTypes содержит операторы, которые могут быть использованы в уравнениях; имейте в виду, что они должны быть допустимыми операторами Python. Вы можете добавить модуль (%) или любой другой допустимый оператор Python в список, чтобы включить эти операторы в игре. Они будут выбраны случайным образом с помощью функции random.choice().

Затем мы определяем список под названием numberRange, который содержит все числа, которые могут появиться в уравнениях. Мы можем сделать это за одну строку.

И последнее, но не менее важное: мы определяем переменную points, которая начинается с 0.

# Variables
questionTypes = ['+', '-', '*', '/', '**']
numbersRange = [num for num in range(1, 20)]
points = 0
Подсказки
Чтобы пользователь знал, что он должен делать, мы печатаем некоторые подсказки об игре.

Позже мы округлим Решения, потому что уравнения, такие как 7 / 4, невозможно записать.

Мы также позволим пользователю остановить игру после каждого вопроса. Вот почему мы упоминаем об этом здесь.

# Hints
print('Round down to one Number after the Comma.')
print('When asked to press enter to continue, type stop to stop.\n')
Создание уравнения
Теперь мы входим в игровой цикл, где начинаем с принятия решения о типе вопроса. Это делается с помощью метода random.choice() из модуля random. При этом будет возвращен один из элементов из questionTypes.

Затем мы строим уравнение, где мы также используем random.choice(), чтобы выбрать случайные элементы из списка numbersRange и вставить их в эту строку.

После этого мы использовали отличную функцию Python eval(). Он берет строку, вычисляет ее и возвращает решение. Мы сохраняем это в переменной solution; позже мы проверим это на соответствие тому, что написал пользователь.

# Game Loop
while  True:
	# Deciding and generating question
	currenType = choice(questionTypes)

	promptEquation = str(choice(numbersRange)) + ' ' + currenType + ' ' + str(choice(numbersRange))
	solution = round(eval(promptEquation), 1)
Прием входных данных
Далее мы используем метод inputNum() из модуля PyInputPlus. Эта функция проверит, был ли вход числом, а если нет, то спросит еще раз. Заполняем его параметр prompt нашей строкой prompt; имейте в виду добавить ' = ' так что это имеет смысл для пользователя. Мы не могли бы сделать это до функции eval(), потому что она будет работать таким образом.

    # Getting answer from User
    answer = pyip.inputNum(prompt=promptEquation + ' = ')
Обратная связь
После получения пользовательского ввода мы тестируем его на соответствие решению, возвращаемому функцией eval(). Если они совпадают, мы поднимаем баллы на единицу и распечатываем хороший комментарий и новый номер пункта.

Если это неправильно, мы опускаем баллы на единицу и распечатываем правильное решение.

    # Feedback and Points
    if answer == solution:
        points += 1
        print('Correct!\nPoints: ',points)
    else:
        points -= 1
        print('Wrong!\nSolution: '+str(solution)+'\nPoints: ',points)
Остановка игры
И последнее, но не менее важное: мы останавливаем игру после каждого вопроса. Если пользователь нажимает клавишу ВВОД, он продолжается. Чтобы это работало, мы должны установить пустое значение True, но если пользовательские типы останавливаются, игра остановится.

    # Stopping the Game
    if pyip.inputStr('Press "Enter" to continue', blank=True) == 'stop':
        break
    
    # Some Padding
    print('\n\n')
Давайте запустим его:

$ python simple_math_game.py

Round down to one Number after the Comma.
When asked to press enter to continue, type stop to stop.

5 ** 4 = 625
Correct!
Points:  1
Press "Enter" to continue

9 ** 18 = 190
Wrong!
Solution: 150094635296999121
Points:  0
Press "Enter" to continue   

7 - 17 = -10
Correct!
Points:  1
Press "Enter" to continue
stop
Замечательно! Теперь вы знаете, как сделать простую консольную математическую игру с PyInputPlus. Вы можете получить полный код здесь.