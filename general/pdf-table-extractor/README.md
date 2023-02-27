# [How to Extract PDF Tables in Python](https://www.thepythoncode.com/article/extract-pdf-tables-in-python-camelot)
To run this:
- You need to install required dependencies for the camelot library [here](https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps).
- `pip3 install -r requirements.txt`.
- `pdf_table_extractor_camelot.py` is using camelot library.
- `pdf_table_extractor_tabula.py` is using tabula-py library.
##
# [[] / []]()
Вы хотите экспортировать таблицы из PDF-файлов с помощью языка программирования Python? Вы находитесь в нужном месте.

Camelot - это библиотека Python и инструмент командной строки, который позволяет любому легко извлекать таблицы данных, захваченные внутри PDF-файлов. Проверьте их официальную документацию и репозиторий GitHub.

В то время как Tabula-py является простой оболочкой Python tabula-java, которая может читать таблицы в PDF. Он позволяет конвертировать PDF-файл в CSV, TSV, JSON или даже pandas DataFrame.

В дополнение к извлечению таблиц из PDF-файлов, вам также может быть интересно узнать, как шифровать и расшифровывать PDF-файлы на Python. Или, возможно, вам нужно объединить PDF-файлы в Python. Еще одной полезной задачей является извлечение всех ссылок из PDF-файла на Python. И если вам нужно преобразовать ваши PDF-файлы в другой формат, вы можете использовать Python для преобразования PDF в Docx. Вы можете проверить все учебники PDF здесь.

В этом уроке вы узнаете, как извлекать таблицы в PDF, используя библиотеки camelot и tabula-py на Python.

Связанные с: Как извлечь изображения из PDF на Python.

Во-первых, вам нужно установить необходимые зависимости для правильной работы библиотеки camelot, а затем вы можете установить библиотеки с помощью командной строки:

pip3 install camelot-py[cv] tabula-py
Обратите внимание, что вам нужно убедиться, что на вашем компьютере правильно установлены Tkinter и ghostscript (которые являются обязательными зависимостями для camelot).

Извлечение таблиц PDF с помощью Камелота
Теперь, когда вы установили все требования для этого учебника, откройте новый файл Python и следуйте инструкциям:

import camelot

# PDF file to extract tables from
file = "foo.pdf"
У меня есть PDF-файл в текущем каталоге под названием «foo.pdf» (получить его здесь), который представляет собой обычную страницу PDF, содержащую одну таблицу, показанную на следующем рисунке:

Таблица в PDF для извлечения на Python

Просто случайная таблица. Давайте извлечем его в Python:

# extract all the tables in the PDF file
tables = camelot.read_pdf(file)
функция read_pdf() извлекает все таблицы в PDF-файле. Напечатаем количество извлеченных таблиц:

# number of tables extracted
print("Total tables extracted:", tables.n)
Это приводит к следующему:

Total tables extracted: 1 
Конечно, он содержит только одну таблицу, печатающую эту таблицу как Pandas DataFrame:

# print the first table as Pandas DataFrame
print(tables[0].df)
Выпуск:

              0            1                2                     3                  4                  5                 6
0  Cycle \nName  KI \n(1/km)  Distance \n(mi)  Percent Fuel Savings
1                                                  Improved \nSpeed  Decreased \nAccel  Eliminate \nStops  Decreased \nIdle
2        2012_2         3.30              1.3                  5.9%               9.5%              29.2%             17.4%
3        2145_1         0.68             11.2                  2.4%               0.1%               9.5%              2.7%
4        4234_1         0.59             58.7                  8.5%               1.3%               8.5%              3.3%
5        2032_2         0.17             57.8                 21.7%               0.3%               2.7%              1.2%
6        4171_1         0.07            173.9                 58.1%               1.6%               2.1%              0.5%
Это точно. Давайте экспортируем таблицу в CSV-файл:

# export individually as CSV
tables[0].to_csv("foo.csv")
CSV — не единственный вариант; Вы также можете использовать методы to_excel(), to_html(), to_json() и to_sqlite(), вот пример экспорта в электронную таблицу Excel:

# export individually as Excel (.xlsx extension)
tables[0].to_excel("foo.xlsx")
Или если вы хотите экспортировать все таблицы за один раз:

# or export all in a zip
tables.export("foo.csv", f="csv", compress=True)
Параметр f указывает формат файла, в данном случае "csv". Установив для параметра сжатия значение True, вы создадите ZIP-файл, содержащий все таблицы в формате CSV.

Вы также можете экспортировать таблицы в формат HTML:

# export to HTML
tables.export("foo.html", f="html")
или вы можете экспортировать в другие форматы, такие как JSON и Excel.

Стоит отметить, что Camelot работает только с текстовыми PDF-файлами, а не со отсканированными документами. Если вы можете щелкнуть и перетащить, чтобы выделить текст в таблице в средстве просмотра PDF, то это текстовый PDF, поэтому он будет работать с документами, книгами, документами и многим другим!

Читайте также: Как разделить PDF-файлы на Python.

Извлечение таблиц PDF с помощью Tabula-py
Откройте новый файл Python и импортируйте tabula:

import tabula
import os
Мы просто используем метод read_pdf() для извлечения таблиц в PDF-файлах (опять же, получите пример PDF здесь):

# read PDF file
tables = tabula.read_pdf("1710.05006.pdf", pages="all")
Мы устанавливаем для страниц значение "all" для извлечения таблиц на всех страницах PDF, метод tabula.read_pdf() возвращает список панд DataFrames, каждый DataFrame соответствует таблице. Вы также можете передать URL-адрес этому методу, и он автоматически загрузит PDF-файл перед извлечением таблиц.

Приведенный ниже код является примером итерации по всем извлеченным таблицам и сохранения их в виде электронных таблиц Excel:

# save them in a folder
folder_name = "tables"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)
# iterate over extracted tables and export as excel individually
for i, table in enumerate(tables, start=1):
    table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)
Это создаст папку таблиц и поместит все обнаруженные таблицы в формате Excel в эту папку, попробуйте.

Теперь, что делать, если вы хотите извлечь все таблицы из PDF-файла и сбросить их в один CSV-файл? Приведенный ниже код делает именно это:

# convert all tables of a PDF file into a single CSV file
# supported output_formats are "csv", "json" or "tsv"
tabula.convert_into("1710.05006.pdf", "output.csv", output_format="csv", pages="all")
Если у вас есть несколько PDF-файлов и вы хотите запустить вышеуказанные файлы для всех из них, вы можете использовать метод convert_into_by_batch():

# convert all PDFs in a folder into CSV format
# `pdfs` folder should exist in the current directory
tabula.convert_into_by_batch("pdfs", output_format="csv", pages="all")
Это заглянет в папку pdfs и выведет CSV-файл для каждого PDF-файла в этой папке.

Заключение
Для больших файлов библиотека камелотов имеет тенденцию превосходить tabula-py. Однако втех случаях, когда вы столкнетесь с NotImplementedError для некоторых PDF-файлов, использующих библиотеку камелотов, вы можете использовать tabula-py в качестве альтернативы.

Обратите внимание, что это не преобразует символы изображения в цифровой текст. Если вы этого хотите, вы можете использовать методы OCR для преобразования оптических символов изображения в фактический текст, которым можно манипулировать в Python. Следующие учебники могут помочь вам:

Оптическое распознавание символов (OCR) в Python
Как извлечь текст из изображений в PDF-файлах с помощью Python
Ниже приведены некоторые связанные с PDF-учебниками, которые могут помочь вам в вашей работе:

Как выделить и отредактировать текст в PDF-файлах с помощью Python
Как извлечь изображения из PDF на Python
Как конвертировать PDF в изображения на Python