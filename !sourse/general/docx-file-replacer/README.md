# [How to Replace Text in Docx Files in Python](https://www.thepythoncode.com/article/replace-text-in-docx-files-using-python)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
В этом уроке мы создадим простую программу командной строки, которую мы можем предоставить с .docx пути к файлу и словами, которые нуждаются в замене.

Импорт
Начнем с импорта.

Библиотека re здесь важна, потому что мы можем использовать ее функцию sub() для замены определенных выражений другим текстом в данной строке.

Нам также нужен модуль sys, чтобы мы могли получить аргументы командной строки с помощью sys.argv.

И последнее, но не менее важное: мы также получаем класс Document из docx, чтобы мы могли работать с файлами Word. Мы должны сначала загрузить его с:

$ pip install python-docx
Давайте начнем:

# Import re for regex functions
import re

# Import sys for getting the command line arguments
import sys

# Import docx to work with .docx files.
# Must be installed: pip install python-docx
from docx import Document
Проверка аргументов командной строки
Далее перейдем к аргументам командной строки. Мы хотим проверить, являются ли входные данные допустимыми.

Теперь, если список sys.argv короче трех элементов, мы знаем, что пользователь не предоставил достаточно информации. Первым аргументом всегда является путь к самому файлу Python. Вторым должен быть путь к файлу, в котором будет заменен текст.

Остальные аргументы будут парами, подобными этому text=replacewith, который говорит нам, что мы заменяем на что. Это то, что мы проверяем в цикле for.

В конце концов, мы также сохраняем путь к файлу в переменную, поэтому нам не нужно каждый раз вводить sys.argv[1].

# Check if Command Line Arguments are passed.
if len(sys.argv) < 3:
    print('Not Enough arguments where supplied')
    sys.exit()

# Check if replacers are in a valid schema
for replaceArg in sys.argv[2:]:
    if len(replaceArg.split('=')) != 2:
        print('Faulty replace argument given')
        print('-> ', replaceArg)
        sys.exit()

# Store file path from CL Arguments.
file_path = sys.argv[1]
Файлы Docx
Если файл заканчивается .docx мы знаем, что должны использовать класс docx. Сначала мы создаем новый объект Document, который мы предоставим вместе с нашим путем к файлу. Затем мы зацикливаемся на аргументах замены так же, как и для файлов .txt.

После этого мы прокручиваем абзацы документа прямо перед циклом через прогоны абзацев. Эти прогоны представляют диапазоны стилей документа; мы заменяем текст, а затем просто сохраняем документ методом save().

if file_path.endswith('.docx'):
    doc = Document(file_path)
    # Loop through replacer arguments
    occurences = {}
    for replaceArgs in sys.argv[2:]:
        # split the word=replacedword into a list
        replaceArg = replaceArgs.split('=')
        # initialize the number of occurences of this word to 0
        occurences[replaceArg[0]] = 0
        # Loop through paragraphs
        for para in doc.paragraphs:
            # Loop through runs (style spans)
            for run in para.runs:
                # if there is text on this run, replace it
                if run.text:
                    # get the replacement text
                    replaced_text = re.sub(replaceArg[0], replaceArg[1], run.text, 999)
                    if replaced_text != run.text:
                        # if the replaced text is not the same as the original
                        # replace the text and increment the number of occurences
                        run.text = replaced_text
                        occurences[replaceArg[0]] += 1
                    
    # print the number of occurences of each word
    for word, count in occurences.items():
        print(f"The word {word} was found and replaced {count} times.")
    
    # make a new file name by adding "_new" to the original file name
    new_file_path = file_path.replace(".docx", "_new.docx")
    # save the new docx file
    doc.save(new_file_path)
else:
    print('The file type is invalid, only .docx are supported')
Давайте запустим его на этом файле документа:

$ python docx_text_replacer.py doc.docx SYN=TEST Linux=Windows TCP=UDP
The word SYN was found and replaced 5 times.
The word Linux was found and replaced 1 times.
The word TCP was found and replaced 1 times. 
Я хотел заменить слово «SYN» на «TEST», «Linux» на «Windows», а «TCP» на «UDP» в документе, и это было успешно!

Заключение
Отлично! Вы успешно создали программу замены файлов с помощью кода Python! Узнайте, как добавить в эту программу дополнительные функции, например добавить дополнительные форматы файлов.