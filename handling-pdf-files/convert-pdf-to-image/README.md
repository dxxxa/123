# [How to Convert PDF to Images in Python](https://www.thepythoncode.com/article/convert-pdf-files-to-images-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To convert the PDF file `bert-paper.pdf` into several images (image per page):
    ```
    $ python convert_pdf2image.py bert-paper.pdf
    ```
##
# [[] / []]()
Существуют различные инструменты для преобразования PDF-файлов в изображения, такие как pdftoppm в Linux. Этот учебник направлен на разработку легкого инструмента командной строки на Python для преобразования PDF-файлов в изображения.

Мы будем использовать PyMuPDF, универсальное, настраиваемое решение для интерпретатора PDF, XPS и электронных книг, которое можно использовать в широком спектре приложений, таких как рендерер PDF, просмотрщик или инструментарий.

Во-первых, давайте установим необходимую библиотеку:

$ pip install PyMuPDF==1.18.9
Импорт библиотек:

import fitz

from typing import Tuple
import os
Определим нашу основную функцию полезности:

def convert_pdf2img(input_file: str, pages: Tuple = None):
    """Converts pdf to image and generates a file by page"""
    # Open the document
    pdfIn = fitz.open(input_file)
    output_files = []
    # Iterate throughout the pages
    for pg in range(pdfIn.pageCount):
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        # Select a page
        page = pdfIn[pg]
        rotate = int(0)
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        zoom_x = 2
        zoom_y = 2
        # The zoom factor is equal to 2 in order to make text clear
        # Pre-rotate is to rotate if needed.
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_page{pg+1}.png"
        pix.writePNG(output_file)
        output_files.append(output_file)
    pdfIn.close()
    summary = {
        "File": input_file, "Pages": str(pages), "Output File(s)": str(output_files)
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return output_files
Приведенная выше функция преобразует PDF-файл в серию файлов изображений. Он выполняет итерацию по выбранным страницам (по умолчанию — все они), делает снимок экрана текущей страницы и создает файл изображения с помощью метода writePNG().

Вы можете изменить zoom_x и zoom_y, чтобы изменить коэффициент масштабирования, не стесняйтесь настраивать эти параметры и поворачивать переменную в соответствии с вашими потребностями.

Теперь воспользуемся этой функцией:

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    convert_pdf2img(input_file)
Давайте протестируем скрипт на многостраничном PDF-файле (получите его здесь):

$ python convert_pdf2image.py bert-paper.pdf
Выходные данные будут следующими:

## Summary ########################################################
File:bert-paper.pdf
Pages:None
Output File(s):['bert-paper_page1.png', 'bert-paper_page2.png', 'bert-paper_page3.png', 'bert-paper_page4.png', 'bert-paper_page5.png', 'bert-paper_page6.png', 'bert-paper_page7.png', 'bert-paper_page8.png', 'bert-paper_page9.png', 'bert-paper_page10.png', 'bert-paper_page11.png', 'bert-paper_page12.png', 'bert-paper_page13.png', 'bert-paper_page14.png', 'bert-paper_page15.png', 'bert-paper_page16.png']
###################################################################
И действительно, изображения были успешно сгенерированы:

Результат преобразования PDF-файла в несколько изображенийЗаключение
Мы надеемся, что вы найдете этот учебник полезным для ваших нужд, вот некоторые другие учебники PDF:

Как добавить водяные знаки к PDF-файлам в Python.
Как выделить и отредактировать текст в PDF-файлах с помощью Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы из PDF на Python.
Как извлечь текст из изображений в PDF-файлах с помощью Python.
Как конвертировать PDF в Docx в Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Проверьте полный код здесь.