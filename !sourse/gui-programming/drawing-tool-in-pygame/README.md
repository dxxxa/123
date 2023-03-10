# [How to Make a Drawing Program in Python](https://www.thepythoncode.com/article/make-a-drawing-program-with-python)
##
# [[] / []]()
В этом уроке мы сделаем простую программу рисования на Python с помощью PyGame. Мы будем использовать кнопки, которые мы сделали в предыдущей статье, чтобы можно было переключать цвета и изменять размер кисти; мы также реализуем функцию сохранения.

Как всегда, мы начинаем с импорта. Поскольку мы используем PyGame, мы также должны иметь в виду, чтобы установить его сначала с помощью следующей команды:

$ pip install pygame
Мы также импортируем sys, чтобы правильно убить процесс, и ctypes, чтобы включить распознавание dpi, чтобы наше окно выглядело более четким, это совершенно необязательно:

# Imports
import sys
import pygame
import ctypes

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)
Связанные с: Как создать проводник с помощью Tkinter в Python.

Конфигурация Pygame
Мы продолжаем использовать конфигурацию pygame. Чтобы использовать модуль, мы должны инициализировать его. Мы устанавливаем переменную fps, которая позже будет передана методу pygame.time.clock.tick(), чтобы ограничить максимальное количество кадров в секунду.

После этого мы делаем объект для этого, а затем объявляем начальную ширину и высоту. Мы направим эти значения в функцию pygame.display.set_mode(), но мы также установим ее флаг режима в pygame. ИЗМЕНЯЕТСЯ РАЗМЕР, чтобы размер окна можно было изменить в любое время.

И последнее, но не менее важное: мы импортируем шрифт, который будет использоваться в наших кнопках:

# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.SysFont('Arial', 20)
Переменные
Теперь мы делаем некоторые переменные для использования позже. Мы начинаем со списка, называемого объектами, где мы храним кнопки. Затем мы устанавливаем начальный цвет кисти в режиме RGB.

После этого мы устанавливаем начальный brushSize и количество пикселей кисти увеличивается или уменьшается при нажатии соответствующей кнопки.

В конце концов, мы определяем размеры нашего полотна, и это та область, где мы сможем рисовать:

# Variables
# Our Buttons will append themself to this list
objects = []
# Initial color
drawColor = [0, 0, 0]
# Initial brush size
brushSize = 30
brushSizeSteps = 3
# Drawing Area Size
canvasSize = [800, 800]
Класс кнопки
Мы используем класс кнопок из этого учебника (не стесняйтесь идти и копировать / вставлять или получить полный код здесь). Поэтому мы вставляем его класс сюда; мы уже составили список объектов, нам нужно только зациклить его в основном цикле, поэтому появляются наши кнопки:

# Button Class
class Button():
    ...
Функции обработчика
Теперь мы настроим три функции для обработки изменений цвета и размера кисти, а также запроса на сохранение.

Изменить цвет
Функция changeColor() просто примет нужный цвет и установит для глобальной переменной drawColor это значение.

# Handler Functions
# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color
Изменение размера кисти
Функция changebrushSize() примет аргумент dir, чтобы проверить, должна ли кисть стать больше или меньше. Если он больше, он добавит brushSizeSteps к нашему brushSize. Во всех остальных случаях происходит обратное, потому что мы предполагаем, что пользователь хочет, чтобы он был меньше.

# Changing the Brush Size
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps
Сохранить на диск
Благодаря модулю pygame.image сохранить наш холст так же просто, как вызвать функцию pygame.image.save() с поверхностью для сохранения и путем к файлу:

# Save the surface to the Disk
def save():
    pygame.image.save(canvas, "canvas.png")
Настройка кнопки
Мы продолжаем настраивать наши кнопки. Сначала определим две переменные, которые представляют ширину и высоту кнопки:

# Button Variables.
buttonWidth = 120
buttonHeight = 35
После этого мы составляем список, который состоит из большего количества списков, где каждый первый элемент является отображаемым текстом, а каждый второй элемент является функцией, которую нужно вызывать:

# Buttons and their respective functions.
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Brush Larger', lambda: changebrushSize('greater')],
    ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Save', save],
]
Теперь мы зациклимся на этом списке и сгенерируем кнопки. Все они будут в ряду и иметь 10-пиксельные зазоры. Это не будет выглядеть красиво, но это сделает работу для нашего небольшого приложения:

# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])
Холст
Теперь мы используем canvasSize, чтобы сделать новую поверхность, которая будет служить холстом, на котором мы рисуем. Заполняем() эту поверхность белым:

# Canvas
canvas = pygame.Surface(canvasSize)
canvas.fill((255, 255, 255))
Связанные с: Как сделать симулятор планеты с PyGame на Python.

Главная петля
Теперь о захватывающей части. Как обычно, мы заполняем весь экран темно-серым цветом, а затем проверяем, нажал ли пользователь красный x в верхней части экрана, чтобы мы могли остановить программу.

Мы также зацикливаемся на нашем списке объектов и вызываем функцию process() для каждого объекта, чтобы нарисовать их.

# Game loop.
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Drawing the Buttons
    for object in objects:
        object.process()
Рисование
Перед тем, как сделать функцию рисования, мы блит() холст в центре экрана:

    # Draw the Canvas at the center of the screen
    x, y = screen.get_size()
    screen.blit(canvas, [x/2 - canvasSize[0]/2, y/2 - canvasSize[1]/2])
Далее проверяем, была ли нажата левая кнопка мыши pygame.mouse.get_pressed()[0]. Затем получаем положение мыши и вычисляем положение мыши на холсте. После этого у нас есть вся информация, необходимая для того, чтобы нарисовать круг, где была нажата мышь. Мы также поставляем эту функцию с нашим drawColor и нашим brushSize.

    # Drawing with the mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # Calculate Position on the Canvas
        dx = mx - x/2 + canvasSize[0]/2
        dy = my - y/2 + canvasSize[1]/2
        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )
В конце мы также рисуем круг, который показывает пользователям, насколько велика кисть и какого цвета:

    # Reference Dot
    pygame.draw.circle(
        screen,
        drawColor,
        [100, 100],
        brushSize,
    )
    pygame.display.flip()
    fpsClock.tick(fps)
Витрина
Витрина текстового редактора

Удивительно, посмотрите, как вы можете настроить инструмент, как вы хотите!

Получить полный код можно здесь.

Если вы хотите узнать больше об использовании Tkinter, ознакомьтесь с этим учебником, где вы создаете приложение калькулятора вместе со многими функциями!

Если вы хотите создать больше графических интерфейсов с помощью Python, посетите нашу страницу учебных пособий по программированию с графическим интерфейсом!