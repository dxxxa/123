# [How to Make a Rich Text Editor with Tkinter in Python](https://www.thepythoncode.com/article/create-rich-text-editor-with-tkinter-python)
##
# [[] / []]()
Идея
В этой статье мы сделаем простой редактор форматированного текста, где мы можем установить несколько предопределенных стилей для частей текста через графический интерфейс пользователя (GUI).

Мы сохраним эту информацию и сделаем так, чтобы пользователь мог ее загрузить. Это будет немного похоже на текстовый редактор, который мы создали ранее. Мы будем использовать текстовый виджет Tkinter и его функциональность tag, чтобы сделать редактор. Виджет «Текст» похож на обычную текстовую область, но он позволяет нам стилизовать определенные части текста по-разному с помощью тегов. Мы реализуем наш собственный формат файла, который в основном является просто JSON.

Импорт
Для этой программы нам, очевидно, понадобится Tkinter для пользовательского интерфейса; Нам также нужно получить askopenfilename и asksaveasfilename из tkinter.filedialog отдельно, чтобы мы могли запросить у пользователя путь к файлу. Мы получаем некоторые функции от functools и json, которые будут полезны позже. Мы также обеспечиваем высокий DPI с ctypes:

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import ctypes
from functools import partial
from json import loads, dumps

ctypes.windll.shcore.SetProcessDpiAwareness(True)
Настройка
Давайте сначала настроим! Мы начинаем с создания нового объекта Tk(), представляющего окно верхнего уровня нашего приложения. Затем мы устанавливаем начальную размерность этого окна, которое сохраняется в корневой переменной с помощью метода geometry(). Затем мы определяем переменную, содержащую имя приложения.

Мы сохраняем эту информацию, чтобы иметь согласованное название для окна позже. Мы будем менять это часто.

# Setup
root = Tk()
root.geometry('600x600')

# Used to make title of the application
applicationName = 'Rich Text Editor'
root.title(applicationName)
Затем мы инициируем переменную, содержащую путь к текущему файлу. Мы также устанавливаем начальный каталог для диалоговых окон файлов.

И последнее, но не менее важное: мы определяем кортеж, содержащий больше кортежей, которые будут типами файлов, которые можно выбрать в диалоговом окне файла. Первый элемент во вложенном кортеже — это имя, а второй — шаблон имени файла. Если вы хотите сделать так, чтобы пользователь мог выбрать любой файл, заканчивающийся на .rte, вы пишете *.rte:

# Current File Path
filePath = None
# initial directory to be the current directory
initialdir = '.'
# Define File Types that can be choosen
validFileTypes = (
    ("Rich Text File","*.rte"),
    ("all files","*.*")
)
Затем мы определяем Bahnschrift как шрифт для текстовой области, которую мы позже вставляем, и мы определяем заполнение для той же текстовой области.

После этого мы инициируем переменную под названием document, которая будет содержать информацию о текущем документе. И последнее, но не менее важное: мы определяем содержимое по умолчанию для этого документа. Это то, что мы сохраняем внутри файлов. Ключ содержимого — это текст, а ключ тегов будет удерживать позиции каждого тега, используемого в документе:

# Setting the font and Padding for the Text Area
fontName = 'Bahnschrift'
padding = 60
# Infos about the Document are stored here
document = None
# Default content of the File
defaultContent = {
    "content": "",
    "tags": {
        'bold': [(), ()]
    },
}
Ниже приведены некоторые теги, которые можно использовать в документе. Словарь можно просто вставить в функцию tag_configure() с помощью соответствующих клавиш. Чтобы сделать шрифт полужирным, добавляем жирный шрифт в конец описания шрифта.

Как видите, мы тоже делаем это курсивом. Затем мы добавляем тег кода, для которого шрифт установлен в consolas, а цвет фона — в светло-серый.

Для цвета мы используем функцию, которая преобразует RGB в шестнадцатеричный. Это тот, который взят из этого учебника. Затем мы также определяем теги, где размер шрифта больше, и теги, в которых изменяются цвета фона и текста. Изменяем цвет текста клавишей переднего плана.

# Add Different Types of Tags that can be added to the document.
tagTypes = {
    # Font Settings
    'Bold': {'font': f'{fontName} 15 bold'},
    'Italic': {'font': f'{fontName} 15 italic'},
    'Code': {'font': 'Consolas 15', 'background': rgbToHex((200, 200, 200))},
    # Sizes
    'Normal Size': {'font': f'{fontName} 15'},
    'Larger Size': {'font': f'{fontName} 25'},
    'Largest Size': {'font': f'{fontName} 35'},
    # Background Colors
    'Highlight': {'background': rgbToHex((255, 255, 0))},
    'Highlight Red': {'background': rgbToHex((255, 0, 0))},
    'Highlight Green': {'background': rgbToHex((0, 255, 0))},
    'Highlight Black': {'background': rgbToHex((0, 0, 0))},
    # Foreground /  Text Colors
    'Text White': {'foreground': rgbToHex((255, 255, 255))},
    'Text Grey': {'foreground': rgbToHex((200, 200, 200))},
    'Text Blue': {'foreground': rgbToHex((0, 0, 255))},
    'Text green': {'foreground': rgbToHex((0, 255, 0))},
    'Text Red': {'foreground': rgbToHex((255, 0, 0))},
}
Виджеты
Далее мы настраиваем виджеты нашей программы. Начнем с textArea, где пользователь пишет свои вещи. Виджет называется Текст; устанавливаем его master в качестве корня и определяем шрифт.

Мы также устанавливаем рельеф на FLAT, чтобы не было контура. Мы можем использовать эту константу таким образом, потому что мы импортировали все из Tkinter.

Затем мы помещаем виджет с помощью метода pack(), устанавливаем fill на BOTH и расширяем значение TRUE. Это будет единственный виджет, поэтому он должен охватывать все окно. Мы также добавляем некоторую набивку на обеих осях с padx и pady.

Привязываем любую клавишу нажатием на этот виджет, чтобы вызвать обратный вызов keyDown. Это сделано для того, чтобы мы могли регистрировать изменения в текстовом контенте. Мы также вызываем функцию resetTags(), которая сделает теги пригодными для использования в редакторе:

textArea = Text(root, font=f'{fontName} 15', relief=FLAT)
textArea.pack(fill=BOTH, expand=TRUE, padx=padding, pady=padding)
textArea.bind("<Key>", keyDown)

resetTags()
Продолжая, мы сделаем меню, которое появится в верхней части окна, где мы сможем выбрать теги, сохранить и открыть файлы. Мы делаем это, создавая и устанавливая меню в окне верхнего уровня следующим образом:

menu = Menu(root)
root.config(menu=menu)
Затем мы добавляем каскад в это меню, создавая другое меню и добавляя его в главное меню с add_cascade(). Для этого вложенного меню мы устанавливаем отрыв на 0, потому что мы не хотим иметь возможность разбить меню окна.

Добавляем к нему три команды; Открыть, сохранить и выйти. Для Open и Save мы устанавливаем функцию partial() в качестве ее команды. Это вызовет функцию fileManager(), которая будет обрабатывать взаимодействие с файлом с открытым или сохраненным как действие. Мы используем функцию partial(), потому что только таким образом мы можем предоставить аргументы.

Для exit мы просто вызываем root.quit(). Но мы также связываем элементы управления o и элементы управления s в качестве сочетаний клавиш для меню с bind_all():

fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label="Open", command=partial(fileManager, action='open'), accelerator='Ctrl+O')
root.bind_all('<Control-o>', partial(fileManager, action='open'))

fileMenu.add_command(label="Save", command=partial(fileManager, action='save'), accelerator='Ctrl+S')
root.bind_all('<Control-s>', partial(fileManager, action='save'))

fileMenu.add_command(label="Exit", command=root.quit)
Затем мы добавляем еще один каскад, который содержит команды для форматирования. Мы зацикливаемся на тегах, которые мы определили ранее, и создаем команду для каждого из них. Мы предоставляем функцию tagToggle() с пониженным именем тега в качестве аргумента. Эта функция будет обрабатывать стилизацию:

formatMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Format", menu=formatMenu)

for tagType in tagTypes:
    formatMenu.add_command(label=tagType, command=partial(tagToggle, tagName=tagType.lower()))
В конце программы нам нужно просто вызвать функцию main loop на корне, чтобы программа начала работать:

root.mainloop()
Функции
Теперь давайте рассмотрим все функции, которые используются в этой программе.

Сброс тегов
Эта функция сбросит все теги textArea. Во-первых, мы зацикливаем все используемые теги и удаляем их с помощью tag_remove(). Затем мы зацикливаемся на всех тегах, определенных в начале программы, и добавляем их пониженное имя и все свойства с помощью функции tag_configure():

def resetTags():
    for tag in textArea.tag_names():
        textArea.tag_remove(tag, "1.0", "end")

    for tagType in tagTypes:
        textArea.tag_configure(tagType.lower(), tagTypes[tagType])
Обработка ключевых событий
Эта функция будет вызываться каждый раз, когда нажимается какая-либо клавиша. Если это так, мы можем предположить, что изменения были внесены в текстовую область, поэтому мы добавляем звездочку в заголовок пути к файлу окна. Мы могли бы сделать больше в этой функции, но на данный момент это все:

def keyDown(event=None):
    root.title(f'{applicationName} - *{filePath}')
Функция переключения тегов
Эта функция срабатывает, когда пользователь нажимает одну из кнопок форматирования. Он будет применять теги к текущему выделению в textArea.

Логика не обязательно должна быть такой большой, потому что она довольно умна в размещении и удалении тегов. Внутри мы сначала сохраняем две строки в переменную: 'sel.first' и 'sel.last' просто сообщаем tag_remove() и tag_add(), что мы хотим принять текущий выбор. Теперь, если тег имеет диапазон, который заключает начало выбора пользователя, мы удаляем тег, в котором находится выделение. Если нет, он просто добавит этот тег в указанную позицию.

def tagToggle(tagName):
    start, end = "sel.first", "sel.last"

    if tagName in textArea.tag_names('sel.first'):
        textArea.tag_remove(tagName, start, end)
    else:
        textArea.tag_add(tagName, start, end)
Функция файлового менеджера
Теперь перейдем к функции файлового менеджера. Это, безусловно, самая большая функция, так как она будет открывать и сохранять наши файлы .rte. Таким образом, он будет декодировать и кодировать теги и их положение.

Он будет принимать параметр события, который никогда не используется, и действие, которое определяет, хотим ли мы сохранить или открыть файл:

# Handle File Events
def fileManager(event=None, action=None):
    global document, filePath
Поэтому, если действие открыто, мы сначала хотим спросить пользователя, какие файлы он хочет. Мы можем сделать это с помощью askopenfilename(). Мы также можем указать допустимые типы файлов и исходный каталог. Сохраняем путь:

# Open
    if action == 'open':
        # ask the user for a filename with the native file explorer.
        filePath = askopenfilename(filetypes=validFileTypes, initialdir=initialdir)
Затем открываем файл и считываем его содержимое в переменную документа. Имейте в виду, чтобы проанализировать его, потому что это будет JSON. Затем мы очищаем текстArea и вставляем содержимое:

        with open(filePath, 'r') as f:
            document = loads(f.read())
        # Delete Content
        textArea.delete('1.0', END)
        # Set Content
        textArea.insert('1.0', document['content'])
        # Set Title
        root.title(f'{applicationName} - {filePath}')
Продолжая, мы сбрасываем теги и добавляем их через цикл для цикла. Они должны храниться внутри документа во вложенном виде:

        # Reset all tags
        resetTags()
        # Add To the Document
        for tagName in document['tags']:
            for tagStart, tagEnd in document['tags'][tagName]:
                textArea.tag_add(tagName, tagStart, tagEnd)
Если пользователь хочет сохранить, мы устанавливаем документ в качестве содержимого по умолчанию и вставляем в него текстовое содержимое:

    elif action == 'save':
        document = defaultContent
        document['content'] = textArea.get('1.0', END)
Затем мы зацикливаемся на всех тегах и добавляем имя каждого тега в качестве ключа к документу. Затем мы зацикливаемся на всех диапазонах этого тега и добавляем их. Они возвращаются странным образом, поэтому нам приходится делать некоторые запутанные вещи, чтобы получить каждую пару:

        for tagName in textArea.tag_names():
            if tagName == 'sel': continue

            document['tags'][tagName] = []
            ranges = textArea.tag_ranges(tagName)
            for i, tagRange in enumerate(ranges[::2]):
                document['tags'][tagName].append([str(tagRange), str(ranges[i+1])])
Теперь, если путь к файлу не задан, мы должны спросить пользователя еще раз:

        if not filePath:
            # ask the user for a filename with the native file explorer.
            newfilePath = asksaveasfilename(filetypes=validFileTypes, initialdir=initialdir)
            # Return in case the User Leaves the Window without
            # choosing a file to save
            if newfilePath is None: return
            filePath = newfilePath
Затем мы добавляем .rte к пути на случай, если его там нет. Наконец, мы сохраняем закодированный контент и снова изменяем заголовок:

        if not filePath.endswith('.rte'):
            filePath += '.rte'
        with open(filePath, 'w') as f:
            print('Saving at: ', filePath)  
            f.write(dumps(document))
        root.title(f'{applicationName} - {filePath}')
Витрина
В GIF ниже вы видите программу в действии.

 



Заключение
Отлично! Вы успешно создали простой редактор форматированного текста с помощью кода Python! Узнайте, как добавить в эту программу дополнительные функции, такие как Экспорт в HTML или PDF.