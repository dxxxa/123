# [How to Control your Keyboard in Python](https://www.thepythoncode.com/article/control-keyboard-python)
To make this work:
- pip3 install -r requirements.txt

And run the lines of code in `control_keyboard.py` individually, that's because it makes no sense to run them at once.
##
# [[] / []]()
В этом уроке вы узнаете, как использовать модуль клавиатуры для управления клавиатурой вашего компьютера в Python, это, конечно, полезно для многих задач, таких как автоматизация различных рутинных задач рабочего стола, создание агентов обучения с подкреплением и многое другое.

Содержание:

Добавление горячих клавиш и аббревиатур
Проверка нажатия кнопки
Нажатие и отпускание кнопок
Написание текста
Запись и воспроизведение событий клавиатуры
Связанные с: Как отправлять электронные письма на Python.

Мы будем использовать модуль клавиатуры, давайте установим его:

pip3 install keyboard
Хорошо, откройте интерактивную оболочку Python или записную книжку / лабораторию Jupyter и следуйте за ними.

Во-первых, давайте импортируем модуль:

import keyboard
Добавление горячих клавиш и аббревиатур
Этот модуль предоставляет нам функцию add_abbreviation(), которая позволяет нам зарегистрировать горячую клавишу, которая заменяет один набранный текст другим. Например, заменим текст "@email" на адрес электронной почты "test@example.com":

# replaces every "@email" followed by a space with an actual email
keyboard.add_abbreviation("@email", "test@example.com")
Теперь выполните эту строку кода, а затем откройте любой текстовый редактор и напишите «@email», за которым следует пробел, вы увидите волшебство!

Во-вторых, вы также можете вызывать обратный вызов при каждом нажатии горячей клавиши:

keyboard.add_hotkey("ctrl+alt+p", lambda: print("CTRL+ALT+P Pressed!"))
«ctrl + alt + p» относится к кнопкам CTRL, ALT и P, нажатым одновременно, поэтому всякий раз, когда эти кнопки нажимаются одновременно, обратный вызов будет вызван, в этом случае он просто распечатает простое сообщение, но вы можете сделать все, что захотите, например, ярлыки на рабочем столе.

Проверка нажатия кнопки
Вы также можете проверить, действительно ли нажата кнопка:

# check if a ctrl is pressed
print(keyboard.is_pressed('ctrl'))
Нажатие и отпускание кнопок
Далее вы также можете имитировать нажатия клавиш с помощью функции send():

# press space
keyboard.send("space")
Это нажмет и освободит кнопку пробела. На самом деле, существует эквивалентная функция press_and_release(), которая делает то же самое.

Вы также можете передать несколько ключей:

# multi-key, windows+d as example shows the desktop in Windows machines
keyboard.send("windows+d")
Оператор + означает, что мы нажимаем обе кнопки одновременно, вы также можете использовать многошаговые горячие клавиши:

# send ALT+F4 in the same time, and then send space, 
# (be carful, this will close any current open window)
keyboard.send("alt+F4, space")
Но что, если вы хотите нажать определенную клавишу, но не хотите ее отпускать? Ну, функции press() и release() вступают в игру:

# press CTRL button
keyboard.press("ctrl")
# release the CTRL button
keyboard.release("ctrl")
Таким образом, это нажмет кнопку CTRL, а затем отпустит ее, вы можете делать все, что между ними, например, спать в течение нескольких секунд и т. Д.

Другой альтернативой является сама функция send(); он имеет два параметра, do_press и do_release которые по умолчанию имеют значение True. Если вы хотите нажать клавишу только с помощью send(), вы можете просто использовать keyboard.send("ctrl", do_release=False), чтобы не отпускать клавишу.

Написание текста
Но что, если вы хотите написать длинный текст, а не только конкретные кнопки? send() будет неэффективным. К счастью для нас, функция write() делает именно это, она отправляет искусственные события клавиатуры в ОС, имитируя набор заданного текста, давайте попробуем:

keyboard.write("Python Programming is always fun!", delay=0.1)
Установка задержки на 0,1 указывает на 0,1 секунды ожидания между нажатиями клавиш, это будет выглядеть причудливо, как в фильмах о взломе!

Запись и воспроизведение событий клавиатуры
Вы можете делать гораздо больше интересных вещей с помощью этого модуля, таких как запись событий клавиатуры с помощью функции record() и их повторное воспроизведение с помощью функции play():

# record all keyboard clicks until esc is clicked
events = keyboard.record('esc')
# play these events
keyboard.play(events)
Я передал 'esc' методу record() для записи нажатий клавиш и отпусканий, пока я не нажму кнопку 'esc', а затем мы снова воспроизводим эти события, используя метод play().

Вы можете узнать, что содержит список событий, просто распечатав его, или вы можете использовать get_typed_strings() для получения введенных строк:

# print all typed strings in the events
print(list(keyboard.get_typed_strings(events)))
Вот что я набрал:

['Python is indeed the best programming language.!', 'right?', '', '']
Другой интересной функцией является функция on_release(), которая принимает обратный вызов, который выполняется всякий раз, когда ключ отпускается:

# log all pressed keys
keyboard.on_release(lambda e: print(e.name))
Это напечатает все, что вы нажимаете на клавиатуре, для получения дополнительной информации о том, как использовать эту функцию для создания кейлоггера в образовательных целях, проверьте этот учебник.

Наконец, если вы хотите удалить все используемые крючки клавиатуры, включая горячие клавиши, аббревиатуры и т. Д.:

keyboard.unhook_all()
Заключение
Я только что представил вам модуль, пожалуйста, проверьте документацию или просто введите help (клавиатуру) в интерактивной оболочке Python для изучения других функций и методов.

Вы также можете взять полный контроль над своей мышью, тот же автор этого модуля сделал еще один для обработки мыши!

С помощью таких модулей вы можете создавать скрипты автоматизации рабочего стола, сочетания клавиш, кейлоггеры (хотя автор не несет ответственности) и многое другое!

Не стесняйтесь посещать этот сайт, если вы хотите получить мгновенную помощь в назначении Python от экспертов. Команда программистов Python сделает вашу домашнюю работу по Python с совершенством.

Погружайтесь глубже с Python
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python, удачи!