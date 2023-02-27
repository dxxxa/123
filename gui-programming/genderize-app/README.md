# [How to Detect Gender by Name using Python](https://www.thepythoncode.com/article/gender-predictor-gui-app-tkinter-genderize-api-python)
##
# [[] / []]()
Гендерное прогнозирование становится все более популярной темой в технологиях и во всем мире. Приложение гендерного предиктора пригодится, если на веб-сайте блога размещен опрос, опрос или обзор продукта. Если бы владельцы выяснили пол, который имеет наибольшее количество голосов, они бы вместо этого использовали приложение гендерного предиктора, чтобы найти пол избирателей и найти количество полов, которые проголосовали больше всего, а не пытаться выяснить пол имен вручную.

В этой статье мы создадим приложение гендерного предиктора с помощью Tkinter, инструментария Python GUI и API от genderize.io. Мы будем использовать API Genderize для определения пола имени пользователя, этот API полностью бесплатен, и ему не нужен ключ API, чтобы иметь возможность делать запросы API.

В конце этой статьи мы собираемся создать приложение, которое выглядит следующим образом:



Мы сделаем это приложение с нуля.

Содержание:

Настройка проекта
Проектирование графического интерфейса пользователя (GUI)
Реализация функции гендерного предиктора
Заключение
Настройка проекта
Первой задачей является настройка проекта. Давайте установим библиотеку запросов:

$ pip install requests
Затем создайте папку и назовите ее genderpredictor и cd в папку:

$ mkdir genderpredictor
$ cd genderpredictor
Внутри папки genderpredictor создайте файл и назовите его genderize_app.py, это не соглашение. Не стесняйтесь называть его так, как вы хотите:



Проектирование графического интерфейса пользователя (GUI)
Мы, прежде всего, создадим главное окно, которое будет содержать все остальные виджеты (фреймы, метки, запись, кнопку), откроем файл и вставим следующий код:

# importing everything from tkinter
from tkinter import *
# tkinter message box to display errors
from tkinter.messagebox import showerror

# colors for the application
gold = '#dca714'
brown = '#31251d'
# creating the main window
window = Tk()
# defining the demensions of the window, width(325), height(300), 500+200 center the window
window.geometry('325x300+500+200')
# this is the title of the application
window.title('Gender Predictor')
# this makes the window unresizable
window.resizable(height=FALSE, width=FALSE)
window.mainloop()
Давайте немного разобьем этот код, мы создаем главное окно с помощью функции Tk(), и мы даем этому окну размеры и заголовок, используя функции geometry() и title(). Параметр resizable() с атрибутами FALSE сделает главное окно неизменяемым, и, наконец, мы хотим запустить окно как цикл, пока пользователь не закроется.

Запустите программу, и выходные данные будут выглядеть следующим образом:



Теперь внутри созданного окна давайте создадим два фрейма, верхний фрейм и нижний фрейм, под этой строкой кода:

window.resizable(height=FALSE, width=FALSE)
Вставьте следующий код:

"""The two frames"""
# this is the top frame inside the main window
top_frame = Frame(window, bg=brown, width=325, height=80)
top_frame.grid(row=0, column=0)
# this is the bottom frame inside the main window
bottom_frame = Frame(window, width=300, height=250)
bottom_frame.grid(row=1, column=0)
Здесь мы создаем две рамы, верхнюю раму и нижнюю раму, и все эти рамки размещаются внутри главного окна. Мы устанавливаем размеры для обоих этих кадров, используя атрибуты width и height. Верхний кадр принимает bg в качестве дополнительного атрибута, это установит цвет фона верхнего кадра на коричневый.

Запустив программу, вывод будет следующим:



Внутри верхней рамки давайте создадим две метки; чуть ниже фреймов вставьте следующий код:

# the label for the big title inside the top_frame
first_label = Label(top_frame, text='GENDER PREDICTOR', bg=brown, fg=gold, pady=10, padx=20, justify=CENTER, font=('Poppins 20 bold'))
first_label.grid(row=0, column=0)

# the label for the small text inside the top_frame
second_label = Label(top_frame, text='Give me any name and i will predict its gender', bg=brown, fg=gold, font=('Poppins 10'))
second_label.grid(row=1, column=0)
Приведенный выше фрагмент кода создаст две метки, которые будут помещены в верхний кадр.

Теперь запустите программу, и вы получите что-то вроде этого:



На этот раз мы создадим оставшиеся виджеты в нижнем фрейме; сразу после двух меток вставьте следующий код:

"""below are widgets inside the top_frame"""
# the name label
label = Label(bottom_frame, text='NAME:', font=('Poppins 10 bold'), justify=LEFT)
label.place(x=4, y=10)
# the entry for entering the user's name
name_entry = Entry(bottom_frame, width=25, font=('Poppins 15 bold'))
name_entry.place(x=5, y=35)
# the empty name label, it will be used to display the name
name_label = Label(bottom_frame, text='', font=('Poppins 10 bold'))
name_label.place(x=5, y=70)
# the empty gender label, it will be used to display the gender
gender_label = Label(bottom_frame, text='', font=('Poppins 10 bold'))
gender_label.place(x=5, y=90)
# the empty probability label, it will be used to display the gender probalility
probability_label = Label(bottom_frame, text='', font=('Poppins 10 bold'))
probability_label.place(x=5, y=110)
# the predict button
predict_button = Button(bottom_frame, text="PREDICT", bg=gold, fg=brown, font=('Poppins 10 bold'))
predict_button.place(x=5, y=140)
Приведенный выше фрагмент кода создает оставшиеся виджеты, четыре метки, запись и кнопку внутри нижнего фрейма.

Давайте запустим программу, и вот вывод:



Поздравляем с успешным проектированием пользовательского интерфейса приложения!

Реализация функции гендерного предиктора
Теперь, когда пользовательский интерфейс завершен, давайте сосредоточимся на реализации функции прогнозирования пола. Мы создадим функцию, которая будет обрабатывать все это за нас, чуть ниже:

# importing everything from tkinter
from tkinter import *
# tkinter message box to display errors
from tkinter.messagebox import showerror
Вставьте следующие строки кода:

# the requests will be used for making requests to the API
import requests
URL-адрес, который мы будем использовать, будет иметь следующий формат:

https://api.genderize.io?name={YOUR_NAME}
Веб-сайт genderize.io предоставляет игровую площадку, где вы можете протестировать API. Вы можете получить доступ к нему здесь.

Давайте теперь создадим функцию для прогнозирования пола, назовем ее predict_gender(), и сделаем так, чтобы она выглядела так:

def predict_gender():
    # executes when code has no errors
    try:
        # getting the input from entry
        entered_name = name_entry.get()
        # making a request to the API, the user's entered name is injected in the url
        response = requests.get(f'https://api.genderize.io/?name={entered_name}').json()
        # getting name from the response
        name = response['name']
        # getting gender from the response  
        gender = response['gender']
        # getting probability from the response 
        probability = 100 * response['probability']
        # adding name to the label that was empty, the name is being uppercased
        name_label.config(text='The name is ' + name.upper())
        # adding gender to the label that was empty, the gender is being uppercased  
        gender_label.config(text='The gender is ' + gender.upper())
        # adding probability to the label that was empty
        probability_label.config(text='Am ' + str(probability) + '%' + ' accurate')
    # executes when errors are caught
    # KeyError, ConnectionTimeoutError   
    except:
        showerror(title='error', message='An error occurred!! Make sure you have internet connection or you have entered the correct data')
Приведенная выше функция получает данные имени из записи с помощью функции get(), и это имя передается в URL-адрес API. Затем запрос отправляется в API для получения ответа. После получения ответа ответ преобразуется в JSON с помощью функции json(), и из этих данных JSON имя, пол и вероятность извлекаются с помощью ключей, и они подключаются к соответствующим меткам.

Мы также упаковываем весь код в блок try/except и показываем ошибку окна всякий раз, когда возникает ошибка.

После создания функции подключим ее с помощью кнопки Predict; мы хотим, чтобы функция запускалась, когда пользователь нажимает на нее. Виджет Button() в Tkinter принимает аргумент command, поэтому замените переменную predict_button следующей:

predict_button = Button(bottom_frame, text="PREDICT", bg=gold, fg=brown, font=('Poppins 10 bold'), command=predict_gender)
Теперь давайте протестируем приложение, запустим его, введем имя jane и нажмем кнопку:



Приложение работает так, как мы ожидали!

Теперь давайте снова запустим приложение, но на этот раз мы оставим запись пустой и нажмем на кнопку Predict:



Заключение
Ну вот! Мы надеемся, что вам понравилась эта статья о том, как создать приложение гендерного предиктора с помощью Tkinter и API Genderize. Мы надеемся, что вы включите полученные знания в свои будущие приложения.

Вы можете получить полный код здесь.