# [How to Build a GUI QR Code Generator and Detector Using Python](https://www.thepythoncode.com/article/make-a-qr-code-generator-and-reader-tkinter-python)
##
# [[] / []]()
QR-код, сокращенно от Quick Response code, представляет собой машиночитаемый штрих-код, используемый для хранения различных типов данных и разработанный в 2D-пиксельной форме.

С развитием технологий каждую секунду QR-коды оказались важными в нашей повседневной жизни; в настоящее время они имеют широкий спектр применения в различных областях. Например, QR-коды используются для совершения онлайн-платежей, обмена паролями Wi-Fi, используются на афишах мероприятий, проверки информации о различных продуктах и т. Д.

В этой статье мы обсудим создание генератора и детектора QR-кодов с помощью Python. Мы начнем с обсуждения различных библиотек Python, которые мы будем использовать в этом проекте. Мы также предоставим пошаговое руководство по коду, чтобы вы могли понять, как все работает. К концу этой статьи у вас будет полнофункциональный генератор и детектор QR-кодов с графическим пользовательским интерфейсом, который вы можете использовать самостоятельно.

Обратите внимание, что если вам нужна только функциональность генерации и чтения QR-кода, у нас есть учебник для этого. Этот учебник направлен на создание полнофункционального графического приложения для генерации и обнаружения QR-кода.

В конце этой четкой статьи вот приложение, которое мы собираемся построить:

Генератор-детектор QR-кодов

И:



Мы создадим каждую часть этого крутого приложения с нуля, поэтому, если вы готовы и взволнованы, давайте погрузимся!

Содержание:

Настройка среды
Импорт всех необходимых модулей
Проектирование графического интерфейса пользователя
Создание главного окна и добавление значка главного окна
Определение всех используемых стилей виджетов
Создание записной книжки и двух вкладок
Добавление холста на каждую вкладку
Добавление виджетов на вкладку генератора QR-кодов
Метка изображения
Две наклейки и две записи
Две кнопки
Добавление виджетов на вкладку детектора QR-кодов
Изображение и метка данных
Запись файла и кнопка Обзора
Кнопка "Обнаружить"
Реализация функции закрытия приложения
Реализация функциональных возможностей приложения
Генерация QR-кода
Сброс или очистка метки изображения QR-кода
Укажите путь к файлу QR-кода
Обнаружение QR-кода
Заключение
Настройка среды
Первое, с чего мы начнем, это настройка окружающей среды; это потребует установки всех необходимых модулей. Поэтому в терминале выполните команду:

$ pip install qrcode opencv-python
Импорт всех необходимых модулей
Теперь, когда мы закончили настройку среды проекта, давайте начнем работать над фактическим кодом.

Во-первых, давайте создадим новый файл Python и назовем его qrcode_generator_detector.py; вы можете называть его как угодно; убедитесь, что само имя имеет смысл. Откройте файл и выполните следующие операции импорта:

# this imports everything from the tkinter module
from tkinter import *
# importing the ttk module from tkinter that's for styling widgets
from tkinter import ttk
# importing message boxes like showinfo, showerror, askyesno from tkinter.messagebox
from tkinter.messagebox import showinfo, showerror, askyesno
# importing filedialog from tkinter
from tkinter import filedialog as fd 
# this imports the qrcode module
import qrcode
# this imports the cv2 module
import cv2
Давайте разберем импорт в приведенном выше фрагменте кода от первой строки до последней. Мы в первую очередь импортируем все из tkinter, это делается с помощью символа asterisk(*), затем мы импортируем модуль ttk, который предназначен для стилизации виджетов (меток, записей, кнопок и т. Д.) Для приложения.

Мы также импортируем окна сообщений, такие как showerror, showinfo и askyesno, они предназначены для отображения определенных полезных сообщений пользователю, когда в приложении произошло определенное действие, а filedialog поможет нам в просмотре и указании путей к файлам.

Наши последние два импорта - это модули qrcode и cv2, модуль qrcode предназначен для генерации QR-кодов, а модуль cv2 - для обнаружения этих QR-кодов соответственно.

Проектирование графического интерфейса пользователя
В этом разделе мы начнем разработку графического интерфейса приложения. Процесс проектирования будет глубоким, чтобы вы понимали, что происходит и насколько мощным является модуль Tkinter, когда дело доходит до разработки шикарных графических пользовательских интерфейсов.

Создание главного окна и добавление значка главного окна
Поэтому нашей первой задачей в процессе проектирования графического интерфейса является создание главного окна и добавление значка. Чуть ниже импорта вставьте следующие строки кода:

# creating the window using the Tk() class
window = Tk()
# creates title for the window
window.title('QR Code Generator-Detector')
# adding the window's icon
window.iconbitmap(window, 'icon.ico')
# dimensions and position of the window
window.geometry('500x480+440+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)
# run the main window infinitely
window.mainloop()
Здесь, в фрагменте кода выше, мы создаем главное окно с помощью встроенного класса Tkinter Tk(), а затем даем заголовок главному окну с помощью функции title().

Чтобы добавить иконку в главное окно, мы используем функцию iconbitmap(), которая принимает окно и фактическую иконку в качестве аргументов, здесь убедитесь, что файл значка находится в той же папке, что и файл Python:



Файл иконки также может быть расположен в любом месте; вам нужно только правильно указать его путь в функции iconbitmap(), чтобы использовать его.

Функция geometry() предназначена для придания размеров и положения главному окну, 500x480 - для ширины и высоты соответственно и 440 + 180 - для позиционирования главного окна по горизонтали и вертикали. Чтобы сделать главное окно неизменяемым, мы используем функцию resizable(), высота и ширина которой имеют значение FALSE, это отключит кнопку свертывания или разворота главного окна.

Наконец, мы вызываем функцию mainloop(), которая позволяет главному окну работать в бесконечном режиме, пока окно не будет закрыто.

Чтобы запустить программу, используйте следующую команду:

$ python qrcode_generator_detector.py
И вот какой вывод вы получите:



А в левом верхнем углу добавлен новый значок:



Определение всех используемых стилей виджетов
Теперь, когда мы позаботились о главном окне, давайте определим все стили виджетов, которые мы будем использовать. Мы определим стили для следующих виджетов, меток, записей и кнопок.

Итак, ниже этой строки кода:

window.resizable(height=FALSE, width=FALSE)
Добавьте следующий код:

"""Styles for the widgets, labels, entries, and buttons"""
# style for the labels
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 11))
# style for the entries
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
# style for the buttons
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('DotumChe', 10))
Ради того, чтобы быть на одной странице, давайте разберем код выше. Для создания объекта стиля мы используем ttk. Style() встроен в класс для модуля ttk, в нашем случае мы создаем три объекта стиля, для всех меток, записей и кнопок.

Для настройки этих стилей мы используем функцию configure(), для стиля метки функция configure() принимает три аргумента: TLabel в качестве имени стиля, передний план и шрифт. Для стиля записи она принимает имя стиля TEntry и шрифт, и, наконец, для стиля кнопки функция принимает TButton, передний план и шрифт.

Создание записной книжки и двух вкладок
Теперь мы создадим виджет «Ноутбук» и две вкладки; Записная книжка — это всего лишь контейнер вкладок или элемент управления вкладками. Под кодом определения стилей вставьте следующий код:

# creating the Notebook widget
tab_control = ttk.Notebook(window)
# creating the two tabs with the ttk.Frame()
first_tab = ttk.Frame(tab_control)
second_tab = ttk.Frame(tab_control)
# adding the two tabs to the Notebook
tab_control.add(first_tab, text='QR Code Generator')
tab_control.add(second_tab, text='QR Code Detector')
# this makes the Notebook fill the entire main window so that its visible
tab_control.pack(expand=1, fill="both")
Мы создаем блокнот с помощью ttk. Функция Notebook() и добавление ее в главное окно. Затем мы создаем две вкладки с помощью ttk. Функция Frame(); эти два элемента добавляются в записную книжку.

Чтобы добавить две вкладки в записную книжку, мы используем функцию add(), которая принимает вкладку и текст в качестве аргументов. Мы назвали вкладки QR Code Generator и QR Code Detector, первая вкладка предназначена для генерации QR-кодов, а вторая - для обнаружения QR-кодов.

И, наконец, мы упаковываем блокнот с помощью функции pack(), и чтобы сделать две вкладки видимыми, мы передаем аргументы expand и fill с 1 и обоими в качестве значений соответственно функции pack().

С добавлением приведенного выше кода, это вывод, который мы получаем при запуске программы:



Если вы переключитесь между двумя вкладками, вы заметите, что они оба пусты, мы добавим их соответствующие виджеты через мгновение.

Добавление холста на каждую вкладку
Прежде чем мы добавим виджеты на вкладки, мы должны создать два холста и добавить их к каждому. Эти холсты будут контейнерами для виджетов для каждой вкладки, и они помогут нам гибко выровнять виджеты. Под этой строкой кода:

tab_control.pack(expand=1, fill="both")
Добавьте следующий код:

# creates the canvas for containing all the widgets in the first tab
first_canvas = Canvas(first_tab, width=500, height=480)
# packing the canvas to the first tab
first_canvas.pack()
# creates the canvas for containing all the widgets in the second tab
second_canvas = Canvas(second_tab, width=500, height=480)
# packing the canvas to the second tab
second_canvas.pack()
Здесь мы создаем два виджета canvas с помощью функции Canvas(), первый холст помещается на первую вкладку, а второй холст помещается на вторую вкладку, и оба они имеют ширину 500 и высоту 480.

Если вы запустите программу, вы не увидите ничего нового, но знайте, что холст подходит, как показано ниже, в соответствии с размерами, которые мы ему дали:



Если вы больше хотите увидеть, как подходит холст, передайте аргумент background со значением цвета в функцию Canvas().

Добавление виджетов на вкладку генератора QR-кодов
Позаботившись о холстах, пришло время обратить наше внимание на добавление виджетов на вкладку Генератор QR-кодов. Напоминаем, что эта вкладка будет обрабатывать генерацию QR-кода.

Метка изображения
Первый виджет, который мы добавим, это метка изображения для отображения изображения QR-кода после его генерации. Под холстами вставьте следующий код:

"""Widgets for the first tab"""

# creating an empty label
image_label1 = Label(window)
# adding the label to the canvas
first_canvas.create_window(250, 150, window=image_label1)
В приведенном выше коде мы создаем пустую метку с помощью функции Label() и добавляем ее на холст с помощью функции create_window(). Функция принимает 250 и 150, а виджет, 250 и 150, предназначен для позиционирования метки внутри холста.

Две наклейки и две записи
Перейдем к добавлению двух меток и записей; начнем с первой строки с меткой и записью. Поэтому под меткой изображения добавьте следующие строки кода:

# creating a ttk label
qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')
# creating a ttk entry
data_entry = ttk.Entry(window, width=55, style='TEntry')
# adding the label to the canvas
first_canvas.create_window(70, 330, window=qrdata_label)
# adding the entry to the canvas
first_canvas.create_window(300, 330, window=data_entry)
Здесь мы создаем два виджета, метку для отображения текста и запись для получения данных от пользователя с помощью ttk. Label() и ttk. Запись() соответственно.

ТТК. Label() принимает три аргумента: окно, текст и стиль, в то время как ttk. Entry() также принимает окно, ширину и стиль. Наконец, мы добавляем эти виджеты на холст с помощью функции create_window(), которая занимает 300 и 330 для позиционирования виджета.

Выходные данные для вышеуказанного кода выглядят следующим образом:



Теперь добавим метку и запись во вторую строку. Под меткой и записью в первой строке вставьте следующий код:

# creating a ttk label
filename_label = ttk.Label(window, text='Filename', style='TLabel')
# creating a ttk entry
filename_entry = ttk.Entry(width=55, style='TEntry')
# adding the label to the canvas
first_canvas.create_window(84, 360, window=filename_label)
# adding the entry to the canvas
first_canvas.create_window(300, 360, window=filename_entry)
В этом фрагменте кода мы снова создаем метку и запись, используя две функции, ttk. Label() и ttk. Запись(). Окно, текст и стиль являются аргументами для ttk. Label() и для ttk. Entry(), ширина и стиль являются аргументами. Чтобы добавить эти два виджета на холст, мы используем функцию create_window().

Запустив программу, получаем вывод:



Пока всё в порядке; приложение принимает ожидаемую форму!

Две кнопки
Давайте закончим добавление виджетов на вкладку генератора QR-кодов, создав последние две кнопки. Первая кнопка предназначена для сброса или очистки метки изображения, а вторая — для генерации самого QR-кода. Под второй строкой виджетов добавьте следующий код:

# creating the reset button in a disabled mode
reset_button = ttk.Button(window, text='Reset', style='TButton', state=DISABLED)
# creating the generate button
generate_button = ttk.Button(window, text='Generate QRCode', style='TButton')
# adding the reset button to the canvas
first_canvas.create_window(300, 390, window=reset_button)
# adding the generate button to the canvas
first_canvas.create_window(410, 390, window=generate_button)
С помощью этого фрагмента кода мы создаем две кнопки с помощью ttk. Функция Button(), все аргументы одинаковы для обеих кнопок, окна, текста и стиля, за исключением состояния для кнопки Сброс. Здесь мы хотим, чтобы кнопка Reset была включена только тогда, когда QR-код был сгенерирован, в противном случае DISABLED будет его первым состоянием после запуска приложения.

Результат, который мы получаем после добавления приведенного выше кода, таков:



Теперь мы закончили добавлять виджеты на первую вкладку.

Добавление виджетов на вкладку детектора QR-кодов
В этой части статьи мы начнем добавлять виджеты на вкладку QR Code Detector, и это виджеты, о которых предполагается позаботиться, метка изображения, метка данных, запись, кнопка Browse и кнопка Detect.

Изображения и метки данных
Первыми виджетами являются метка изображения, которая отображает изображение QR-кода так же, как и на первой вкладке, и метка данных для отображения данных QR-кода после обнаружения. В файле, чуть ниже этой строки кода:

first_canvas.create_window(410, 390, window=generate_button)
Вставьте это:

"""Below are the widgets for the second tab"""
# creating the second image label
image_label2 = Label(window)
# creating the data label
data_label = ttk.Label(window)
# adding the second image label to the second_canvas
second_canvas.create_window(250, 150, window=image_label2)
# adding the data label to the canvas
second_canvas.create_window(250, 300, window=data_label)
Здесь мы создаем две пустые метки с помощью Label() и ttk. Функции Label(), одна для отображения изображения QR-кода, а другая для отображения данных QR-кода. Аргументом для обеих функций является окно, затем эти две метки добавляются на холст внутри второй вкладки через функцию create_window().

Запись файла и кнопка Обзора
Теперь давайте создадим запись для файла и кнопку для просмотра файлов. Под метками добавьте следующий код:

# creating the file_entry
file_entry = ttk.Entry(window, width=60, style='TEntry')
# creating the browse button
browse_button = ttk.Button(window, text='Browse', style='TButton')

# adding the entry to the second canvas in the second tab
second_canvas.create_window(200, 350, window=file_entry)
# adding the generate button to the second canvas in the second tab
second_canvas.create_window(430, 350, window=browse_button)
Во фрагменте кода мы создаем запись файла и кнопку обзора с помощью ttk. Entry() и ttk. Функции Button(). Как и в случае с другими записями ttk, ttk. Функция Entry() принимает в качестве аргументов окно, ширину и стиль, и то же самое относится к ttk. Функция Button(), которая принимает окно, текст и стиль в качестве аргументов. Наконец, оба этих виджета добавляются на холст второй вкладки с помощью функции create_window().

Запустив программу, получаем следующий вывод:

Кнопка "Обнаружить"
Давайте теперь добавим последний виджет, который является кнопкой Detect, под записью файла и кодом кнопки обзора, добавим этот код:

# creating the detect button
detect_button = ttk.Button(window, text='Detect QRCode', style='TButton')
# adding the detect button to the canvas
second_canvas.create_window(65, 385, window=detect_button)
С добавлением приведенного выше кода, это то, что мы получаем после запуска программы:



Реализация функции закрытия приложения
Мы почти закончили проектирование графического интерфейса приложения. Тем не менее, как и сейчас, приложение быстро закрывается, когда пользователь нажимает кнопку закрытия, поэтому мы хотим, чтобы приложение могло спросить пользователя, закрывать его или нет. Для этого мы создадим функцию, поэтому под импортом вставьте этот код:

# the function to close the window
def close_window():
    # this will ask the user whether to close or not
    # if the value is yes/True the window will close
    if askyesno(title='Close QR Code Generator-Detector', message='Are you sure you want to close the application?'):
        # this destroys the window
        window.destroy()
В приведенном выше коде мы создаем функцию с именем close_window(), и внутри этой функции у нас есть окно сообщения askyesno, это окно сообщения вычисляет два логических значения True или False. Если пользователь предоставляет значение yes, которое имеет значение True, будет выполнена функция destroy(), и главное окно будет закрыто. Если значение askyesno равно False, окно все равно будет запущено.

О функции закрытия окна позаботились, но этого недостаточно, чтобы закрыть окно для нас. Нам нужно позволить главному окну прослушивать событие закрытия окна, поэтому для этого ниже этой строки кода:

window.resizable(height=FALSE, width=FALSE)
Добавьте следующую строку кода:

# this is for closing the window via the close_window() function
window.protocol('WM_DELETE_WINDOW', close_window)
Функция protocol() принимает два аргумента: WM_DELETE_WINDOW и функцию close_window. С помощью WM_DELETE_WINDOW функция будет прослушивать событие закрытия главного окна, которое выдается всякий раз, когда пользователь нажимает кнопку закрытия главного окна.

Если событие обнаружено, выполняется функция close_window(), и появляется окно сообщения askyesno, если пользователь нажимает кнопку «Да», окно закрывается, а если нет, то окно все равно запускается.

Если вы запустите программу и нажмете кнопку закрытия, вот что вы получите:



Реализация функциональных возможностей приложения
После завершения процесса проектирования графического интерфейса мы теперь остаемся с самой захватывающей задачей, чтобы сделать это красивое приложение функциональным. Мы будем реализовывать каждый функционал с нуля.

Генерация QR-кода
Первой функциональностью, которая будет реализована, является генерация QR-кодов, что будет сделано на вкладке Генератор QR-кодов. Итак, под функцией close_window() вставьте следующий код:

 # the function for generating the QR Code
def generate_qrcode():
    # getting qrcode data from data_entry via get() function
    qrcode_data = str(data_entry.get())
    # getting the qrcode name from the filename_entry via get() function
    qrcode_name = str(filename_entry.get())
    # checking if the qrcode_name/filename_entry is empty
    if qrcode_name == '':
        # if its empty display an error message to the user
        showerror(title='Error', message='An error occurred' \
                   '\nThe following is ' \
                    'the cause:\n->Empty filename entry field\n' \
                    'Make sure the filename entry field is filled when generating the QRCode')
    # the else statement will execute when the qrcode_name/filename_entry is filled
    else:
        # confirm from the user whether to generate QR code or not
        if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
            # the try block for generating the QR Code
            try:
                # Creating an instance of QRCode class
                qr = qrcode.QRCode(version = 1, box_size = 6, border = 4)
                # Adding data to the instance 'qr'
                qr.add_data(qrcode_data)
                # this helps with the dimensions of the QR code
                qr.make(fit = True)
                # the name for the QRCode
                name = qrcode_name + '.png'
                # making the QR code
                qrcode_image = qr.make_image(fill_color = 'black', back_color = 'white')
                # saving the QR code
                qrcode_image.save(name)
                # making the Image variable global
                global Image
                # opening the qrcode image file
                Image = PhotoImage(file=f'{name}')
                # displaying the image on the canvas via the image label
                image_label1.config(image=Image)
                # the button for resetting or clearing the QR code image on the canvas
                reset_button.config(state=NORMAL)
            # this will catch all the errors that might occur
            except:
                showerror(title='Error', message='Please provide a valid filename')
Мы создаем функцию с именем generate_qrcode(); Вот что происходит внутри функции:

Мы получаем данные QR-кода и имя из двух полей ввода через функцию get().
Затем проверяем, пусто ли поле ввода имени. Если это так, мы показываем сообщение об ошибке, что-то, что стоит заметить здесь, вы можете сгенерировать QR-код с данными или без них, но ему должно быть дано имя.
В противном случае мы подтверждаем, хочет ли пользователь сгенерировать QR-код с предоставленной информацией (имя и данные).
Затем у нас есть блок try/except. Внутри оператора try мы создаем экземпляр QR-кода с помощью функции QRCode(); он принимает версию, box_size и границу в качестве аргументов, а версия начинается от 1 до 40. Затем мы добавляем данные, полученные из поля ввода, в QR-код с помощью функции add_data(). Функция make(), значение соответствия которой имеет значение True, помогает с размерами QR-кода и обеспечивает их правильное использование.
Чтобы создать QR-код, мы используем функцию make_image(), которая принимает fill_color и back_color в качестве аргументов. Fill_color — для переднего плана, а back_color — для фона QR-кода. Функция save() предназначена для сохранения QR-кода и принимает имя QR-кода в качестве аргумента.
Чтобы отобразить сгенерированный QR-код, мы создаем глобальную переменную Image, а затем открываем фактическое изображение QR-кода с помощью функции PhotoImage(). Теперь, чтобы отобразить QR-код на этикетке изображения, мы передаем изображение в функцию config().
После генерации QR-кода мы включаем кнопку Reset; мы поговорим об этой кнопке буквально через минуту. Оператор except улавливает любые ошибки и после этого отображает сообщение для пользователя.
Теперь давайте привяжем функцию generate_qrcode() с кнопкой Сгенерировать QRCode и отредактируем код кнопки так, чтобы он выглядел следующим образом:

generate_button = ttk.Button(window, text='Generate QRCode', style='TButton',  command=generate_qrcode)
Аргумент команды указывает на функцию, активируемую при нажатии кнопки.

Давайте попробуем сгенерировать наш первый QR-код, поэтому запустите программу, заполните два поля ввода и нажмите enter; вот что вы получаете:



И если вы нажмете кнопку Да, вы получите следующий вывод:



И здесь следует отметить одну вещь, кнопка Reset была включена после того, как мы успешно сгенерировали наш первый QR-код. Чтобы проверить, действительно ли QR-код был сгенерирован и сохранен, проверьте папку проекта:



Сброс или очистка метки изображения QR-кода
Теперь мы дадим возможность пользователю сбросить или очистить изображение QR-кода. Под функцией generate_qrcode() вставьте код:

# the function for resetting or clearing the image label
def reset():
    # confirming if the user wants to reset or not
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        # if yes reset the label
        image_label1.config(image='')
        # and disable the button again
        reset_button.config(state=DISABLED)
С помощью этого фрагмента кода мы создаем функцию reset(), которая проверяет, является ли значение окна сообщения askyesno True или False. Если это значение True, мы сбрасываем или очищаем метку изображения и отключаем кнопку Reset.

Функция reset() должна быть снова связана кнопкой Reset, поэтому внутри функции generate_qrcode() найдите следующую строку кода:

reset_button.config(state=NORMAL)
И отредактируйте его, чтобы он выглядел следующим образом:

reset_button.config(state=NORMAL, command=reset)
Здесь с помощью функции config() мы изменяем состояние кнопки на NORMAL и привязываем его к функции reset().

Попробуем сгенерировать еще один QR-код:



Поскольку кнопка Сброс включена, при ее нажатии будет получен следующий результат:



Если нажать кнопку Да, результат будет выглядеть следующим образом:



Теперь изображение очищено, а кнопка снова отключена, приложение работает как положено.

Укажите путь к файлу QR-кода
Позаботившись о функциональности генерации QR-кода, мы приступим к работе над реализацией функциональности считывания QR-кода. Но перед этим нам нужно иметь возможность просматривать файлы и выбирать файл для обнаружения. Под функцией reset() вставьте следующий код:

# the function to open file dialogs  
def open_dialog():
    # getting the file name via the askopenfilename() function
    name = fd.askopenfilename()
    # deleting every data from the file_entry
    file_entry.delete(0, END)
    # inserting the file in the file_entry
    file_entry.insert(0, name)
Мы создаем функцию под названием open_dialog(), в которой получаем файл и полный путь к нему; затем мы удаляем все из записи файла с помощью функции delete(). Это поможет нам не иметь двух путей к файлам в записи файла, добавленных одновременно. И, наконец, мы вставляем файл вместе с его путем в запись файла.

Теперь свяжите эту функцию с помощью кнопки Обзор; код должен выглядеть следующим образом:

browse_button = ttk.Button(window, text='Browse', style='TButton', command=open_dialog)
Давайте протестируем эту функциональность, запустим программу, и вы получите следующий вывод:



Сразу после выбора файла он будет вставлен в поле ввода, если вы просмотрите и выберете другой файл, предыдущие данные записи будут удалены, а новый файл будет вставлен в запись. Прекрасно! Эта функциональность, похоже, работает.

Обнаружение QR-кода
Теперь давайте реализуем окончательный функционал приложения, которое обнаруживает QR-коды. Под функцией open_dialog() вставьте следующий код:

# the function to detect the QR codes
def detect_qrcode():
    # getting the image file from the file entry via get() function
    image_file = file_entry.get()
    # checking if the image_file is empty
    if image_file == '':
        # show error when the image_file entry is empty
        showerror(title='Error', message='Please provide a QR Code image file to detect')
    # executes when the image_file is not empty
    else:
        # code inside the try will detect the QR codes
        try:
            # reading the image file with cv2 
            qr_img = cv2.imread(f'{image_file}')  
            # using the QRCodeDetector() function  
            qr_detector = cv2.QRCodeDetector()  
            # making the qrcodde_image global
            global qrcode_image
            # opening the qrcode_image using the PhotoImage
            qrcode_image = PhotoImage(file=f'{image_file}')
            # displaying the image via the image label
            image_label2.config(image=qrcode_image)
            # using the detectAndDecode() function detect and decode the QR code
            data, pts, st_code = qr_detector.detectAndDecode(qr_img)  
            # displaying data on the data_label
            data_label.config(text=data)
        # this catches any errors that might occur
        except:
            # displaying an error message
            showerror(title='Error', message='An error occurred while detecting data from the provided file' \
                   '\nThe following could be ' \
                    'the cause:\n->Wrong image file\n' \
                    'Make sure the image file is a valid QRCode')
В приведенной выше функции мы сначала получаем файл изображения QR-кода из записи файла через функцию get(). После этого мы проверяем, пуст ли файл изображения. Если это так, мы отобразим сообщение об ошибке. В противном случае выполните код внутри оператора else.

Внутри оператора else у нас есть код для обнаружения QR-кода. мы используем функцию cv2.imread() для чтения изображения.

Для создания объекта детектора QR-кода мы используем cv2. Функция QRCodeDetector(), затем мы создаем глобальную переменную с именем qrcode_image. После этого мы создаем объект изображения с помощью функции PhotoImage(), которая принимает файл изображения в качестве входных данных.

Чтобы отобразить изображение QR-кода на этикетке, мы используем функцию config() и предоставляем изображение в качестве входных данных. Наконец, чтобы обнаружить и декодировать QR-код, мы используем следующую строку кода:

data, pts, st_code = qr_detector.detectAndDecode(qr_img)
Приведенная выше функция detectAndDecode() принимает изображение QR-кода в качестве входных данных и возвращает данные QR-кода, точки или координаты углов поля и бинаризованный QR-код.

Давайте свяжем функцию detect_qrcode() с кнопкой «Обнаружить QRCode» и отредактируем код кнопки, чтобы он выглядел следующим образом:

detect_button = ttk.Button(window, text='Detect QRCode', style='TButton', command=detect_qrcode)
Давайте определим некоторые QR-коды здесь, мы обнаружим те, которые мы сгенерировали до сих пор, или вы можете сгенерировать новые. Выберите любой QR-код по вашему выбору, определите его, и вы получите следующий вывод:



Предположим, пользователь выбирает неправильный файл; приложение должно выдавать следующие выходные данные:



Если пользователь забывает выбрать QR-код для обнаружения и нажимает кнопку «Обнаружить QRCode», вот вывод:



И если вы попытаетесь сгенерировать QR-код с пустым полем ввода имени файла, это результат:



И, наконец, если вы предоставите недопустимое имя файла, вы получите следующее:



Заключение
Вот и все из этой статьи! Мы надеемся, что вы многому научились на этом пути. В этой статье объясняется, как создать генератор и детектор QR-кодов с помощью Python. В статье рассматривалась установка необходимых библиотек, проектирование графического пользовательского интерфейса, кодирование генератора и детектора.

Вы можете получить полный код здесь.

Узнайте также: Как создать приложение для записи голоса с графическим интерфейсом на Python