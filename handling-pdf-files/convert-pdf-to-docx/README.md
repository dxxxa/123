# [How to Convert PDF to Docx in Python](https://www.thepythoncode.com/article/convert-pdf-files-to-docx-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To convert `letter.pdf` to `letter.docx`, run:
    ```
    $ python convert_pdf2docx.py letter.pdf letter.docx
    ```
##
# [[] / []]()
В этом уроке мы углубимся в то, как мы можем использовать библиотеку pdf2docx для преобразования pdf-файлов в расширение docx.

Целью этого учебника является разработка легкой утилиты на основе командной строки с помощью модулей на основе Python, не полагаясь на внешние утилиты за пределами экосистемы Python для преобразования одного или коллекции PDF-файлов, расположенных в папке.

pdf2docx - это библиотека Python для извлечения данных из PDF с помощью PyMuPDF, синтаксического анализа макета с помощью правил и создания файла docx с помощью python-docx. python-docx - это еще одна библиотека, которая используется pdf2docx для создания и обновления файлов Microsoft Word (.docx).

Переходя к требованиям:

$ pip install pdf2docx==0.5.1
Начнем с импорта модулей:

# Import Libraries
from pdf2docx import parse
from typing import Tuple
Определимся с функцией, ответственной за преобразование PDF в Docx:

def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    """Converts pdf to docx"""
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file,
                   docx_with_path=output_file, pages=pages)
    summary = {
        "File": input_file, "Pages": str(pages), "Output File": output_file
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return result
Функция convert_pdf2docx() позволяет указать диапазон страниц для преобразования, преобразует PDF-файл в файл Docx и в конце печатает сводку процесса преобразования.

Давайте воспользуемся им сейчас:

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_pdf2docx(input_file, output_file)
Мы просто используем встроенный sys-модуль Python для получения входных и выходных имен файлов из аргументов командной строки. Давайте попробуем конвертировать пример PDF-файла (получить его здесь):

$ python convert_pdf2docx.py letter.pdf letter.docx
В текущем каталоге появится новый файл letter.docx, и вывод будет выглядеть следующим образом:

Parsing Page 1: 1/1...
Creating Page 1: 1/1...
--------------------------------------------------
Terminated in 0.10869679999999998s.
## Summary ########################################################
File:letter.pdf
Pages:None
Output File:letter.docx
###################################################################
Вы также можете указать нужные страницы в функции convert_pdf2docx().

Я надеюсь, что вам понравился этот короткий учебник, и вы нашли этот конвертер полезным.

Узнайте также: Как заменить текст в файлах Docx на Python.

Учебники, связанные с PDF:

Как добавить водяные знаки к PDF-файлам в Python.
Как выделить и отредактировать текст в PDF-файлах с помощью Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы из PDF на Python.
Как извлечь текст из изображений в PDF-файлах с помощью Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!