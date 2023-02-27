# [How to Build a YouTube Audio Downloader in Python](https://www.thepythoncode.com/article/build-a-youtube-mp3-downloader-tkinter-python)
##
# [[] / []]()
Ни для кого не секрет, что Python является мощным и наиболее используемым языком программирования. Его универсальный характер делает его популярным выбором для разработчиков во всем мире.

Эта статья для вас, если вы хотели создать свой собственный загрузчик MP3 из URL-адресов видео YouTube. В этой статье мы покажем вам, как использовать возможности Python для создания загрузчика MP3.

Если вы хотите загружать видео с YouTube на Python, есть аналогичный учебник по загрузке видео YouTube с желаемым качеством.

Мы проведем вас через создание собственного загрузчика MP3 с помощью Python. Мы начнем с обсуждения зависимостей, которые вам понадобятся для этого проекта. Затем мы перейдем к разработке графического пользовательского интерфейса для приложения. Наконец, мы покажем вам, как протестировать загрузчик MP3, чтобы убедиться, что он работает правильно. Итак, если вы готовы начать, давайте погрузимся!

В конце этой статьи мы собираемся создать шикарное приложение, которое выглядит следующим образом:

Мы сделаем каждый кусочек этого с нуля.

Вот оглавление:

Настройка среды
Проектирование графического интерфейса пользователя
Проектирование главного окна и холста
Определение стилей виджетов
Добавление логотипа MP3 и метки загрузчика
Создание метки и записи
Создание метки хода выполнения и индикатора выполнения
Создание кнопки «Загрузить MP3»
Реализация функции загрузки MP3-файла
Заключение
Настройка среды
Прежде всего, давайте установим основную библиотеку, которую мы будем использовать для загрузки аудиофайлов, pytube:

$ pip install pytube
Проектирование графического интерфейса пользователя
После установки необходимой библиотеки приступим к процессу проектирования графического интерфейса. Создайте новый файл Python и назовите его mp3_downloader.py; вы можете назвать его так, как вы хотите. Просто убедитесь, что имя файла имеет смысл. Откройте его и добавьте следующие импорты:

from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
import os
Давайте разберем импорт в фрагменте кода. Мы импортируем все из ткинтера; это делается с помощью символа *, затем мы импортируем ttk из tkinter, модуля для стилизации виджетов. Из pytube мы импортируем объект YouTube; это поможет нам извлечь аудио из видео YouTube, а затем загрузить этот аудиофайл.

Мы также импортируем messagebox из tkinter, таких как showinfo, showerror и askokcancel. Библиотека потоков поможет приложению выполнять задачи одновременно, такие как запуск окна и одновременное извлечение и загрузка аудиофайла. Наконец, мы импортируем библиотеку os; , чтобы преобразовать загруженный аудиофайл в файл .mp3 типа.

Проектирование главного окна и холста
Теперь, когда необходимый импорт был выполнен, давайте перейдем непосредственно к задаче проектирования графического интерфейса; мы начнем с проектирования главного окна и холста, поэтому чуть ниже импорта добавьте следующий код:

# creates the window using Tk() function
window = Tk()
# creates title for the window
window.title('MP3 Downloader')
# the icon for the application, this will replace the default tkinter icon
window.iconbitmap(window, 'icon.ico')
# dimensions and position of the window
window.geometry('500x400+430+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)
# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()
# this runs the app infinitely
window.mainloop()
Разбивая приведенный выше фрагмент кода, мы создаем главное окно, используя встроенный в Tkinter класс Tk(); затем мы даем ему заголовок, используя функцию title(). Функция iconbitmap() используется для добавления в окно значка, который заменяет значок Tkinter по умолчанию; убедитесь, что значок находится в той же папке, что и файл Python.

Чтобы задать размеры и положение главного окна, мы используем функцию geometry(). Для высоты и ширины у нас есть 500x400, а для позиционирования окна вертикально и горизонтально у нас есть 430+180. Мы хотим, чтобы размер окна не изменялся, поэтому для этого давайте использовать функцию resizable() с высотой и шириной, установленными на FALSE, это отключит кнопку развернуть /свернуть в окне.

Позаботившись о главном окне, мы создаем холст с помощью функции Canvas(); это виджет Tkinter, который действует как контейнер для других виджетов. Мы размещаем его внутри главного окна и придаем ему высоту 500 и ширину 400. Наконец, чтобы главное окно работало бесконечно, мы используем функцию mainloop(), поэтому окно будет открыто до тех пор, пока пользователь не закроет его.

Если мы запустим код, мы получим следующий результат:

Хотя холст не виден, вот как он помещается внутри главного окна:

Определение стилей виджетов
Прежде чем мы начнем создавать виджеты внутри холста, давайте, прежде всего, определим стили. Для этой задачи мы будем использовать модуль ttk. Чуть ниже холста добавьте следующий код:

"""Styles for the widgets"""
# style for the label 
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))
# style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
# style for the button
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')
Фрагмент кода использует ttk. Класс Style() для создания трех объектов стиля. После завершения каждого стиля мы используем функцию configure() для именования стилей; в нашем случае мы назвали стили TLabel, TEntry и TButton. Функция также принимает другие аргументы, такие как передний план и шрифт.

Добавление логотипа MP3 и метки загрузчика
Теперь, когда мы создали холст, содержащий все другие виджеты, и успешно определили стили виджетов, мы можем приступить к созданию виджетов. Сначала мы добавим логотип MP3 и текст Downloader. Для этого добавьте следующий код сразу после стилей:

 # loading the MP3 logo
logo = PhotoImage(file='mp3_icon.png')
# creates dimensions for the logo
logo = logo.subsample(2, 2)
# adding the logo to the canvas
canvas.create_image(180, 80, image=logo)
# the Downloader label just next to the logo
mp3_label = ttk.Label(window, text='Downloader', style='TLabel')
canvas.create_window(340, 125, window=mp3_label)
Давайте сведем код к минимуму, так что мы на одной странице. Мы загружаем иконку с помощью встроенной функции Tkinter PhotoImage(), а после загрузки иконки придаем ей размеры с помощью функции subsample() и добавляем ее на холст с помощью функции create_image(). Чтобы расположить иконку горизонтально, мы используем 180 и 80 по вертикали.

Рядом со значком мы добавляем метку с текстом Downloader с помощью ttk. Функция Label(); эта функция принимает окно, текст и стиль в качестве аргументов. Как обычно, мы также добавляем его на холст.

Выходные данные кода будут следующими:

Создание метки и записи
Теперь мы можем сделать Запись и ее Метку. Под меткой загрузчика добавьте следующий код:

# creating a ttk label
url_label = ttk.Label(window, text='Enter MP3 URL:', style='TLabel')
# creating a ttk entry
url_entry = ttk.Entry(window, width=72, style='TEntry')
# adding the label to the canvas
canvas.create_window(114, 200, window=url_label)
# adding the entry to the canvas
canvas.create_window(250, 230, window=url_entry)
Здесь мы создаем метку и запись с помощью ttk. Label() и ttk. Функции Entry(), эти два виджета добавляются на холст с помощью функции canvas create_window().

Запустив приведенный выше код, мы получаем следующий вывод:

Пока всё в порядке; приложение обретает форму.

Создание метки хода выполнения и индикатора выполнения
Поскольку мы хотим, чтобы отображался ход загрузки, мы добавим метку для отображения процента загрузки и размера файла, а под ним будет индикатор выполнения:

# creating the empty label for displaying download progress
progress_label = Label(window, text='')
# adding the label to the canvas
canvas.create_window(240, 280, window=progress_label)
# creating a progress bar to display progress
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
# adding the progress bar to the canvas
canvas.create_window(250, 300, window=progress_bar)
В приведенном выше коде мы создаем метку Tkinter по умолчанию с помощью функции Label(); он принимает окно и пустую строку в качестве текста. Затем мы делаем индикатор выполнения, используя ttk. Функция Progressbar(); эта функция принимает четыре аргумента: окно, ориентир, длина и режим. После создания этих виджетов мы добавляем их на холст.

С добавлением приведенного выше кода, вот что мы получаем сейчас:

Создание кнопки «Загрузить MP3»
Зайдя так далеко, у нас осталась только кнопка загрузки, поэтому под индикатором выполнения добавьте следующее:

# creating the button
download_button = ttk.Button(window, text='Download MP3', style='TButton')
# adding the button to the canvas
canvas.create_window(240, 330, window=download_button)
Приведенный выше код прост; мы создаем кнопку с помощью ttk. Функция Button() и аргументы, которые принимает функция, — это окно, текст и стиль. Наконец, мы добавляем его на холст.

Код даст нам следующий вывод:

Let us finish off the GUI design by making it possible for the application to ask the user whether to close it; we do not want the application to close without the user's confirmation. Just below the imports, add this code:

# the function for closing the application
def close_window():
    # if askokcancel is True, close the window
    if askokcancel(title='Close', message='Do you want to close MP3 downloader?'):
        # this distroys the window
        window.destroy()
Здесь функция close_window() уничтожит окно через функцию destroy(), если askokcancel имеет значение True, если это False, окно все равно будет работать. Чтобы эта функция сработала, нам нужно подключить ее к самому окну. Ниже этой строки:

window = Tk()
Добавьте следующую строку кода:

# this will listen to the close window event
window.protocol('WM_DELETE_WINDOW', close_window)
Функция protocol() принимает WM_DELETE_WINDOW, а функция close_window(). Логика всего этого заключается в том, что функция protocol() будет прослушивать событие закрытия окна. Если пользователь нажмет кнопку закрытия окна, сработает функция close_window().

Давайте протестируем и посмотрим, как приложение будет работать после модификации:

Если пользователь нажмет ok, значение askokcancel будет равно True, тем самым вызывая функцию destroy().

Реализация функции загрузки MP3-файла
Успешно разработав графический пользовательский интерфейс, мы теперь сосредоточимся на реализации функции загрузки MP3. Под функцией close_window() вставьте следующий код:

# the function to download the mp3 audio
def download_audio():
    # the try statement to excute the download the video code
    # getting video url from entry
    mp3_link = url_entry.get()
    # checking if the entry and combobox is empty
    if mp3_link == '':
        # display error message when url entry is empty
        showerror(title='Error', message='Please enter the MP3 URL')
    # else let's download the audio file  
    else:
        # this try statement will run if the mp3 url is filled
        try:
            # this function will track the audio file download progress
            def on_progress(stream, chunk, bytes_remaining):
                # the total size of the audio
                total_size = stream.filesize
                # this function will get the size of the audio file
                def get_formatted_size(total_size, factor=1024, suffix='B'):
                    # looping through the units
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total_size < factor:
                            return f"{total_size:.2f}{unit}{suffix}"
                        total_size /= factor
                    # returning the formatted audio file size
                    return f"{total_size:.2f}Y{suffix}"
                    
                # getting the formatted audio file size calling the function
                formatted_size = get_formatted_size(total_size)
                # the size downloaded after the start
                bytes_downloaded = total_size - bytes_remaining
                # the percentage downloaded after the start
                percentage_completed = round(bytes_downloaded / total_size * 100)
                # updating the progress bar value
                progress_bar['value'] = percentage_completed
                # updating the empty label with the percentage value
                progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                # updating the main window of the app
                window.update()
                
            # creating the YouTube object and passing the the on_progress function
            audio = YouTube(mp3_link, on_progress_callback=on_progress)     
            # extracting and downloading the audio file 
            output = audio.streams.get_audio_only().download()
            # this splits the audio file, the base and the extension
            base, ext = os.path.splitext(output)
		    # this converts the audio file to mp3 file
            new_file = base + '.mp3'
		    # this renames the mp3 file
            os.rename(output, new_file)
            # popup for dispalying the mp3 downlaoded success message
            showinfo(title='Download Complete', message='MP3 has been downloaded successfully.')
            # ressetting the progress bar and the progress label
            progress_label.config(text='')
            progress_bar['value'] = 0           
        # the except will run when an expected error occurs during downloading
        except:
            showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the MP3\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the MP3 link is valid')
                # ressetting the progress bar and the progress label
            progress_label.config(text='')
            progress_bar['value'] = 0
Мы создаем функцию download_audio(), в которой мы получаем MP3-адрес через функцию get(), и у нас есть оператор if, который проверяет, пуста ли запись. Если он пуст, мы отобразим окно сообщения об ошибке. В противном случае выполните инструкцию else. Внутри оператора else у нас есть блок try/except. Внутри оператора try происходит фактическая загрузка.

У нас есть функция on_progress() с потоком, блоком и bytes_remaining в качестве аргументов, эта функция будет отслеживать ход загрузки. Внутри функции on_progress() у нас есть еще одна функция под названием get_formatted_size(), которая предназначена для форматирования размера файла MP3 в удобочитаемый формат, такой как KBs, MBs, GBs, TB и т. Д.

После функции get_formatted_size() on_progress() получает форматированный размер путем вызова get_formatted_size() и вычисляет загруженные байты и процент выполненных. Загруженные байты и процент выполненных добавляются к пустой метке хода выполнения и индикатору выполнения соответственно. После всего этого мы обновляем окно с помощью функции update().

Теперь за пределами функции on_progress() мы создаем объект YouTube, который принимает URL-адрес mp3 и функцию on_progress(). После этого мы извлекаем аудиофайл из MP4-файла и загружаем его через следующую строку кода:

output = audio.streams.get_audio_only().download()
Поэтому, чтобы преобразовать этот аудиофайл в формате MP4 в фактический файл MP3, мы используем эту строку кода:

# this splits the audio file, the base and the extension
base, ext = os.path.splitext(output)
# this converts the audio file to mp3 file
new_file = base + '.mp3'
# this renames the mp3 file
os.rename(output, new_file)
После успешной загрузки аудиофайла и преобразования его в MP3 приложение отображает пользователю успешное сообщение, а метка хода выполнения и индикатор выполнения сбрасываются.

Сумев создать функцию download_audio(), создадим другую функцию и назовем ее downloadThread(). Основная цель этой функции заключается в том, что мы хотим, чтобы она запускала функцию download_audio() в виде потока, поскольку она обрабатывает множество задач одновременно. Итак, под функцией download_audio() вставьте следующие строки кода:

# the function to run the download_audio function as a thread   
def downloadThread():
    t1 = threading.Thread(target=download_audio)
    t1.start() 
Здесь мы просто создаем поток с помощью класса Thread(); целевым объектом потока является функция download_audio(). Для запуска потока мы используем функцию start().

Мы почти там, чтобы загрузить наш первый файл MP3; Единственная задача, с которой мы остаемся, это привязка кнопки Download MP3 с функцией downloadThread(), для этого отредактируйте download_button и сделайте его следующим образом:

download_button = ttk.Button(window, text='Download MP3', style='TButton', command=downloadThread)
Здесь, когда пользователь нажмет кнопку, сработает функция downloadThread(), это, в конце концов, вызовет функцию download_audio() и запустит ее как поток.

Откройте приложение и вставьте URL-адрес видео YouTube, аудиофайл которого вы хотите скачать, в поле ввода и нажмите кнопку; Если загрузка прошла успешно, вы получите следующий результат:

Если вы проверите папку проекта, вы увидите, что там есть файл MP3:



Предположим, пользователь нажимает кнопку, не вводя URL-адрес; Приложение выдаст следующие выходные данные:

Если пользователь вводит недопустимый URL-адрес, следующие выходные данные должны быть получены следующим образом:

И в случае, если у нас есть сломанное или нестабильное интернет-соединение, когда фактическая загрузка выполняется, это результат, который мы получаем:

Что ж, приложение, кажется, работает отлично!

Примечание: Что-то, достойное вашего внимания и заслуживающее упоминания здесь, некоторые видео YouTube, чьи MP3-файлы вы хотите загрузить, не будут загружены, если видео является прямой трансляцией, не разрешено, недоступно в вашем регионе или является премиум-видео и т. Д.

Заключение
Создание загрузчика MP3 - отличный способ изучить и освоить многие концепции Python. Эта статья содержит пошаговое руководство о том, как это сделать. Теперь мы надеемся, что вы многому научились из этой статьи и примените полученные знания в своих будущих проектах Python.