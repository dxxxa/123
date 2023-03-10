# [How to Extract All PDF Links in Python](https://www.thepythoncode.com/article/extract-pdf-links-with-python)
To run this:
- `pip3 install -r requirements.txt`
- Use `pdf_link_extractor.py` to get clickable links, and `pdf_link_extractor_regex.py` to get links that are in text form.
##
# [[] / []]()
Вы хотите извлечь URL-адреса, которые находятся в определенном PDF-файле? Если это так, вы находитесь в правильном месте. В этом уроке мы будем использовать библиотеки pikepdf и PyMuPDF на Python для извлечения всех ссылок из PDF-файлов.

Мы будем использовать два метода для получения ссылок из определенного PDF-файла, первый - это извлечение аннотаций, которые представляют собой разметки, заметки и комментарии, которые вы можете фактически щелкнуть по своей обычной программе чтения PDF и перенаправить в свой браузер, тогда как второй - извлечение всего необработанного текста и использование регулярных выражений для анализа URL-адресов.

Чтобы начать работу, давайте установим следующие библиотеки:

pip3 install pikepdf PyMuPDF
Метод 1: Извлечение URL-адресов с помощью аннотаций
В этом методе мы будем использовать библиотеку pikepdf, чтобы открыть PDF-файл, перебрать все аннотации каждой страницы и посмотреть, есть ли там URL- адрес:

import pikepdf # pip3 install pikepdf

file = "1810.04805.pdf"
# file = "1710.05006.pdf"
pdf_file = pikepdf.Pdf.open(file)
urls = []
# iterate over PDF pages
for page in pdf_file.pages:
    for annots in page.get("/Annots"):
        uri = annots.get("/A").get("/URI")
        if uri is not None:
            print("[+] URL Found:", uri)
            urls.append(uri)

print("[*] Total URLs extracted:", len(urls))
Я тестирую на этом PDF-файле, но не стесняйтесь использовать любой PDF-файл по вашему выбору, просто убедитесь, что в нем есть несколько кликабельных ссылок.

После выполнения этого кода я получаю следующие выходные данные:

[+] URL Found: https://github.com/google-research/bert
[+] URL Found: https://github.com/google-research/bert
[+] URL Found: https://gluebenchmark.com/faq
[+] URL Found: https://gluebenchmark.com/leaderboard
...<SNIPPED>...
[+] URL Found: https://gluebenchmark.com/faq
[*] Total URLs extracted: 30
Удивительно, мы успешно извлекли 30 URL-адресов из этой PDF-бумаги.

Связанные с: Как извлечь все ссылки на веб-сайты на Python.

Метод 2: Извлечение URL-адресов с помощью регулярных выражений
В этом разделе мы извлекем весь необработанный текст из нашего PDF-файла, а затем используем регулярные выражения для анализа URL-адресов. Во-первых, давайте получим текстовую версию PDF:

import fitz # pip install PyMuPDF
import re

# a regular expression of URLs
url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
# extract raw text from pdf
file = "1710.05006.pdf"
# file = "1810.04805.pdf"
# open the PDF file
with fitz.open(file) as pdf:
    text = ""
    for page in pdf:
        # extract text of each PDF page
        text += page.getText()
Теперь текст - это целевая строка, которую мы хотим проанализировать URL-адреса, давайте использовать модуль re для их разбора:

urls = []
# extract all urls using the regular expression
for match in re.finditer(url_regex, text):
    url = match.group()
    print("[+] URL Found:", url)
    urls.append(url)
print("[*] Total URLs extracted:", len(urls))
Выпуск:

[+] URL Found: https://github.com/
[+] URL Found: https://github.com/tensor
[+] URL Found: http://nlp.seas.harvard.edu/2018/04/03/attention.html
[+] URL Found: https://gluebenchmark.com/faq.
[+] URL Found: https://gluebenchmark.com/leaderboard).
[+] URL Found: https://gluebenchmark.com/leaderboard
[+] URL Found: https://cloudplatform.googleblog.com/2018/06/Cloud-
[+] URL Found: https://gluebenchmark.com/
[+] URL Found: https://gluebenchmark.com/faq
[*] Total URLs extracted: 9
Заключение
На этот раз мы извлекаем только 9 URL-адресов из того же PDF-файла, теперь это не означает, что второй метод не точен. Этот метод анализирует только URL-адреса в текстовой форме (не кликабельные).

Однако с этим методом возникает проблема, так как URL-адреса могут содержать новые строки (\n), поэтому вы можете разрешить это в url_regex выражении.

Итак, в заключение, если вы хотите получить URL-адреса, которые являются кликабельными, вы можете использовать первый метод, который является предпочтительным. Но если вы хотите получить URL-адреса в текстовой форме, второй может помочь вам в этом!

Если вы хотите извлечь таблицы или изображения из PDF, есть учебники для этого:

Как извлечь все ссылки PDF на Python
Как извлечь таблицы PDF на Python
Узнайте также: Как создать экстрактор электронной почты в Python.