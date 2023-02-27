# [How to Minify CSS with Python](https://www.thepythoncode.com/article/minimize-css-files-in-python)
To run this:
- `pip install -r requirements.txt`.
- Put your CSS file in the `style` folder.
- Put your HTML file in the current (root) folder.
- Run `python minimize.py`
- A new file will appear named `min.css` in the current working folder.
##
# [[] / []]()
В этой статье мы создадим программу Python, которая будет искать классы, используемые во всех HTML-файлах в проекте, а затем искать и компилировать эти файлы из css-файлов. Программа будет служить определенной цели, так как она будет строго соответствовать классам; это означает, что bg-black не будет bg-black:hover, используемые классы должны отображаться в таблицах стилей по мере их использования.

Этот способ минимизации полезен для служебных классов, таких как width-800px или color-grey-800, которые изменяются только в свойстве. Теперь, возможно, ваши служебные классы также влекут за собой что-то вроде этого шаблона: child-margin-2rem, который в таблице стилей на самом деле является child-margin-2rem > *, это не будет соответствовать по умолчанию, но мы дадим возможность заменить такие шаблоны соответствующим селектором.

Наконец, вы можете изменить код, чтобы минимизированный код лучше работал для вашего случая, или вы даже можете переделать его самостоятельно с полученными знаниями.

Мы будем использовать библиотеку CSS под названием CSSUtils, которая позволяет нам анализировать, читать и писать CSS.

Импорт
Давайте начнем с модулей и библиотек, которые мы должны импортировать для нашей маленькой программы. Наиболее важным будет cssutils, который должен быть загружен с pip install cssutils. Мы также хотим импортировать re, os, time. Мы получаем модуль ведения журнала просто для того, чтобы отключить ведение журнала, потому что cssutils выдает много ошибок. Затем мы очищаем консоль с помощью os.system("cls") и сохраняем время запуска программы в переменной.

import cssutils
import re
import logging
import os
import time
cssutils.log.setLevel(logging.CRITICAL)

startTime = time.time()
os.system('cls')
Получение файлов
Во-первых, мы получаем списки файлов, заканчивающихся на .html и .css. Мы сохраняем эти списки на потом.

htmlFiles = getFilesByExtension('.html', '.')

cssFiles = getFilesByExtension('.css', 'style')
Давайте также рассмотрим функцию, которая ищет все эти файлы. Имейте в виду, что он должен быть определен перед его использованием. Здесь мы используем os.walk(), который получает путь и возвращает данные о каждом подкаталоге и самом каталоге.

Нам нужны только файлы, которые являются третьим элементом возвращенного кортежа. Мы зацикливаемся на них, и если они заканчиваются указанным расширением, мы добавляем их в список foundFiles. Наконец, нам также необходимо вернуть этот список:

def getFilesByExtension(ext, root):
    foundFiles = []
    for root, directories, files in os.walk(root):
        for f in files:
            if f.endswith(ext):
                # os.path.join(root, f) is the full path to the file
                foundFiles.append(os.path.join(root, f)) 
    return foundFiles
Поиск всех используемых классов
Далее мы хотим найти все используемые классы во всех HTML-файлах. Для этого мы сначала создаем словарь для хранения имени каждого класса в виде элемента, чтобы в конце концов у нас не было дубликатов.

Затем мы перебираем все HTML-файлы, и для каждого из них мы получаем содержимое, используя регулярное выражение, чтобы найти все строки класса.

Продолжая, мы разделяем каждую из этих найденных строк, потому что классы разделены пробелом. Наконец, мы возвращаем ключи найденного словаря списков, которые являются классами.

usedClasses = findAllCSSClasses()

def findAllCSSClasses():
    usedClasses = {}
    # Find all used classes
    for htmlFile in htmlFiles:
        with open(htmlFile, 'r') as f:
            htmlContent = f.read()
        regex = r'class="(.*?)"'
        # re.DOTALL is needed to match newlines
        matched = re.finditer(regex, htmlContent, re.MULTILINE | re.DOTALL) 
        # matched is a list of re.Match objects
        for i in matched:
            for className in i.groups()[0].split(' '): # i.groups()[0] is the first group in the regex
                usedClasses[className] = ''
    return list(usedClasses.keys())
Перевод используемых классов
Теперь мы переводим некоторые классы; это полезно, если имя класса не будет точно совпадать с селектором, но оно следует шаблону, как и все классы, начинающиеся с дочернего - > * добавлены к их селектору, и здесь мы обрабатываем это. Мы определяем каждый перевод в списке, где первым элементом является regex, а вторым - замена:

# Use Translations if the class names in the Markup don't exactly 
# match the CSS Selector ( Except for the dot at the beginning. )
translations = [
    [
        '@',
        '\\@'
    ],
    [
        r"(.*?):(.*)",
        r"\g<1>\\:\g<2>:\g<1>",
    ],
    [
        r"child(.*)",
        "child\\g<1> > *",
    ],
]

usedClasses = translateUsedClasses(usedClasses)
Затем в функции мы зацикливаемся на каждом регулярном выражении для каждого класса, чтобы каждая трансляция потенциально применялась к имени каждого класса. Затем мы просто применяем замену методом re.sub().

def translateUsedClasses(classList):
    for i, usedClass in enumerate(classList):
        for translation in translations:
            # If the class is found in the translations list, replace it
            regex = translation[0]
            subst = translation[1]
            if re.search(regex, usedClass):
                # re.sub() replaces the regex with the subst
                result = re.sub(regex, subst, usedClass, 1, re.MULTILINE) # 1 is the max number of replacements
                # Replace the class in the list
                classList[i] = result
    return classList
Получение использованных классов из таблиц стилей
После этого мы получаем определение стиля из таблиц стилей с cssutils. Прежде чем мы зацикливаемся на найденных таблицах стилей, мы сначала определяем путь к минимизированному CSS, который в данном случае является мин.css, мы также создаем переменную под названием newCSS, которая будет содержать новое содержимое CSS.

output = 'min.css'

newCSS = ''
Мы продолжаем зацикливаться на всех CSS-файлах. Мы анализируем каждый файл с помощью cssutils.parsefile(path) и получаем все правила в таблице стилей с помощью пользовательской функции flattenStyleSheet(), позже мы рассмотрим, как она работает, но по сути она поместит все правила, скрытые внутри медиазапросов, в тот же список, что и правила верхнего уровня. затем мы определяем список, который будет содержать все имена селекторов, которые не являются классами, с которыми мы сталкиваемся. Мы делаем это, потому что не следует упускать из виду что-то вроде ввода.

Затем мы зацикливаемся на каждом правиле и каждом классе, и если селектор и текст селектора правила совпадают, мы добавляем весь CSS-текст правила в строку newCSS. Нам просто нужно следить за тем, есть ли у правила родительское правило, которое будет медиа-запросом. Мы делаем то же самое для всех правил, не начиная с точки:

for cssFile in cssFiles:
    # Parse the CSS File
    sheet = cssutils.parseFile(cssFile)
    rules = flattenStyleSheet(sheet)
    noClassSelectors = []
    for rule in rules:
        for usedClass in usedClasses:
            if '.' + usedClass == rule.selectorText:
                # If the class is used in the HTML, add it to the new CSS
                usedClasses.remove(usedClass) # Remove the class from the list
                if rule.parentRule:
                    newCSS += str(rule.parentRule.cssText)
                else:
                    newCSS += str(rule.cssText)
        if rule.selectorText[0] != '.' and not rule.selectorText in noClassSelectors: 
            # If the selector doesnt start with a dot and is not already in the list,
            # add it
            noClassSelectors.append(rule.selectorText)
            if rule.parentRule:
                newCSS += str(rule.parentRule.cssText)
            else:
                newCSS += str(rule.cssText)
функция flattenStyleSheet()
Давайте быстро перейдем к функции flattenstylesheet(). Он получит лист в качестве параметра и зациклится на каждом правиле на этом листе. Затем он проверит, является ли правило просто правилом стиля или правилом мультимедиа, чтобы оно могло добавить все правила в одномерный список.

def flattenStyleSheet(sheet):
    ruleList = []
    for rule in sheet.cssRules:
        if rule.typeString == 'MEDIA_RULE':
            ruleList += rule.cssRules
        elif rule.typeString == 'STYLE_RULE':
            ruleList.append(rule)
    return ruleList
Сохранение нового CSS
Наконец, мы минируем CSS дальше, удаляя разрывы строк и двойные пробелы, и мы сохраняем этот новый CSS в указанном месте:

newCSS = newCSS.replace('\n', '')
newCSS = newCSS.replace('  ', '')

with open(output, 'w') as f:
    f.write(newCSS)

print('TIME: ', time.time() - startTime)
Запуск программы
Вы должны поместить свои CSS-файлы в папку «style», чтобы запустить программу. После этого поместите HTML-файлы в текущий рабочий каталог (такой же, как .py файл). Затем выполните:

$ python minimize.py
TIME TOOK:  0.04069924354553223
Это распечатает время, затраченное на процесс, и в текущем рабочем каталоге появится новый файл min.css.

Заключение
Отлично! Вы успешно создали CSS Minifier с помощью кода Python! Узнайте, как добавить дополнительные функции в эту программу, такие как конфигурационный файл для дополнительных параметров. Кроме того, имейте в виду, что эта программа может нуждаться в некоторой оптимизации, поскольку она работает очень медленно на более крупных проектах.

Вы всегда можете обернуть весь код в функцию, чтобы сделать его более удобным, читаемым и расширяемым в ваших проектах.