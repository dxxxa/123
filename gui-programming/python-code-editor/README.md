# [How to Make a Python Code Editor using Tkinter in Python](https://www.thepythoncode.com/article/python-code-editor-using-tkinter-python)
##
# [[] / []]()
В этом уроке мы создадим простой редактор кода для скриптов Python, который поддерживает выполнение кода с помощью сочетания клавиш и подсветки синтаксиса, что стало возможным с помощью regex. Расширенные функции, такие как сохранение и загрузка файлов Python, оставлены для создания, хотя мы сделали эту функцию в учебнике текстового редактора.

Импорт
Для этой программы нам нужен tkinter для пользовательского интерфейса, ctypes для увеличения DPI, re для подсветки синтаксиса и os для запуска программы:

from tkinter import *
import ctypes
import re
import os

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)
Настройка
После того, как мы импортировали необходимые модули, мы настраиваем Tkinter с помощью функции Tk(), а затем устанавливаем начальный размер окна методом geometry().

# Setup Tkinter
root = Tk()
root.geometry('500x500')
Затем мы определяем переменную, которая будет содержать предыдущее содержимое области редактирования. Мы будем использовать его, чтобы гарантировать, что подсветка синтаксиса перерисовывается только в том случае, если содержимое действительно изменилось. Мы также можем использовать это для создания функции сохранения.

Затем мы определяем цвета для различных типов токенов и фона. Мы также устанавливаем шрифт на Consolas, монотипию, часто используемую в кодировании. Для цветов мы используем функцию RGB, определенную в этой статье редактора markdown, которая преобразует кортежи RGB в шестнадцатеричные значения. Это сделано потому, что Tkinter не поддерживает RGB, но RGB более читаем, чем шестнадцатеричный:

previousText = ''

# Define colors for the variouse types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
font = 'Consolas 15'
После этого мы вводим цвета в использование, сохраняя их во вложенном списке с подходящим регулярным выражением. Итак, вы видите, что первый предназначен для ключевых слов, а следующие два - для строк с " и ' и последний - для комментариев с хэштегом #.

В другой функции, которая будет вызываться каждый раз при возникновении изменений, мы выделим текст, используя этот список:

# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]
Виджеты
Продолжая, мы делаем editArea, который является просто текстовым виджетом. Они довольно мощные, когда дело доходит до выделения, потому что мы можем определить теги со всеми видами стилей и применить эти стили к определенным диапазонам внутри виджета. Позже мы увидим, как это делается на практике.

Для этого виджета «Текст» мы устанавливаем фон и цвет текста. Нам также нужно задать цвет каретики с параметром insertbackground. Чтобы добавить набивку, мы устанавливаем ширину границы на 30, а рельеф на FLAT. Это просто означает, что граница не будет иметь линии. Наконец, мы также устанавливаем шрифт.

# Make the Text Widget
# Add a hefty border width so we can achieve a little bit of padding
editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    borderwidth=30,
    font=font
)
Затем мы размещаем виджет, вызывая его функцию pack(). Мы устанавливаем для заливки значение BOTH и расширяем значение true (или единицу), поэтому виджет будет охватывать все окно, даже если его размер изменен. После этого мы также вставляем некоторый начальный текст с помощью метода insert():

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    expand=1
)

# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """from argparse import ArgumentParser
from random import shuffle, choice
import string

# Setting up the Argument Parser
parser = ArgumentParser(

    prog='Password Generator.',
    description='Generate any number of passwords with this tool.'
)
""")
Затем мы также привязываем KeyRelease на editArea к функции изменений, которую мы определим позже. Он будет обрабатывать замену тегов.

Затем мы также устанавливаем Control-r для вызова функции execute, которая будет запускать программу, как следует из ее названия. Затем вызываем функцию, которая все подсвечивает и запускает программу:

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Bind Control + R to the exec function
root.bind('<Control-r>', execute)

changes()
root.mainloop()
Имейте в виду, что функции, используемые здесь, определены заранее.

Функция выполнения
Теперь перейдем к функции, которая фактически запускает программу. Это вызовется, когда пользователь нажмет control + r. В функции мы просто открываем файл с именем run.py, который будет временно хранить код, который мы получаем с get(start, end),а затем запускаем этот файл с start cmd /K "python run.py". Мы делаем это таким образом, поэтому открывается новое окно командной строки. Мы хотим, чтобы программа работала отдельно от текущей.

# Execute the Programm
def execute(event=None):

    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    # Start the File in a new CMD Window
    os.system('start cmd /K "python run.py"')
Функция "Изменение и поиск шаблона"
Теперь о функции changes(), которая будет обрабатывать подсветку синтаксиса. Он очень похож на функцию changes() из этой статьи, с ключевым отличием в том, что она редактирует тот же текстовый виджет, из которого он получает текст.

В функции мы начинаем с проверки, совпадает ли текущее содержимое виджета «Текст» с предыдущим текстом. Это делается для того, чтобы не перерисовывать излишне:

# Register Changes made to the Editor Content
def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        return
Затем мы зацикливаемся на всех используемых тегах в виджете и удаляем их с помощью tag_remove():

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")
Затем мы зацикливаемся на заменах и далее зацикливаемся на возвращаемом значении функции search_re(). Позже мы рассмотрим эту функцию. Затем мы добавляем тег в каждую позицию. Мы используем переменную i, чтобы присвоить всем тегам уникальное имя:

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i+=1
И последнее, но не менее важное: мы также сохраняем текущее значение виджета в переменную previousText:

    previousText = editArea.get('1.0', END)
Теперь давайте также рассмотрим функцию search_re(). Он вернет все позиции шаблона в тексте. Итак, мы начнем со списка, в котором будут храниться эти позиции. Затем зацикливайтесь на строках текста и на результате finditer(), затем добавьте каждое совпадение начало и конец списка так же, как позиции написаны в виджетах Tkinter Text:

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches
Витрина
Заключение
Отлично! Вы успешно создали редактор кода Python! Посмотрите, как вы можете добавить дополнительные функции в эту программу, такие как сохранение и открытие .py файлов.