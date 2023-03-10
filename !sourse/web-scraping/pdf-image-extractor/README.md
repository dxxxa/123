# [How to Extract Images from PDF in Python](https://www.thepythoncode.com/article/extract-pdf-images-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To extract and save all images of `1710.05006.pdf` PDF file, you run:
    ```
    python pdf_image_extractor.py 1710.05006.pdf
    ```
    This will save all available images in the current directory and outputs:
    ```
    [!] No images found on page 0
    [+] Found a total of 3 images in page 1
    [+] Found a total of 3 images in page 2
    [!] No images found on page 3
    [!] No images found on page 4
    ```
##
# [[] / []]()
В этом уроке мы напишем код Python для извлечения изображений из PDF-файлов и сохранения их на локальном диске с помощью библиотек PyMuPDF и Pillow.

С помощью PyMuPDF вы можете получить доступ к PDF, XPS, OpenXPS, epub и многим другим расширениям. Он должен работать на всех платформах, включая Windows, Mac OSX и Linux.

Давайте установим его вместе с Pillow:

pip3 install PyMuPDF Pillow
Откройте новый файл Python и приступим к работе. Во-первых, давайте импортируем библиотеки:

import fitz # PyMuPDF
import io
from PIL import Image
Я собираюсь проверить это с этим PDF-файлом, но вы можете принести и PDF-файл и поместить его в свой текущий рабочий каталог, давайте загрузим его в библиотеку:

# file path you want to extract images from
file = "1710.05006.pdf"
# open the file
pdf_file = fitz.open(file)
Поскольку мы хотим извлечь изображения со всех страниц, нам нужно перебрать все доступные страницы и получить все объекты изображений на каждой странице, следующий код делает это:

# iterate over PDF pages
for page_index in range(len(pdf_file)):
    # get the page itself
    page = pdf_file[page_index]
    # get image list
    image_list = page.get_images()
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(image_list, start=1):
        # get the XREF of the image
        xref = img[0]
        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        # load it to PIL
        image = Image.open(io.BytesIO(image_bytes))
        # save it to local disk
        image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
Связанные с: Как конвертировать PDF в изображения на Python.

Мы используем метод getImageList() для перечисления всех доступных объектов изображений в виде списка кортежей на этой конкретной странице. Чтобы получить индекс объекта изображения, мы просто получаем первый элемент возвращенного кортежа.

После этого мы используем метод extractImage(), который возвращает изображение в байтах и дополнительную информацию, такую как расширение изображения.

Наконец, мы преобразуем байты изображения в экземпляр образа PIL и сохраняем его на локальный диск с помощью метода save(), который принимает указатель на файл в качестве аргумента; мы просто называем изображения соответствующими страницами и индексами изображений.

После запуска скрипта я получил следующий вывод:

[!] No images found on page 0
[+] Found a total of 3 images in page 1
[+] Found a total of 3 images in page 2
[!] No images found on page 3
[!] No images found on page 4
Изображения также сохраняются в текущем каталоге:

Извлеченные изображения с помощью PythonЗаключение
Хорошо, мы успешно извлекли изображения из этого PDF-файла без потери качества изображения. Для получения дополнительной информации о том, как работает библиотека, я предлагаю вам взглянуть на документацию.

Вы можете получить полный код здесь.

Вот некоторые учебные пособия, связанные с PDF:

Как конвертировать HTML в PDF в Python
Как извлечь все ссылки PDF на Python.
Как извлечь таблицы PDF на Python.
Как извлечь текст из PDF на Python.
Кроме того, вы можете проверить эту страницу для обработки PDF-документов в учебниках по Python.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!