# [How to Extract PDF Metadata in Python](https://www.thepythoncode.com/article/extract-pdf-metadata-in-python)
##
# [[] / []]()
Метаданные в PDF-файлах — это полезная информация о PDF-документе, она включает в себя название документа, автора, дату последнего изменения, дату создания, тему и многое другое. Некоторые PDF-файлы получили больше информации, чем другие, и в этом уроке вы узнаете, как извлекать метаданные PDF на Python.

В Python есть много библиотек и утилит для достижения того же, но мне нравится использовать pikepdf, так как это активная и поддерживаемая библиотека. Давайте установим его:

$ pip install pikepdf
Pikepdf — это pythonic-оболочка вокруг библиотеки C++ QPDF. Давайте импортируем его в наш скрипт:

import pikepdf
import sys
Мы также будем использовать модуль sys для получения имени файла из аргументов командной строки:

# get the target pdf file from the command-line arguments
pdf_filename = sys.argv[1]
Загрузим PDF-файл с помощью библиотеки и получим метаданные:

# read the pdf file
pdf = pikepdf.Pdf.open(pdf_filename)
docinfo = pdf.docinfo
for key, value in docinfo.items():
    print(key, ":", value)
Атрибут docinfo содержит словарь метаданных документа. Вот пример выполнения:

$ python extract_pdf_metadata_simple.py bert-paper.pdf
Выпуск:

/Author : 
/CreationDate : D:20190528000751Z
/Creator : LaTeX with hyperref package
/Keywords :
/ModDate : D:20190528000751Z
/PTEX.Fullbanner : This is pdfTeX, Version 3.14159265-2.6-1.40.17 (TeX Live 2016) kpathsea version 6.2.2
/Producer : pdfTeX-1.40.17
/Subject :
/Title :
/Trapped : /False
Связанные с: Как разделить PDF-файлы в Python.

Вот еще один PDF-файл:

$ python extract_pdf_metadata_simple.py python_cheat_sheet.pdf
Выпуск:

/CreationDate : D:20201002181301Z
/Creator : wkhtmltopdf 0.12.5
/Producer : Qt 4.8.7
/Title : Markdown To PDF
Как видите, не все документы имеют одинаковые поля, некоторые содержат гораздо меньше информации.

Обратите внимание, что /ModDate и /CreationDate являются датой последнего изменения и датой создания соответственно в формате даты и времени PDF. Если вы хотите преобразовать этот формат в формат даты и времени Python, то я скопировал этот код из StackOverflow и немного отредактировал его для запуска на Python 3:

import pikepdf
import datetime
import re
from dateutil.tz import tzutc, tzoffset
import sys

pdf_date_pattern = re.compile(''.join([
    r"(D:)?",
    r"(?P<year>\d\d\d\d)",
    r"(?P<month>\d\d)",
    r"(?P<day>\d\d)",
    r"(?P<hour>\d\d)",
    r"(?P<minute>\d\d)",
    r"(?P<second>\d\d)",
    r"(?P<tz_offset>[+-zZ])?",
    r"(?P<tz_hour>\d\d)?",
    r"'?(?P<tz_minute>\d\d)?'?"]))

def transform_date(date_str):
    """
    Convert a pdf date such as "D:20120321183444+07'00'" into a usable datetime
    http://www.verypdf.com/pdfinfoeditor/pdf-date-format.htm
    (D:YYYYMMDDHHmmSSOHH'mm')
    :param date_str: pdf date string
    :return: datetime object
    """
    global pdf_date_pattern
    match = re.match(pdf_date_pattern, date_str)
    if match:
        date_info = match.groupdict()

        for k, v in date_info.items():  # transform values
            if v is None:
                pass
            elif k == 'tz_offset':
                date_info[k] = v.lower()  # so we can treat Z as z
            else:
                date_info[k] = int(v)

        if date_info['tz_offset'] in ('z', None):  # UTC
            date_info['tzinfo'] = tzutc()
        else:
            multiplier = 1 if date_info['tz_offset'] == '+' else -1
            date_info['tzinfo'] = tzoffset(None, multiplier*(3600 * date_info['tz_hour'] + 60 * date_info['tz_minute']))

        for k in ('tz_offset', 'tz_hour', 'tz_minute'):  # no longer needed
            del date_info[k]

        return datetime.datetime(**date_info)

# get the target pdf file from the command-line arguments
pdf_filename = sys.argv[1]
# read the pdf file
pdf = pikepdf.Pdf.open(pdf_filename)
docinfo = pdf.docinfo
for key, value in docinfo.items():
    if str(value).startswith("D:"):
        # pdf datetime format, convert to python datetime
        value = transform_date(str(pdf.docinfo["/CreationDate"]))
    print(key, ":", value)
Вот тот же вывод ранее, но с форматами даты и времени, преобразованными в объекты даты и времени Python:

/Author : 
/CreationDate : 2019-05-28 00:07:51+00:00
/Creator : LaTeX with hyperref package
/Keywords :
/ModDate : 2019-05-28 00:07:51+00:00
/PTEX.Fullbanner : This is pdfTeX, Version 3.14159265-2.6-1.40.17 (TeX Live 2016) kpathsea version 6.2.2
/Producer : pdfTeX-1.40.17
/Subject :
/Title :
/Trapped : /False
Гораздо лучше. Я надеюсь, что этот быстрый учебник помог вам получить метаданные PDF-документов с помощью Python.

Проверьте полный код здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!