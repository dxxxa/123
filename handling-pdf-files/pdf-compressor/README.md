# [How to Compress PDF Files in Python](https://www.thepythoncode.com/article/compress-pdf-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To compress `bert-paper.pdf` file:
    ```
    $ python pdf_compressor.py bert-paper.pdf bert-paper-min.pdf
    ```
    This will spawn a new compressed PDF file under the name `bert-paper-min.pdf`.
##
# [[] / []]()
Сжатие PDF позволяет уменьшить размер файла как можно меньше, сохраняя при этом качество мультимедиа в этом PDF-файле. В результате это значительно повышает эффективность и делимость.

Из этого туториала Вы узнаете, как сжимать PDF-файлы с помощью библиотеки PDFTron на Python.

PDFNetPython3 - это оболочка для PDFTron SDK. С помощью компонентов PDFTron вы можете создавать надежные и быстрые приложения, которые могут просматривать, создавать, печатать, редактировать и комментировать PDF-файлы в различных операционных системах. Разработчики используют PDFTron SDK для чтения, записи и редактирования PDF-документов, совместимых со всеми опубликованными версиями спецификаций PDF (включая последнюю версию ISO32000).

PDFTron не является бесплатным программным обеспечением. Он предлагает два типа лицензий в зависимости от того, разрабатываете ли вы внешний /коммерческий продукт или собственное решение.

Мы будем использовать бесплатную пробную версию этого SDK для этого учебника. Целью этого учебника является разработка легкой утилиты на основе командной строки с помощью модулей на основе Python, не полагаясь на внешние утилиты за пределами экосистемы Python (например, Ghostscript), которые сжимают PDF-файлы.

Обратите внимание, что этот учебник работает только для сжатия PDF-файлов, а не для любого файла. Вы можете проверить этот учебник для сжатия и архивации файлов.

Читайте также: Как сжимать изображения в Python.

Чтобы начать работу, давайте установим оболочку Python с помощью pip:

$ pip install PDFNetPython3==8.1.0
Откройте новый файл Python и импортируйте необходимые модули:

# Import Libraries
import os
import sys
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
Далее определим функцию, которая выводит размер файла в соответствующем формате (взятом из этого туториала):

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
Теперь давайте определим нашу основную функцию:

def compress_file(input_file: str, output_file: str):
    """Compress PDF file"""
    if not output_file:
        output_file = input_file
    initial_size = os.path.getsize(input_file)
    try:
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error compress_file=", e)
        doc.Close()
        return False
    compressed_size = os.path.getsize(output_file)
    ratio = 1 - (compressed_size / initial_size)
    summary = {
        "Input File": input_file, "Initial Size": get_size_format(initial_size),
        "Output File": output_file, f"Compressed Size": get_size_format(compressed_size),
        "Compression Ratio": "{0:.3%}.".format(ratio)
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True
Эта функция сжимает PDF-файл, удаляя избыточную информацию и сжимая потоки данных; затем он выводит сводку, показывающую степень сжатия и размер файла после сжатия. Он принимает pdf-input_file и создает сжатый PDF-output_file.

Теперь определим наш основной код:

if __name__ == "__main__":
    # Parsing command line arguments entered by user
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    compress_file(input_file, output_file)
Мы просто получаем входные и выходные файлы из аргументов командной строки, а затем используем нашу определенную функцию compress_file() для сжатия PDF-файла.

Давайте проверим это:

$ python pdf_compressor.py bert-paper.pdf bert-paper-min.pdf
Ниже приведены выходные данные:

PDFNet is running in demo mode.
Permission: read     
Permission: optimizer
Permission: write
## Summary ########################################################
Input File:bert-paper.pdf
Initial Size:757.00KB
Output File:bert-paper-min.pdf
Compressed Size:498.33KB
Compression Ratio:34.171%.
###################################################################
Как видите, новый сжатый PDF-файл размером 498 КБ вместо 757 КБ. Взгляните:

Сжатый PDF-файлЗаключение
Я надеюсь, что вам понравился учебник и вы нашли этот PDF-компрессор полезным для ваших задач.

Вот некоторые другие связанные с PDF-учебниками:

Как конвертировать HTML в PDF в Python.
Как выделить и отредактировать текст в PDF-файлах с помощью Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы из PDF на Python.
Как извлечь текст из изображений в PDF-файлах с помощью Python.
Как извлечь метаданные PDF в Python.
Как подписывать PDF-файлы на Python.
Проверьте полный код здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!