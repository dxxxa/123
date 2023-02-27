# [How to Watermark PDF Files in Python](https://www.thepythoncode.com/article/watermark-in-pdf-using-python)
To run this:
- `pip3 install -r requirements.txt`
- ```python pdf_watermarker.py --help```

**Output:**
```

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter the path of the file or the folder to process
  -a {watermark,unwatermark}, --action {watermark,unwatermark}
                        Choose whether to watermark or to unwatermark
  -m {RAM,HDD}, --mode {RAM,HDD}
                        Choose whether to process on the hard disk drive or in memory
  -w WATERMARK_TEXT, --watermark_text WATERMARK_TEXT
                        Enter a valid watermark text
  -p PAGES, --pages PAGES
                        Enter the pages to consider e.g.: [2,4]
```
- To add a watermark with any text on `lorem-ipsum.pdf` file and output it as `watermarked_lorem-ipsum.pdf`:
    ```
    python pdf_watermarker.py -i lorem-ipsum.pdf -a watermark -w "text here" -o watermarked_lorem-ipsum.pdf
    ```
##
# [[] / []]()
Portable Document Format (PDF), стандартизированный как ISO 32000, представляет собой формат файлов, разработанный Adobe в 1993 году для представления документов, включая форматирование текста и изображений, способом, независимым от прикладного программного обеспечения, аппаратного обеспечения и операционных систем.

На основе языка PostScript каждый PDF-файл инкапсулирует полное описание плоского документа с фиксированной компоновкой, включая текст, шрифты, векторную графику, растровые изображения и другую информацию, необходимую для его отображения.

Знакомство с PDF привело к его быстрому и широкому внедрению в качестве решения в области цифрового архивирования. Поскольку PDF-файлы более универсальны, чем другие форматы файлов, информация, которую они отображают, легко просматривается практически из любой операционной системы или устройства.

Из этого туториала Вы узнаете, как пометить водяной знак PDF-файлом или папкой, содержащей коллекцию PDF-файлов, с помощью PyPDF4 и reportlab на Python.

Для начала установим необходимые библиотеки:

$ pip install PyPDF4==1.27.0 reportlab==3.5.59
Начиная с кода, давайте импортируем библиотеки и определим некоторую конфигурацию, которая нам понадобится:

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_
import os
import argparse
from io import BytesIO
from typing import Tuple
# Import the reportlab library
from reportlab.pdfgen import canvas
# The size of the page supposedly A4
from reportlab.lib.pagesizes import A4
# The color of the watermark
from reportlab.lib import colors

PAGESIZE = A4
FONTNAME = 'Helvetica-Bold'
FONTSIZE = 40
# using colors module
# COLOR = colors.lightgrey
# or simply RGB
# COLOR = (190, 190, 190)
COLOR = colors.red
# The position attributes of the watermark
X = 250
Y = 10
# The rotation angle in order to display the watermark diagonally if needed
ROTATION_ANGLE = 45
Далее, определяя нашу первую функцию утилиты:

def get_info(input_file: str):
    """
    Extracting the file info
    """
    # If PDF is encrypted the file metadata cannot be extracted
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file, strict=False)
        output = {
            "File": input_file, "Encrypted": ("True" if pdf_reader.isEncrypted else "False")
        }
        if not pdf_reader.isEncrypted:
            info = pdf_reader.getDocumentInfo()
            num_pages = pdf_reader.getNumPages()
            output["Author"] = info.author
            output["Creator"] = info.creator
            output["Producer"] = info.producer
            output["Subject"] = info.subject
            output["Title"] = info.title
            output["Number of pages"] = num_pages
    # To Display collected metadata
    print("## File Information ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in output.items()))
    print("######################################################################")
    return True, output
Функция get_info() собирает метаданные входного PDF-файла, могут быть извлечены следующие атрибуты: автор, создатель, производитель, тема, заголовок и количество страниц.

Стоит отметить, что вы не можете извлечь эти атрибуты для зашифрованного PDF-файла.

def get_output_file(input_file: str, output_file: str):
    """
    Check whether a temporary output file is needed or not
    """
    input_path = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    # If output file is empty -> generate a temporary output file
    # If output file is equal to input_file -> generate a temporary output file
    if not output_file or input_file == output_file:
        tmp_file = os.path.join(input_path, 'tmp_' + input_filename)
        return True, tmp_file
    return False, output_file
Приведенная выше функция возвращает путь к временному выходному файлу, если выходной файл не указан или если пути к входному и выходному файлам равны.

def create_watermark(wm_text: str):
    """
    Creates a watermark template.
    """
    if wm_text:
        # Generate the output to a memory buffer
        output_buffer = BytesIO()
        # Default Page Size = A4
        c = canvas.Canvas(output_buffer, pagesize=PAGESIZE)
        # you can also add image instead of text
        # c.drawImage("logo.png", X, Y, 160, 160)
        # Set the size and type of the font
        c.setFont(FONTNAME, FONTSIZE)
        # Set the color
        if isinstance(COLOR, tuple):
            color = (c/255 for c in COLOR)
            c.setFillColorRGB(*color)
        else:
            c.setFillColor(COLOR)
        # Rotate according to the configured parameter
        c.rotate(ROTATION_ANGLE)
        # Position according to the configured parameter
        c.drawString(X, Y, wm_text)
        c.save()
        return True, output_buffer
    return False, None
Эта функция выполняет следующие функции:

Создает файл водяного знака и сохраняет его в памяти.
Примените параметры, определенные ранее, на созданном нами холсте с помощью reportlab.
Обратите внимание, что вместо использования метода drawString() для написания текста можно использовать drawImage() для рисования изображения, записанного в виде комментария в приведенной выше функции.

def save_watermark(wm_buffer, output_file):
    """
    Saves the generated watermark template to disk
    """
    with open(output_file, mode='wb') as f:
        f.write(wm_buffer.getbuffer())
    f.close()
    return True
save_watermark() сохраняет сгенерированный шаблон водяного знака в физический файл на случай, если вам нужно его визуализировать.

Теперь давайте напишем функцию, которая отвечает за добавление водяного знака в данный PDF-файл:

def watermark_pdf(input_file: str, wm_text: str, pages: Tuple = None):
    """
    Adds watermark to a pdf file.
    """
    result, wm_buffer = create_watermark(wm_text)
    if result:
        wm_reader = PdfFileReader(wm_buffer)
        pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
        pdf_writer = PdfFileWriter()
        try:
            for page in range(pdf_reader.getNumPages()):
                # If required to watermark specific pages not all the document pages
                if pages:
                    if str(page) not in pages:
                        continue
                page = pdf_reader.getPage(page)
                page.mergePage(wm_reader.getPage(0))
                pdf_writer.addPage(page)
        except Exception as e:
            print("Exception = ", e)
            return False, None, None
        return True, pdf_reader, pdf_writer
Эта функция направлена на объединение введенного PDF-файла с сгенерированным водяным знаком. Он принимает следующие параметры:

input_file: путь PDF-файла к водяному знаку.
wm_text: текст, устанавливаемый в качестве водяного знака.
pages: страницы с водяным знаком.
Он выполняет следующие действия:

Создает водяной знак и сохраняет его в буфере памяти.
Выполняет итерацию по страницам входного файла и объединяет каждую из выбранных страниц с ранее созданным водяным знаком. Водяной знак действует как наложение в верхней части страницы.
Добавляет результирующую страницу в объект pdf_writer.
def unwatermark_pdf(input_file: str, wm_text: str, pages: Tuple = None):
    """
    Removes watermark from the pdf file.
    """
    pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
    pdf_writer = PdfFileWriter()
    for page in range(pdf_reader.getNumPages()):
        # If required for specific pages
        if pages:
            if str(page) not in pages:
                continue
        page = pdf_reader.getPage(page)
        # Get the page content
        content_object = page["/Contents"].getObject()
        content = ContentStream(content_object, pdf_reader)
        # Loop through all the elements page elements
        for operands, operator in content.operations:
            # Checks the TJ operator and replaces the corresponding string operand (Watermark text) with ''
            if operator == b_("Tj"):
                text = operands[0]
                if isinstance(text, str) and text.startswith(wm_text):
                    operands[0] = TextStringObject('')
        page.__setitem__(NameObject('/Contents'), content)
        pdf_writer.addPage(page)
    return True, pdf_reader, pdf_writer
Целью этой функции является удаление текста водяного знака из PDF-файла. Он принимает следующие параметры:

input_file: путь PDF-файла к водяному знаку.
wm_text: текст, устанавливаемый в качестве водяного знака.
pages: страницы с водяным знаком.
Он выполняет следующие действия:

Итерация по страницам входного файла и захват содержимого каждой страницы.
Используя захваченное содержимое, он находит оператор TJ и заменяет строку (текст водяного знака) после этого оператора.
Добавляет результирующую страницу после слияния в объект pdf_writer.
def watermark_unwatermark_file(**kwargs):
    input_file = kwargs.get('input_file')
    wm_text = kwargs.get('wm_text')
    # watermark   -> Watermark
    # unwatermark -> Unwatermark
    action = kwargs.get('action')
    # HDD -> Temporary files are saved on the Hard Disk Drive and then deleted
    # RAM -> Temporary files are saved in memory and then deleted.
    mode = kwargs.get('mode')
    pages = kwargs.get('pages')
    temporary, output_file = get_output_file(
        input_file, kwargs.get('output_file'))
    if action == "watermark":
        result, pdf_reader, pdf_writer = watermark_pdf(
            input_file=input_file, wm_text=wm_text, pages=pages)
    elif action == "unwatermark":
        result, pdf_reader, pdf_writer = unwatermark_pdf(
            input_file=input_file, wm_text=wm_text, pages=pages)
    # Completed successfully
    if result:
        # Generate to memory
        if mode == "RAM":
            output_buffer = BytesIO()
            pdf_writer.write(output_buffer)
            pdf_reader.stream.close()
            # No need to create a temporary file in RAM Mode
            if temporary:
                output_file = input_file
            with open(output_file, mode='wb') as f:
                f.write(output_buffer.getbuffer())
            f.close()
        elif mode == "HDD":
            # Generate to a new file on the hard disk
            with open(output_file, 'wb') as pdf_output_file:
                pdf_writer.write(pdf_output_file)
            pdf_output_file.close()
            pdf_reader.stream.close()
            if temporary:
                if os.path.isfile(input_file):
                    os.replace(output_file, input_file)
                output_file = input_file
Вышеуказанная функция принимает несколько параметров:

input_file: путь PDF-файла к водяному знаку.
wm_text: текст, устанавливаемый в качестве водяного знака.
действие: действие, выполняемое для создания водяного знака или удаления файла водяного знака.
mode: расположение временного файла в памяти или на жестком диске.
pages: страницы с водяным знаком.
функция watermark_unwatermark_file() вызывает ранее определенные функции watermark_pdf() или unwatermark_pdf() в зависимости от выбранного действия.

На основе выбранного режима, и если выходной файл имеет путь, аналогичный входному файлу, или выходной файл не указан, то будет создан временный файл в случае, если выбранный режим HDD (жесткий диск).

Далее добавим возможность добавлять или удалять водяные знаки из папки, содержащей несколько PDF-файлов:

def watermark_unwatermark_folder(**kwargs):
    """
    Watermarks all PDF Files within a specified path
    Unwatermarks all PDF Files within a specified path
    """
    input_folder = kwargs.get('input_folder')
    wm_text = kwargs.get('wm_text')
    # Run in recursive mode
    recursive = kwargs.get('recursive')
    # watermark   -> Watermark
    # unwatermark -> Unwatermark
    action = kwargs.get('action')
    # HDD -> Temporary files are saved on the Hard Disk Drive and then deleted
    # RAM -> Temporary files are saved in memory and then deleted.
    mode = kwargs.get('mode')
    pages = kwargs.get('pages')
    # Loop though the files within the input folder.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # Check if pdf file
            if not filename.endswith('.pdf'):
                continue
            # PDF File found
            inp_pdf_file = os.path.join(foldername, filename)
            print("Processing file:", inp_pdf_file)
            watermark_unwatermark_file(input_file=inp_pdf_file, output_file=None,
                                       wm_text=wm_text, action=action, mode=mode, pages=pages)
        if not recursive:
            break
Эта функция зацикливает файлы указанной папки либо рекурсивно, либо не в зависимости от значения рекурсивного параметра, и обрабатывает эти файлы один за другим.

Далее давайте сделаем служебную функцию, чтобы проверить, является ли путь путем к файлу или путем к каталогу:

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
Теперь, когда у нас есть все функции, необходимые для этого учебника, давайте сделаем последнюю для синтаксического анализа аргументов командной строки:

def parse_args():
    """
    Get user command line parameters
    """
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
                        required=True, help="Enter the path of the file or the folder to process")
    parser.add_argument('-a', '--action', dest='action', choices=[
                        'watermark', 'unwatermark'], type=str, default='watermark',
                        help="Choose whether to watermark or to unwatermark")
    parser.add_argument('-m', '--mode', dest='mode', choices=['RAM', 'HDD'], type=str,
                        default='RAM', help="Choose whether to process on the hard disk drive or in memory")
    parser.add_argument('-w', '--watermark_text', dest='watermark_text',
                        type=str, required=True, help="Enter a valid watermark text")
    parser.add_argument('-p', '--pages', dest='pages', type=tuple,
                        help="Enter the pages to consider e.g.: [2,4]")
    path = parser.parse_known_args()[0].input_path
    if os.path.isfile(path):
        parser.add_argument('-o', '--output_file', dest='output_file',
                            type=str, help="Enter a valid output file")
    if os.path.isdir(path):
        parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
            str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively")
    # To Porse The Command Line Arguments
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args
Ниже приведены определенные аргументы:

input_path: Обязательный параметр для ввода пути к файлу или папке для обработки, этот параметр связан с ранее определенной функцией is_valid_path().
действие: выполняемое действие, которое является либо водяным знаком, либо удалением водяного знака pdf-файла, по умолчанию является водяным знаком.
mode: Чтобы указать назначение сгенерированного временного файла, будь то память или жесткий диск.
watermark_text: строка, устанавливаемая в качестве водяного знака.
страницы: страницы с водяным знаком (например, первая страница [0], вторая страница и четвертая страница [1, 3] и т. Д.). Если не указано, то все страницы.
output_file: путь к выходному файлу.
рекурсивный: следует ли обрабатывать папку рекурсивно.
Теперь, когда у нас есть все, давайте напишем основной код для выполнения на основе переданных параметров:

if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    # If File Path
    if os.path.isfile(args['input_path']):
        # Extracting File Info
        get_info(input_file=args['input_path'])
        # Encrypting or Decrypting a File
        watermark_unwatermark_file(
            input_file=args['input_path'], wm_text=args['watermark_text'], action=args[
                'action'], mode=args['mode'], output_file=args['output_file'], pages=args['pages']
        )
    # If Folder Path
    elif os.path.isdir(args['input_path']):
        # Encrypting or Decrypting a Folder
        watermark_unwatermark_folder(
            input_folder=args['input_path'], wm_text=args['watermark_text'],
            action=args['action'], mode=args['mode'], recursive=args['recursive'], pages=args['pages']
        )
Связанные с: Как извлечь изображения из PDF на Python.

Теперь давайте протестируем нашу программу, если вы откроете окно терминала и наберете:

$ python pdf_watermarker.py --help
Он покажет определенные параметры и их соответствующее описание:

usage: pdf_watermarker.py [-h] -i INPUT_PATH [-a {watermark,unwatermark}] [-m {RAM,HDD}] -w WATERMARK_TEXT [-p PAGES]

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter the path of the file or the folder to process
  -a {watermark,unwatermark}, --action {watermark,unwatermark}
                        Choose whether to watermark or to unwatermark
  -m {RAM,HDD}, --mode {RAM,HDD}
                        Choose whether to process on the hard disk drive or in memory
  -w WATERMARK_TEXT, --watermark_text WATERMARK_TEXT
                        Enter a valid watermark text
  -p PAGES, --pages PAGES
                        Enter the pages to consider e.g.: [2,4]
Теперь давайте пометим мое резюме водяным знаком в качестве примера:

$ python pdf_watermarker.py -a watermark -i "CV Bassem Marji_Eng.pdf" -w "CONFIDENTIAL" -o CV_watermark.pdf
Будут получены следующие результаты:

## Command Arguments #################################################
input_path:CV Bassem Marji_Eng.pdf
action:watermark
mode:RAM
watermark_text:CONFIDENTIAL
pages:None
output_file:CV_watermark.pdf
######################################################################
## File Information ##################################################
File:CV Bassem Marji_Eng.pdf
Encrypted:False
Author:TMS User
Creator:Microsoft® Word 2013
Producer:Microsoft® Word 2013
Subject:None
Title:None
Number of pages:1
######################################################################
Вот как выглядит выходной CV_watermark.pdf файл:

PDF с водяными знаками и PythonТеперь уберем добавленный водяной знак:

$ python pdf_watermarker.py -a unwatermark -i "CV_watermark.pdf" -w "CONFIDENTIAL" -o CV.pdf
На этот раз водяной знак будет удален и сохранен в новый PDF-файл CV.pdf.

Вы также можете установить -m и -p для режима и страниц соответственно. Можно также пометить водяным знаком список PDF-файлов, расположенных по определенному пути:

$ python pdf_watermarker.py -i "C:\Scripts\Test" -a "watermark" -w "CONFIDENTIAL" -r False
Или удаление водяного знака из кучи PDF-файлов:

$ python pdf_watermarker.py -i "C:\Scripts\Test" -a "unwatermark" -w "CONFIDENTIAL" -m HDD -p[0] -r False
Заключение
Из этого туториала Вы узнали, как добавлять и удалять водяные знаки из PDF-файлов с помощью библиотек reportlab и PyPDF4 на Python. Я надеюсь, что эта статья помогла вам усвоить эту классную функцию.

Вот некоторые другие учебные пособия, связанные с PDF:

Как конвертировать PDF в Docx в Python
Как объединить PDF-файлы в Python
Как извлечь метаданные PDF в Python