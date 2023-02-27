# [How to Make a Typing Speed Tester with Tkinter in Python](https://www.thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter)
##
# [[] / []]()
Идея
В этом уроке мы собираемся сделать простой тест скорости набора текста с Python и его встроенной библиотекой пользовательского интерфейса Tkinter. У пользователя есть 60 секунд, чтобы набрать как можно больше слов, а после этого мы показываем, сколько слов было написано.

Ниже вы увидите, как может выглядеть макет того, как может выглядеть пользовательский интерфейс, появится счетчик, который сообщает пользователю, сколько времени прошло, а часть, где он пишет, будет разделена на две части.

Слева находятся буквы/слова, которые уже были написаны, а справа мы видим буквы, которые будут написаны. Мы всегда хотим, чтобы пользователь набрал букву, которая в настоящее время находится слева от серых букв, чтобы эта буква двигалась.

Вы также видите внизу букву o, указывающую, что пользователь должен ввести ее сейчас, чтобы продолжить.

 

введите описание изображения здесь

По прошествии 60 секунд мы переключим экран и покажем пользователю, насколько высок WPM (слов в минуту), а также сделаем кнопку перезагрузки, чтобы пользователь мог попробовать ее снова, не перезапуская саму программу.

введите описание изображения здесь

Давайте начнем!

Поскольку окна Tkinter всегда выглядят довольно плохо по умолчанию, мы импортируем ctypes, что позволяет нам обнаруживать dpi нашего компьютера, и поэтому окно выглядит лучше.

Это делается с помощью функции в последней строке. Последнее, что мы импортируем, это случайный модуль, потому что позже у нас будет список текстов, которые выбраны случайным образом.

from tkinter import *
import ctypes
import random
import tkinter
 
# For a sharper window
ctypes.windll.shcore.SetProcessDpiAwareness(1)
Настройка Ткинтера
Начнем с настройки окна Tkinter. Здесь мы начинаем с создания нового объекта Tk() и сохраняем его в корневой переменной. Затем мы устанавливаем заголовок окна и размер окна с его методами title() и geometry() соответственно.

В последних двух строках мы устанавливаем шрифт для всех Labels and Buttons с помощью метода option_add() монофоническим шрифтом Consolas размером 30. Важно, чтобы мы использовали монофонический шрифт, чтобы буквы всегда были упорядочены, потому что с другими шрифтами они будут прыгать и раздражать пользователя.

# Setup
root = Tk()
root.title('Type Speed Test')

# Setting the starting window dimensions
root.geometry('700x700')

# Setting the Font for all Labels and Buttons
root.option_add("*Label.Font", "consolas 30")
root.option_add("*Button.Font", "consolas 30")
Вспомогательные функции
Теперь перейдем к сути программы. Вспомогательные функции выполняют большую часть работы здесь; они отображают виджеты и удаляют их.

resetWritingLabels()
Эта функция генерирует виджеты для письменного теста и запускает тест.

Вфункции мы начинаем с определения списка возможных текстов, а затем выбираем один из текстов в списке случайным образом с помощью функции random.choice().

def resetWritingLabels():
    # Text List
    possibleTexts = [
        'For writers, a random sentence can help them get their creative juices flowing. Since the topic of the sentence is completely unknown, it forces the writer to be creative when the sentence appears. There are a number of different ways a writer can use the random sentence for creativity. The most common way to use the sentence is to begin a story. Another option is to include it somewhere in the story. A much more difficult challenge is to use it to end a story. In any of these cases, it forces the writer to think creatively since they have no idea what sentence will appear from the tool.',
        'The goal of Python Code is to provide Python tutorials, recipes, problem fixes and articles to beginner and intermediate Python programmers, as well as sharing knowledge to the world. Python Code aims for making everyone in the world be able to learn how to code for free. Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.',
        'As always, we start with the imports. Because we make the UI with tkinter, we need to import it. We also import the font module from tkinter to change the fonts on our elements later. We continue by getting the partial function from functools, it is a genius function that excepts another function as a first argument and some args and kwargs and it will return a reference to this function with those arguments. This is especially useful when we want to insert one of our functions to a command argument of a button or a key binding.'
    ]
    # Chosing one of the texts randomly with the choice function
    text = random.choice(possibleTexts).lower()
Связанные с: Как генерировать случайные данные в Python.

Теперь, когда у нас есть текст, который пользователь должен будет написать, мы можем начать с создания виджетов. Но перед этим мы определяем, где текст будет начинаться/разделяться для меток. Это делается потому, что есть две метки; один, где письменный текст, и тот, где текст, который будет написан. Эти два расположены рядом, поэтому пользователь не заметит, что они не являются одной меткой.

Это именно то, что мы делаем в следующих нескольких строках. Для обеих сторон мы делаем метку, сохраняем ее в переменную с соответствующим именем и помещаем в окно с помощью place(). Этот способ позиционирования виджета является точным или, по крайней мере, более точным, чем pack(). Мы поставляем его relx и полагаемся на параметры с 0,5, что означает, что элементы всегда будут находиться посередине относительно самого окна.

Аргумент привязки сообщает ему, какая точка ограничивающего прямоугольника будет находиться в координатах. Один должен быть E для востока и один W для запада, чтобы они были близко друг к другу и имели бесшовный вид. Мы также делаем переменные глобально доступными, чтобы другие функции могли взаимодействовать с метками, сделанными здесь.

    # defining where the text is split
    splitPoint = 0
    # This is where the text is that is already written
    global labelLeft
    labelLeft = Label(root, text=text[0:splitPoint], fg='grey')
    labelLeft.place(relx=0.5, rely=0.5, anchor=E)

    # Here is the text which will be written
    global labelRight
    labelRight = Label(root, text=text[splitPoint:])
    labelRight.place(relx=0.5, rely=0.5, anchor=W)
После первых двух лейблов мы продолжаем делать еще два. Один из них показывает пользователю текущее письмо, которое должно быть написано, а другой показывает ему, сколько времени осталось. Мы размещаем их так же, как и предыдущие:

    # This label shows the user which letter he now has to press
    global currentLetterLabel
    currentLetterLabel = Label(root, text=text[splitPoint], fg='grey')
    currentLetterLabel.place(relx=0.5, rely=0.6, anchor=N)

    # this label shows the user how much time has gone by
    global timeleftLabel
    timeleftLabel = Label(root, text=f'0 Seconds', fg='grey')
    timeleftLabel.place(relx=0.5, rely=0.4, anchor=S)
Теперь мы также настроили некоторые вещи для работы клавиатуры и таймера.

Записываемая переменная имеет значение True, если тест продолжается, а если значение False, тест будет завершен. Затем мы привязываем каждое ключевое событие к функции keyPress(), которую мы рассмотрим позже. Переменная passedSeconds используется для ввода двух вышеупомянутых меток. И последнее, но не менее важное: мы установим наш корень для вызова функции stopTest() через 60 секунд и для вызова функции addSecond() через одну секунду. Это делается методом after() нашего корня:

    global writeAble
    writeAble = True
    root.bind('<Key>', keyPress)

    global passedSeconds
    passedSeconds = 0

    # Binding callbacks to functions after a certain amount of time.
    root.after(60000, stopTest)
    root.after(1000, addSecond)
stopTest()
Теперь рассмотрим функцию, которая останавливает тест. Как мы видели ранее, это будет вызвано корнем через 60 секунд. Сначала для переменной writeAble будет установлено значение False. Затем мы вычисляем количество слов, написанных пользователем. Для этого мы просто получаем текст из левой метки и разбиваем его на пустые пробелы, и считаем длину полученного списка. После этого мы уничтожаем этикетки из теста методом их уничтожения:

def stopTest():
    global writeAble
    writeAble = False

    # Calculating the amount of words
    amountWords = len(labelLeft.cget('text').split(' '))

    # Destroy all unwanted widgets.
    timeleftLabel.destroy()
    currentLetterLabel.destroy()
    labelRight.destroy()
    labelLeft.destroy()
Затем мы отобразим результат теста в метке и поместим кнопку для перезапуска теста под меткой результата:

    # Display the test results with a formatted string
    global ResultLabel
    ResultLabel = Label(root, text=f'Words per Minute: {amountWords}', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Display a button to restart the game
    global ResultButton
    ResultButton = Button(root, text=f'Retry', command=restart)
    ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)
restart()
Эта функция перезапустит тест, сначала удалив метку результата и кнопку перезагрузки, а затем вызвав функцию resetWritingLables(), которая запускает тест:

def restart():
    # Destry result widgets
    ResultLabel.destroy()
    ResultButton.destroy()

    # re-setup writing labels.
    resetWritingLables()
addSecond()
Эта функция обновит то, что отображается в метке timeleftLabel. Он просто добавит один в passedSeconds и установит текст метки соответствующим образом, затем он вызовет себя снова через одну секунду, если тест все еще выполняется.

def addSecond():
    # Add a second to the counter.

    global passedSeconds
    passedSeconds += 1
    timeleftLabel.configure(text=f'{passedSeconds} Seconds')

    # call this function again after one second if the time is not over.
    if writeAble:
        root.after(1000, addSecond)
keyPress()
Теперь перейдем к функции keyPress; это основа теста, так как здесь обрабатываются нажатия клавиш. Поэтому он всегда будет получать объект события, содержащий информацию о нажатых клавишах.

Сначала мы проверяем, совпадает ли характер события со следующей буквой, которую нужно нажать, и если это имеет значение True, мы удаляем эту букву с правой стороны и добавляем ту же букву в левую метку, чтобы она выглядела так, как будто пользователь печатает. Мы также устанавливаем метку для текущей буквы, чтобы показать правильную.

def keyPress(event=None):
    try:
        if event.char.lower() == labelRight.cget('text')[0].lower():
            # Deleting one from the right side.
            labelRight.configure(text=labelRight.cget('text')[1:])
            # Deleting one from the right side.
            labelLeft.configure(text=labelLeft.cget('text') + event.char.lower())
            #set the next Letter Lavbel
            currentLetterLabel.configure(text=labelRight.cget('text')[0])
    except tkinter.TclError:
        pass
Связанные с: Модуль клавиатуры: Управление клавиатурой в Python.

Гротлуп
И последнее, но не менее важное: мы вызываем функцию resetWritingLables и запускаем основной цикл окна Tkinter.

# This will start the Test
resetWritingLables()

# Start the mainloop
root.mainloop()
Витрина
Ниже вы видите витрину программы под рукой:

введите описание изображения здесь

Заключение
Отлично! Вы успешно создали тестер скорости набора текста с помощью кода Python! Посмотрите, как вы можете добавить в эту программу дополнительные функции, такие как случайные отправные точки, больше текста или добавление калькулятора опечаток, где вы разрешаете опечатку, но вычисляете ее в конце.

Если вы хотите создать больше графических интерфейсов с помощью Python, посетите нашу страницу учебных пособий по программированию с графическим интерфейсом!

Вы можете проверить полный код здесь.