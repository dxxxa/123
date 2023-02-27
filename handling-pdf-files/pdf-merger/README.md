# [How to Merge PDF Files in Python](https://www.thepythoncode.com/article/merge-pdf-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
-
    ```
    $ python pdf_merger.py --help
    ```
    **Output:**
    ```
    usage: pdf_merger.py [-h] -i [INPUT_FILES [INPUT_FILES ...]] [-p [PAGE_RANGE [PAGE_RANGE ...]]] -o OUTPUT_FILE [-b BOOKMARK]

    Available Options

    optional arguments:
    -h, --help            show this help message and exit
    -i [INPUT_FILES [INPUT_FILES ...]], --input_files [INPUT_FILES [INPUT_FILES ...]]
                            Enter the path of the files to process
    -p [PAGE_RANGE [PAGE_RANGE ...]], --page_range [PAGE_RANGE [PAGE_RANGE ...]]
                            Enter the pages to consider e.g.: (0,2) -> First 2 pages
    -o OUTPUT_FILE, --output_file OUTPUT_FILE
                            Enter a valid output file
    -b BOOKMARK, --bookmark BOOKMARK
                            Bookmark resulting file
    ```
- To merge `bert-paper.pdf` with `letter.pdf` into a new `combined.pdf`:
    ```
    $ python pdf_merger.py -i bert-paper.pdf,letter.pdf -o combined.pdf
    ```
##
# [[] / []]()
Основной целью объединения PDF-файлов является правильное управление файлами, архивирование, массовая печать или объединение таблиц, электронных книг и отчетов. Вам определенно нужен эффективный инструмент для объединения небольших PDF-файлов в один PDF-файл.

Из этого туториала Вы узнаете, как объединить список PDF-файлов в один PDF-файл с помощью языка программирования Python. Объединенный PDF-файл может включать закладки для улучшения навигации, где каждая закладка связана с содержимым одного из введенных PDF-файлов.

Для этой цели мы будем использовать библиотеку PyPDF4. PyPDF4 - это библиотека PDF с чистым python, способная разделять, объединять, обрезать и преобразовывать страницы PDF-файлов. Он также может добавлять пользовательские данные, параметры просмотра и пароли к ФАЙЛАМ PDF. Он может извлекать текст и метаданные из PDF-файлов, а также объединять целые файлы вместе.

Давайте установим его:

$ pip install PyPDF4==1.27.0
Импорт библиотек:

#Import Libraries
from PyPDF4 import PdfFileMerger
import os,argparse
Определим нашу основную функцию:

def merge_pdfs(input_files: list, page_range: tuple, output_file: str, bookmark: bool = True):
    """
    Merge a list of PDF files and save the combined result into the `output_file`.
    `page_range` to select a range of pages (behaving like Python's range() function) from the input files
        e.g (0,2) -> First 2 pages 
        e.g (0,6,2) -> pages 1,3,5
    bookmark -> add bookmarks to the output file to navigate directly to the input file section within the output file.
    """
    # strict = False -> To ignore PdfReadError - Illegal Character error
    merger = PdfFileMerger(strict=False)
    for input_file in input_files:
        bookmark_name = os.path.splitext(os.path.basename(input_file))[0] if bookmark else None
        # pages To control which pages are appended from a particular file.
        merger.append(fileobj=open(input_file, 'rb'), pages=page_range, import_bookmarks=False, bookmark=bookmark_name)
    # Insert the pdf at specific page
    merger.write(fileobj=open(output_file, 'wb'))
    merger.close()
Поэтому мы сначала создаем объект PDFFileMerger, а затем перебираем input_files из входных данных. После этого для каждого входного PDF-файла мы определяем закладку, если это необходимо, в зависимости от переменной bookmark и добавляем ее в объект слияния с учетом выбранного page_range.

Затем мы используем метод append() из слияния, чтобы добавить наш PDF-файл.

Наконец, мы записываем выходной PDF-файл и закрываем объект.

Теперь добавим функцию для синтаксического анализа аргументов командной строки:

def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-i', '--input_files', dest='input_files', nargs='*',
                        type=str, required=True, help="Enter the path of the files to process")
    parser.add_argument('-p', '--page_range', dest='page_range', nargs='*',
                        help="Enter the pages to consider e.g.: (0,2) -> First 2 pages")
    parser.add_argument('-o', '--output_file', dest='output_file',
                        required=True, type=str, help="Enter a valid output file")
    parser.add_argument('-b', '--bookmark', dest='bookmark', default=True, type=lambda x: (
        str(x).lower() in ['true', '1', 'yes']), help="Bookmark resulting file")
    # To Porse The Command Line Arguments
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args
Теперь воспользуемся ранее определенными функциями в нашем основном коде:

if __name__ == "__main__":
    # Parsing command line arguments entered by user
    args = parse_args()
    page_range = None
    if args['page_range']:
        page_range = tuple(int(x) for x in args['page_range'][0].split(','))
    # call the main function
    merge_pdfs(
        input_files=args['input_files'], page_range=page_range, 
        output_file=args['output_file'], bookmark=args['bookmark']
    )
Хорошо, мы закончили с кодированием, давайте протестируем его:

$ python pdf_merger.py --help
Выпуск:

usage: pdf_merger.py [-h] -i [INPUT_FILES [INPUT_FILES ...]] [-p [PAGE_RANGE [PAGE_RANGE ...]]] -o OUTPUT_FILE [-b BOOKMARK]

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT_FILES [INPUT_FILES ...]], --input_files [INPUT_FILES [INPUT_FILES ...]]
                        Enter the path of the files to process
  -p [PAGE_RANGE [PAGE_RANGE ...]], --page_range [PAGE_RANGE [PAGE_RANGE ...]]
                        Enter the pages to consider e.g.: (0,2) -> First 2 pages
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Enter a valid output file
  -b BOOKMARK, --bookmark BOOKMARK
                        Bookmark resulting file
Вот пример объединения двух PDF-файлов в один:

$ python pdf_merger.py -i bert-paper.pdf letter.pdf -o combined.pdf
Необходимо разделять входные PDF-файлы запятой (,) в аргументе -i, и не следует добавлять пробел.

В текущем каталоге, содержащем оба входных PDF-файла, появился новый комбинированный.pdf вывод:

## Command Arguments #################################################
input_files:['bert-paper.pdf', 'letter.pdf']
page_range:None
output_file:combined.pdf
bookmark:True
######################################################################
Убедитесь, что при передаче аргумента -i используется правильный порядок входных файлов.

Заключение
Я надеюсь, что этот код помог вам легко объединить PDF-файлы и без 3-х сторонних или онлайн-инструментов, использование Python для выполнения таких задач более удобно.

Если вы хотите разделить PDF-документы вместо этого, этот учебник, безусловно, поможет вам.

Проверьте полный код здесь.

Вот некоторые связанные учебники по Python:

Как выделить и отредактировать текст в PDF-файлах с помощью Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы из PDF на Python.
Как зашифровать и расшифровать PDF-файлы на Python
Как конвертировать PDF в Docx в Python.
Как сжимать PDF-файлы на Python.