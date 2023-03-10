# [How to Split PDF Files in Python](https://www.thepythoncode.com/article/split-pdf-files-in-python)
##
# [[] / []]()
Существует множество сценариев, в которых требуется автоматически разделить PDF-документ на несколько файлов. Из этого туториала Вы узнаете, как создать сплиттер PDF на Python с помощью библиотеки pikepdf.

Чтобы начать работу, давайте установим pikepdf:

$ pip install pikepdf
Откройте новый файл Python и давайте импортируем его:

import os
from pikepdf import Pdf
Прежде всего, давайте создадим словарь Python, который сопоставляет новый индекс PDF-файла с диапазоном страниц исходного PDF-файла:

# a dictionary mapping PDF file to original PDF's page range
file2pages = {
    0: [0, 9], # 1st splitted PDF file will contain the pages from 0 to 9 (9 is not included)
    1: [9, 11], # 2nd splitted PDF file will contain the pages from 9 (9 is included) to 11
    2: [11, 100], # 3rd splitted PDF file will contain the pages from 11 until the end or until the 100th page (if exists)
}
В приведенной выше настройке мы собираемся разделить наш PDF-файл на 3 новых PDF-документа, первый содержит первые 9 страниц, от 0 до 9 (в то время как 9 не включено). Второй файл будет содержать страницы от 9 (включено) до 11, а последний файл будет содержать диапазон страниц от 11 до конца или до достижения страницы 100, если он существует.

Таким образом, мы гарантируем максимальную гибкость, так как у каждого из вас есть свой собственный вариант использования. Если вы хотите разделить каждую страницу на новый PDF-документ, вы можете просто заменить [0, 9] на [0], так что это будет список одного элемента, и это первая страница, и так далее.

Это файл, который мы собираемся разделить (вы можете получить его здесь, если хотите следить за ним):

# the target PDF document to split
filename = "bert-paper.pdf"
Загрузка файла:

# load the PDF file
pdf = Pdf.open(filename)
Далее мы составляем полученные PDF-файлы (3 в данном случае) в виде списка:

# make the new splitted PDF files
new_pdf_files = [ Pdf.new() for i in file2pages ]
# the current pdf file index
new_pdf_index = 0
Чтобы создать новый PDF-файл, просто вызовите метод Pdf.new(). Переменная new_pdf_index является индексом файла, он будет увеличиваться только тогда, когда мы закончим с созданием предыдущего файла. Погружение в основную петлю:

# iterate over all PDF pages
for n, page in enumerate(pdf.pages):
    if n in list(range(*file2pages[new_pdf_index])):
        # add the `n` page to the `new_pdf_index` file
        new_pdf_files[new_pdf_index].pages.append(page)
        print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
    else:
        # make a unique filename based on original file name plus the index
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}-{new_pdf_index}.pdf"
        # save the PDF file
        new_pdf_files[new_pdf_index].save(output_filename)
        print(f"[+] File: {output_filename} saved.")
        # go to the next file
        new_pdf_index += 1
        # add the `n` page to the `new_pdf_index` file
        new_pdf_files[new_pdf_index].pages.append(page)
        print(f"[*] Assigning Page {n} to the file {new_pdf_index}")

# save the last PDF file
name, ext = os.path.splitext(filename)
output_filename = f"{name}-{new_pdf_index}.pdf"
new_pdf_files[new_pdf_index].save(output_filename)
print(f"[+] File: {output_filename} saved.")
Во-первых, мы перебираем все PDF-файлы, используя атрибут pdf.pages. Если индекс страницы находится в диапазоне страниц файла в словаре file2pages, то мы просто добавляем страницу в наш новый файл. В противном случае мы знаем, что закончили с предыдущим файлом, и пришло время сохранить его на диск с помощью метода save(), и мы продолжаем цикл, пока все страницы не будут назначены их файлам. И, наконец, мы сохраняем последний файл вне цикла.

Вот выходные данные при запуске кода:

[*] Assigning Page 0 to the file 0
[*] Assigning Page 1 to the file 0
[*] Assigning Page 2 to the file 0
[*] Assigning Page 3 to the file 0
[*] Assigning Page 4 to the file 0
[*] Assigning Page 5 to the file 0
[*] Assigning Page 6 to the file 0
[*] Assigning Page 7 to the file 0
[*] Assigning Page 8 to the file 0
[+] File: bert-paper-0.pdf saved.
[*] Assigning Page 9 to the file 1 
[*] Assigning Page 10 to the file 1
[+] File: bert-paper-1.pdf saved.
[*] Assigning Page 11 to the file 2
[*] Assigning Page 12 to the file 2
[*] Assigning Page 13 to the file 2
[*] Assigning Page 14 to the file 2
[*] Assigning Page 15 to the file 2
[+] File: bert-paper-2.pdf saved.
И действительно, новые PDF-файлы создаются:

Разделенные PDF-документыЗаключение
И вот! Я надеюсь, что это краткое руководство помогло вам разделить ваш PDF-файл на несколько документов, вы можете проверить полный код здесь. Если вы хотите объединить несколько PDF-файлов в один, то этот туториал вам обязательно поможет.

У нас есть другие учебные пособия по обработке PDF с Python, убедитесь, что вы проверили их, если вам интересно!

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Узнайте также: Как объединить PDF-файлы в Python