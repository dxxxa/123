# [Data Cleaning with Pandas in Python](https://www.thepythoncode.com/article/data-cleaning-using-pandas-in-python)
##
# [[] / []]()
Очистка данных — это процесс подготовки набора данных для дальнейшего анализа. На этапе очистки данных мы стандартизируем данные в нашем наборе данных, удаляя любые значения, которые могут привести к ошибочным выводам.

Выводы, основанные на ошибочных данных, могут иметь дорогостоящие или катастрофические последствия, поэтому важно основывать наш анализ на чистых данных.

В этом уроке мы рассмотрим несколько методов очистки данных, чтобы мы могли провести анализ с нашим набором данных в наилучшем состоянии.

Содержание:

Создание набора данных
Код моделирования
Диагностика проблем
Визуальный осмотр
Другие средства диагностики
Очистка данных
Типы данных
Противоречивость
Вне диапазона и повторяющиеся значения
Отсутствующие значения
Заключение
Создание набора данных
Мы будем генерировать наши собственные грязные данные, чтобы гарантировать, что мы можем практиковать несколько методов очистки данных на одном наборе данных. Мы будем моделировать набор данных, который представляет данные, собранные о донорах по всей территории Соединенных Штатов для конкретной организации.

Была собрана информация для сбора имен, адресов и сумм пожертвований этих доноров. Мы будем моделировать грязные данные, случайным образом внося несоответствия в набор данных.

Код моделирования
Мы создадим наш код моделирования, создав набор вспомогательных функций. Создайте файл с именем helpers.py и импортируйте случайный модуль в helpers.py. После этого добавьте следующие функции:

import random

def add_donations(rows):
    total_donations = len(rows)
    donations = []
    # create list of random donation values 
    donations = list_of_donations(total_donations)
    # add donations onto main records
    count = 0
    while count < total_donations:
        rows[count].append(donations[count])
        count += 1

def create_row_base():
    first_name_options = ['Rosemaria', 'Jodi', 'Alvy', 'Blake', 'Ellis', '']
    last_name_options = ['Roderick', 'Hesbrook', 'Summerton', 'Rappport', 'Alben', '']
    city_options = ['Hialeah', 'Arlington', 'Springfield', 'Carrollton', 'Cambridge', '']
    state_options = ['CT', 'NY', 'VA', 'WA', 'AZ', '']
    first_name = random.choice(first_name_options)
    last_name = random.choice(last_name_options)
    street =  street_address()
    city = random.choice(city_options)
    state = random.choice(state_options)
    return [first_name, last_name, street, city, state]

def list_of_donations(size):
    donations = []
    donation_amt = random_dollar_amt()
    for i in range(size):
        # randomly change donation value
        if random.choice([1, 2, 3, 4, 5]) > 1:
            donation_amt = random_dollar_amt()
        donations.append(donation_amt)
    return donations

def random_dollar_amt():
    dollars = random.randint(-50, 200)
    cents = random.randint(0, 99)
    return '${}.{}'.format(dollars, cents)

def scramble_capitalization(str):
    final_str = ''
    for letter in str:
        final_str += random.choice([letter.upper(), letter.lower()])
    return final_str

def street_address():
    num = random.randint(40,1001)
    road_name = random.choice(['Western Plank', 'Forest Run', 'Kings', 'Oaktree'])
    road_type = random.choice(['Street', 'St', 'Road', 'Rd', ''])
    address = '{} {} {}'.format(num, road_name, road_type)   
    return address
Функция add_donations() принимает список строк данных в качестве аргумента. В нашем симуляторе список строк данных, которые будут переданы этой функции, — это базовые записи, которые имеют только first_name, last_name, street_address, город и штат.

Функция create_row_base() используется для создания значений, связанных с именем и адресом, для записей в нашем наборе данных.

Функция list_of_donations() используется для создания списка случайных значений пожертвований. Некоторые из этих значений будут повторяться. Эта функция будет вызываться внутри функции add_donations().

Функция random_dollar_amount() используется для генерации случайных значений доллара, включая некоторые отрицательные значения.

Функция scramble_capitalization() используется для того, чтобы сделать форматирование адресов улиц непоследовательным.

Наконец, функция street_address() используется для генерации уличных адресов. Обратите внимание, что для road_type можно выбрать пустую строку (''). Опция пустой строки есть, поэтому у нас будут данные с отсутствующими значениями.

Теперь, когда мы прошлись по всем функциям в модуле помощников, давайте поговорим о нашем основном скрипте симулятора. Создайте новый скрипт Python с именем simulator.py и импортируйте следующие модули:

import csv
import random
import helpers
Нам нужен модуль csv, потому что мы будем выводить сгенерированные данные в CSV-файл. Случайный модуль имеет несколько полезных инструментов для генерации случайных чисел, которые мы будем использовать, чтобы сделать наш набор данных непоследовательным.

Наконец, вспомогательный модуль дает нам доступ ко всем вспомогательным функциям, которые мы создали ранее.

После инструкций импорта добавьте следующий код для завершения работы нашего симулятора:

def generate_dataset():
    rows = []
    count = 0
    # generate list of base records: names data + address data
    while count < 20:
        row_to_add = helpers.create_row_base()
        rows.append(row_to_add)
        # randomly add duplicate records 
        if random.choice([1, 2, 3, 4, 5]) > 2:
            rows.append(row_to_add.copy())
            # scramble formatting of street address
            rows[-1][2] = helpers.scramble_capitalization(rows[-1][2])
        count += 1
    # add donation amounts to each record
    helpers.add_donations(rows)
    return rows

with open('simulated_data.csv', 'w') as f:
    f_csv = csv.writer(f)
    # write headers first
    f_csv.writerow(['first_name','last_name','street_address',
        'city','state', 'donation'])
    f_csv.writerows(generate_dataset())
Сценарий simulator.py, изображенный выше, создает набор данных со следующими заголовками:

first_name, last_name, street_address, город, штат, пожертвование

Набор данных содержит значения, иллюстрирующие различные типы проблем, которые необходимо устранить.

При запуске файла simulator.py .csv файл с именем simulated_data.csv будет создан в том же каталоге, что и simulator.py файл.

Мы будем использовать данные в файле simulated_data.csv для очистки данных.

Диагностика проблем
Прежде чем мы начнем процесс очистки данных, нам необходимо диагностировать проблемы в нашем наборе данных. Чтобы диагностировать проблемы, нам сначала нужно иметь контекст.

Наличие контекста означает, что нам нужно понять область данных, иметь в виду конкретный вариант использования набора данных и узнать как можно больше о том, как данные были собраны. Устанавливая контекст, мы можем развить ощущение того, где искать потенциальные проблемы.

Как упоминалось выше, мы знаем, что наш набор данных представляет информацию о донорах для конкретной организации, которая живет в различных местах по всей территории Соединенных Штатов.

Наша задача – найти информацию о количестве денег, пожертвованных донорами, проживающими в отдельных регионах США. Мы также знаем, что все значения в нашем наборе данных хранятся в виде строк.

Имея это в виду этот контекст, давайте создадим новый скрипт, в котором мы будем использовать панд для изучения нашего набора данных и начнем искать проблемы, которые могут потребовать очистки:

import pandas as pd

# Config settings
pd.set_option('max_columns', None)
pd.set_option('max_rows', 12)
# Import CSV data
data_frames = pd.read_csv (r'simulated_data.csv')
print(data_frames.head(10))
Мы используем функцию set_option() для изменения настроек по умолчанию для количества столбцов и строк, отображаемых при печати data_frames в консоль. Изменение этих настроек позволит нам видеть каждый столбец в нашем наборе данных и больше строк, чем в противном случае было бы отображено.

Затем мы импортируем наш файл данных в pandas. Затем мы распечатываем первые десять строк наших данных.

При выполнении этого сценария создаются следующие выходные данные:



Визуальный осмотр
При визуальном осмотре мы можем выявить несколько проблем. Во-первых, мы видим значение NaN несколько раз в наших данных. NaN - это то, как панды представляют ценности, которые отсутствуют.

Кроме того, мы можем видеть адреса улиц, которые являются непоследовательными. «864 Forest Run Street» и «864 forESt Run StREet» представляют один и тот же адрес, хотя их корпус отличается. Мы не хотим, чтобы они рассматривались как разные адреса, поэтому мы должны устранить это несоответствие.

Наконец, в колонке пожертвований мы видим отрицательные суммы в долларах. Отрицательная сумма в долларах не имеет смысла в контексте пожертвований. Эти значения находятся вне диапазона, поэтому мы должны определить, как их обрабатывать.

Визуальный осмотр данных помог нам диагностировать отсутствующие значения, противоречивые данные и значения вне диапазона. Однако нам не нужно полагаться только на визуальный осмотр. У панд есть и другие инструменты, которые мы можем использовать для диагностики этих и других проблем.

Другие средства диагностики
Что делать, если бы «грязные» значения данных отсутствовали в нашем визуальном образце? Существуют и другие способы диагностики проблем набора данных с помощью панд.

Например, чтобы определить, отсутствуют ли значения, можно выполнить следующий сценарий:

import pandas as pd

# Config settings
pd.set_option('max_columns', None)
pd.set_option('max_rows', 12)
# Import CSV data
data_frames = pd.read_csv (r'simulated_data.csv')
print(data_frames.info())
Вызов метода info() в нашем кадре данных и печать выходных данных этого вызова метода дает нам следующую таблицу:



В верхней части выходных данных мы видим следующие две строки:

RangeIndex: 29 записей, от 0 до 28
Столбцы данных (всего 6 столбцов):
Это означает, что наш набор данных содержит двадцать девять записей и шесть атрибутов. Под этой информацией мы видим таблицу, в которой перечислены общие записи, отличные от NULL, и тип данных для каждого из шести атрибутов.

Основываясь на этой таблице, мы видим, что атрибуты first_name, last_name, города и штата имеют отсутствующие значения. Кроме того, эта таблица также позволяет нам знать, что тип данных атрибута donation не является числовым.

Учитывая, что нам нужно будет выполнить математические расчеты по стоимости пожертвования, эта таблица помогла нам диагностировать проблему типа данных.

У панд есть еще один мощный инструмент, который поможет нам диагностировать дублирование записей. Тем не менее, нам нужно немного очистить данные, прежде чем применять их.

Давайте продолжим и начнем очищать некоторые из проблем, которые мы диагностировали в нашем наборе данных.

Очистка данных
Типы данных
Во-первых, мы рассмотрим проблему типа данных, которую мы только что обнаружили. В настоящее время ценности, связанные с пожертвованиями, имеют тип объекта. Pandas использует тип данных объекта для строк. Нам нужно преобразовать тип данных объекта в числовой тип данных.

Но сначала давайте еще раз взглянем на строки в колонке пожертвований. Обратите внимание, что эти строки начинаются с символа доллара ($):



Прежде чем пытаться преобразовать эти строки в числа, нам нужно устранить символ доллара. Мы можем удалить символ доллара из значений пожертвований, используя следующий код:

data_frames['donation'] = data_frames['donation'].str.strip('$')
Чтобы привести значения пожертвования из строки в плавающую точку, мы можем использовать следующий код:

data_frames['donation'] = data_frames['donation'].astype('float64')
Создайте еще один скрипт, который объединит все это вместе:

import pandas as pd

# Config settings
pd.set_option('max_columns', None)
pd.set_option('max_rows', 12)
# Import CSV data
data_frames = pd.read_csv (r'simulated_data.csv')
# Data Type Conversion
# Remove '$' from donation strings
data_frames['donation'] = data_frames['donation'].str.strip('$')
# Convert donation stings into numerical data type
data_frames['donation'] = data_frames['donation'].astype('float64')
print(data_frames.head(10))
print(data_frames.info())
При выполнении приведенного выше сценария будут получены следующие две таблицы:





Как видите, значения пожертвований представлены числовым типом данных. Теперь мы сможем выполнять вычисления по этим значениям.

Противоречивость
Теперь, когда мы рассмотрели проблемы типов данных, которые мы диагностировали, давайте обратимся к проблеме противоречивых данных. На этапе диагностики мы увидели несогласованность данных в атрибуте street_address:



Здесь есть три типа несоответствий. Во-первых, у нас непоследовательная капитализация. Далее, мы имеем дело с непоследовательным использованием аббревиатур. Например, в некоторых случаях мы видим «Улицу», в то время как в других мы видим «Св.».

И, наконец, у нас есть некоторые неполные уличные адреса, такие как «155 королей», как показано выше.

Чтобы устранить проблему с заглавными буквами, мы добавим следующий код в сценарий, который мы использовали для преобразования типа данных пожертвования:

import pandas as pd

# Config settings
pd.set_option('max_columns', None)
pd.set_option('max_rows', 12)
# Import CSV data
data_frames = pd.read_csv (r'simulated_data.csv')
# Data Type Conversion
# Remove '$' from donation strings
data_frames['donation'] = data_frames['donation'].str.strip('$')
# Convert donation stings into numerical data type
data_frames['donation'] = data_frames['donation'].astype('float64')
# Handle Data Inconsistencies
# Capitalize strings
data_frames['street_address'] = data_frames['street_address'].str.split()

def capitalize_words(arr):
    for index, word in enumerate(arr):
        if index == 0:
            pass
        else:
            arr[index] = word.capitalize()

data_frames['street_address'].apply(lambda x: capitalize_words(x))
data_frames['street_address'] = data_frames['street_address'].str.join(' ')
print(data_frames['street_address'])
В строке 20 мы используем:

data_frames['donation'].str.split()
Чтобы разбить street_address строку на список строк. Оттуда нам нужно будет применить функцию к каждой строке в street_address серии.

Для этого мы создадим функцию, которая будет использовать заглавные буквы в каждой строке в списке, кроме первой строки. Мы пропускаем первую строку, потому что эта строка представляет числовую часть street_address. Номер не требует капитализации.

Получив функцию, которую мы хотим применить к каждой строке ряда street_address, мы можем использовать следующий код для применения функции:

data_frames['street_address'].apply(lambda x: capitalize_words(x))
На этом этапе наш street_address ряд содержит список строк, в котором все строки (кроме первой строки) пишутся с заглавной буквы.

Нам нужно сделать последний шаг преобразования списка строк обратно в одну строку, причем каждое слово разделено пробелом (' '). Мы можем сделать это, используя следующую строку кода:

data_frames['street_address'].str.join(' ')
После того, как мы добавили все эти обновления в наш сценарий, мы можем запустить сценарий, чтобы создать следующую распечатку street_address серии:

Обратите внимание, что заглавные буквы для каждого слова в адресе были очищены и стандартизированы; только первая буква каждого слова пишется с заглавной буквы.

Теперь нам нужно решить вторую проблему несоответствия: непоследовательное использование аббревиатур. Давайте расширим код, который мы только что создали для заглавных букв. Здесь мы объединяем работу по капитализации каждого слова в строке с работой по расширению сокращенных типов дорог.

data_frames['street_address'] = data_frames['street_address'].str.split()

def normalize_words(arr):
    for index, word in enumerate(arr):
        if index == 0:
            pass
        else:
            arr[index] = normalize(word)

def normalize(word):
    if word.lower() == 'st':
        word = 'street'
    elif word.lower() == 'rd':
        word = 'road'
    return word.capitalize()

data_frames['street_address'].apply(lambda x: normalize_words(x))
data_frames['street_address'] = data_frames['street_address'].str.join(' ')
print(data_frames.head(10))
Когда мы запустим обновленный скрипт, изображенный выше, мы увидим следующее:



Наконец, мы должны решить, что делать с неполными адресами. Именно здесь мы должны снова полагаться на контекст, чтобы помочь нам принять решение. Мы должны определить, указывают ли эти ошибки на мусорные данные, которые мы не хотим включать в наш анализ.

Для наших целей в этой статье мы оставим записи с неполными адресами на этом этапе.

Неполный street_address недостаточно сигнала для мусорных данных, чтобы отбросить всю строку. На следующих шагах мы рассмотрим другие индикаторы, которые являются более сильными сигналами мусорных данных, которые необходимо отбросить.

Вне диапазона и повторяющиеся значения
Затем нам нужно посмотреть на выбросы в нашем наборе данных. Как упоминалось ранее, любые отрицательные значения пожертвований не имеют смысла в контексте нашей проблемной области. Если мы включим эти отрицательные значения в наши расчеты пожертвований, они ошибочно исказит наши итоги.

Это сильный сигнал для мусорных данных, поэтому мы просто отфильтруем любые записи с отрицательными значениями пожертвований.

Чтобы отфильтровать записи с отрицательными значениями пожертвований, мы можем добавить в наш скрипт следующий код:

# Remove Out-of-Range Data
# create boolean Series for out of range donations 
out_of_range = data_frames['donation'] < 0
# keep only the rows that are NOT out of range
data_frames['donation'] = data_frames['donation'][~out_of_range]
print(data_frames.head(10))
Создаем логический ряд и присваиваем его переменной out_of_range. Логическая серия основана на том, меньше ли значение в столбце пожертвования.

Затем мы используем эту логическую серию, чтобы отфильтровать отрицательные значения в нашей серии пожертвований. Мы сохраняем те значения, которые не находятся вне диапазона.

Как только мы запустим обновленный скрипт, мы сможем увидеть следующую таблицу:



Обратите внимание, что все отрицательные значения пожертвований были отфильтрованы. В таблице значение NaN указывает на то, что там больше нет значения.

Дубликаты записей также должны быть удалены из нашего набора данных. В нашем донорском сценарии маловероятно, что у него будет дублированное пожертвование от одного и того же человека, живущего по тому же адресу.

Как и отрицательные значения пожертвований, эти типы дубликатов являются сильными сигналами для мусорных данных. Они могут исказить результаты любых расчетов, которые мы проводим по атрибуту пожертвования. Нам также нужно будет их убрать.

Добавьте следующий код в наш сценарий, чтобы создать новый фрейм данных, в котором нет строк с одинаковым именем, фамилией, адресом улицы, городом и штатом. Этот код сохранит первое вхождение любой такой строки и удалит любые дубликаты.

# Remove duplicates
columns_to_check = ['first_name', 'last_name', 'street_address', 'city', 'state']
data_frames_no_dupes = data_frames.drop_duplicates(subset=columns_to_check, keep='first')
print(data_frames_no_dupes.info())
При запуске обновленного сценария будет создана следующая информационная таблица:



Обратите внимание, что общее количество записей в нашем data_frames_no_dupes фрейме данных уменьшилось.

Отсутствующие значения
Ранее в статье мы видели, что у нас есть несколько отсутствующих значений для разных атрибутов набора данных.

Эти отсутствующие значения изначально находились в атрибутах first_name, last_name, города и штата. Но мы ввели больше отсутствующих значений под атрибутом donation, отфильтровав отрицательные значения.

Мы намеренно сохранили этот шаг до конца, чтобы мы могли увидеть, что осталось в нашем наборе данных после прохождения всех других методов очистки. Некоторые отсутствующие значения терпимы, в то время как другие могут помешать нашему анализу набора данных.

На данный момент мы видим, что любые ряды с отсутствующим пожертвованием бесполезны для нас, поэтому мы их отбросим.

Кроме того, отсутствующая государственная ценность отбросит нашу попытку агрегировать информацию о пожертвованиях по регионам Соединенных Штатов. В этом случае мы также предпочтем отказаться от этих строк.

Чтобы удалить строки с отсутствующими значениями пожертвования или состояния, мы можем добавить в наш скрипт следующий код:

# Drop Missing Data
columns_to_check = ['state', 'donation']
data_frames_no_missing = data_frames_no_dupes.dropna(subset=columns_to_check)
print(data_frames_no_missing.head(20))
Этот код удалит все строки со значениями NaN в столбцах состояния или пожертвования. При выполнении этого обновленного сценария будет распечатана следующая таблица:



Наш набор данных теперь выглядит намного чище!

Теперь, когда мы закончили очистку наших данных, мы можем экспортировать чистый набор данных в новый файл .csv, добавив следующий код в наш скрипт:

data_frames_no_missing.to_csv(r'clean_donations_data.csv', index=False)
Этот чистый файл набора данных (clean_donations_data.csv) теперь можно использовать на последующих этапах конвейера анализа данных.

Заключение
В этой статье мы рассмотрели процесс очистки данных. Процесс начинается с диагностики различных способов, которыми наш набор данных может быть непоследовательным.

Оттуда у нас есть много методов для очистки данных. Важно иметь контекст в области нашей проблемы, чтобы знать, какой метод лучше всего подходит для проблем, которые мы видим в нашем наборе данных.

Очистка данных имеет решающее значение, потому что она может помочь нам избежать ошибочных выводов и действий на основе ошибочных предположений.