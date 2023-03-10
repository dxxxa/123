# [How to Extract Text from PDF in Python](https://www.thepythoncode.com/article/extract-text-from-pdf-in-python)
To run this:
- `pip3 install -r requirements.txt`
- `python extract_text_from_pdf.py --help`
##
# [[] / []]()
В настоящее время компании среднего и крупного бизнеса ежедневно используют большое количество PDF-документов. Среди них счета-фактуры, квитанции, документы, отчеты и многое другое.

В этом учебнике вы узнаете, как извлечь текст из PDF-документов на Python с помощью библиотеки PyMuPDF.

В этом учебнике рассматривается проблема, когда текст не сканируется, то есть не является изображением в PDF- файле. Если вы хотите извлечь текст из изображений в документах PDF, этот учебник для вас.

Чтобы начать работу, нам нужно установить PyMuPDF:

$ pip install PyMuPDF==1.18.9
Откройте новый файл Python и импортируем библиотеки:

import fitz
import argparse
import sys
import os
from pprint import pprint
PyMuPDF имеет имя fitz при импорте в Python, поэтому имейте это в виду.

Поскольку мы собираемся создать скрипт Python, который извлекает текст из PDF-документов, мы должны использовать модуль argparse для анализа переданных параметров в командной строке. Следующая функция анализирует аргументы и выполняет некоторую обработку:

def get_arguments():
    parser = argparse.ArgumentParser(
        description="A Python script to extract text from PDF documents.")
    parser.add_argument("file", help="Input PDF file")
    parser.add_argument("-p", "--pages", nargs="*", type=int,
                        help="The pages to extract, default is all")
    parser.add_argument("-o", "--output-file", default=sys.stdout,
                        help="Output file to write text. default is standard output")
    parser.add_argument("-b", "--by-page", action="store_true",
                        help="Whether to output text by page. If not specified, all text is joined and will be written together")
    # parse the arguments from the command-line
    args = parser.parse_args()

    input_file = args.file
    pages = args.pages
    by_page = args.by_page
    output_file = args.output_file
    # print the arguments, just for logging purposes
    pprint(vars(args))
    # load the pdf file
    pdf = fitz.open(input_file)
    if not pages:
        # if pages is not set, default is all pages of the input PDF document
        pages = list(range(pdf.pageCount))
    # we make our dictionary that maps each pdf page to its corresponding file
    # based on passed arguments
    if by_page:
        if output_file is not sys.stdout:
            # if by_page and output_file are set, open all those files
            file_name, ext = os.path.splitext(output_file)
            output_files = { pn: open(f"{file_name}-{pn}{ext}", "w") for pn in pages }
        else:
            # if output file is standard output, do not open
            output_files = { pn: output_file for pn in pages }
    else:
        if output_file is not sys.stdout:
            # a single file, open it
            output_file = open(output_file, "w")
            output_files = { pn: output_file for pn in pages }
        else:
            # if output file is standard output, do not open
            output_files = { pn: output_file for pn in pages }

    # return the parsed and processed arguments
    return {
        "pdf": pdf,
        "output_files": output_files,
        "pages": pages,
    }
Во-первых, мы сделали наш парсер с помощью ArgumentParserи добавили следующие параметры:

файл: входной PDF-документ для извлечения текста.
-p или --pages: Индексы страниц для извлечения, начиная с 0, если вы не укажете, по умолчанию будут все страницы.
-o или --output-file: выходной текстовый файл для записи извлеченного текста. Если вы не укажете, содержимое будет напечатано в стандартном выводе (т.е. в консоли).
-b или --by-page: это логическое значение, указывающее, следует ли выводить текст по страницам. Если этот параметр не указан, весь текст объединяется в один файл (при указании -o).
Во-вторых, мы открываем наш output_files для записи, если указан -b. В противном случае в словаре output_files будет один файл.

Наконец, мы возвращаем необходимые переменные: PDF-документ, выходные файлы и список номеров страниц.

Далее сделаем функцию, которая принимает вышеуказанные параметры и соответственно извлечем текст из PDF-документов:

def extract_text(**kwargs):
    # extract the arguments
    pdf          = kwargs.get("pdf")
    output_files = kwargs.get("output_files")
    pages        = kwargs.get("pages")
    # iterate over pages
    for pg in range(pdf.pageCount):
        if pg in pages:
            # get the page object
            page = pdf[pg]
            # extract the text of that page and split by new lines '\n'
            page_lines = page.get_text().splitlines()
            # get the output file
            file = output_files[pg]
            # get the number of lines
            n_lines = len(page_lines)
            for line in page_lines:
                # remove any whitespaces in the end & beginning of the line
                line = line.strip()
                # print the line to the file/stdout
                print(line, file=file)
            print(f"[*] Wrote {n_lines} lines in page {pg}")    
    # close the files
    for pn, f in output_files.items():
        if f is not sys.stdout:
            f.close()
Мы перебираем страницы; если страница, на которой мы находимся, находится в списке страниц, мы извлекаем текст этой страницы и записываем его в указанный файл или стандартный вывод. Наконец, мы закрываем файлы.

Давайте объединим все вместе и запустим функции:

if __name__ == "__main__":
    # get the arguments
    kwargs = get_arguments()
    # extract text from the pdf document
    extract_text(**kwargs)
Удивительно, давайте попробуем извлечь текст со всех страниц этого файла и записать каждую страницу в текстовый файл:

$ python extract_text_from_pdf.py bert-paper.pdf -o text.txt -b
Выпуск:

{'by_page': True,
 'file': 'bert-paper.pdf', 
 'output_file': 'text.txt',
 'pages': None}
[*] Wrote 97 lines in page 0
[*] Wrote 108 lines in page 1
[*] Wrote 136 lines in page 2
[*] Wrote 107 lines in page 3
[*] Wrote 133 lines in page 4
[*] Wrote 158 lines in page 5
[*] Wrote 163 lines in page 6
[*] Wrote 128 lines in page 7
[*] Wrote 158 lines in page 8
[*] Wrote 116 lines in page 9
[*] Wrote 124 lines in page 10
[*] Wrote 115 lines in page 11
[*] Wrote 135 lines in page 12
[*] Wrote 111 lines in page 13
[*] Wrote 153 lines in page 14
[*] Wrote 127 lines in page 15
Это сработало отлично. Вот выходные файлы:

Выходные файлыТеперь укажем страницы 0, 1, 2, 14 и 15:

$ python extract_text_from_pdf.py bert-paper.pdf -o text.txt -b -p 0 1 2 14 15   
{'by_page': True,
 'file': 'bert-paper.pdf',
 'output_file': 'text.txt',
 'pages': [0, 1, 2, 14, 15]}
[*] Wrote 97 lines in page 0
[*] Wrote 108 lines in page 1
[*] Wrote 136 lines in page 2
[*] Wrote 153 lines in page 14
[*] Wrote 127 lines in page 15
Мы также можем печатать в консоли вместо того, чтобы сохранять его в файл, не устанавливая опцию -o:

$ python extract_text_from_pdf.py bert-paper.pdf -p 0
{'by_page': False,
 'file': 'bert-paper.pdf',
 'output_file': <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>,
 'pages': [0]}
BERT: Pre-training of Deep Bidirectional Transformers for
Language Understanding
Jacob Devlin
Ming-Wei Chang
Kenton Lee
Kristina Toutanova
Google AI Language
{jacobdevlin,mingweichang,kentonl,kristout}@google.com
Abstract
We introduce a new language representa-
tion model called BERT, which stands for
Bidirectional Encoder Representations from
...
<SNIPPED>
[*] Wrote 97 lines in page 0
Или сохранение всего текста PDF-документа в один текстовый файл:

$ python extract_text_from_pdf.py bert-paper.pdf -o all-text.txt
Выходной файл появится в текущем каталоге:

Выходной файл SingeЗаключение
Хорошо, вот и все для этого урока. Как упоминалось ранее, вы всегда можете извлечь текст из отсканированных PDF-документов учебника, если ваши документы отсканированы (т. Е. Как изображения и не могут быть выбраны в вашем PDF-ридере).

Кроме того, вы можете отредактировать и выделить текст в вашем PDF-файле. Ниже приведены некоторые другие связанные с PDF-учебниками:

Как извлечь таблицы из PDF на Python
Как зашифровать и расшифровать PDF-файлы на Python
Как подписывать PDF-файлы на Python
Как разделить PDF-файлы в Python
Как извлечь все ссылки PDF на Python
Или вы можете исследовать их все здесь.

Проверьте полный код здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!