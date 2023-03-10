# [How to Plot Weather Temperature in Python](https://www.thepythoncode.com/article/interactive-weather-plot-with-matplotlib-and-requests)
##
# [[] / []]()
В этом уроке мы сделаем интерактивный линейный график Matplotlib, показывающий температуру города в течение следующих семи дней. Таким образом, мы узнаем о matplotlib.widgets и о запросах, потому что мы используем API open-meteo.com для наших данных. Мы также используем модуль json, чтобы мы могли считывать данные ответа.

Для начала импортируем необходимые библиотеки:

$ pip install requests matplotlib seaborn
Мы будем использовать seaborn для автоматического укладки. Откройте новый файл Python и импортируйте следующее:

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import seaborn
seaborn.set_style("darkgrid")
import requests
import json
Местонахождения
После импорта мы определяем некоторые местоположения, из которых пользователь может выбирать. API, который мы будем использовать, принимает только координаты WG84, а не географические названия.

Поэтому мы ищем некоторые места и их координаты и вставляем их в словарь, где ключом является название места, а значением является список из двух элементов с широтой и долготой. Вы можете расширить этот словарь Python, если хотите:

# Define some Locations to choose from.
# Latitude and Longitude
locations = {
    'Schaffhausen': ['47.7', '8.6'],
    'Sydney': ['-33.86', '151.20'],
    'Kyiv': ['50.4422', '30.5367'],
    'Constantine': ['36.368258', '6.560254'],
    'Yakutsk': ['62.0', '129.7'],
}
Вы также можете использовать геокодирование для автоматического получения широты и долготы из названия города; этот учебник должен помочь.

Настройка Matplotlib
Теперь давайте настроим matplotlib. Для этого мы вызываем функцию subplots() и сохраняем два возвращаемых ею элемента в двух переменных. Мы обычно используем эту функцию, если хотим несколько осей. Переменная fig содержит информацию обо всем этом, а ax содержит информацию об одном графике. Затем мы определяем переменную p, которая будет хранить информацию о графике нашего единственного графика:

# Setting Up Matplotlib, using the OOP Approach
fig, ax = plt.subplots()
# the plot is created with the first location
p = None
Функция получения температуры
В приведенной ниже функции мы используем библиотеку запросов для получения данных из open-meteo.com свободного API, а затем анализируем их с помощью модуля json и возвращаем время и температуру:

# make a function to get the temperatures of a given location
def getTemperatures(location):
    # get the lat and long of the location
    lat, lon = locations[location]
    req = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m')
    req = json.loads(req.text)
    # get the tempratures
    temperatures = req['hourly']['temperature_2m']
    # get the times
    times = req['hourly']['time']
    return times, temperatures
Мы можем запросить этот URL-адрес с помощью метода из . Оттуда мы анализируем данные JSON в допустимый словарь Python с помощью функции . Здесь вы можете увидеть, как может выглядеть такой запрос.get()requestsjson.loads()

Загрузка и хранение данных
Давайте сделаем словарь Python, который хранит местоположение и соответствующее время и температуру:

# Make a dictionary with the locations as keys and the getTemperatures() function as values
location2data = {}
for location in locations:
    location2data[location] = getTemperatures(location)
Функция изменения местоположения
Теперь давайте перейдем к функции, которая изменит местоположение, которое мы в настоящее время показываем. Кнопки вызовут его, и это соединение передаст имя кнопки функции, и это имя будет новым желаемым местоположением. Мы также получаем глобальную переменную p, которую мы определили ранее:

def changeLocation(newLocation):
    global p
Затем мы просто используем location2data, чтобы получить время и температуру пройденного местоположения:

    # get the data of the location from the dictionary
    times, temperatures = location2data[newLocation]
После получения данных мы проверяем, не является ли p None, и если это так, мы устанавливаем данные на наше недавно найденное значение температуры и обновляем график:

    if p:
        p.set_ydata(temperatures)
        # reflect changes in the plot
        plt.draw()
Если p не определено, мы должны сделать это первыми. Для этого мы используем метод plot() на ax. Мы даем ему список времени как ось x, и мы делаем понимание списка для оси Y. Мы также устанавливаем стиль line с ls, ширину линии с lw.

Эта функция сделает график и вернет список каждой строки. Мы получаем первый и единственный элемент оттуда и сохраняем его в p:

    else:
        # Make a Plot and save the first object to a variable
        # p will be a Line2D object which can be changed at a later time
        p = ax.plot(times, temperatures, ls=':', lw=3)[0]
Теперь мы также редактируем палочки, потому что они не будут хорошими со 168 точками данных. Для этого начнем с составления списка, где выбираются семь чисел по 24 (часа) друг от друга:

        # set the x-axis to the times
        xRange = list(range(0, 168, 24)) + [168]
        ax.set_xticks(xRange)
Установка оси y для температур, а также:

        # set the y-axis to the temperatures
        yRange = list(range(-20, 55, 5))
        ax.set_yticks(yRange)
И последнее, но не менее важное: мы также устанавливаем цвет метки и поворот для этих меток с помощью метода tick_params.

        plt.tick_params(axis="both", which='both', labelrotation=-10) # rotate the labels
Во всех случаях мы обновляем заголовок, чтобы отразить текущее местоположение. Мы можем сделать это на лету. А после того, как функция определена, мы вызываем ее со стартовым расположением, чтобы график не был пустым:

    # set the title
    ax.set_title('Temperatures in ' + newLocation)


# Call the change Location function for the first time
changeLocation('Schaffhausen')
Переключатели настройки
Теперь мы делаем несколько переключателей. Для этого мы просто вызываем класс RadioButtons() и предоставляем ему позицию, которая представлена осями, и даем имена местоположений в качестве аргумента меток.

# Making the Radio Buttons
buttons = RadioButtons(
    ax=plt.axes([0.1, 0.1, 0.2, 0.2]),
    labels=locations.keys()
)
Затем нам нужно также подключить событие нажатия этих кнопок к нашей функции.

# Connect clicked event to function.
buttons.on_clicked(changeLocation)
Мы также корректируем положение графика, поэтому есть место для радиокнопки.

# adjust the plot size
plt.subplots_adjust(left=0.1, bottom=0.40)
Метки и отображение графика
В конце концов, прежде чем мы покажем график, мы также дадим оси x и y метку и раскрасим их.

# Label the Plot
ax.set_xlabel('Times [Next Seven Days]')
ax.xaxis.label.set_color(labelColor)

ax.set_ylabel('Temperatures [Celcius]')
ax.yaxis.label.set_color(labelColor)

plt.show()
Витрина
Ниже вы видите нашу маленькую программу в действии. В Константине становится жарко!

Витрина

Заключение
Отлично! Вы успешно научились:

Создайте интерактивный сюжет с помощью matplotlib.
Выполняйте простые HTTP GET-запросы к open-meteo.com API.
Посмотрите, как вы можете добавить в эту программу дополнительные функции, такие как поле Entry для широты и долготы или автоматическое получение координат из названия города; этот учебник должен вам помочь.