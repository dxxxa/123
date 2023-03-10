# [How to Build a GUI Currency Converter using Tkinter in Python](https://www.thepythoncode.com/article/currency-converter-gui-using-tkinter-python)
##
# [[] / []]()
Tkinter является одной из тех замечательных встроенных библиотек Python, которые существуют уже давно; он используется для создания шикарных графических пользовательских интерфейсов (GUI) для настольных приложений. Эта статья научит вас создавать приложение для конвертера валют с использованием библиотеки Tkinter и API ExchangeRate.

Если вы хотите использовать другой источник данных, ознакомьтесь с этим учебником, где мы использовали пять различных источников для конвертации валют, включая Fixer API, Yahoo Finance и многое другое.

ExchangeRate API - это валютный API в режиме реального времени, который является как бесплатным, так и профессиональным, он поддерживает курсы конвертации валют для 161 валюты, а для счета freemium вы должны делать 250 запросов в месяц, поэтому использование бесплатной учетной записи сэкономит нам день.

В конце этой статьи мы собираемся создать приложение, которое выглядит следующим образом:

Конвертер валют

Вот оглавление:

Настройка проекта
Разработка графического интерфейса пользователя (GUI)
Получение ключа API для API ExchangeRate
Заполнение полей со списком валютами
Реализация функции конвертации валют
Перехват исключений
Заключение
Настройка проекта
Прежде всего, давайте настроим проект. Мы начнем с создания виртуальной среды, а затем установим библиотеку запросов Python.

Создайте папку с именем currencyconverter и cd в папку:

$ mkdir currencyconverter 
$ cd currencyconverter
Мы создадим виртуальную среду в этой папке и назовем ее env или любое имя по вашему выбору:

$ python -m venv env
Активируйте виртуальную среду в Windows:

$ .\env\Scripts\activate.bat
В Linux/macOS:

$ source env/bin/activate
Теперь, когда виртуальная среда активирована, давайте установим библиотеку запросов:

$ pip install requests
Проектирование графического интерфейса пользователя (GUI)
В этом разделе мы начнем проектирование графического интерфейса для приложения с нуля. Прежде всего, создайте файл с именем currency_converter.py это не соглашение; Вы можете назвать его как угодно:

Проектирование графического интерфейса пользователя (GUI)

Начнем с создания главного окна приложения. Откройте файл и вставьте следующий код:

# importing everything from tkinter
from tkinter import *
# importing ttk widgets from tkinter
from tkinter import ttk

# creating the main window
window = Tk()
# this gives the window the width(310), height(320) and the position(center)
window.geometry('310x340+500+200')
# this is the title for the window
window.title('Currency Converter')
# this will make the window not resizable, since height and width is FALSE
window.resizable(height=FALSE, width=FALSE)
# this runs the window infinitely until it is closed
window.mainloop()
В приведенном выше коде мы создаем главное окно с помощью функции Tk(), которая поставляется с Tkinter. Затем мы определяем размеры окна с помощью функции geometry(). Чтобы присвоить окну заголовок, мы используем функцию title().

Мы также используем функцию resizable() с атрибутами FALSE, чтобы сделать окно неизменяемым. Наконец, функция mainloop() будет держать окно приложения открытым, пока пользователь не закроет его.

Если вы запустите эту программу, вы получите следующие выходные данные:

Проектирование графического интерфейса пользователя (GUI)

Теперь давайте создадим два фрейма, верхний кадр и рамку кнопки. Верхний фрейм будет содержать текст «Конвертер валют» и выглядеть он должен выглядеть следующим образом:

Конвертер валют

Сразу после этой строки кода:

window.resizable(height=FALSE, width=FALSE)
Вставьте следующие строки кода:

# colors for the application
primary = '#081F4D'
secondary = '#0083FF'
white = '#FFFFFF'

# the top frame
top_frame = Frame(window, bg=primary, width=300, height=80)
top_frame.grid(row=0, column=0)
# label for the text Currency Converter
name_label = Label(top_frame, text='Currency Converter', bg=primary, fg=white, pady=30, padx=24, justify=CENTER, font=('Poppins 20 bold'))
name_label.grid(row=0, column=0)
Мы добавили несколько цветов и создали верхнюю рамку, содержащую метку. Верхняя рамка должна быть размещена внутри главного окна, которое мы только что создали; рамка принимает три других атрибута: bg, ширину и высоту.

Выходные данные этого кода выглядят следующим образом:



Давайте теперь создадим нижнюю рамку; этот фрейм будет содержать виджеты, такие как метки, поля со списком, запись и кнопка. Это будет выглядеть следующим образом



Под name_label вставьте следующий код:

# the top frame
top_frame = Frame(window, bg=primary, width=300, height=80)
top_frame.grid(row=0, column=0)
# label for the text Currency Converter
name_label = Label(top_frame, text='Currency Converter', bg=primary, fg=white, pady=30, padx=24, justify=CENTER, font=('Poppins 20 bold'))
name_label.grid(row=0, column=0)
# the bottom frame
bottom_frame = Frame(window, width=300, height=250)
bottom_frame.grid(row=1, column=0)
# widgets inside the bottom frame
from_currency_label = Label(bottom_frame, text='FROM:', font=('Poppins 10 bold'), justify=LEFT)
from_currency_label.place(x=5, y=10)
to_currency_label = Label(bottom_frame, text='TO:', font=('Poppins 10 bold'), justify=RIGHT)
to_currency_label.place(x=160, y=10)
# this is the combobox for holding from_currencies
from_currency_combo = ttk.Combobox(bottom_frame, width=14, font=('Poppins 10 bold'))
from_currency_combo.place(x=5, y=30)
# this is the combobox for holding to_currencies
to_currency_combo = ttk.Combobox(bottom_frame, width=14, font=('Poppins 10 bold'))
to_currency_combo.place(x=160, y=30)
# the label for AMOUNT
amount_label = Label(bottom_frame, text='AMOUNT:', font=('Poppins 10 bold'))
amount_label.place(x=5, y=55)
# entry for amount
amount_entry = Entry(bottom_frame, width=25, font=('Poppins 15 bold'))
amount_entry.place(x=5, y=80)
# an empty label for displaying the result
result_label = Label(bottom_frame, text='', font=('Poppins 10 bold'))
result_label.place(x=5, y=115)
# an empty label for displaying the time
time_label = Label(bottom_frame, text='', font=('Poppins 10 bold'))
time_label.place(x=5, y=135)
# the clickable button for converting the currency
convert_button = Button(bottom_frame, text="CONVERT", bg=secondary, fg=white, font=('Poppins 10 bold'))
convert_button.place(x=5, y=165)
Мы создаем нижнюю раму; как и верхняя рама, мы разместим нижнюю раму внутри главного окна. Внутри этого фрейма мы разместим оставшиеся виджеты, две метки, два поля со списком, запись и кнопку.

Запустив код, вы получите следующий вывод:



Поздравляем с успешным проектированием графического пользовательского интерфейса приложения!

Получение ключа API для API ExchangeRate
API ExchangeRate требует, чтобы у нас был ключ API, который позволит нам делать успешные запросы к нему. Чтобы получить ключ API, перейдите по этому URL-адресу и введите свой адрес электронной почты в поле электронной почты:

 Получение ключа API для API ExchangeRate

Нажмите кнопку Получить бесплатный ключ, и вам будет предложено создать учетную запись. После предоставления учетных данных вы попадете в следующее окно:



Войдите в свою учетную запись электронной почты и подтвердите свой адрес электронной почты, чтобы активировать учетную запись API ExchangeRate. Вы найдете письмо в папке акций; если нет, проверьте основную папку или папку спама.

Если вы успешно подтвердили, вы попадете на панель мониторинга API ExchangeRate, а на панели мониторинга вы также найдете свой личный секретный ключ API. По соображениям безопасности этот ключ не подлежит совместному использованию.

На панели мониторинга на боковой панели навигации в разделе Документация щелкните ссылку Обзор документов:



Или посетите этот URL-адрес. Здесь мы сосредоточимся на двух запросах, стандартном и парном преобразовании:



Стандартный запрос вернет весь список валют, которые предоставляет API, и он принимает следующий формат:

https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD
С другой стороны, запрос на конвертацию пары преобразует две заданные валюты, и он принимает следующий формат:

https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/EUR/GBP
Заполнение полей со списком валютами
Мы создали поля со списком, но они не содержат значений, поэтому давайте заполним их валютами, чтобы пользователь выбрал из них валюты. Для этого мы будем использовать стандартный запрос, чтобы предоставить нам список валют. Below ваш импорт, paste эти строки кода:

import requests
import json

API_KEY = "put your API key here"
# the Standard request url
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
# making the Standard request to the API and converting the request to json
response = requests.get(f'{url}').json()
# converting the currencies to dictionaries
currencies = dict(response['conversion_rates'])
Обязательно замените API_KEY реальным ключом API.

Прокрутите вниз до того места, где вы определили два поля со списком. Поле со списком принимает аргумент, называемый значениями, и его тип данных должен быть списком. Теперь сделайте так, чтобы первое поле со списком выглядело следующим образом:

from_currency_combo = ttk.Combobox(bottom_frame, values=list(currencies.keys()), width=14, font=('Poppins 10 bold'))
Как вы можете заметить, мы добавили аргумент values в поле со списком, и он принимает все ключи словаря валют в виде списка.

Тестирование этого:



Давайте также заполним второе поле со списком:

to_currency_combo = ttk.Combobox(bottom_frame, values=list(currencies.keys()), width=14, font=('Poppins 10 bold'))
Результат:



Реализация функции конвертации валют
Теперь, когда все поля со списком работают, пришло время реализовать функциональность конвертации валюты. Все это будет сделано внутри функции. Не забудьте сделать парную конвертацию; мы используем этот URL:

https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/EUR/GBP
Создание функции конвертации двух пар валют чуть выше:

window = Tk()
Вставьте следующий код:

def convert_currency():
    # getting currency from first combobox
    source = from_currency_combo.get()
    # getting currency from second combobox
    destination = to_currency_combo.get()
    # getting amound from amount_entry
    amount = amount_entry.get()
    # sending a request to the Pair Conversion url and converting it to json
    result = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{source}/{destination}/{amount}').json()
    # getting the conversion result from response result
    converted_result = result['conversion_result']
    # formatting the results
    formatted_result = f'{amount} {source} = {converted_result} {destination}'
    # adding text to the empty result label
    result_label.config(text=formatted_result)
    # adding text to the empty time label
    time_label.config(text='Last updated,' + result['time_last_update_utc'])
Функция convert_currency() получает валюты из двух полей со списком и сумму из записи с помощью функции get(). Эти значения и ключ API передаются в запрос API. Результат запроса преобразуется в JSON с помощью функции json().

Эта функция будет активирована, когда мы нажмем кнопку Конвертировать, поэтому нам нужно сказать кнопке, чтобы активировать эту функцию. В Tkinter кнопки принимают аргумент команды с функцией в качестве значения, поэтому мы сделаем так, чтобы кнопка выглядела следующим образом:

convert_button = Button(bottom_frame, text="CONVERT", bg=secondary, fg=white, font=('Poppins 10 bold'), command=Convert_Currency)
Теперь кнопка знает, какую функцию активировать после ее нажатия, давайте проверим это, запустим программу и заполните поля со списком данными (от EUR до USD) и введем сумму 1000, нажмем кнопку и убедитесь, что вы получаете следующий вывод:



Перехват исключений
Приложение запускается успешно, но что делать, если пользователь нажимает кнопку Конвертировать, не заполняя обязательные поля? Ответ очевиден, приложение выдаст ошибку, но пользователь не увидит эту ошибку, так как она возникнет в бэкэнде.

Итак, далее нам нужно улучшить пользовательский опыт приложения; мы дадим возможность пользователю узнать, какие ошибки произошли. В файл в разделе импорта вставьте следующий код:

# tkinter message box for displaying errors
from tkinter.messagebox import showerror
Код внутри функции convert_currency() будет находиться внутри блока try/except. Код, заключенный в инструкцию try, будет выполняться, если исключений нет. В противном случае будет выполнен код внутри инструкции except:

def convert_currency():
    # will execute the code when everything is ok
    try:
        # getting currency from first combobox
        source = from_currency_combo.get()
        # getting currency from second combobox
        destination = to_currency_combo.get()
        # getting amound from amount_entry
        amount = amount_entry.get()
        # sending a request to the Pair Conversion url and converting it to json
        result = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{source}/{destination}/{amount}').json()
        # getting the conversion result from response result
        converted_result = result['conversion_result']
        # formatting the results
        formatted_result = f'{amount} {source} = {converted_result} {destination}'
        # adding text to the empty result label
        result_label.config(text=formatted_result)
        # adding text to the empty time label
        time_label.config(text='Last updated,' + result['time_last_update_utc'])
    # will catch all the errors that might occur 
    # ConnectionTimeOut, JSONDecodeError etc
    except:
        showerror(title='Error', message='An error occurred!!')
Повторно запустите приложение, но на этот раз не заполняйте обязательные поля и нажмите кнопку Преобразовать. Мы получим следующий результат:



Теперь приложение может улавливать все ошибки и отображать их пользователю.

Заключение
Поздравляем с успешным созданием графического приложения конвертера валют. Вы можете получить полный код для этого приложения здесь.

Вот и все для этого туториала! Мы надеемся, что вам понравилась эта статья о том, как создать приложение конвертера валют с использованием Python, Tkinter и ExchangeRate API. Мы надеемся, что это поможет вам в ваших будущих проектах Python.

В этом уроке мы создали пять различных конвертеров валют с использованием ExchangeRate API, Fixer API, Yahoo Finance, Xe и X-RATES. Обязательно проверьте его и объедините с этим графическим интерфейсом.