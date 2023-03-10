# [Highlighting Text in PDF with Python](https://www.thepythoncode.com/article/redact-and-highlight-text-in-pdf-with-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```python pdf_highlighter.py --help```
    **Output:**
    ```
    usage: pdf_highlighter.py [-h] -i INPUT_PATH [-a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}] [-p PAGES]

    Available Options

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT_PATH, --input_path INPUT_PATH
                            Enter the path of the file or the folder to process
    -a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}, --action {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}
                            Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Strikeout or to Remove
    -p PAGES, --pages PAGES
                            Enter the pages to consider e.g.: [2,4]
    ```
##
# [[] / []]()
Выделение или аннотирование текста в PDF-файле является отличной стратегией для чтения и сохранения ключевой информации. Этот метод может помочь в немедленном доведении важной информации до сведения читателя. Нет никаких сомнений в том, что текст, выделенный желтым цветом, вероятно, привлечет ваше внимание первым.

Редактирование PDF-файла позволяет скрыть конфиденциальную информацию, сохранив при этом форматирование документа. Это сохраняет частную и конфиденциальную информацию перед обменом. Кроме того, это еще больше повышает целостность организации и доверие к обработке конфиденциальной информации.

Из этого туториала Вы узнаете, как редактировать, обрамлять или выделять текст в PDF-файлах с помощью Python.

Блок-схема процесса для учебника

В этом руководстве мы будем использовать библиотеку PyMuPDF, которая является очень универсальным, настраиваемым решением для интерпретатора PDF, XPS и электронных книг, которое можно использовать в широком спектре приложений в качестве рендерера PDF, средства просмотра или инструментария.

Целью этого учебника является разработка упрощенной утилиты на основе командной строки для редактирования, фрейма или выделения текста, включенного в один PDF-файл или в папку, содержащую коллекцию PDF-файлов. Кроме того, это позволит вам удалить основные моменты из PDF-файла или коллекции PDF-файлов.

Давайте установим требования:

$ pip install PyMuPDF==1.18.9
Откройте новый файл Python, и давайте начнем:

# Import Libraries
from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz


def extract_info(input_file: str):
    """
    Extracts file info
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    output = {
        "File": input_file, "Encrypted": ("True" if pdfDoc.isEncrypted else "False")
    }
    # If PDF is encrypted the file metadata cannot be extracted
    if not pdfDoc.isEncrypted:
        for key, value in pdfDoc.metadata.items():
            output[key] = value
    # To Display File Info
    print("## File Information ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in output.items()))
    print("######################################################################")
    return True, output
extract_info() собирает метаданные PDF-файла, атрибуты, которые могут быть извлечены: формат, заголовок, автор, тема, ключевые слова, создатель, производитель, дата создания, дата изменения, треппинг, шифрование и количество страниц. Стоит отметить, что эти атрибуты не могут быть извлечены при нацеливании на зашифрованный PDF-файл.

def search_for_text(lines, search_str):
    """
    Search for the search string within the document lines
    """
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result
Эта функция выполняет поиск строки в строках документа с помощью функции re.findall(), re. IGNORECASE - это игнорирование случая во время поиска.

def redact_matching_data(page, matched_values):
    """
    Redacts matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # Redact matching values
        [page.addRedactAnnot(area, text=" ", fill=(0, 0, 0))
         for area in matching_val_area]
    # Apply the redaction
    page.apply_redactions()
    return matches_found
Эта функция выполняет следующие функции:

Зацикливайтесь на совпадающих значениях строки поиска, которую мы ищем.
Отредактируйте совпадающие значения.
Применение редактирования к выбранной странице.
Вы можете изменить цвет редактирования с помощью аргумента заполнения в методе page.addRedactAnnot(), установив для него значение (0, 0, 0), это приведет к черному редактированию. Это значения RGB в диапазоне от 0 до 1. Например, (1, 0, 0) приведет к красному редактированию и так далее.

def frame_matching_data(page, matched_values):
    """
    frames matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        for area in matching_val_area:
            if isinstance(area, fitz.fitz.Rect):
                # Draw a rectangle around matched values
                annot = page.addRectAnnot(area)
                # , fill = fitz.utils.getColor('black')
                annot.setColors(stroke=fitz.utils.getColor('red'))
                # If you want to remove matched data
                #page.addFreetextAnnot(area, ' ')
                annot.update()
    return matches_found
Функция frame_matching_data() рисует красный прямоугольник (рамку) вокруг совпадающих значений.

Далее определим функцию для выделения текста:

def highlight_matching_data(page, matched_values, type):
    """
    Highlight matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        # print("matching_val_area",matching_val_area)
        highlight = None
        if type == 'Highlight':
            highlight = page.addHighlightAnnot(matching_val_area)
        elif type == 'Squiggly':
            highlight = page.addSquigglyAnnot(matching_val_area)
        elif type == 'Underline':
            highlight = page.addUnderlineAnnot(matching_val_area)
        elif type == 'Strikeout':
            highlight = page.addStrikeoutAnnot(matching_val_area)
        else:
            highlight = page.addHighlightAnnot(matching_val_area)
        # To change the highlight colar
        # highlight.setColors({"stroke":(0,0,1),"fill":(0.75,0.8,0.95) })
        # highlight.setColors(stroke = fitz.utils.getColor('white'), fill = fitz.utils.getColor('red'))
        # highlight.setColors(colors= fitz.utils.getColor('red'))
        highlight.update()
    return matches_found
Приведенная выше функция применяет адекватный режим подсветки к совпадающим значениям в зависимости от типа подсветки, введенной в качестве параметра.

Цвет выделения всегда можно изменить с помощью метода highlight.setColors(), как показано в комментариях.

def process_data(input_file: str, output_file: str, search_str: str, pages: Tuple = None, action: str = 'Highlight'):
    """
    Process the pages of the PDF File
    """
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0
    # Iterate through pages
    for pg in range(pdfDoc.pageCount):
        # If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        # Select the page
        page = pdfDoc[pg]
        # Get Matching Data
        # Split page by lines
        page_lines = page.getText("text").split('\n')
        matched_values = search_for_text(page_lines, search_str)
        if matched_values:
            if action == 'Redact':
                matches_found = redact_matching_data(page, matched_values)
            elif action == 'Frame':
                matches_found = frame_matching_data(page, matched_values)
            elif action in ('Highlight', 'Squiggly', 'Underline', 'Strikeout'):
                matches_found = highlight_matching_data(
                    page, matched_values, action)
            else:
                matches_found = highlight_matching_data(
                    page, matched_values, 'Highlight')
            total_matches += matches_found
    print(f"{total_matches} Match(es) Found of Search String {search_str} In Input File: {input_file}")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())
Связанные с: Как извлечь текст из PDF в Python

Основное назначение функции process_data() заключается в следующем:

Откройте входной файл.
Создайте буфер памяти для временного хранения выходного файла.
Инициализируйте переменную для хранения общего количества совпадений строки, которую мы искали.
Выполните итерацию по выбранным страницам входного файла и разделите текущую страницу на строки.
Найдите строку на странице.
Примените соответствующее действие (например, «Отредактировать», «Кадр», «Выделить» и т. Д.)
Отображение сообщения о состоянии процесса поиска.
Сохраните и закройте входной файл.
Сохраните буфер памяти в выходной файл.
Он принимает несколько параметров:

input_file: путь к обрабатываемому PDF-файлу.
output_file: путь к PDF-файлу, создаваемому после обработки.
search_str: строка для поиска.
pages: страницы, которые следует учитывать при обработке PDF-файла.
действие: действие, выполняемое с PDF-файлом.
Далее давайте напишем функцию для удаления выделения в случае, если мы хотим:

def remove_highlght(input_file: str, output_file: str, pages: Tuple = None):
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    # Initialize a counter for annotations
    annot_found = 0
    # Iterate through pages
    for pg in range(pdfDoc.pageCount):
        # If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        # Select the page
        page = pdfDoc[pg]
        annot = page.firstAnnot
        while annot:
            annot_found += 1
            page.deleteAnnot(annot)
            annot = annot.next
    if annot_found >= 0:
        print(f"Annotation(s) Found In The Input File: {input_file}")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())
Функция remove_highlight() предназначена для удаления выделений (а не редактирований) из PDF-файла. Он выполняет следующие действия:

Откройте входной файл.
Создайте буфер памяти для временного хранения выходного файла.
Выполните итерацию по страницам входного файла и проверьте, найдены ли аннотации.
Удалите эти заметки.
Отображение сообщения о состоянии этого процесса.
Закройте входной файл.
Сохраните буфер памяти в выходной файл.
Теперь сделаем функцию-оболочку, которая использует предыдущие функции для вызова соответствующей функции в зависимости от действия:

def process_file(**kwargs):
    """
    To process one single file
    Redact, Frame, Highlight... one PDF File
    Remove Highlights from a single PDF File
    """
    input_file = kwargs.get('input_file')
    output_file = kwargs.get('output_file')
    if output_file is None:
        output_file = input_file
    search_str = kwargs.get('search_str')
    pages = kwargs.get('pages')
    # Redact, Frame, Highlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    if action == "Remove":
        # Remove the Highlights except Redactions
        remove_highlght(input_file=input_file,
                        output_file=output_file, pages=pages)
    else:
        process_data(input_file=input_file, output_file=output_file,
                     search_str=search_str, pages=pages, action=action)
Действие может быть «Отредактировать», «Кадр», «Выделить», «Волнистый», «Подчеркнуть», «Зачеркнуть» и «Удалить».

Давайте определим ту же функцию, но с папками, содержащими несколько PDF-файлов:

def process_folder(**kwargs):
    """
    Redact, Frame, Highlight... all PDF Files within a specified path
    Remove Highlights from all PDF Files within a specified path
    """
    input_folder = kwargs.get('input_folder')
    search_str = kwargs.get('search_str')
    # Run in recursive mode
    recursive = kwargs.get('recursive')
    #Redact, Frame, Highlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    pages = kwargs.get('pages')
    # Loop though the files within the input folder.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # Check if pdf file
            if not filename.endswith('.pdf'):
                continue
             # PDF File found
            inp_pdf_file = os.path.join(foldername, filename)
            print("Processing file =", inp_pdf_file)
            process_file(input_file=inp_pdf_file, output_file=None,
                         search_str=search_str, action=action, pages=pages)
        if not recursive:
            break
Эта функция предназначена для обработки PDF-файлов, включенных в определенную папку.

Он зацикливается на файлах указанной папки либо рекурсивно, либо нет в зависимости от значения параметра рекурсивный и обрабатывает эти файлы один за другим.

Он принимает следующие параметры:

input_folder: путь к папке, содержащей обрабатываемые PDF-файлы.
search_str: текст, который нужно искать для манипулирования.
рекурсивный: следует ли запускать этот процесс рекурсивно путем зацикливания по вложенным папкам или нет.
действие: действие, которое необходимо выполнить среди ранее упомянутого списка.
pages: страницы для рассмотрения.
Прежде чем мы сделаем наш основной код, давайте создадим функцию для синтаксического анализа аргументов командной строки:

def is_valid_path(path):
    """
    Validates the path inputted and checks whether it is a file path or a folder path
    """
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")


def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
                        required=True, help="Enter the path of the file or the folder to process")
    parser.add_argument('-a', '--action', dest='action', choices=['Redact', 'Frame', 'Highlight', 'Squiggly', 'Underline', 'Strikeout', 'Remove'], type=str,
                        default='Highlight', help="Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Strikeout or to Remove")
    parser.add_argument('-p', '--pages', dest='pages', type=tuple,
                        help="Enter the pages to consider e.g.: [2,4]")
    action = parser.parse_known_args()[0].action
    if action != 'Remove':
        parser.add_argument('-s', '--search_str', dest='search_str'                            # lambda x: os.path.has_valid_dir_syntax(x)
                            , type=str, required=True, help="Enter a valid search string")
    path = parser.parse_known_args()[0].input_path
    if os.path.isfile(path):
        parser.add_argument('-o', '--output_file', dest='output_file', type=str  # lambda x: os.path.has_valid_dir_syntax(x)
                            , help="Enter a valid output file")
    if os.path.isdir(path):
        parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
            str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively")
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args
Напоследок напишем основной код:

if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    # If File Path
    if os.path.isfile(args['input_path']):
        # Extracting File Info
        extract_info(input_file=args['input_path'])
        # Process a file
        process_file(
            input_file=args['input_path'], output_file=args['output_file'], 
            search_str=args['search_str'] if 'search_str' in (args.keys()) else None, 
            pages=args['pages'], action=args['action']
        )
    # If Folder Path
    elif os.path.isdir(args['input_path']):
        # Process a folder
        process_folder(
            input_folder=args['input_path'], 
            search_str=args['search_str'] if 'search_str' in (args.keys()) else None, 
            action=args['action'], pages=args['pages'], recursive=args['recursive']
        )
Now let's test our program:

$ python pdf_highlighter.py --help
Output:

usage: pdf_highlighter.py [-h] -i INPUT_PATH [-a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}] [-p PAGES]

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter the path of the file or the folder to process
  -a {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}, --action {Redact,Frame,Highlight,Squiggly,Underline,Strikeout,Remove}
                        Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Strikeout or to Remove
  -p PAGES, --pages PAGES
                        Enter the pages to consider e.g.: [2,4]
Before exploring our test scenarios, let me clarify few points:

To avoid encountering the PermissionError, please close the input PDF file before running this utility.
The input PDF file to process must not be a scanned PDF file.
The search string complies with the rules of regular expressions using Python's built-in re module. For example, setting the search string to "organi[sz]e" match both "organise" and "organize".
As a demonstration example, let’s highlight the word "BERT" in the BERT paper:

$ python pdf_highlighter.py -i bert-paper.pdf -a Highlight -s "BERT"
Выпуск:

## Command Arguments #################################################
input_path:bert-paper.pdf
action:Highlight
pages:None
search_str:BERT
output_file:None
######################################################################
## File Information ##################################################
File:bert-paper.pdf
Encrypted:False
format:PDF 1.5
title:
author:
subject:
keywords:
creator:LaTeX with hyperref package
producer:pdfTeX-1.40.17
creationDate:D:20190528000751Z
modDate:D:20190528000751Z
trapped:
encryption:None
######################################################################
121 Match(es) Found of Search String BERT In Input File: bert-paper.pdf
Как видите, было выделено 121 совпадение, можно использовать и другие параметры подсветки, такие как подчеркивание, фрейм и другие. Вот полученный PDF-файл:

Пример выделенияДавайте удалим его сейчас:

$ python pdf_highlighter.py -i bert-paper.pdf -a Remove
Полученный PDF-файл удалит выделение.

Заключение
Я приглашаю вас поиграть с другими действиями, так как мне довольно интересно делать это автоматически с Python.

Если вы хотите выделить текст из нескольких PDF-файлов, вы можете либо указать папку для параметра -i, либо объединить PDF-файлы вместе и запустить код, чтобы создать один PDF-файл, в котором есть весь текст, который вы хотите выделить.

Надеюсь, вам понравилась эта статья и она показалась вам интересной. Проверьте полный код здесь.

Другие связанные с обработкой PDF учебные пособия:

Как добавить водяные знаки к PDF-файлам в Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы из PDF на Python.
Как конвертировать PDF в изображения в Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!