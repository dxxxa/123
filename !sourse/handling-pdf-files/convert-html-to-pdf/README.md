# [How to Convert HTML to PDF in Python](https://www.thepythoncode.com/article/convert-html-to-pdf-in-python)
To run this:
- Install wkhtmltopdf, shown in the tutorial.
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Есть много онлайн-инструментов, которые обеспечивают преобразование HTML в PDF-документы, и большинство из них бесплатны. В этом учебнике вы узнаете, как это можно сделать с помощью Python.

Мы будем использовать инструмент wkhtmltopdf, утилиту командной строки с открытым исходным кодом, которая отображает HTML в PDF с помощью движка рендеринга Qt WebKit.

Вот оглавление этого учебника:

Установка wkhtmltopdf
На окнах
На Linux
На macOS
Преобразование HTML из URL в PDF
Преобразование локального HTML-файла в PDF
Преобразование строки HTML в PDF
Чтобы начать, мы должны установить инструмент wkhtmltopdf и его оболочку pdfkit на Python.

Установка wkhtmltopdf
На окнах
Перейдите на официальную страницу загрузок wkhtmltopdf и загрузите установщик Windows для вашей архитектуры Windows. В моем случае я загрузил 64-разрядную архитектуру, которая поддерживается в Vista или более поздней версии, так как у меня Windows 10.

После того, как вы скачали установщик и успешно установили инструмент wkhtmltopdf, теперь вам нужно добавить его в переменную среды PATH.

Для этого необходимо зайти в Windows search и написать «среда», вы увидите «Редактировать системные переменные среды», нажмите на нее:

Изменение переменных средыَ Появится новое окно, и нажмите на "Переменные среды...":

Свойства системыВ новом окне вы можете выбрать системные или пользовательские переменные и найти переменную PATH для редактирования:

Найдена переменная PATHПосле того, как вы нажмете редактировать на любой переменной, перейдите и добавьте путь к тому, где вы установили wkhtmltopdf, в переменную PATH:

wkhtmltopdf добавлен в путьПосле того, как вы это сделаете, нажмите кнопку OK и закройте предыдущие окна, и все готово.

На Linux
Если вы используете Linux, это намного проще, так как он будет автоматически добавлен в PATH с помощью вашего менеджера пакетов.

Ниже приведена команда для Ubuntu/Debian:

$ apt update
$ apt install wkhtmltopdf
А ниже приведено для Debian/CentOS:

$ sudo yum makecache --refresh
$ sudo yum -y install wkhtmltopdf
На macOS
Вы можете просто установить его с помощью brew:

$ brew install Caskroom/cask/wkhtmltopdf
Преобразование HTML из URL в PDF
pdfkit проделал большую работу по обертыванию wkhtmltopdf в Python; мы используем легкие методы для выполнения таких сложных задач. Давайте установим его:

$ pip install pdfkit
Например, давайте преобразуем страницу поиска Google в PDF-документ:

import pdfkit

# directly from url
pdfkit.from_url("https://google.com", "google.pdf", verbose=True)
print("="*50)
Первым аргументом функции from_url() является URL-адрес, который требуется преобразовать, а вторым аргументом является имя документа PDF, которое вы хотите создать. Вот выходной PDF-документ:

Гугл PDF

Преобразование локального HTML-файла в PDF
Вы также можете преобразовать локальный HTML-файл на вашем компьютере в PDF-документ; Вот как это сделать:

# from file
pdfkit.from_file("webapp/index.html", "index.pdf", verbose=True, options={"enable-local-file-access": True})
print("="*50)
Папка webapp/ (в которой вы можете просмотреть его здесь) содержит индекс.html, его стиль.css CSS-файл и образец изображения.png.

Вот содержимое индекса.html:

<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]>      <html class="no-js"> <!--<![endif]-->
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="style.css">
        <style>
            table, th, td {
                border: 1px solid black;
            }
        </style>
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="#">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
        <img src="image.png" alt="Python logo">
        <p>Sample text here. Random HTML table that is styled with CSS:</p>
        <table bordered>
            <thead>
                <th>ID</th>
                <th>Name</th>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Abdou</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Rockikz</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>John</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Doe</td>
                </tr>
            </tbody>
        </table>
        <p class="red-text">This should be a red paragraph.</p>
    </body>
</html>
Мы используем функцию from_file(), первым аргументом является расположение HTML-файла, а вторым - результирующий путь к PDF-документу, мы устанавливаем enable-local-file-access значение True в параметре options, чтобы разрешить локальный доступ к файлам из этого HTML-файла к изображениям и файлам CSS / JS.

Вот содержимое индекса.pdf:

Преобразование локального HTML-файла в PDF-документ на Python

Преобразование строки HTML в PDF
Наконец, вы также можете преобразовать HTML-содержимое из строки Python в документ PDF:

# from HTML content
pdfkit.from_string("<p><b>Python</b> is a great programming language.</p>", "string.pdf", verbose=True)
print("="*50)
Вот содержимое строки.pdf:

Конвертированное HTML-содержимое в PDF на PythonЗаключение
Удивительно, я надеюсь, что этот учебник был полезен, чтобы вы начали работу с инструментом wkhtmltopdf, который помогает конвертировать HTML из URL-адреса, локального файла или строки в PDF-документ на Python с помощью библиотеки-оболочки pdfkit.

Вы можете получить полный код здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Узнайте также: Как конвертировать PDF в Docx в Python