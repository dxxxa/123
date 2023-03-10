# [How to Build a GUI Dictionary App with Tkinter in Python](https://www.thepythoncode.com/article/make-a-gui-audio-dictionary-python)
##
# [[] / []]()
Словарь - это приложение, которое позволяет пользователям искать конкретное слово и предоставляет значения слова и его синоним и антоним взамен. Аудиословарь с графическим интерфейсом - отличный способ выучить новый язык или улучшить произношение языка, с которым вы уже знакомы. Если вам когда-либо нравилась идея создания собственного, это практический проект, который научит вас многому о том, как использовать язык программирования Python.

Этот учебник проведет вас через процесс создания словарного приложения с использованием Tkinter с аудио произношением шаг за шагом. Вы узнаете, как создать пользовательский интерфейс с помощью основной библиотеки Python Tkinter и как использовать код Python для работы словаря. Создание GUI Audio Dictionary - это веселый и сложный проект, который научит вас многому о Python и о том, как использовать его для создания полезных приложений.

Вот что мы собираемся построить к концу этого учебника:

Аудио словарьМы собираемся построить каждую часть этого приложения с нуля, чтобы мы были на одной странице.

Если вы хотите создать словарное приложение с использованием Django, то у нас также есть учебник по этому вопросу, обязательно проверьте его, если вы больше любите Django, чем Tkinter.

Содержание:
Настройка среды
Импорт всех необходимых модулей
Проектирование графического интерфейса пользователя
Создание главного окна и добавление его значка
Определение всех используемых стилей виджетов
Добавление холста
Добавление виджетов на холст
Метка заголовка
Поле ввода и кнопка поиска
Метка и кнопка аудио
Текстовое поле
Реализация функции закрытия приложения
Реализация функциональности приложения
Функциональность поиска значения слова
Функциональность произношения слов
Заключение
Настройка среды
Начнем с настройки рабочей среды проекта, создадим виртуальную среду с помощью команды:

$ python -m venv project
Все необходимые модули проекта будут установлены в этой виртуальной среде, поэтому давайте активируем ее.

В Windows активируйте его с помощью:

$ ./project/Scripts/activate
А на macOS или Linux используйте:

$ source project/bin/activate
Активировав виртуальную среду, установим в нее необходимые модули. Использование:

$ pip install PyDictionary pyttsx3
Импорт всех необходимых модулей
Теперь создайте файл Python и назовите его audio-dictionary.py, вы можете назвать его как хотите, но просто убедитесь, что имя имеет смысл. Откройте файл и вставьте следующий код:

# this imports everything from the tkinter module
from tkinter import *
# importing the ttk module from tkinter that's for styling widgets
from tkinter import ttk
# importing message boxes like showinfo, showerror, askyesno from tkinter.messagebox
from tkinter.messagebox import showerror, askyesno
# importing the PyDictionary library
from PyDictionary import PyDictionary
# this package converts text to speech
import pyttsx3
Разбивая фрагмент кода, от первой до последней строки, вот что мы имеем. Мы импортируем все из tkinter с помощью символа asterisk(*), затем мы импортируем модуль ttk для стилизации виджетов приложения (меток, кнопок, записей и т. Д.).

Мы также импортируем окна сообщений для отображения сообщений пользователю, когда в приложении запускается определенное действие. С последними двумя строками мы импортируем модуль PyDictionary для поиска значений слов и pyttsx3 для преобразования текста в речь.

Проектирование графического интерфейса пользователя
В этом разделе мы начнем проектирование графического интерфейса приложения. Процесс проектирования будет глубоким, чтобы вы понимали, что происходит и насколько мощным является модуль Tkinter, когда дело доходит до проектирования шикарных графических интерфейсов.

Создание главного окна и добавление его значка
Начнем с главного окна и его иконки (вы можете получить иконку в текущем рабочем каталоге проекта на GitHub), чуть ниже импорты добавят следующие строки кода:

# creates the window using Tk() fucntion
window = Tk()
# creates title for the window
window.title('Audio-Dictionary')
# adding the window's icon
window.iconbitmap(window, 'dictionary.ico')
# dimensions and position of the window
window.geometry('560x480+430+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)

# runs the window infinitely
window.mainloop()
В фрагменте кода мы создаем главное окно с помощью встроенного класса Tkinter Tk(), а затем даем заголовок главному окну с помощью функции title(). Мы используем функцию iconbitmap() для добавления значка в главное окно, эта функция принимает окно и фактический значок в качестве аргументов. Убедитесь, что файл значка находится в той же папке, что и файл Python:

словарь.icoФункция geometry() предназначена для придания размеров и положения главному окну, 560x480 - для ширины и высоты соответственно и 430 +180 - для позиционирования главного окна по горизонтали и вертикали. Чтобы сделать главное окно неизменяемым, мы используем функцию resizable(), высота и ширина которой имеют значение FALSE, это отключит кнопку свертывания или разворота главного окна.

Наконец, мы вызываем функцию mainloop(), которая позволяет главному окну работать в бесконечном режиме, пока окно не будет закрыто.

Запустите программу с помощью следующей команды:

$ python audio-dictionary.py
Результаты будут следующими:

А в левом верхнем углу окна добавлена иконка:

Определение всех используемых стилей виджетов
Поскольку мы хотим, чтобы приложение имело стилизованные виджеты, в этом разделе мы определим все стили. Ниже строки:

window.resizable(height=FALSE, width=FALSE)
Вставьте следующие строки кода:

"""Styles for the widgets"""
# style for the big text label 
big_label_style = ttk.Style()
big_label_style.configure('big_label_style.TLabel', foreground='#000000', font=('OCR A Extended', 40))
# style for small text labels
small_label_style = ttk.Style()
small_label_style.configure('small_label_style.TLabel', foreground='#000000', font=('OCR A Extended', 15))
# style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 20))
# style for the two buttons
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')
Во фрагменте кода мы создаем четыре объекта стиля с помощью ttk. Встроенный класс Style() для модуля ttk. Эти стили предназначены для этих виджетов, меток, кнопок и поля ввода, и для их настройки мы используем функцию configure(), которая принимает такие аргументы, как имя стиля (TLabel, TEntry, TButton и т. Д.), Шрифт, передний план и т. Д.

Добавление холста
Позаботившись о стилях виджетов, добавим Canvas в главное окно, этот Canvas будет контейнером для всех виджетов для приложения. Чуть ниже кода стилей добавьте следующий код:

# creates the canvas for containing all the widgets
canvas = Canvas(window, width=480, height=560)
# packing the canvas
canvas.pack()
С помощью этих двух строк кода мы создаем Canvas шириной 480 и высотой 560 и помещаем его в главное окно, и, наконец, мы упаковываем его с помощью системы менеджера геометрии pack().

Если вы запустите программу, вы не увидите Canvas, но практически это пространство, которое он занимает в главном окне:

Добавление виджетов на холст
После добавления Canvas, давайте теперь начнем добавлять в него виджеты. Как упоминалось ранее, Canvas будет содержать все виджеты. Здесь стоит упомянуть, так как все кнопки будут использовать значки, убедитесь, что все значки находятся в той же папке, что и файл Python, как показано ниже:

Метка заголовка
Первый виджет, который мы добавляем в Canvas, — это метка для большого текста, поэтому под Canvas добавьте следующий код:

# creating a ttk label
text_label = ttk.Label(window, text='Audio Dictionary', style='big_label_style.TLabel')
# adding the label to the canvas
canvas.create_window(250, 55, window=text_label)
Здесь мы создаем метку с помощью ttk. Функция Label(), которая принимает окно, текст и стиль в качестве аргументов. Наконец, мы добавляем эту метку на холст с помощью функции create_window(), она принимает три аргумента, 250, 55 и window.

Вот выходные данные для добавленного кода:

Поле ввода и кнопка поиска
Здесь мы добавим два виджета, запись и кнопку поиска, под меткой вставьте этот код:

# creating a ttk entry
word_entry = ttk.Entry(window, width=73, style='TEntry')
# adding the entry to the canvas
canvas.create_window(230, 110, window=word_entry, height=35)
# loading the icon
search_icon = PhotoImage(file='search.png')
# creates dimensions of the icon
logo = search_icon.subsample(20, 20)
# creating a ttk button with a search icon
search_button = ttk.Button(window, image=logo, style='TButton')
# adding the entry to the canvas
canvas.create_window(468, 110, window=search_button)
Во фрагменте кода мы создаем запись с помощью ttk. Entry(), который принимает в качестве аргументов окно, ширину и стиль. Чтобы добавить его в Canvas, мы используем функцию create_window(), она принимает 230, 110, окно и высоту в качестве аргументов.

Затем мы создаем объект изображения с помощью функции PhotoImage(), которая принимает файл значка в качестве входных данных. Чтобы изменить размер значка, мы используем функцию subsample() с 20 и 20 в качестве аргументов.

Наконец, мы являемся кнопкой, использующей ttk. Функция Button(), которая принимает окно, изображение и стиль в качестве аргументов, и снова мы используем функцию create_window() для добавления ее в Canvas.

Добавленный код приведет к следующему выводу:

Метка и кнопка аудио
Добавим другие виджеты, пустую метку для отображения слова и кнопку отключенного аудио. Под записью и кнопкой выше добавьте код:

# loading the icon
audio_icon = PhotoImage(file='speaker.png')
# creates dimensions of the logo
icon = audio_icon.subsample(10, 10)
word_label = ttk.Label(window, style='small_label_style.TLabel')
# adding the label to the canvas
canvas.create_window(80, 145, window=word_label)
# creating another ttk button with a speaker icon
audio_button = ttk.Button(window, image=icon, style='TButton', state=DISABLED)
# adding the entry to the canvas
canvas.create_window(25, 190, window=audio_button) 
Разберем фрагмент кода, мы в первую очередь создаем объект изображения с помощью функции PhotoImage(), входом которой является файл иконки. Для изменения размера значка используется функция subsample().

Затем мы создаем метку с помощью ttk. Функция Label(), ее аргументами являются окно и стиль, а функция create_window() предназначена для добавления ее в Canvas.

Наконец, мы создаем отключенную кнопку с помощью ttk. Функция Button(), которая принимает окно, изображение, стиль и состояние в качестве аргументов. Чтобы добавить его в Canvas, мы используем функцию create_window().

Текстовое поле
Последним виджетом, который будет добавлен в Canvas, является текстовое поле, под кнопкой аудио вставьте этот код:

# creating the text field
text_field = Text(window, height=15, width=60)
# adding the text field to the canvas
canvas.create_window(248, 340, window=text_field)
Это то, что происходит в коде выше, мы создаем текстовое поле с помощью функции Text(), которая принимает окно, высоту и ширину. Чтобы добавить его в Canvas, мы используем обычную функцию create_window() с 248, 340 и окном в качестве аргументов.

Запустив программу, вы получите такой вывод:

Реализация функции закрытия приложения
Давайте закончим проектирование графического интерфейса, реализовав функциональность близкого приложения. Под импортом вставьте следующий код:

# the function for closing the application
def close_window():
    # this will ask the user whether to close or not
    # if the value is yes/True the window will close
    if askyesno(title='Close Audio Dictionary', message='Are you sure you want to close the application?'):
        # this destroys the window
        window.destroy()
Вот что происходит во фрагменте кода, у нас есть функция под названием close_window(), а внутри нее у нас есть окно сообщения askyesno, которое вычисляет в два логических значения True или False. Если пользователь предоставляет значение yes, которое имеет значение True, будет выполнена функция destroy(), и главное окно будет закрыто. Если значение askyesno равно False, окно все равно будет запущено.

Теперь, когда функция закрытия окна была выполнена, нам нужно позволить главному окну прослушивать событие закрытия окна, чтобы сделать это, под этой строкой кода:

window.title('Audio-Dictionary')
Добавьте следующую строку кода:

# this is for closing the window via the close_window() function
window.protocol('WM_DELETE_WINDOW', close_window)
В этой строке кода функция protocol() принимает WM_DELETE_WINDOW, а функция close_window в качестве аргументов. С помощью WM_DELETE_WINDOW функция будет прослушивать событие закрытия главного окна, которое выдается всякий раз, когда пользователь нажимает кнопку закрытия в главном окне.

Если событие обнаружено, выполняется функция close_window(), и появляется окно сообщения askyesno, если пользователь нажимает кнопку «Да», окно закрывается, а если нет, то окно все равно запускается.

Если вы запустите программу и нажмете кнопку закрытия в главном окне, это результат, который вы получите:

Реализация функциональности приложения
Теперь, когда мы закончили разработку графического интерфейса, в этом разделе мы сосредоточимся на реализации всех функциональных возможностей приложения, чтобы у нас было полнофункциональное приложение.

Функциональность поиска значения слова
Первой функциональностью, которую нужно реализовать, является значение поискового слова, поэтому под функцией close_window() добавьте следующий код:

# function for searching the word meaning
def search_word():
    # getting the word from the entry using the get()
    word = word_entry.get()
    # checking if the word variable is empty
    if word == '':
        # message box to display if the word variable is empty
        showerror(title='Error', message='Please enter the word you wanna search for!!')
   
    # the else statement will execute if the word variable is not empty  
    else:
        # this will execute the code that will find the word meanings
        try:
            # creating a dictionary object
            dictionary = PyDictionary()
            # passing a word to the dictionary object
            meanings = dictionary.meaning(word)
            # deleting content in the text field
            text_field.delete(1.0, END)
            # inserting content(meanings) in the text field
            text_field.insert('1.0', meanings)
            # adding the word to the empty label
            word_label.config(text=word)
            # enabling the audio button to normal state
            audio_button.config(state=NORMAL)
        # this will catch all the exceptions, No/slow internet connection, word with wrong spellings
        except:
            # display the error to the user
            showerror(title='Error', message='An error occurred while trying to search word meaning' \
                   '\nThe following could be ' \
                    'the cause:\n->No/Slow internet connection\n' \
                    '->Wrong word spelling\n' \
                    'Please make sure you have a stable internet connection&\nthe word spelling is correct')
Мы создаем функцию под названием search_word(), и внутри нее происходит следующее:

Мы получаем слово из поля ввода через функцию get().
Затем у нас есть блок if/else, с оператором if, который мы проверяем, пусто ли слово. Если это так, мы отобразим сообщение об ошибке с помощью окна сообщения showerror().
Внутри оператора else мы создаем объект PyDictionary, чтобы получить значение слова, мы передаем слово этому объекту через функцию meaning(). Перед вставкой значений в текстовое поле очищаем текстовое поле с помощью функции delete(), аргументами которой являются 1.0 и END.
Чтобы вставить значение в текстовое поле, мы используем функцию insert(), которая принимает '1.0' и значения в качестве аргументов. После этого мы добавляем слово в пустую метку, которую мы создали ранее с помощью функции config().
Наконец, мы меняем состояние звуковой кнопки обратно в нормальное, это означает, что кнопка будет кликать только тогда, когда будет найдено значение слова.
А в операторе except мы перехватываем каждую ошибку, обнаруженную при поиске значения слова, и показываем ошибку пользователю с помощью окна сообщения showerror().
Теперь давайте привяжем эту функцию к кнопке поиска, поэтому отредактируйте код кнопки поиска и сделайте его следующим образом:

search_button = ttk.Button(window, image=logo, style='TButton', command=search_word)
Здесь мы говорим кнопке, что она должна активировать функцию search_word() после ее нажатия. Давайте найдем слово и посмотрим, работает ли функционал нормально.

Найдите любое слово, и вы получите следующий вывод:

А если присмотреться, то кнопка аудио включена:

Это связано с тем, что в функции search_word() мы указали, что в момент нахождения значения слова кнопка должна быть включена.

Функциональность произношения слов
В этом разделе мы реализуем функцию произношения слов, другими словами, мы хотим, чтобы наше словарное приложение преобразовывало слова в речь. Функция очень похожа на наш учебник по преобразованию текста в речь. Вставьте этот код под функцию search_word():

# function to turn textual data into audio data
def speak():
    # getting the word from the entry
    word = word_entry.get()
    # initializing the pyttsx3 object
    engine = pyttsx3.init()
    # gets the speaking rate
    rate = engine.getProperty('rate')
    # setting the speaking rate
    engine.setProperty('rate', 125)
    # getting the available voices
    voices = engine.getProperty('voices')
    # setting the second voice, the female voice
    engine.setProperty('voice', voices[1].id)
    # this function takes the word to be spoken
    engine.say(word)
    # this fucntion processes the voice commands
    engine.runAndWait()
В функции speak() мы получаем слово из записи через функцию get(), затем инициализируем объект pyttsx3 через pyttsx3.init(). Чтобы получить скорость речи, мы используем функцию getProperty(), а чтобы установить ее на другую скорость, мы используем функцию setProperty().

Библиотека pyttsx3 поставляется с голосами, для доступа к этому голосу мы снова используем функцию getProperty(), а чтобы установить ее на другой голос, мы используем функцию setProperty() в нашем случае мы устанавливаем ее на женский голос. Для произнесения слова мы используем функцию say(), а функция runAndWait() обрабатывает голосовые команды.

Нам нужно привязать эту функцию к кнопке audio, поэтому внутри функции search_word() в операторе try отредактируйте кнопку audio так, чтобы она выглядела следующим образом:

audio_button.config(state=NORMAL, command=speak)
Теперь запустите программу поиска слова и попробуйте нажать кнопку аудио, вы услышите, как слово произносится слышно.

Если пользователь оставил поле ввода пустым и нажал кнопку поиска, это обратная связь, которую приложение выдаст:

Если не было подключения к Интернету или предоставленное слово было неправильным в написании, это результат, который приложение выдаст:

Поздравляем с успешным построением вашего аудиословаря, кажется, что приложение работает просто отлично.

Заключение
Целью этого учебника было создание аудиословаря с графическим интерфейсом с использованием Python. Первым шагом была установка необходимых модулей, проектирование графического пользовательского интерфейса и реализация функциональных возможностей приложения. Наконец, учебник проведет вас через процесс тестирования приложения. Мы надеемся, что вы многому научились и что вы примените полученные знания в своих будущих проектах Python.