# [How to Make a Calculator with Tkinter in Python](https://www.thepythoncode.com/article/make-a-calculator-app-using-tkinter-in-python)
You can get the original version of the calculator [here](https://github.com/Maximinodotpy/calculator).
##
# [[] / []]()
Идея
В этом уроке мы сделаем калькулятор с Tkinter, встроенной библиотекой графического интерфейса на Python. Мы собираемся сделать сетку 3 на 3 с кнопками, которые представляют возможные входные данные, систему отображения результатов в реальном времени, функцию истории вычислений и вставку переменных.

Итак, давайте сразу перейдем к этому. Вы всегда можете получить полный код здесь.

Импорт
Как всегда, мы начинаем с импорта. Поскольку мы создаем пользовательский интерфейс с помощью tkinter, нам нужно импортировать его. Мы также импортируем модуль шрифтов из tkinter, чтобы изменить шрифты на наших элементах позже.

Мы продолжаем, получая функцию partial() из functools, это гениальная функция, которая исключает другую функцию в качестве первого аргумента и некоторые args и kwargs, и она вернет ссылку на эту функцию с этими аргументами. Это особенно полезно, когда мы хотим вставить одну из наших функций в аргумент команды привязки кнопки или ключа.

В следующей строке мы импортируем ctypes, что позволяет нам включить высокий dpi, делая наше окно более четким. Это делается с помощью вызова функции в последней строке блока кода этого раздела.

Поскольку мы сохраняем нашу историю в JSON-файле, мы импортируем модуль json для работы с файлами JSON. Нам также нужен встроенный модуль re для нашей функции вставки переменных.

И последнее, но не менее важное: мы получаем математический модуль:

from tkinter import *
import tkinter.font as font
from functools import partial
import ctypes
import json
import re
# so the functions that can be used from the math module can be used in the line edit.
import math

ctypes.windll.shcore.SetProcessDpiAwareness(1)
Переменные и настройка Tkinter
Далее мы делаем некоторые переменные и настраиваем tkinter:

# Colors
buttonColor = (255, 255, 255)
historyPanelBackground = (255, 255, 255)
# Tkinter Setup
root = Tk()
root.geometry("550x270")
root.title("Calculator")
# Setting icon for the Application
photo = PhotoImage(file = "icon.png")
root.iconphoto(False, photo)
# Loading Font from font name
myFont = font.Font(family='Consolas', size=12)
Первые две переменные (buttonColor и historyPanelBackground) — это просто цвета для наших кнопок и фона панели истории.

Далее мы настраиваем tkinter, вызывая его класс Tk() и сохраняя этот объект в корневой переменной. Затем мы устанавливаем размеры окна с помощью метода geometry() и заголовок окна с помощью title().

Затем мы импортируем изображение из нашего каталога (вы можете получить файлы каталога здесь), которое мы можем установить в качестве значка нашей программы. После этого мы импортируем шрифт Consolas размером 12. Мы делаем это с помощью класса Font() из модуля шрифтов tkinter.

Формулы и вставки переменных
Теперь я объясню функцию вставки переменных, или, по крайней мере, попробую! Таким образом, идея состоит в том, что мы можем иметь пространство после наших уравнений, где мы объявляем переменные, вставленные в уравнение заполнителями. Рассмотрим это на конкретном примере. Если мы наберем текст ниже в строку редактирования:

{a} * {b} ? a=7 & b=3
Это должно принести нам такой результат:

21
Потому что a будет поставлено на 7, а b на 3. Поэтому уравнение будет оценено до 21. Позже мы рассмотрим, как это делается на практике.

Ниже мы определим список формул, которые можно вставить в строку редактирования. Мы сделаем их доступными для выбора из меню:

# Formula Templates
formulas = [
    ['Pythagoras->c', '(({a}**2)+({b}**2))**0.5 ? a=5 & b=5'],
    ['Pythagoras->c**2', '({a}**2)+({b}**2) ? a=5 & b=5'],
    ['pq->(x1, x2)', '-({p}/2) + sqrt(({p}/2)**2 - ({q})), -({p}/2) - sqrt(({p}/2)**2 - ({q})) ? p=-1 & q=-12'],
    ['abc->(x1, x2)', 'quadratic_formula({a}, {b}, {c}) ? a=1 & b=5 & c=6'],
    ['Incline->y', '{m}*{x} + {q} ? m=4 & x=5 & q=6'],
]
Настройка истории
Затем мы настроим функцию истории. Мы начинаем с объявления списка, в котором будут храниться наши элементы истории. Затем у нас есть переменная, которая содержит расположение файла history.json.

В итоге у нас есть блок try and except, где есть попытка сделать файл в указанном месте. Это просто сделано, поэтому файл существует во всех случаях.

# All the history equations are in this list.
history = []
# Where the history file is located.
historyFilePath = 'history.json'
print("Reading history from:", historyFilePath)
# Creating History file if it does not exist.
try:
    with open(historyFilePath, 'x') as fp:
        pass
    print("Created file at:", historyFilePath)
except:
    print('File already exists')
RGB к шестнадцатеричной и математической функции
Теперь поговорим о двух функциях, которые имеют лишь незначительное значение:

rgb_to_hex() просто преобразует цвета RGB в шестнадцатеричные цвета, потому что tkinter разрешает только имена цветов и шестнадцатеричные цвета.
quadratic_formula() — это пользовательская математическая функция, которую можно использовать при редактировании строки.
# converting RGB values to HEX
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def quadratic_formula(a, b, c):
    disc = b**2 - 4 * a * c
    x1 = (-b - math.sqrt(disc)) / (2 * a)
    x2 = (-b + math.sqrt(disc)) / (2 * a)
    return (x1, x2)
Вспомогательные функции
Теперь мы рассмотрим несколько вспомогательных функций, необходимых для работы программы.

Функция addSymbol()
Эта функция будет вызываться из кнопок для вставки операторов типа * или + и чисел в строку редактирования. Вот где появляется параметр symbol. Если символ <, мы не будем его добавлять; мы сократим текущий вход. Мы фактически изменяем строковую переменную, которая содержит текущий вход.

# Add something to the current calculation
def addSymbol(event=None, symbol=None):
    if symbol == '<':
        entryVariable.set(entryVariable.get()[:-1])
    else:
        entryVariable.set(entryVariable.get()+symbol)
Функция varChange()
Эта функция будет подключена к изменениям событий на входной переменной. В этой функции мы также оценим уравнение и вставим его в метку результата.

Ранее мы рассмотрели, как функционирует функция вставки переменных, а теперь посмотрим, как мы это делаем на практике:

def varChange(*args):
    evaluationString = entryVariable.get().replace(' ', '').split('?')[0]
    print('Before insertion: ',evaluationString)
    if len(entryVariable.get().split('?')) == 2:
        parameters = entryVariable.get().replace(' ', '').split('?')[1]
        for param in parameters.split('&'):
            where, what = param.split('=')
            evaluationString = re.sub('{'+where+'}', what, evaluationString)
    try:
        print('After insertion: ', evaluationString)
        resultLabel.config(text=str(eval(evaluationString)))
    except:
        resultLabel.config(text='Invalid Input')
Как видите, сначала мы разделяем входную строку на ? а затем сохраняем ее в переменной evaluationString.

После этого мы проверяем, приведет ли входная строка, разделенная на ?, к списку с двумя элементами. Если это так, мы знаем, что существуют переменные вставки. Затем мы получаем эту сторону строки и зацикливаемся на другой разделенной версии этого, где разделитель находится &. Там мы модифицируем evaluationString с помощью этих переменных.

В любом случае мы постараемся вставить вычисляемое значение в метку результата. Возможно, это не сработает, потому что ввод недействителен, поэтому мы рассмотрим и этот случай.

Функция saveCurrentInputToHistory()
Эта функция просто сохраняет текущие входные данные редактирования строки в файл истории. Сначала мы проверяем, есть ли значение уже в списке, чтобы у нас не было дубликатов. Затем мы сохраняем список истории в файл истории. Здесь мы используем функцию json.dump():

def saveCurrentInputToHistory(event=None):
    if entryVariable.get() in history:
        return
    history.append(entryVariable.get())
    with open(historyFilePath, 'w') as file:
        file.write(json.dumps(history))
    updateListBox()
Мы также вызываем функцию updateListBox(), которая будет объяснена в следующем разделе.

Функция updateListBox()
Эта функция удалит все содержимое списка истории и отобразит его снова. Вот почему нам нужна переменная истории здесь.

Удаляем все элементы списка методом delete(start, end). Затем мы открываем файл истории и получаем оттуда JSON. В конце концов, мы зацикливаемся на списке истории и вставляем эти значения в historyList:

def updateListBox(event=None):
    global history
    historyList.delete(0, END)
    try:
        with open(historyFilePath, 'r') as file:
            history = json.loads(file.read())
    except json.decoder.JSONDecodeError:
        print('File does not contain JSON')
    for index, item in enumerate(history):
        historyList.insert(index, item)
Функции setEntryFromHistory() и addFormula()
Эти две функции имеют простые задания:

Функция setEntryFromHistory() позволяет нам щелкнуть элемент списка, и этот элемент будет вставлен в редактирование строки.
Функция addFormula() будет делать то же самое только для формул, выбранных из выпадающего меню.
def setEntryFromHistory(event=None):
    historyItem = historyList.get(historyList.curselection()[0])
    entryVariable.set(historyItem)

def addFormula(formula=''):
    saveCurrentInputToHistory()
    entryVariable.set(formula)
Создание пользовательского интерфейса
Теперь мы сделаем пользовательский интерфейс. Я не буду вдаваться в подробности. Макет выполняется с помощью метода pack() всех виджетов и выполняет настройку с двумя столбцами с помощью Frame.

# Work with Frames to split the window in two parts: the calculator and the History Panel.
# Calculation Panel
calcSide = Frame(root)
calcSide.pack(side=LEFT, fill=BOTH, expand=1)
# Entry Variable for the calculations
entryVariable = StringVar(root, '4/2**2')
entryVariable.trace('w', varChange)

Entry(calcSide, textvariable=entryVariable, font=myFont, borderwidth=0).pack(fill=X, ipady=10, ipadx=10)
resultLabel = Label(calcSide, text='Result', font=myFont, borderwidth=0,anchor="e")
resultLabel.pack(fill=X, ipady=10)
# History Panel
historySide = Frame(root, bg=rgb_to_hex(historyPanelBackground))
historySide.pack(side=LEFT, fill=BOTH, expand=1)

historyTopBar = Frame(historySide)
historyTopBar.pack(fill=X)
Label(historyTopBar, text='History').pack(side=LEFT)
Button(historyTopBar, text='Save Current Input', bg=rgb_to_hex(buttonColor), borderwidth=0, command=saveCurrentInputToHistory).pack(side=RIGHT)

historyList = Listbox(historySide, borderwidth=0)
historyList.pack(fill=BOTH, expand=True)
historyList.bind("<Double-Button-1>", setEntryFromHistory)
Мы также вызываем эту функцию, поэтому список обновляется при запуске:

# Insert stuff into the history
updateListBox()
Ниже вы увидите, как сделаны кнопки. Сначала мы определяем список с другими списками, где расположены символы на кнопке.

Затем мы зацикливаемся на этом первом списке и создаем новый кадр для каждой строки, и мы продолжаем, зацикливаясь на этих внутренних списках и генерируя кнопки с заданными символами.

Мы устанавливаем цвет фона на этих кнопках на цвет нашей кнопки, а затем опускаем каждое число из кортежа цвета кнопки; это даст нам хороший градиент для кнопок:

# Button Symbols (and their position)
symbols = [
    ['1', '2', '3', '+'],
    ['4', '5', '6', '-'],
    ['7', '8', '9', '/'],
    ['0', '.', '<', '*'],
]

for rowList in symbols:
    # Make a row
    row = Frame(calcSide)
    row.pack(fill=BOTH, expand=True)
    for symbol in rowList:
        # Making and packing the Button
        Button(
            row, text=symbol, command=partial(addSymbol, symbol=symbol),
            font=myFont, bg=rgb_to_hex(buttonColor), borderwidth=0) \
        .pack(side=LEFT, fill=BOTH, expand=1)
        # Change button color each iteration for gradient.
        buttonColor = (buttonColor[0] - 10, buttonColor[1] - 10, buttonColor[1] - 2)
Мы составляем меню, в которое у нас есть все наши формулы, готовые к вставке:

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

# Add all Formulas to the dropdown menu.
for formula in formulas:
    filemenu.add_command(label=formula[0], command=partial(addFormula, formula[1]))

filemenu.add_separator()
# Quit command
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(menu=filemenu, label='Formulas')

root.config(menu=menubar)
Наконец, мы вызываем функцию valueChange(), чтобы входные данные вычислялись при запуске, и вызываем метод mainloop():

# Call the var change once so it is evaluated without actual change.
varChange('foo')
root.mainloop()
Витрина
Ниже вы видите небольшую демонстрацию того, как работает калькулятор:

Демонстрация приложения "Калькулятор"

Заключение
Отлично! Вы успешно создали калькулятор с помощью кода Python! Посмотрите, как вы можете добавить больше функций в эту программу, таких как больше формул или конвертер для различных вещей, таких как дюймы в сантиметры.