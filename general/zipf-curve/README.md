# [Zipf's Word Frequency Plot with Python](https://www.thepythoncode.com/article/plot-zipfs-law-using-matplotlib-python)
To run this code, install:
- `pip install -r requirements.txt`
- The `texts` folder already exists if you want to use it.
##
# [[] / []]()
Идея и закон Ципфа
В этом уроке мы будем использовать Python и его модуль построения matplotlib для иллюстрации частотных распределений слов текстов. Это называется законом Ципфа, который гласит, что частота слов обратно пропорциональна их рангу и наиболее распространенному слову.

Таким образом, это означает, что второе наиболее частое слово в два раза чаще, чем наиболее распространенное, третье на треть чаще, чем наиболее распространенное, и так далее. Мы проанализируем тексты и покажем эти частоты на линейном графике.

Чтобы начать работу, давайте установим matplotlib, NumPy и scipy:

$ pip install numpy matplotlib scipy
Импорт
Давайте начнем с импорта некоторых модулей, чтобы помочь создать эту программу. Во-первых, мы получаем OS, чтобы мы могли перечислить все файлы в каталоге с функцией os.list_dir(), потому что мы делаем это так, чтобы мы могли сбрасывать файлы .txt в определенную папку, и наша программа будет включать их динамически. Далее мы получаем pyplot из matplotlib, простого необъективно-ориентированного API для matplotlib.

После этого мы получаем строку, которая нам нужна, потому что мы удалим все знаки препинания текста, и мы можем использовать строку в этом модуле. Последующие два импорта выполняются, чтобы мы могли позже сгладить кривую:

# Imports
import os
from matplotlib import pyplot as plt
import string
import numpy as np
from scipy.interpolate import make_interp_spline
Настройка
Далее мы настраиваем некоторые переменные. тексты будут содержать тексты файлов, доступные по их имени файла без расширения. Следующий довольно похож. Он будет просто иметь длину каждого текста. textwordamount будет содержать другой словарь, где каждый ключ представляет слово и значение его количества вхождений в тексте. После этого получаем переменную пунктуации из строки и сохраняем список в переменной:

# define some dictionaries
texts = {}
textlengths = {}
textwordamounts = {}

unwantedCharacters = list(string.punctuation)
После этого мы также определяем, насколько глубоко мы хотим зайти с проверкой вхождений, и мы также определяем ось X, потому что она всегда будет одинаковой в диапазоне от 1 до 10 (или того, что мы указали как глубину):

# How many ranks well show
depth = 10
xAxis = [str(number) for number in range(1, depth+1)]
Получение текстов
После настройки мы можем, наконец, начать с получения текстов. Для этого нам сначала понадобятся имена всех файлов в папке texts. Вы можете назвать это как угодно. Затем мы зацикливаемся на этих именах, открываем их и читаем их содержание в словаре текстов. Мы устанавливаем ключ path.split('.') [] таким образом, мы получаем имя файла без расширения:

# Getting all files in text folder
filePaths = os.listdir('texts')
# Getting text from .txt files in folder
for path in filePaths:
    with open(os.path.join('texts', path), 'r', encoding='UTF-8') as f:
        texts[path.split('.')[0]] = f.read()
Очистка текстов и подсчет слов
Теперь продолжаем очищать тексты от нежелательных символов и подсчитывать слова. Итак, мы зацикливаемся на каждом ключе в словаре, и для этого цикла, соответственно, мы зацикливаемся на каждом нежелательном символе, заменяем его в тексте и устанавливаем текст в указанной паре ключ/значение в эту новую и очищенную строку:

# Cleaning and counting the Text
for text in texts:
    # Remove unwanted characters from the texts
    for character in unwantedCharacters:
        texts[text] = texts[text].replace(character, '').lower()
После этого разбиваем текст на пустые пробелы и сохраняем длину этого списка в нашем словаре textlengths:

    splittedText = texts[text].split(' ')
    # Saving the text length to show in the label of the line later
    textlengths[text] = len(splittedText)
Продолжая, мы создаем новый словарь в текстовом словаре для хранения вхождений для каждого слова. После этого начинаем цикл над словами текущего текста:

    # Here will be the amount of occurence of each word stored
    textwordamounts[text] = {}
    # Loop through all words in the text
    for i in splittedText:
Затем проверяем, есть ли уже текущее слово в словаре. Если это так, мы увеличиваем на единицу, а если нет, мы устанавливаем значение в единицу, начиная отсчитывать отсюда:

        # Add to the word at the given position if it already exists
        # Else set the amount to one essentially making a new item in the dict
        if i in textwordamounts[text].keys():
            textwordamounts[text][i] += 1
        else:
            textwordamounts[text][i] = 1
После этого мы сортируем словарь с помощью функции sorted(). Мы преобразуем диктант в список кортежей из двух элементов. Мы также можем определить пользовательский ключ, который мы должны установить для второго элемента предоставленных объектов. Это глоток. Мы делаем это с помощью лямбды. Мы получаем только ограниченное количество элементов обратно, указанное глубиной.

    # Sorting the dict by the values with sorted
    # define custom key so the function knows what to use when sorting
    textwordamounts[text] = dict(
        sorted(
            textwordamounts[text ].items(),
            key=lambda x: x[1],
            reverse=True)[0:depth]
        )
Вспомогательные функции
Теперь сделаем две вспомогательные функции. Начнем с функции percentify(). Это довольно просто. Он принимает значение и max, а также вычисляет процент.

# Get the percentage value of a given max value
def percentify(value, max):
    return round(value / max * 100)
Следующая функция используется для сглаживания кривых, генерируемых вхождениями слов. Мы не будем углубляться здесь, потому что это чисто косметическое средство, но вывод заключается в том, что мы используем массивы NumPy и make_interp_spline(), чтобы сгладить его. В конце концов, мы возвращаем новые оси x и y.

# Generate smooth curvess
def smoothify(yInput):
    x = np.array(range(0, depth))
    y = np.array(yInput)
    # define x as 600 equally spaced values between the min and max of original x
    x_smooth = np.linspace(x.min(), x.max(), 600) 
    # define spline with degree k=3, which determines the amount of wiggle
    spl = make_interp_spline(x, y, k=3)
    y_smooth = spl(x_smooth)
    # Return the x and y axis
    return x_smooth, y_smooth
Идеальная кривая Zipf
Таким образом, мы можем сравнить наши тексты с Zipf, теперь мы также делаем идеальную кривую Zipf. Мы делаем это с пониманием списка, который даст нам такие значения: [100, 50, 33, 25, 20, ...]. Затем мы используем функцию smoothify() с этим списком и сохраняем оси x и y, чтобы использовать ее в функции plot() pyplot. Мы также устанавливаем стиль линии на пунктирный, а цвет на серый:

# Make the perfect Curve
ziffianCurveValues = [100/i for i in range(1, depth+1)]
x, y = smoothify(ziffianCurveValues)
plt.plot(x, y, label='Ziffian Curve', ls=':', color='grey')
Отображение данных
Давайте наконец перейдем к отображению данных. Для этого мы зацикливаем словарь textwordamounts, и получаем значение первого элемента, которое будет самым распространенным словом для каждого текста.

# Plot the texts
for i in textwordamounts:
    maxValue = list(textwordamounts[i].values())[0]
Затем мы используем нашу функцию percentify() с каждым значением суммы dict. Теперь, конечно, для наиболее распространенного значения это вернет 100, потому что оно является наиболее распространенным, и оно проверяется по самому себе.

    yAxis = [percentify(value, maxValue) for value in list(textwordamounts[i].values())]
После этого мы используем эту вновь созданную ось Y и передаем ее нашей функции smoothify().

    x, y = smoothify(yAxis)
И последнее, но не менее важное: мы строим график данных, которые мы сделали, и даем им метку, которая показывает текстовое имя и количество слов. Задаем непрозрачность с помощью параметра alpha.

    plt.plot(x, y, label=i+f' [{textlengths[i]}]', lw=1, alpha=0.5)
Уборка
И после контура построения мы устанавливаем тики x, чтобы они выглядели правильно. Мы вызываем функцию legend(), поэтому отображаются все метки, и сохраняем график с высоким dpi на нашем диске. И в самом конце мы показываем сюжет, который мы только что сделали с show().

plt.xticks(range(0, depth), xAxis)

plt.legend()
plt.savefig('wordamounts.png', dpi=300)
plt.show()
Витрина
Витрина
Ниже вы видите витрину нашей небольшой программы. Как видите, мы сбрасываем много текстовых файлов в текстовые папки, а затем запускаем программу. Как видите. Учебник по генерации паролей и простой текстовый редактор с Tkinter довольно близки к идеальной кривой, в то время как Planet Simulation с PyGame еще далеко.

витрина

Заключение
Отлично! Вы успешно создали график с помощью кода Python! Посмотрите, как вы можете анализировать другие данные с этими знаниями!