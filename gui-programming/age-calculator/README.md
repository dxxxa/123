# [How to Make an Age Calculator in Python](https://www.thepythoncode.com/article/age-calculator-using-tkinter-python)
##
# [[] / []]()
Если вам пришла в голову идея создания собственного приложения калькулятора возраста с использованием Python, то вы находитесь в правильном месте, потому что эта статья только для вас.

Прежде чем мы углубимся в эту статью, давайте сначала поймем, что такое приложение калькулятора возраста; это приложение вычисляет возраст пользователя, используя его дату рождения (день, месяц и год).

Эта статья разделена на два раздела. В первом разделе мы создадим версию командной строки, и, наконец, во втором разделе мы сделаем GUI-версию приложения. Мы построим все это с нуля.

Вот оглавление:

Настройка среды
Построение версии командной строки
Построение версии графического интерфейса пользователя
Проектирование пользовательского интерфейса
Реализация функции расчета возраста
Заключение
Настройка среды
Прежде всего, давайте настроим среду, создадим два новых файла Python и назовем их age_calculator_cli.py и age_calculator_ui.py:



Вы можете называть их как угодно в соответствии с вашими предпочтениями; убедитесь, что имена файлов содержательны.

Построение версии командной строки
Теперь, когда среда полностью задана, откройте файл age_calculator_cli.py и выполните следующий импорт:

from datetime import date
Здесь мы импортируем дату из datetime, этот модуль предоставляет несколько функций и классов для обработки даты и времени.

Теперь создадим функцию для вычисления возраста; назовем его calculate_age(). Чуть ниже импорта вставьте следующие строки кода:

# defining the for calculating the age, the function takes day
def calculate_age(day, month, year):
    # we are getting the current date using the today()
    today = date.today()
    # convering year, month and day into birthdate
    birthdate = date(year, month, day)
    # calculating the age 
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    # return the age value
    return age
В приведенной выше функции мы передаем три аргумента функции, дату, месяц и год, мы получим эти аргументы от пользователя.

Внутри функции мы получаем текущую дату из модуля datetime с помощью функции today(). После этого создаем переменную birthdate с помощью функции date(); это занимает год, месяц и день в качестве аргументов. Оттуда мы теперь вычисляем возраст, делая некоторые вычитания, код:

((today.month, today.day) < (birthdate.month, birthdate.day))
Проверяет, предшествует ли день или месяц переменной today дню или месяцу переменной birthdate, возвращаемое значение является логическим значением, и, наконец, мы возвращаем вычисляемый возраст.

Теперь нам нужно получить день, месяц и год от пользователя, сразу после определения функции, вставить следующие строки кода:

# the try/except block
# the try will execute if there are no exceptions
try:
    # we are getting day, month, and year using input() function
    day = input('Enter day:')
    month = input('Enter month:')
    year = input('Enter year:')
    # creating a variable called age_result and we are also calling the claculate_age function
    age_result = calculate_age(int(day), int(month), int(year))
    print(f'You are {age_result} years old')
    
# the except will catch all errors
except:
    print(f'Failed to calculate age, either day or month or year is invalid')
Здесь у нас есть блок try/except, внутри оператора try у нас есть код для получения данных от пользователя; это делается с помощью функции input(), и с помощью этих пользовательских данных мы вычисляем возраст с помощью вызова функции. Если при выполнении кода возникнут какие-либо ошибки, на помощь придет оператор except.

Чтобы протестировать программу, используйте следующее:

$ python age_calculator_cli.py
Если вы вводите допустимые данные, вывод будет выглядеть следующим образом:

Enter day:12
Enter month:10
Enter year:2000
You are 21 years old
Программа работает как положено, перезапустите ее, но на этот раз введем недопустимые данные. Результаты будут следующими:

Enter day:-1
Enter month:h
Enter year:0.5
Failed to calculate age, either day or month or year is invalid
Мы успешно создали версию калькулятора возраста для командной строки!

Построение версии графического интерфейса пользователя
В этом разделе мы теперь сосредоточимся на создании версии Tkinter нашего калькулятора возраста. Его функциональность не отличается от версии командной строки. Единственное отличие заключается в том, что приложение версии Tkinter имеет пользовательский интерфейс, который позволяет пользователям вводить данные. Вот что мы собираемся построить в конце этого раздела:



Итак, без лишних слов, давайте начнем создавать приложение.

Проектирование пользовательского интерфейса
Прежде всего, давайте начнем с проектирования пользовательского интерфейса, сделаем следующие необходимые импорты следующим образом в age_calculator_ui.py:

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from datetime import date
Вот что означает импорт; начиная с первого, мы импортируем все из tkinter. Для этого мы используем звездочку или подстановочный знак. После этого мы импортируем ttk из tkinter, ttk - для стилизации виджетов (меток, кнопок, записей и т.д.).

Мы также импортируем окно сообщения showerror для отображения сообщений об ошибках для пользователя из tkinter.messagebox. Наконец, мы импортируем модуль datetime.

Мы создадим окно сразу после импорта. Вставьте следующие строки кода:

# creating the main window
window = Tk()
# the title for the window
window.title('Age Calculator')
# the dimensions and position of the windodw
window.geometry('500x260+430+300')
# making the window nonresizabale
window.resizable(height=FALSE, width=FALSE)

# runs the window infinitely until uses closes it
window.mainloop()
Ради того, чтобы быть на одной странице, давайте немного сломаем код. Во-первых, мы создаем главное окно с помощью функции Tk(), которая поставляется с Tkinter, затем мы даем окну заголовок с помощью функции title(), затем мы определяем размеры (500x260) и положение (430 + 300) для окна с помощью функции geometry(), чтобы сделать окно неизменяемым, мы используем функцию resizable() с высотой и шириной, установленными на FALSE.

Запустив программу, вы получите следующее:



После создания окна нам теперь нужно сделать контейнер для всех виджетов; мы будем использовать виджет Canvas. Этот холст будет находиться внутри главного окна, и он будет занимать высоту и ширину следующим образом:



Итак, сразу после:

window.resizable(height=FALSE, width=FALSE)
Вставьте следующий код:

# the canvas to contain all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()
Мы создаем холст с помощью функции Canvas() и помещаем его в главное окно. Для размера полотна мы используем ширину и высоту.

Теперь нам нужно создать виджеты, которые будут размещены внутри созданного холста, но прежде чем делать виджеты, давайте создадим их стили; чуть ниже определения холста добавьте следующие строки кода:

# ttk styles for the labels
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 14))

# ttk styles for the button
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('DotumChe', 16))

# ttk styles for the entries
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
В приведенном выше коде мы создаем стили для виджетов; для этого мы используем модуль ttk.

Мы строим объект стиля с помощью ttk. Функция Style(), поэтому для добавления стилей к объекту мы будем использовать функцию configure(), эта функция принимает имя стиля (TLabel, TButton или TEntry), передний план и font() в качестве некоторых своих аргументов.

В наших виджетах мы будем использовать имена стилей, чтобы ссылаться или указывать на нужные нам стили. Теперь, когда о стилях позаботились, мы создадим виджеты. Начнем с метки для отображения крупного текста. Под стилями добавьте следующий код:

# the label for displaying the big text
big_label = Label(window, text='AGE CALCULATOR', font=('OCR A Extended', 25))

# placing the big label inside the canvas
canvas.create_window(245, 40, window=big_label)
Код создает метку с помощью Label(), мы передаем окно, текст и шрифт в качестве аргументов, здесь следует отметить, что эта метка имеет независимые стили; он не использует созданные нами стили.

Под меткой мы добавляем его на холст с помощью функции create_window(), эта функция принимает два целых числа (245 и 40) и окно в качестве аргументов, первое целое число позиционирует метку горизонтально, а второе целое число позиционирует ее вертикально.

Запустив программу, вы получите следующее:



Пока всё в порядке. Наше приложение обретает форму; теперь создадим оставшиеся виджеты; добавьте этот код под big_label:

# label and entry for the day
day_label = ttk.Label(window, text='Day:', style='TLabel')
day_entry = ttk.Entry(window, width=15, style='TEntry')
# label and entry for the month
month_label = ttk.Label(window, text='Month:', style='TLabel')
month_entry = ttk.Entry(window, width=15, style='TEntry')
# label and entry for the year
year_label = ttk.Label(window, text='Year:', style='TLabel')
year_entry = ttk.Entry(window, width=15, style='TEntry')
# the button 
calculate_button = ttk.Button(window, text='Calculate Age', style='TButton', command=calculate_age)
# label for display the calculated age
age_result = ttk.Label(window, text='', style='TLabel')
# adding the day label and entry inside the canvas
canvas.create_window(114, 100, window=day_label)
canvas.create_window(130, 130, window=day_entry)
# adding the month label and entry inside the canvas
canvas.create_window(250, 100, window=month_label)
canvas.create_window(245, 130, window=month_entry)
# adding the year label and entry inside the canvas
canvas.create_window(350, 100, window=year_label)
canvas.create_window(360, 130, window=year_entry)
# adding the age_result and entry inside the canvas
canvas.create_window(245, 180, window=age_result)
# adding the calculate button inside the canvas
canvas.create_window(245, 220, window=calculate_button)
С помощью этого фрагмента кода мы создаем следующие виджеты:

Метки для отображения дня, месяца, года и age_result тексте:
day_label
month_label
year_label
age_result, пока это пусто.
Записи для захвата значений дня, месяца и года:
day_entry
month_entry
year_entry
Кнопка:
calculate_button
Все эти виджеты являются виджетами ttk, поэтому для их стилизации мы передаем аргумент style, например, виджет кнопки использует стиль TButton, который мы создали.

Тестируя приложение, мы получаем следующее:



Поздравляем с успешной разработкой пользовательского интерфейса приложения!

Реализация функции расчета возраста
Теперь, когда о пользовательском интерфейсе позаботились, давайте сделаем приложение реактивным. Приложение должно иметь возможность получать данные от пользователя и вычислять возраст. Для этого создадим функцию чуть ниже импортов под названием calculate_age(), вставим этот код:

# the function for calculating the age
def calculate_age():
    # the try/except block
    try:
        # getting current date
        today = date.today()
        # getting day from the day entry
        day = int(day_entry.get())
        # # getting month from the month entry
        month = int(month_entry.get())
        # getting year from the year entry
        year = int(year_entry.get())
        # creating a date object
        birthdate = date(year, month, day)
        # calculating the age
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        # displaying the age using the age result label
        age_result.config(text='You are ' + str(age) + ' years old')
    # if an error occurs the showerror window will pop up
    except:
        showerror(title='Error', message='An error occurred while trying to ' \
                    'calculate age\nThe following could ' \
                    'be the causes:\n->Invalid input data\n->An empty field/fields\n'\
                     'Make sure you enter valid data and fill all the fields')
Эта функция все такая же, как та, которую мы использовали в версии приложения для командной строки; единственное отличие здесь заключается в том, что в операторе try мы получаем день, месяц и год из записей с помощью функции get(), а также в операторе except все ошибки, которые будет улавливать приложение, будут отображаться во всплывающем окне showerror.

Ничего не произойдет, если вы запустите приложение, введете действительные данные в записи и нажмете кнопку. Причина в том, что мы не связали функцию calculate_age() с кнопкой. Мы хотим, чтобы функция была активирована, как только пользователь нажмет кнопку. Для этого мы воспользуемся аргументом команды, который поставляется с виджетом кнопки, отредактируем код кнопки calculate_age и сделаем так, чтобы он выглядел следующим образом:

calculate_button = ttk.Button(window, text='Calculate Age', style='TButton', command=calculate_age)
Повторно запустите приложение, повторно введите допустимые данные, и вы получите следующее:



Что делать, если пользователь вводит недопустимые данные или оставляет одну или все записи пустыми и нажимает кнопку? Результат будет следующим:



Это означает, что приложение работает отлично!

Заключение
В этой статье показано, как создать калькулятор возраста с помощью Python. Мы провели вас через создание двух версий приложения калькулятора возраста, командной строки и версии Tkinter. Мы надеемся, что вы будете использовать знания, полученные из этой статьи, в своих будущих проектах!