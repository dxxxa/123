# [How to Generate SVG Country Maps in Python](https://www.thepythoncode.com/article/generate-svg-country-maps-python)
##
# [[] / []]()
В этом учебнике мы будем использовать API страны GADM для создания файлов SVG для каждой страны. Мы сделаем это, чтобы страна идеально вписывалась в тег SVG. Для этого мы должны проанализировать данные. Мы также будем использовать модуль pycountry, чтобы получить все трехбуквенные коды стран. Давайте разберемся в этом!

Установка pycountry:

$ pip install pycountry
Импорт библиотек:

# Default Library
import requests
import json
import os

# Download with pip install pycountry
import pycountry
Настройка
Весь остальной код находится внутри цикла for, потому что мы загрузим каждую страну. Для этого мы преобразуем словарь стран в список и зацикливаемся на нем. Объект country будет содержать объект Country с трехбуквенным кодом в качестве свойства.

for country in list(pycountry.countries):
Затем мы определяем четыре переменные. Первый будет содержать все координаты нынешней границы страны. Второй будет содержать координаты в том виде, в котором они сгруппированы в API. Это необходимо, потому что большинство стран состоят из нескольких неподключенных частей. Последние два содержат трехбуквенный код страны и название страны из объекта страны:

    # All Points from all Groups
    # used to analyze
    allPoints = []

    # Countries that dont consist of one body 
    # will have multiple groups of coordinates
    pointGroups = []

    # Country Code with 3 letters
    countryCode = country.alpha_3
    countryName = country.name
Прежде чем мы углубимся в цикл, мы проверим, создали ли мы уже карту SVG для этой страны. Мы сохраним SVG в выходной папке, а имя файла будет просто именем страны. Поэтому мы объединяем строку с этой информацией и отдаем ее функции os.path.exists(). Если файл существует, мы пропускаем эту итерацию с оператором continue.

    # Check if the SVG file already Exists and skip if it does
    if os.path.exists(f'output/{countryName}.svg'):
        print(f'{countryName}.svg Already exists ... Skipping to next Country\n')
        continue

    print('Generating Map for: ', countryName)
Запрос данных
Теперь мы запрашиваем данные. Данные представляют собой просто файл .json, находящийся на веб-сервере. URL-адрес швейцарских данных выглядит следующим образом. Для других стран мы должны просто поменять CHE кодом другой страны:

https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_CHE_0.json
Поэтому мы вставляем этот код страны в этот URL-адрес и используем его в функции get() из запросов. После этого мы пытаемся расшифровать возвращенный текст. Если это не сработает, возможно, мы сделали недействительный запрос. Если это так, мы пропускаем итерацию.

    # Get the Data
    re = requests.get(f'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{countryCode}_0.json')

    # If the string cant be parsed an invalid country was requested
    try:
        data = json.loads(re.text)
    except json.decoder.JSONDecodeError:
        print('Could not decode ... Skipping to next Country\n')
        continue
Организация данных
Теперь нам нужно организовать данные для последующего использования. Для этого мы зацикливаемся на данных, пока не столкнемся с группами; мы добавляем их в список, который мы определили ранее. Затем мы также проходим через эту группу и добавляем точки в список allPoints:

    # Organise the Data 
    # Get the groups and all coordinates
    for i in data['features'][0]['geometry']['coordinates']:
        for group in i:
            pointGroups.append(group)
            for coord in group:
                allPoints.append(coord)

    print(f'\n{len(allPoints)} Points')
Анализ данных
После этого мы анализируем данные. Мы хотим узнать самые низкие и самые высокие точки для каждой оси, потому что мы хотим сделать так, чтобы путь, который мы позже генерируем, идеально вписывался в файл SVG. Итак, мы определяем переменные для каждой из этих четырех точек:

    # Analyse Data
    # Use these Information to calculate 
    # offset, height and width of the Country
    lowestX = 9999999999
    highestX = -9999999999

    lowestY = 9999999999
    highestY = -9999999999
Затем мы зацикливаемся на списке allPoints и устанавливаем каждое значение соответствующим образом. Мы делаем это с троичным оператором:

    for x, y in allPoints:
        lowestX = x if x < lowestX else lowestX
        highestX = x if x > highestX else highestX

        lowestY = y if y < lowestY else lowestY
        highestY = y if y > highestY else highestY
Затем мы показываем некоторую отладочную информацию:

    print('lowestX', lowestX)
    print('highestX', highestX)

    print('lowestY', lowestY)
    print('highestY', highestY)
Затем мы можем рассчитать высоту и ширину SVG, или там я говорю страну с информацией, которую мы только что получили.

    svgWidth = (highestX - lowestX)
    svgHeight = (highestY - lowestY)
Отображение данных
Давайте отобразим страну с помощью SVG. Будем использовать многоугольный элемент. Некоторые знания HTML были бы хороши для следующей части, потому что SVG - это просто HTML.

Таким образом, мы определяем полигональную переменную, которая будет содержать строки полигонального элемента. Затем мы зацикливаемся на группах и определяем coordinateString, который будет сохранять текущие координаты. Затем мы также зацикливаемся на этой группе и распаковываем ее.

Мы вычитаем самую нижнюю часть каждой оси, поэтому страна прилипает к краям. Затем добавляем пару в строку координат. После того, как мы зациклились на группе, мы делаем полигональную строку с координатной строкой, вставленной в правильное место.

    # Transfrom Points to Polygon Strings
    polygonString = ''
    for group in pointGroups:
        coordinateString = ''
        for x, y in group:
            x  = (x - lowestX)
            y  = (y - lowestY)

            coordinateString = coordinateString + f'{x},{y} '

        polygonString += f'<polygon points="{coordinateString}"></polygon>'
Затем вставляем все полигоны в строку SVG с правильными настройками:

    svgContent = f"""
    <svg width="{svgWidth}" height="{svgHeight}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="transform: scale(1, -1)">
        {polygonString}
    </svg>
    """
И последнее, но не менее важное: мы записываем эту строку в файл, названный в честь страны:

    # make the output folder
    if not os.path.isdir("output"):
        os.mkdir("output")
    # write the svg file
    with open(f'output/{countryName}.svg', 'w') as f:
        f.write(svgContent)
    # new line
    print('\n')
Заключение
Эта программа попытается сделать границу страны SVG файлы всех стран мира и сохранит их в выходной папке.

Обратите внимание, что небольшие страны будут выглядеть крошечными по сравнению с более крупными, обязательно масштабируйте их, если вы хотите использовать любой из них.