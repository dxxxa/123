# [How to Build a GUI Voice Recorder App in Python](https://www.thepythoncode.com/article/make-a-gui-voice-recorder-python)
##
# [[] / []]()
Эта статья покажет вам, как создать приложение с графическим интерфейсом диктофона с помощью Tkinter в Python. Вы узнаете, как использовать мощные отличные библиотеки для обработки аудиоданных, а также как записывать и сохранять аудиофайлы. К концу этой статьи у вас будет полностью функционирующее приложение для диктофона, которое вы можете использовать для записи своего голоса или любых других звуков.

Обратите внимание, что этот учебник посвящен созданию графического интерфейса для диктофона; если вы хотите быстрый способ записи голоса, то этот учебник для вас.

Вот приложение, которое мы построим в конце этой статьи:

Мы собираемся развивать каждый его кусочек с нуля. Итак, без лишних слов, давайте погрузимся!

Вот оглавление:

Настройка среды
Импорт всех необходимых модулей
Проектирование графического интерфейса пользователя
Создание главного окна и добавление значка окна
Определение всех стилей виджетов
Создание холста и добавление логотипа
Создание метки и записи
Создание метки хода выполнения и кнопки записи
Реализация функции записи голоса
Заключение
Настройка среды
Прежде всего, мы начнем с настройки среды проекта; мы создадим виртуальную среду, поэтому в вашем терминале выполните команду:

$ python -m venv project
Сумев создать виртуальную среду, мы должны активировать ее и выполнить команду:

$ .\project\Scripts\activate
Теперь в этой виртуальной среде мы установим все необходимые пакеты для проекта. Чтобы установить эти пакеты, выполните следующую команду:

$ pip install scipy sounddevice
Импорт всех необходимых модулей
Наша следующая задача - импортировать все необходимые модули, которые будут использоваться для этого проекта, создать новый файл Python и сохранить его как voice_recorder.py, как хорошая практика, убедитесь, что ваши файлы Python имеют осмысленные имена.

Откройте файл и вставьте следующий код:

# importing everything from tkinter
from tkinter import *
# importing the styling module ttk from tkinter
from tkinter import ttk
# importing the message boxes from tkinter
from tkinter.messagebox import showinfo, showerror, askokcancel
# this is for recording the actual voice
import sounddevice
# this is for saving the recorded file to wav file format
from scipy.io.wavfile import write
# threading will help the app's tasks run concurrently
import threading
# importing datetime from datetime to handle dates
from datetime import datetime
# this will handle time
import time
# os module will be used for renaming files
import os
Сначала мы импортируем все из tkinter с помощью звездочки (*), затем мы импортируем модуль ttk, который предназначен для стилизации виджетов (меток, записей, кнопок и т. Д.).

Мы также импортируем окна сообщений (showinfo, showerror, askokcancel) из tkinter, так как приложение должно предупредить пользователя о какой-либо ошибке или действии. Затем идет модуль звукового устройства. Согласно документации, он предназначен для воспроизведения и записи массивов Numpy, содержащих аудиосигналы. После записи нам придется записать записанный файл в формате WAV, поэтому для этого мы импортируем write() из scipy.io.wavfile.

Мы также импортируем модуль многопоточности; это поможет приложению работать плавно, выполняя такие задачи, как запуск графического интерфейса пользователя и одновременная запись. Модули даты и времени предназначены для использования даты и времени соответственно.

Наконец, мы импортируем модуль ОС; это поможет в переименовании записанных файлов.

Проектирование графического интерфейса пользователя
В этом разделе мы начнем процесс проектирования графического интерфейса; мы сделаем это в идеальном темпе, чтобы мы все были на одной странице и чтобы вы могли понять все вовлеченные концепции.

Создание главного окна и добавление значка окна
Теперь начнем с создания главного окна и добавления иконки. Этот значок заменит значок Tkinter по умолчанию, поэтому под импортом вставьте следующие строки кода:

# creates the window using Tk() fucntion
window = Tk()
# creates title for the window
window.title('Voice Recorder')
# the icon for the application, this replaces the default icon
window.iconbitmap(window, 'voice_recorder_icon.ico')
# dimensions and position of the window
window.geometry('500x450+440+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)
# this will run the main window infinitely
window.mainloop()
Мы создаем главное окно приложения, используя встроенный в Tkinter класс Tk(). Чтобы присвоить заголовок окну, мы используем функцию title().

И чтобы добавить значок в окно, мы используем функцию iconbitmap(), обратите внимание, что это принимает окно и фактический файл значка формата .ico в качестве аргументов, и убедитесь, что файл значка находится в той же папке, что и файл программы. Для высоты и ширины окна и его положения мы используем функцию geometry() со значениями 500x450+440+180, 500 и 450 , являющимися высотой и шириной, и 440 и 180 для позиционирования окна вертикально и горизонтально.

Чтобы сделать главное окно неизменяемым или, другими словами, отключить кнопку разворачивать или сворачивать окно, мы используем функцию variablesizable() с высотой и шириной, установленными на FALSE.

Наконец, чтобы главное окно работало бесконечно, пока пользователь не закроет его, мы используем функцию mainloop().

Чтобы протестировать это приложение, выполните следующую команду в терминале:

$ python voice_recorder.py
Вот результат, который мы получим:

А в левом верхнем углу главного окна у нас есть новая иконка:

Определение всех стилей виджетов
Перед созданием виджетов мы должны сначала определить их стили. Итак, чуть ниже этой строки кода:

window.resizable(height=FALSE, width=FALSE)
Вставьте следующий код:

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
Здесь мы создаем три объекта стиля с помощью ttk. Класс Style(), объекты стиля предназначены для виджетов, которые мы создадим через мгновение. Для настройки этих стилей мы используем функцию configure(), которая принимает имя стиля; в нашем случае мы назвали наши стили TEntry, TLabel и TButton. Шрифт и передний план являются другими аргументами, которые он принимает.

Создание холста и добавление логотипа
Позаботившись о стилях, нам теперь нужно создать полотно; он будет содержать все виджеты для приложения. Внутри этого холста мы добавим логотип. Под определением стилей добавьте следующий код:

# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()
# loading the logo
logo = PhotoImage(file='recorder.png')
# creates dimensions of the logo
logo = logo.subsample(2, 2)
# adding the logo to the canvas
canvas.create_image(240, 135, image=logo)
Это то, что происходит в приведенном выше фрагменте кода; мы создаем холст с помощью функции Canvas(), добавляем этот холст внутрь окна и придаем ему ширину 500 и высоту 400.

Затем мы загружаем логотип и придаем ему размеры с помощью функции subsample(), и, наконец, добавляем его на холст через функцию create_image(). Для горизонтального позиционирования логотипа мы используем 240, а вертикально – 135. Убедитесь, что файл изображения, используемый для логотипа, находится в той же папке, что и файл программы.

С добавлением приведенного выше кода приложение выглядит следующим образом:



Холст может быть не виден, но вот как он вписывается в главное окно с размерами, которые мы ему дали:

Создание метки и записи
Теперь давайте создадим первые два виджета, метку и запись; мы разместим их внутри холста. Под кодом логотипа вставьте следующий код:

# creating a ttk label
duration_label = ttk.Label(window, text='Enter Recording Duration in Seconds:', style='TLabel')
# creating a ttk entry
duration_entry = ttk.Entry(window, width=76, style='TEntry')
# adding the label to the canvas
canvas.create_window(235, 290, window=duration_label)
# adding the entry to the canvas
canvas.create_window(250, 315, window=duration_entry)
Здесь мы создаем метку и запись с помощью ttk. Label() и ttk. Функции Entry(). ТТК. Label() принимает окно, текст и стиль в качестве аргументов, в то время как ttk. Entry() принимает в качестве аргументов окно, ширину и стиль. После создания этих двух мы добавляем их на холст с помощью функции create_window().

Запустив приложение, вы получите следующий вывод:

Создание метки хода выполнения и кнопки записи
В этом разделе мы завершим процесс проектирования графического интерфейса, создав последние два виджета, пустую метку, которую мы будем использовать для отображения длительности записи и кнопку для записи. Сразу после кода записи вставьте следующий код:

# creating the empty label for displaying download progress
progress_label = ttk.Label(window, text='')
# creating the button
record_button = ttk.Button(window, text='Record', style='TButton')
# adding the label to the canvas
canvas.create_window(240, 365, window=progress_label)
# adding the button to the canvas
canvas.create_window(240, 410, window=record_button)
Этот код создает метку и кнопку с помощью двух функций ttk. Label() и ttk. Button() соответственно, с окном и текстом в качестве аргументов для метки и окна, текстом и стилем в качестве аргументов для кнопки. Как обычно, после создания этих виджетов мы добавляем их на холст через функцию create_window().

После добавления приведенного выше кода, давайте посмотрим, как будет выглядеть приложение. Запустите его, и вы получите следующий вывод:

Мы почти закончили проектирование графического интерфейса, но оставшаяся вещь заключается в том, чтобы сделать приложение интерактивным, когда мы его закроем. Мы хотим, чтобы приложение закрылось с подтверждением пользователя, поэтому под импортом вставьте этот код:

# the function for closing the main window
def close_window():
    # here we are checking if the value of askokcancel is True
    if askokcancel(title='Close Voice Recorder', message='Are you sure you want to close the Voice Recorder?'):
        # this kills the window
        window.destroy()
Мы создаем простую функцию с именем close_window(), и внутри нее у нас есть оператор if для проверки того, является ли логическое значение askokcancel() True или False. Если это true, мы закроем его с помощью функции destroy().

Создания функции недостаточно, чтобы сделать всю магию за нас; нам нужно, чтобы кнопка закрытия окна знала, какую функцию активировать при нажатии, поэтому ниже:

window = Tk()
Вставьте следующий код:

# this will listen to the close window event
window.protocol('WM_DELETE_WINDOW', close_window)
В коде у нас есть функция protocol(), принимающая два аргумента, WM_DELETE_WINDOW и функцию close_window(). Вся логика этого кода заключается в том, что главное окно будет прослушивать событие закрытия окна, инициированное кнопкой закрытия, и как только это событие будет обнаружено, сработает функция close_window().

Запустите приложение и нажмите кнопку закрытия, вот что вы получите:

Если вы нажмете ok, окно закроется, а если вы нажмете кнопку отмены, окно по-прежнему будет работать в mainloop.

Реализация функции записи голоса
Теперь, когда о графическом пользовательском интерфейсе позаботились, нам нужно реализовать функциональность записи голоса. Мы начнем с создания функции record_voice(), поэтому под функцией close_window() вставьте этот код:

# function for recording sound
def record_voice():
    # the try statement is for 
    try:
        # this is the frequence at which the record will happen   
        freq = 44100
        # getting the recording duration from the entry
        duration = int(duration_entry.get())
        # calling the recorder via the rec() function
        recording  = sounddevice.rec(duration*freq, samplerate=freq, channels=2)
        # declaring the counter
        counter = 0
        # the loop is for displaying the recording progress
        while counter < duration:
            # updating the window
            window.update()
            # this will help update the window after every 1 second
            time.sleep(1)
            # incrementing the counter by 1
            counter += 1
            # displaying the recording duration
            progress_label.config(text=str(counter))
        # this records audio for the specified duration 
        sounddevice.wait()
        # writing the audio data to recording.wav
        write('recording.wav', freq, recording)
        # looping through all the files in the current folder
        for file in os.listdir():
            # checking if the file name is recording.wav
            if file == 'recording.wav':
                # spliting the base and the extension
                base, ext = os.path.splitext(file)
                # getting current time
                current_time = datetime.now()
                # creating a new name for the recorded file
                new_name = 'recording-' + str(current_time.hour) + '.' + str(current_time.minute) + '.' + str(current_time.second) + ext
                # renaming the file
                os.rename(file, new_name)
        # display a message when recording is done  
        showinfo('Recording complete', 'Your recording is complete')
    # function for catching all errors   
    except:
        # display a message when an error is caught
        showerror(title='Error', message='An error occurred' \
                   '\nThe following could ' \
                    'be the causes:\n->Bad duration value\n->An empty entry field\n' \
                    'Do not leave the entry empty and make sure to enter a valid duration value')
Давайте разобьем код функции, чтобы он находился на одной странице. Внутри функции у нас есть блок try/except, оператор except поймает все ошибки и сообщит об этом пользователю. Внутри блока try мы объявляем переменную частоты дискретизации, называемую freq, и после этого мы получаем длительность из записи через функцию get(), эта длительность всегда в секундах.

Затем мы вызываем рекордер через функцию sounddevice.rec(), которая принимает duration*freq, частоту дискретизации и каналы в качестве аргументов. После этого объявляем переменную счетчика и устанавливаем для нее значение 0; это будет использоваться для отслеживания хода записи.

У нас также есть цикл while, который будет выполняться только в том случае, если счетчик меньше длительности. Внутри этого цикла мы обновляем окно с помощью функции update(), которая будет происходить через каждую секунду через time(1). Мы увеличиваем счетчик на единицу и выводим счетчик через функцию config() метки прогресса.

Вне цикла while мы записываем аудио через функцию sounddevice.wait(), после того, как мы закончили, мы сохраняем его с помощью функции write() из модуля scipy. Файл сохраняется как запись.wav.

Функция write() после завершения записи всегда будет сохранять файл как запись.wav, и если мы попытаемся записать три раза, мы получим не три файла, а одну запись.wav. Это означает, что записанный в данный момент файл всегда будет перезаписывать старый, что не очень хорошо, потому что мы хотим сохранить все записанные файлы.

Итак, в цикле for мы просматриваем все файлы в текущей рабочей папке, затем у нас есть оператор if, который проверяет, записывается ли файл.wav, если файл записывается.wav мы разделим его базу и расширение с помощью модуля OS следующим образом:

base, ext = os.path.splitext(file)
После разделения мы получаем текущее время, используя datetime.now(), затем мы генерируем новое имя файла следующей строкой кода:

new_name = 'recording-' + str(current_time.hour) + '.' + str(current_time.minute) + '.' + str(current_time.second) + ext
Мы добавляем расширение и строки current_time.hour, current_time.minute и current_time.second к базовому имени. Чтобы переименовать файл, мы использовали:

os.rename(file, new_name)
После всего этого программа выводит успешное сообщение по завершении записи.

Поскольку функция record_voice() делает так много, что мы не будем запускать ее напрямую, а будем запускать ее как поток через другую функцию. Запуск функции record_voice() в виде потока пригодится, так как он будет выполняться одновременно с другими задачами, выполняемыми приложением. Под функцией record_voice() вставьте следующий код:

# the function to run record_voice as a thread
def recording_thread():
    # creating the thread whose target is record_voice()
    t1 = threading.Thread(target=record_voice)
    # starting the thread
    t1.start()
Что касается фрагмента кода, мы создаем функцию с именем recording_thread(), в которой мы создаем поток с помощью класса Thread(), целью которого является функция record_voice(), затем мы, наконец, запускаем поток.

Теперь нам нужно связать эту функцию потока с кнопкой Record, отредактировать код кнопки и сделать его таким:

record_button = ttk.Button(window, text='Record', style='TButton', command=recording_thread)
Мы все готовы. Давайте теперь сделаем нашу первую запись, мы сделаем 10-секундную запись, и вот что вы получите:

И если вы вернетесь в папку проекта, вы увидите новый файл, который похож на этот:



Попробуем сделать вторую запись, вы можете ввести любые секунды в качестве длительности, и после успешной записи вы получите новый файл:



К файлу мы добавляем часы, минуты и секунды текущего времени; Вы можете записать столько файлов, сколько захотите, и ни один из них не будет перезаписан.

Если пользователь оставил запись пустой или ввел неправильное значение длительности, приложение будет выдавать следующие выходные данные:



Приложение работает должным образом. Поздравляем с созданием приложения для диктофона на Python!

Заключение
Вот и все из этой статьи; Теперь мы надеемся, что вы изучили много концепций, связанных с Python, и будете применять их в будущих проектах!

В этой статье объясняется, как создать приложение для записи голоса с помощью Python. Первым шагом была настройка среды и установка необходимых модулей. Затем мы разработали графический пользовательский интерфейс с нуля. Наконец, мы реализовали функциональность записи голоса и протестировали приложение, чтобы убедиться, что оно работает должным образом.

Вы можете получить полный код здесь.