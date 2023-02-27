# [How to Make a File Explorer using Tkinter in Python](https://www.thepythoncode.com/article/create-a-simple-file-explorer-using-tkinter-in-python)
##
# [[] / []]()
В этой статье мы сделаем простой проводник файлов с Python и его GUI Library Tkinter. Мы перенимаем некоторые функции из стандартного проводника файлов, такие как редактирование строки, добавление сверху, открытие файлов с помощью их обычной программы и добавление новых файлов или папок.

Давайте начнем!

Импорт
Как всегда, мы импортируем необходимые библиотеки. We получить модуль ОС; это играет особую роль, так как мы выполняем все взаимодействия с файлами с его помощью, такие как получение всех файлов в каталог или добавление файлов. Импорт ctypes является необязательным; мы просто включаем высокий dpi (точек на дюйм). Вызов функции в последней строке сделает именно это. Это приведет к более плавной графике:

from tkinter import *
import os
import ctypes
import pathlib

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)
Настройка Ткинтера
Теперь мы настроили Tkinter. Начнем с создания нового объекта Tk(). После этого мы устанавливаем заголовок окна.

Далее настраиваем один столбец и одну строку. Эти две функции (grid_columnconfigure() и grid_rowconfigure()) гарантируют, что второй столбец и вторая строка развернуты. Мы разместим там наши самые важные виджеты, чтобы они получили много места. Имейте в виду, что вы можете вызвать эти функции на любом виджете контейнера.

root = Tk()
# set a title for our file explorer main window
root.title('Simple Explorer')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
Функции обработчика
После настройки Tkinter мы продолжим создавать некоторые функции, которые обрабатывают большинство вещей, происходящих, когда пользователь что-то делает.

Некоторые из этих функций имеют параметр event=None, и вы заметили, что эти параметры события не используются в функции. Это связано с тем, что функции вызываются из двух входов. Во-первых, есть вызовы из кнопок или меню, и эти виды вызовов не отправляют никаких аргументов в предоставленные командные функции.

С другой стороны, привязки клавиатуры будут отправлять событие клавиатуры в функцию, но нам не нужна эта информация. Этот параметр гарантирует, что функции будут вызываться правильно в любом случае.

Событие изменения Stringvar
Начнем с функции pathChange(). Это будет называться каждый раз, когда наш путь меняется. Мы привяжем к нему StringVar. Он обновит список файлов и папок и будет отвечать за их отображение.

Мы начнем с получения списка всех файлов и папок в заданном пути с помощью функции os.listdir(). После этого мы очищаем наш список с помощью метода delete(start, end). И последнее, но не менее важное: мы перебираем каждый элемент в списке каталогов и вставляем его в список с помощью метода insert(index, name).

def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        list.insert(0, file)
Изменение пути нажатием кнопки "Нажмите" или "Ввод"
Функция changePathByClick() выполняет то, что написано в поле: она обрабатывает, когда пользователь щелкает элемент в списке, а затем изменяет путь или открывает файл.

Начнем с получения имени выбранного элемента, объединив две функции. Мы предоставляем list.get() первое значение, возвращаемое list.curselection().

Последний возвращает массив всех выбранных элементов; вот почему нам нужен только первый пункт. Мы продолжаем, соединяя с os.path.join() этот выбранный файл или папку с нашим текущим путем, который хранится в StringVar.

Проверяем, является ли данный путь файлом с помощью функции os.path.isfile(path). Если это оказывается True, мы вызываем os.startfile(path) с нашим путем, чтобы открыть файл с помощью его стандартной программы. Если он имеет значение False, мы установим для StringVar новый путь, который запускает функцию pathChange(), которую мы определили ранее, и обновим отображаемые файлы.

def changePathByClick(event=None):
    # Get clicked item.
    picked = list.get(list.curselection()[0])
    # get the complete path by joining the current path with the picked item
    path = os.path.join(currentPath.get(), picked)
    # Check if item is file, then open it
    if os.path.isfile(path):
        print('Opening: '+path)
        os.startfile(path)
    # Set new path, will trigger pathChange function.
    else:
        currentPath.set(path)
Перемещение одной папки вверх
В changePathByClick() мы сделали так, чтобы мы могли вводить папки; теперь мы хотим обратного: мы хотим иметь возможность вернуться.

Здесь мы будем использовать родительский атрибут pathlib. Path() для получения родительской папки нашей текущей папки. После этого нам просто нужно вызвать функцию set(string) на нашем StringVar и установить для нее этот новый путь. Это снова вызовет функцию pathChange().

def goBack(event=None):
    # get the new path
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath
    currentPath.set(newPath)
    # simple message
    print('Going Back')
Создание и открытие всплывающего окна нового файла или папки
В этой функции мы сделаем всплывающее окно, которое появляется при нажатии кнопки меню.

Мы начинаем с получения глобальной переменной с именем top, которая определена вне функции, и нам нужно сделать это, чтобы другая функция имела доступ к этой переменной.

Он содержит объект окна, который выполнен в следующей строке с помощью Toplevel(). Поскольку это новое окно, оно также имеет функции title() и geometry(), которые задают имя и размеры окна.

Мы также устанавливаем для обеих осей значение, не изменяемое с помощью метода resizeable(False, False). После этого мы настраиваем несколько столбцов и делаем метку, которая говорит пользователю, что делать.

Мы определяем Entry(), который получает другой StringVar, который содержит нашу новую папку или файл. Это также делается для предоставления другой функции доступа к этой функции. В итоге делаем кнопку, которая вызывает эту функцию:

def open_popup():
    global top
    top = Toplevel(root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')
Новый файл или папка
Приведенный ниже обрабатывает создание новых файлов или папок.

Сначала мы начнем с проверки, является ли путь, предоставленный пользователем, файлом или путем. Мы не можем сделать это с помощью os.path.isfile(path), потому что он проверяет, существует ли файл.

Вот почему мы разделяем строку на '.' и проверяем, имеет ли результирующий массив другую длину, чем единица. Строка будет любить файл.txt приведет к True, а что-то вроде папки/пути — False. Если это имя файла, мы создаем его, просто открыв путь со встроенной функцией open(path, mode), потому что, если файл не существует, он его сделает. Если это имя папки, нам нужен модуль os и его функция mkdir(), чтобы создать новый каталог.

После этого закрываем всплывающее окно методом destroy(). и мы вызываем функцию pathChange(), чтобы каталог был обновлен:

def newFileOrFolder():
    # check if it is a file name or a folder
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange()

top = ''
Строковые переменные
Теперь мы сделали все необходимые функции, продолжим со строковыми переменными:

newFileName: новый файл, используемый при запросе на создание нового файла или папки.
currentPath: — переменная текущего пути. Любые изменения, внесенные в него, мы связываем с его методом trace().
# String variables
newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(
    root,
    name='currentPath',
    value=pathlib.Path.cwd()
)
# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)
Связанные с: Как создать программу для рисования на Python

Виджеты
Давайте настроим несколько виджетов! Мы начинаем с создания кнопки, которая поднимает папку вверх. Он вызывает метод goBack(), потому что мы предоставили ссылку на его параметр команды.

Затем мы помещаем его на сетку с помощью метода grid(). Параметр sticky означает, куда должен расширяться виджет. Мы поставляем его с NSEW, что означает, что он будет расширяться во всех направлениях.

После этого подключаем сочетание клавиш Alt-Up к той же функции, вызываемой кнопкой.

В конце концов, мы создаем Entry(), который удерживает путь, на котором мы сейчас находимся. Чтобы он правильно работал с StringVar, мы должны установить параметр textvariable для нашей строковой переменной. Мы также размещаем это на сетке и устанавливаем некоторые набивки с ipadx и ipady.

Button(root, text='Folder Up', command=goBack).grid(
    sticky='NSEW', column=0, row=0
)
# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)
Entry(root, textvariable=currentPath).grid(
    sticky='NSEW', column=1, row=0, ipady=10, ipadx=10
)
Следующий виджет - это список, который отображает файлы и папки текущего пути, и мы также привязываем некоторые события клавиатуры, которые происходят на нем, к нашей функции changePathByClick():

# List of files and folder
list = Listbox(root)
list.grid(sticky='NSEW', column=1, row=1, ipady=10, ipadx=10)
# List Accelerators
list.bind('<Double-1>', changePathByClick)
list.bind('<Return>', changePathByClick)
Последний виджет представляет собой простую строку меню с двумя кнопками, одна из которых открывает новое окно файла или папки, а другая завершает работу программы. Мы можем выйти из программы с помощью root.quit():

# Menu
menubar = Menu(root)
# Adding a new File button
menubar.add_command(label="Add File or Folder", command=open_popup)
# Adding a quit button to the Menubar
menubar.add_command(label="Quit", command=root.quit)
# Make the menubar the Main Menu
root.config(menu=menubar)
Главная петля
Теперь, прежде чем мы начнем основной цикл, мы вызываем функцию pathChange(), чтобы список был сгенерирован в первый раз:

# Call the function so the list displays
pathChange('')
# run the main program
root.mainloop()
Витрина
Давайте запустим его. Вы можете взглянуть на проводник в действии:

Демонстрация нашего проводника файлов, сделанного с помощью Python

Заключение
Отлично! Вы успешно создали простой проводник с помощью кода Python! Узнайте, как добавить в эту программу дополнительные функции, такие как переименование файлов или сортировка файлов и папок.

Если вы хотите узнать больше об использовании Tkinter, ознакомьтесь с этим учебником, где вы создаете приложение калькулятора вместе со многими функциями!