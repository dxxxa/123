# [How to Control your Mouse in Python](https://www.thepythoncode.com/article/control-mouse-python)
The script `control_mouse.py` is suggested to be run on an interactive python shell, such as ipython, jupyter lab, etc.
Install requirements:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Управление компьютерной мышью в коде является удобной задачей, так как это может быть полезно для автоматизации рабочего стола, создания полезных агентов рабочего стола и т. Д. В этом учебнике вы узнаете, как управлять мышью в Python.

Мы будем использовать удобную библиотеку мыши, давайте установим ее:

$ pip3 install mouse
Этот модуль помогает нам полностью контролировать нашу мышь, например, перехватывать глобальные события, регистрировать горячие клавиши, имитировать движение мыши и щелчки и многое другое!

Во-первых, давайте посмотрим, как мы можем имитировать щелчки мыши:

import mouse

# left click
mouse.click('left')

# right click
mouse.click('right')

# middle click
mouse.click('middle')
Заметка: Рекомендуется выполнять эти инструкции по отдельности в интерактивной оболочке Python, такой как записная книжка Jupyter или IPython.

Функция mouse.click() делает то, что подсказывает ее название, она отправляет щелчок с заданной кнопкой, попробуйте!

Во-вторых, вы также можете получить текущее положение мыши:

In [22]: mouse.get_position()
Out[22]: (646, 407)
Вы можете перетащить что-то мышью:

# drag from (0, 0) to (100, 100) relatively with a duration of 0.1s
mouse.drag(0, 0, 100, 100, absolute=False, duration=0.1)
Установка абсолютного значения False с начальными позициями (0, 0) означает, что он перетаскивает из текущего положения на 100 дальше (в x и y).

Проверьте это на файле, который вы хотите перетащить на свой рабочий стол!

Далее вы также можете определить, нажата ли кнопка:

# whether the right button is clicked
In [25]: mouse.is_pressed("right")
Out[25]: False
Вы также можете перемещать мышь:

# move 100 right & 100 down
mouse.move(100, 100, absolute=False, duration=0.2)
Это позволит перемещать мышь относительно на 0,2 секунды.

Можно также выполнять обратные вызовы, которые вызываются всякий раз, когда происходит событие, например щелчок мышью:

# make a listener when left button is clicked
mouse.on_click(lambda: print("Left Button clicked."))
# make a listener when right button is clicked
mouse.on_right_click(lambda: print("Right Button clicked."))
Приведенный выше код делает простые обратные вызовы всякий раз, когда нажимаются кнопки мыши, здесь мы просто использовали лямбда-функции в демонстрационных целях, вы можете использовать любую функцию, чтобы делать все, что захотите.

Если вы хотите удалить прослушиватели, вы можете вызвать unhook_all(), чтобы удалить все прослушиватели:

# remove the listeners when you want
mouse.unhook_all()
Вы также можете управлять колесом мыши, давайте прокрутим вниз:

# scroll down
mouse.wheel(-1)
Scrolling up:

# scroll up
mouse.wheel(1)
Наконец, вы можете записать все события мыши, а затем воспроизвести их:

# record until you click right
events = mouse.record()
Это будет записывать все события мыши, пока не будет нажата правая кнопка. Затем он возвращает список записанных событий, давайте воспроизведем их:

# replay these events
mouse.play(events[:-1])
Причина, по которой я устанавливаю события[:-1] вместо всех событий, заключается в том, что я не хочу играть правой кнопкой мыши.

Вот несколько идей, которые вы можете сделать с помощью этого модуля:

Создание обучающих агентов с подкреплением, играющих в видеоигры.
Автоматизация скучных настольных вещей.
Гораздо больше!
Вы можете комбинировать это с управлением клавиатурой в Python, и давайте посмотрим, что вы можете построить с их помощью!