# [How to Create an Alarm Clock App using Tkinter in Python](https://www.thepythoncode.com/article/build-an-alarm-clock-app-using-tkinter-python)
##
# [[] / []]()
Будильник является неотъемлемой частью нас. Мы полагаемся на него, чтобы напомнить нам о времени, которое нам нужно для выполнения конкретной задачи. Создать его на Python не так уж и сложно. В этом уроке мы сделаем простой будильник на Python с помощью следующих библиотек:

tkinter - Эта библиотека графического интерфейса пользователя (GUI) позволяет нам отображать пользовательский интерфейс будильника.
playsound - Помогает нам создавать звуки для нашего будильника.
time - Предоставляет функции, связанные со временем
datetime - упрощает доступ к атрибутам вещи, связанной с датами, временем и часовыми поясами.
threading — обеспечивает асинхронное выполнение некоторых функций в приложении. Установка модулей в интерфейсе командной строки
$ pip install playsound
Модули datetime, time и tkinter предустановлены вместе с Python.
Для импорта в наш редактор кода:

from tkinter import *
import datetime
import time
from playsound import playsound
from threading import *
import * означает, что мы импортируем все библиотеки из модуля Tkinter.

Затем мы проектируем, как будет выглядеть графический пользовательский интерфейс, используя tkinter:

root = Tk()  # initializes tkinter to create display window
root.geometry('450x250')  # width and height of the window
root.resizable(0, 0)  # sets fix size of window
root.title(' Alarm Clock')  # gives the window a title


addTime = Label(root, fg="red", text="Hour     Min     Sec",
                font='arial 12 bold').place(x=210)
setYourAlarm = Label(root, text="Set Time(24hrs): ",
                     bg="grey", font="arial 11 bold").place(x=80, y=40)
hour = StringVar()
min = StringVar()
sec = StringVar()

# make the time input fields
hourTime = Entry(root, textvariable=hour, relief=RAISED, width=4, font=(20)).place(x=210, y=40)
minTime = Entry(root, textvariable=min, width=4, font=(20)).place(x=270, y=40)
secTime = Entry(root, textvariable=sec, width=4, font=(20)).place(x=330, y=40)
Мы проектируем интерфейс, устанавливая его ширину и высоту и давая ему название. Затем мы создаем две метки, одна из которых показывает нам, где вводить часы, минуты и секунды, а другая направляет нас на то, где установить время. Используя Entry(), мы также создаем, куда будут введены данные.

StringVar() указывает тип переменной, при которой час, min и sec являются строковыми переменными.

Наш интерфейс теперь выглядит следующим образом:


Прекрасно. Давайте теперь создадим функцию main alarm(), которая меняет оставшееся время каждую секунду и проверим, достигнуто ли время тревоги. Если это так, то он воспроизводит звук будильника и показывает простое окно сообщения:

def start_alarm():
    t1 = Thread(target=alarm)
    t1.start()


def alarm():
    while True:
        set_alarm_time = f"{hour.get()}:{min.get()}:{sec.get()}"
        # sleep for 1s to update the time every second
        time.sleep(1)
        # Get current time
        actual_time = datetime.datetime.now().strftime("%H:%M:%S")
        FMT = '%H:%M:%S'
        # get time remaining
        time_remaining = datetime.datetime.strptime(
            set_alarm_time, FMT) - datetime.datetime.strptime(actual_time, FMT)
        # displays current time
        CurrentLabel = Label(
            root, text=f'Current time: {actual_time}', fg='black')
        CurrentLabel.place(relx=0.2, rely=0.8, anchor=CENTER)
        # displays alarm time
        AlarmLabel = Label(
            root, text=f'Alarm time: {set_alarm_time}', fg='black')
        AlarmLabel.place(relx=0.2, rely=0.9, anchor=CENTER)
        # displays time remaining
        RemainingLabel = Label(
            root, text=f'Remaining time: {time_remaining}', fg='red')
        RemainingLabel.place(relx=0.7, rely=0.8, anchor=CENTER)
        # Check whether set alarm is equal to current time
        if actual_time == set_alarm_time:
            # Playing sound
            playsound('audio.mp3')
            messagebox.showinfo("TIME'S UP!!!")
Мы также определяем функцию start_alarm(), которая устанавливает экземпляр Thread и инструктирует его начать новый поток тревоги с помощью .start().

Метод strptime() создает объект datetime из заданной строки и принимает два аргумента: строку, преобразуемую в datetime, и код формата времени. Мы преобразовали строки в datetime и сохранили их в формате %H:%M:%S. Это позволяет нам найти временной интервал между заданным временем тревоги и текущим временем и сохранить его как time_remaining.

Мы идем дальше и создаем метку для отображения оставшегося времени как RemainingLabel, с красным цветом шрифта. Мы также создаем две метки, отображающие текущее время и время тревоги. Когда текущее время и заданное время будильника совпадают, воспроизводится звук и в интерфейсе отображается сообщение.

Мы добавляем аудиофайл, который будет воспроизводиться при срабатывании будильника, и сохраняем его в домашнем каталоге.

Теперь давайте создадим кнопку, которая устанавливает наш будильник при нажатии:

# create a button to set the alarm
submit = Button(root, text="Set Your Alarm", fg="red", width=20,
                command=start_alarm, font=("arial 20 bold")).pack(pady=80, padx=120)
Напоследок запустим программу:

# run the program
root.mainloop()
Теперь наш интерфейс должен выглядеть следующим образом:

Когда будильник срабатывает, воспроизводится и отображается сообщение, в котором говорится, что время истекло:audio.mp3


Заключение
Мы успешно создали будильник на Python; посмотрите, как вы можете добавить больше функций к этому!