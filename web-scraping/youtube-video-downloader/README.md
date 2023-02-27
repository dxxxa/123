# [How to Make a YouTube Video Downloader in Python](https://www.thepythoncode.com/article/make-a-youtube-video-downloader-in-python)
##
# [[] / []]()
YouTube - отличная платформа, где вы можете найти тонны отличных видеоресурсов, будь то программирование, предпринимательство, фильмы и т. Д. Это платформа, которая также позволяет пользователям транслировать и смотреть видео в Интернете. Вы можете столкнуться с ситуацией, когда вы хотите иметь некоторые из ваших любимых видео YouTube на своем локальном компьютере. Для этого вам понадобится загрузчик видео для загрузки этих видео.

Если вам когда-либо нравилась идея создания собственного загрузчика видео на YouTube, то эта статья для вас; он покажет вам шаг за шагом, как создать загрузчик видео YouTube с помощью Python. Эта статья разделена на два раздела. В первом разделе мы сосредоточимся на создании версии командной строки, а во втором разделе мы создадим расширенную версию графического интерфейса пользователя (GUI).

Если вы хотите загружать только аудио из видео YouTube, то этот учебник должен быть полезен.

Содержание:

Построение версии командной строки
Построение версии графического интерфейса пользователя
Проектирование пользовательского интерфейса
Создание поля со списком «Разрешение»
Создание индикатора выполнения и кнопки загрузки
Реализация функции разрешения видео поиска
Реализация функции загрузки видео
Заключение 
Нам нужно установить первичную библиотеку, которая является pytube:

$ pip install pytube
Давайте создадим два новых файла Python и назовем их следующим образом:



Не стесняйтесь называть их так, как вы предпочитаете, но просто убедитесь, что имена имеют смысл.

Построение версии командной строки
Приступим к созданию версии приложения для командной строки. Откройте файл youtube_downloader_cli.py и выполните следующий импорт:

from pytube import YouTube
Здесь мы импортируем объект YouTube из pytube, согласно документации pytube, это просто легкая библиотека для загрузки видео YouTube. Это все, что нам нужно для нашего импорта. Теперь перейдем к созданию функции, которая будет обрабатывать фактическую загрузку видео; мы будем называть его video_downloader(). Под импортом вставьте следующие строки кода:

# the function takes the video url as an argument
def video_downloader(video_url):
    # passing the url to the YouTube object
    my_video = YouTube(video_url)
    # downloading the video in high resolution
    my_video.streams.get_highest_resolution().download()
    # return the video title
    return my_video.title
Давайте разобьем код так, чтобы мы были на одной странице; функция принимает video_url в качестве аргумента, этот video_url затем передается объекту YouTube().

С YouTube() мы можем получить доступ к видеоинформации, такой как потоки, заголовок, thumbnail_url, channel_id и т. Д., Этот объект назначается переменной под названием my_video. Поэтому для загрузки видео мы используем этот набор функций сразу, streams.get_highest_resolution().download(); это загрузит видео в самом высоком разрешении, и, наконец, мы возвращаем название видео.

Библиотека pytube поставляется с множеством опций для загрузки ваших видео. Если вы хотите загрузить видео с самым низким разрешением, используйте:

YouTube(url).streams.first().download()
Или, если вы хотите указать разрешение видео, вы можете использовать следующий код:

YouTube(url).streams.filter(res="Your_Resolution").first().download()
Просто замените заполнитель Your_Resolution на предпочтительное разрешение, например, 144p, 240p, 360p, 480p, 720p и т. Д.

Давайте сделаем так, чтобы приложение предлагало пользователю ввести URL-адрес видео. Чуть ниже функции вставьте следующий код:

# the try statement will run if there are no errors
try:
    # getting the url from the user
    youtube_link = input('Enter the YouTube link:')
    print(f'Downloading your Video, please wait.......')
    # passing the url to the function
    video = video_downloader(youtube_link)
    # printing the video title
    print(f'"{video}" downloaded successfully!!')
#the except will catch ValueError, URLError, RegexMatchError and simalar
except:
    print(f'Failed to download video\nThe '\
          'following might be the causes\n->No internet '\
          'connection\n->Invalid video link')
В фрагменте кода у нас есть блок try/except, внутри оператора try у нас есть код для получения URL-адреса от пользователя с помощью функции input(), и этот URL передается функции video_downloader() для загрузки видео. Внутри оператора except мы просто печатаем сообщение после обнаружения ошибок.

Теперь, когда у нас есть полный рабочий код, давайте протестируем его, скопируем URL-адрес из любого видео YouTube и запустим:

$ python youtube_downloader_cli.py
Вам будет предложено ввести URL-адрес видео, и после его ввода вы получите следующий вывод:

Enter the YouTube link:https://youtu.be/i9TlSFrsh4Q
Downloading your Video, please wait.......
"Find your next Python or ML job with my new job board!" downloaded succussfully!!
Если вы вернете папку вашего проекта, вы найдете mp4-файл:



Теперь повторно запустите приложение и на этот раз попробуйте предоставить недопустимую ссылку:

Enter the YouTube link:this is my link
Downloading your Video, please wait.......
Failed to download video
The following might be the causes
->No internet connection
->Invalid video link
Наша версия командной строки загрузчика видео на YouTube работает отлично!

Построение версии графического интерфейса пользователя
In this section, we will build the GUI version of the YouTube video downloader app. This is what we are going to be building:



Проектирование пользовательского интерфейса
Итак, без лишних слов, давайте начнем с нашего процесса проектирования. Первое, что мы сделаем, это импортируем необходимые библиотеки, поэтому сделаем следующее:

from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
В приведенном выше коде мы импортируем все из tkinter, мы также импортируем ttk из tkinter, ttk - это модуль, который предоставляет стили для виджетов, из pytube мы импортируем объект YouTube, это даст нам доступ ко всем функциям, доступным в pytube.

Мы также импортируем окна сообщений showinfo и showerror, которые являются всплывающими окнами для отображения сообщений пользователю, и, наконец, мы импортируем потоки; это поможет задачам нашего приложения (загрузка видео, запуск окна и поиск разрешений видео) выполняться одновременно.

Теперь, когда импорт выполнен, пришло время создать главное окно для приложения; чуть ниже импорта вставьте следующие строки кода:

from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading

# creates the window using Tk() fucntion
window = Tk()
# creates title for the window
window.title('YouTube Video Downloader')
# dimensions and position of the window
window.geometry('500x460+430+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)
# runs the window infinitely
window.mainloop()
Давайте разберем этот код. Для создания главного окна мы используем встроенный в tkinter класс Tk(). После создания окна мы создаем его заголовок с помощью функции ; затем мы даем ему размеры и положение.title()

Для высоты и ширины мы используем 500x460, а для положения, которое является горизонтальным и вертикальным, мы используем 430 + 180, и чтобы сделать окно неизменяемым, мы устанавливаем высоту и ширину на FALSE, и, наконец, мы вызываем функцию mainloop(), которая позволяет окну работать бесконечно, пока пользователь не нажмет кнопку закрытия.

Теперь, когда окно создано, нам нужно создать контейнер, который будет содержать все остальные виджеты, поэтому мы будем использовать виджет Canvas. Под этой строкой кода:

window.resizable(height=FALSE, width=FALSE)
Paste this code:

# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()
В коде мы создаем холст, помещая его в главное окно; внутри главного окна он будет занимать ширину 500 и высоту 400, как это:



Наш контейнер для виджетов готов. Давайте теперь начнем добавлять в него виджеты. Первым из них будет логотип YouTube. Убедитесь, что логотип находится в той же папке, что и youtube_downloader_ui.py файл:



Чтобы создать логотип, вставьте следующие строки кода:

# loading the logo
logo = PhotoImage(file='youtubelogo.png')
# creates dimensions of the logo
logo = logo.subsample(10, 10)
# adding the logo to the canvas
canvas.create_image(250, 80, image=logo)
В фрагменте кода мы, прежде всего, загружаем логотип с помощью функции PhotoImage(), затем мы даем размеры логотипа с помощью функции subsample(), и, наконец, мы добавляем логотип на холст с помощью функции create_image(), мы позиционируем логотип 250 по горизонтали и 80 по вертикали.

Давайте проверим, был ли логотип успешно добавлен на холст. Вот результат:



Приложение принимает свою форму; теперь мы определим стили для виджетов, которые мы добавим через мгновение; чуть ниже кода логотипа вставьте этот код:

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
Давайте разберем фрагмент кода выше; мы создаем стили для виджетов; для этого мы используем модуль ttk.

We are creating a style object using the ttk.Style() class, so to add styles to the object, we will use the configure() function, this function takes the style name; in our case, we have TLabel, TButton, and TEntry as style names, foreground, and font() are the other arguments the Style() class is taking.

In our widgets, we will use the style names to refer to or point to the style we want to use. Now that the styles are taken care of, we will now create and add the first two widgets to the canvas, the label and the entry. Below the styles, add this code:

# creating a ttk label
url_label = ttk.Label(window, text='Enter Video URL:', style='TLabel')
# creating a ttk entry
url_entry = ttk.Entry(window, width=76, style='TEntry')
# adding the label to the canvas
canvas.create_window(114, 200, window=url_label)
# adding the entry to the canvas
canvas.create_window(250, 230, window=url_entry)
To create a styled label, we are using a ttk.Label() class that comes from the ttk module, this function takes window, text, and the style as arguments, and to create a styled entry, we are using the ttk.Entry() class, also has arguments, window, width, and style.

Now to add these widgets to the canvas we are using the create_window() canvas function, takes two integers, in our case, 114 and 200 for the label and 250 and 230 for the entry; all these are for positioning the widget.

Running the app, we will get this output:



Создание поля со списком «Разрешение»
Теперь мы должны добавить метку разрешения и Combobox, который будет содержать разрешения видео; оба будут находиться под виджетом входа; добавьте этот код:

# creating resolution label
resolution_label = Label(window, text='Resolution:')
# adding the label to the canvas
canvas.create_window(50, 260, window=resolution_label)
# creating a combobox to hold the video resolutions
video_resolution = ttk.Combobox(window, width=10)
# adding the combobox to the canvas
canvas.create_window(60, 280, window=video_resolution)
Мы создаем два виджета; первый - это метка для отображения текста Resolution, что-то, что стоит отметить здесь, эта метка не является меткой ttk. После метки мы создаем фактический Combobox, он принимает окно и ширину в качестве аргументов, и, наконец, мы добавляем все это на холст, как обычно. С добавлением приведенного выше кода мы получаем следующее:



В настоящее время Combobox пуст, и кое-что стоит вашего внимания о Combobox; вы также можете ввести значения, на случай, если нужное значение не находится в поле со списком.

Поскольку мы хотим искать разрешения видео, мы добавим кнопку для функции поиска. Для этого добавьте следующий код под полем со списком:

# creating a button for searching resolutions
search_resolution = ttk.Button(window, text='Search Resolution')
# adding the button to the canvas
canvas.create_window(85, 315, window=search_resolution)
С добавлением приведенного выше кода, это вывод:



Создание индикатора выполнения и кнопки загрузки
Давайте закончим дизайн графического интерфейса, добавив наши последние три виджета, пустую метку, индикатор выполнения и кнопку «Загрузить видео»; пустая метка и индикатор выполнения будут использоваться для отображения хода загрузки видео. После кнопки Разрешение поиска добавьте следующий код:

# creating the empty label for displaying download progress
progress_label = Label(window, text='')
# adding the label to the canvas
canvas.create_window(240, 360, window=progress_label)
# creating a progress bar to display progress
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
# adding the progress bar to the canvas
canvas.create_window(250, 380, window=progress_bar)
# creating the button
download_button = ttk.Button(window, text='Download Video', style='TButton')
# adding the button to the canvas
canvas.create_window(240, 410, window=download_button)
Здесь мы создаем пустую метку, индикатор выполнения и стилизованную кнопку с помощью Label(), ttk. Progressbar() и ttk. Button() функции, в индикатор выполнения перед добавлением его на холст мы передаем окно, ориентир, длину и режим в качестве аргументов.

В progress_label мы добавляем окно и пустой текст, а в виджет кнопки мы также передаем окно аргументов, текст и стиль, а затем добавляем все эти виджеты на холст.

Вот что мы получаем после добавления пустой метки, индикатора выполнения и кнопки:



Поздравляем с успешной разработкой графического интерфейса приложения!

Реализация функции разрешения видео поиска
Теперь пришло время реализовать функцию разрешения видео поиска. Для этого нам нужно создать функцию для этого, поэтому после импорта вставьте следующий код:

# function for searching video resolutions
def searchResolution():
    # getting video url from entry
    video_link = url_entry.get()
    # checking if the video link is empty
    if video_link == '':
        showerror(title='Error', message='Provide the video link please!')
    # if video link not empty search resolution  
    else:
        try:
            # creating a YouTube object
            video = YouTube(video_link)
            # an empty list that will hold all the video resolutions
            resolutions = []
            # looping through the video streams
            for i in video.streams.filter(file_extension='mp4'):
                # adding the video resolutions to the resolutions list
                resolutions.append(i.resolution)
            # adding the resolutions to the combobox
            video_resolution['values'] = resolutions
            # when search is complete notify the user
            showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
        # catch any errors if they occur  
        except:
            # notify the user if errors are caught
            showerror(title='Error', message='An error occurred while searching for video resolutions!\n'\
                'Below might be the causes\n->Unstable internet connection\n->Invalid link')
Давайте разобьем код так, чтобы мы были на одной странице. Прежде всего, мы получаем ссылку на видео из записи. Затем мы проверяем, пуста ли запись ссылки. Если он пуст, мы уведомляем пользователя о предоставлении ссылки. В противном случае мы создадим объект YouTube(); затем пустой список разрешений, содержащий все разрешения видео.

Затем у нас есть цикл for, который зацикливает все разрешения видео, отфильтрованные по file_extension аргументу, затем все эти разрешения видео добавляются в список разрешений через эту строку кода:

resolutions.append(i.resolution)
И добавить все видеопотоки в пустой Combobox, который мы создали ранее; мы используем этот код:

video_resolution['values'] = resolutions
После завершения поиска мы уведомляем пользователя с помощью всплывающего окна showinfo. И, наконец, в операторе except мы ловим все ошибки, и сообщение будет отображаться с помощью всплывающего окна showerror.

Мы хотим запустить функцию searchResolution() в отдельном потоке, поэтому для этого мы создадим другую функцию, которая будет указывать на эту функцию и запускать ее как поток. Под функцией searchResolution() вставьте следующий код:

# the function to run the searchResolution function as a thread
def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()
Приведенный выше код создает функцию searchThread(), а внутри нее мы создаем поток t1, целевой функцией которого является searchResolution(), а затем запускается поток.

Поэтому, чтобы протестировать эту функцию, нам придется привязать функцию searchThread() к кнопке Search Resolution, отредактировать код кнопки search_resolution и сделать его следующим образом:

search_resolution = ttk.Button(window, text='Search Resolution', command=searchThread)
Мы используем аргумент команды, чтобы кнопка знала, какую функцию активировать, когда пользователь нажимает ее. Функция, на которую мы указываем, - это searchThread(),запустите приложение, вставьте URL-адрес видео и нажмите кнопку Разрешение поиска. Первый вывод выглядит следующим образом:



И второй вывод будет следующим после нажатия на Combobox:



Теперь нам удалось добавить все искомые разрешения видео в Combobox.

Связанные с: Как сделать загрузчик аудио YouTube на Python.

Реализация функций загрузки и многопоточности видео
В этой заключительной части статьи мы реализуем функцию загрузки видео. Чуть выше функции searchResolution() вставьте следующий код:

# the function to download the video
def download_video():
    # the try statement to excute the download the video code
    try:
        # getting video url from entry
        video_link = url_entry.get()
        # getting video resolution from Combobox
        resolution = video_resolution.get()
        # checking if the entry and combobox is empty
        if resolution == '' and video_link == '':
            # display error message when combobox is empty
            showerror(title='Error', message='Please enter both the video URL and resolution!!')
        # checking if the resolution is empty
        elif resolution == '':
            # display error message when combobox is empty
            showerror(title='Error', message='Please select a video resolution!!')
        # checking if the comboxbox value is None  
        elif resolution == 'None':
            # display error message when combobox value is None
            showerror(title='Error', message='None is an invalid video resolution!!\n'\
                    'Please select a valid video resolution')    
        # else let's download the video  
        else:
            # this try statement will run if the resolution exists for the video
            try:
                # this function will track the video download progress
                def on_progress(stream, chunk, bytes_remaining):
                    # the total size of the video
                    total_size = stream.filesize
                    # this function will get the size of the video
                    def get_formatted_size(total_size, factor=1024, suffix='B'):
                        # looping through the units
                        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                            if total_size < factor:
                                return f"{total_size:.2f}{unit}{suffix}"
                            total_size /= factor
                        # returning the formatted video size
                        return f"{total_size:.2f}Y{suffix}"
                    # getting the formatted video size calling the function
                    formatted_size = get_formatted_size(total_size)
                    # the size downloaded after the start
                    bytes_downloaded = total_size - bytes_remaining
                    # the percentage downloaded after the start
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                    # updating the progress bar value
                    progress_bar['value'] = percentage_completed
                    # updating the empty label with the percentage value and formatted file size
                    progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                    # updating the main window of the app
                    window.update()
                # creating the YouTube object and passing the the on_progress function
                video = YouTube(video_link, on_progress_callback=on_progress)
                # downlaoding the actual video  
                video.streams.filter(res=resolution).first().download()
                # popup for dispalying the video downlaoded success message
                showinfo(title='Download Complete', message='Video has been downloaded successfully.')
                # ressetting the progress bar and the progress label
                progress_label.config(text='')
                progress_bar['value'] = 0
            # the except will run when the resolution is not available or invalid
            except:
                showerror(title='Download Error', message='Failed to download video for this resolution')
                # ressetting the progress bar and the progress label
                progress_label.config(text='')
                progress_bar['value'] = 0
    # the except statement to catch errors, URLConnectError, RegMatchError  
    except:
        # popup for displaying the error message
        showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the video link is valid')
        # ressetting the progress bar and the progress label
        progress_label.config(text='')
        progress_bar['value'] = 0
В этом коде мы создаем функцию с именем download_video(), а внутри функции у нас есть внешний блок try/except и внутренний блок try/except, который заключен в оператор else. Таким образом, мы получаем URL-адрес видео и разрешение из записи и Combobox соответственно с помощью функции get(), затем мы выполняем некоторую проверку данных с помощью операторов if и elif и соответственно показываем окна ошибок.

Если входные данные проверены, здесь у нас есть внутренний блок try/except, а внутри оператора try у нас есть функция отслеживания хода выполнения под названием on_progress(), аргументами которой являются поток, блок и bytes_remaining.

Внутри этой функции мы вычисляем загруженные байты и процент завершения, который затем добавляется в индикатор выполнения и пустую метку хода выполнения. Наконец, мы обновляем окно с помощью функции update().

Функция get_formatted_size() внутри функции on_progress() вычисляет и возвращает размер видео в формате KBs, MBs, GBs, TB и т.д. Он был взят из этого учебника.

Сразу за пределами функции on_progress() мы создаем объект YouTube(), который принимает URL-адрес видео и функцию on_progress() в качестве аргументов, а затем фактическая загрузка видео обрабатывается следующей строкой кода:

video.streams.filter(res=resolution).first().download()
После успешной загрузки видео появляется сообщение об успешном завершении, и если это ошибки, такие как разрыв интернет-соединения, оператор except обработает все это и уведомит пользователя об ошибках, а также сбросят индикатор выполнения и метку прогресса.

Наконец, у нас есть последняя внешняя инструкция except, которая будет обрабатывать такие ошибки, как недопустимый URL-адрес видео, отсутствие подключения к Интернету и т. Д., И снова сбросит как индикатор выполнения, так и метку прогресса.

Позаботившись о функции download_video(), мы снова создадим другую функцию, которая будет выполнять эту функцию в виде потока, поэтому под функцией searchThread() вставьте этот код:

# the function to run the download_video function as a thread   
def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()
Здесь мы делаем то же самое, что и в функции searchThread(), создаем поток, целью которого является функция download_video(), затем поток запускается с помощью функции start().

Теперь, чтобы загрузить видео, нам нужно привязать функцию downloadThread() с кнопкой «Загрузить видео», поэтому для этого добавьте аргумент команды, и эта команда должна указывать на функцию downloadThread(), как показано ниже:

download_button = ttk.Button(window, text='Download Video', style='TButton', command=downloadThread)
Это то, что означает, когда пользователь нажимает кнопку «Загрузить видео», запускается функция downloadThread() и запускается функция download_video() как поток, это означает, что задачи будут выполняться без конфликтов. Это удобно, потому что приложение будет работать плавно без сбоев, таких как приложение, не отвечающее.

Давайте протестируем приложение, запустим его и вставим URL-адрес видео в запись, найдем разрешение видео, а после успешного поиска выберем разрешение и нажмем кнопку «Загрузить видео», дождитесь загрузки видео, и вы получите этот вывод:



Check in your project’s folder to confirm if the video has been downloaded successfully, you will get this:



If you enter the video URL, search for the video resolution, and leave the Combobox empty, you will get this output:



Если и запись URL-адреса, и поле со списком разрешения оставлены пустыми, и кнопка Загрузить видео нажата. Вот результат:



Если вы хотите найти разрешение видео без указания URL-адреса видео, вы получите следующее:



И, наконец, если ваша загрузка видео выполнялась, и у вас было нестабильное или разорванное подключение к Интернету, результат будет следующим:



Приложение работает отлично, но здесь следует отметить, что вы его используете, это не каждое видео, которое вы можете загрузить с помощью приложения, потому что некоторые видео YouTube являются частными, некоторые заблокированы в определенном регионе, некоторые ограничены по возрасту, а некоторые требуют членства. Список исключений pytube можно найти здесь.

Заключение
Надеемся, вам понравилась статья о создании загрузчика видео на YouTube с помощью Python. Это отличное готовое решение для загрузки ваших любимых видео YouTube в автономном режиме. Мы не рассмотрели все, учитывая, что может сделать библиотека pytube, но мы считаем, что полученные вами знания могут быть использованы для создания чего-то значимого в ваших будущих проектах.