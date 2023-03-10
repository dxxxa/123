# [How to Make a Button using PyGame in Python](https://www.thepythoncode.com/article/make-a-button-using-pygame-in-python)
##
# [[] / []]()
Идея
В этой статье мы собираемся сделать класс кнопок в pygame на Python, который можно использовать по-разному. Мы делаем это, поэтому кнопка вызывает пользовательскую функцию при нажатии. Мы также включаем его для поддержки «нажатия вызова» и «однократного» нажатия. И последнее, но не менее важное: мы создадим систему для нескольких кнопок, чтобы они динамически рисовались без необходимости добавлять их в список вручную. Давайте начнем!

Импорт и настройка
Прежде чем мы создадим класс Button, нам нужно настроить жизнеспособное окно pygame, поэтому мы импортируем sys и pygame. sys потребуется позже для завершения работы окна. После этого мы инициируем pygame с помощью функции pygame.init(). После определения fps мы делаем новые часы pygame.

Мы продолжаем делать экран. После этого мы загружаем шрифт, который мы позже будем использовать в кнопках, вы можете использовать любой шрифт, который вы хотите, но я выберу Arial для этого урока. Наконец, мы составляем список, называемый объектами. Позже нам это понадобится для кнопок и динамического рисования.

# Imports
import sys
import pygame

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 40)

objects = []
Инициализация класса кнопки
Теперь мы можем, наконец, начать с класса Button. Мы кодируем __init__(), чтобы взять несколько аргументов: координаты x и y, ширину и высоту, текст в кнопке, функцию, которая будет вызвана, и будет ли кнопка нажата один раз.

Мы сопоставляем всю эту информацию с переменными в объекте. Мы также определяем некоторые цвета для трех состояний, которые будет иметь кнопка; «нормальный», «зависший» и «нажатый».

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
После того, как мы настроили переменные, мы делаем buttonSurface и buttonRect. Здесь мы используем значения, которые мы определили выше.

Мы также создаем поверхность, содержащую buttonText. Здесь мы используем переменную шрифта, которую мы определили ранее, чтобы вызвать метод render() для нее:

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
И последнее, но не менее важное: мы добавляем сам объект в список объектов. Позже мы зациклимся на этом списке, чтобы вызвать все функции process() из кнопок.

        objects.append(self)
Процесс класса кнопки
Теперь перейдем к методу process(). Это будет называться каждым кадром. Вот почему мы здесь проверяем наведение и щелчок мыши.

Начнем с определения положения мыши. После этого мы заполняем кнопку Surface нашим «нормальным» цветом, это может быть ненужным шагом, потому что она может быть перекрашена в зависимости от наведения или щелчка.

Затем мы проверяем, находится ли положение мыши внутри прямоугольника или нет. Если значение имеет значение True, мы устанавливаем для цвета цвет 'hover'.

Далее проверяем, была ли нажата левая кнопка мыши методом pygame.mouse.get_pressed(). Этот метод возвращает кортеж, представляющий нажатые состояния трех кнопок мыши. Первый – это левая кнопка, которая нам и нужна. Если это также оценивается как True, мы еще раз заполняем кнопку Surface 'нажатым' цветом.

Теперь, если мы установим для переменной onePress значение False (которое является значением по умолчанию), то будет вызвана onclickFunction(),которую мы позже определили. Это означает, что он будет вызван один раз, когда мышь нажмет на кнопку. Чтобы это работало, нам также нужен атрибут alreadyPressed в объекте, который имеет значение True при нажатии и устанавливается в False, когда мы его отпускаем.

Но, возможно, вы хотите позвонить, пока вы нажимаете на него. Вот для чего предназначено первое заявление if. Когда мы устанавливаем для onePress значение True, это происходит.

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
Последнее, что мы делаем в методе process(), это переносим текст на кнопку Surfaceface, а затем эту поверхность на экран.

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
Определение объектов кнопок
Теперь, когда мы создали класс Button, мы можем сделать небольшую функцию, которая будет передана конструктору класса. В нашем примере он просто распечатывает «Кнопка нажата».

Давайте сделаем два объекта кнопки. Нам не нужно сохранять их в переменную или что-то в этом роде, потому что конструктор уже делает это:

def myFunction():
    print('Button Pressed')

Button(30, 30, 400, 100, 'Button One (onePress)', myFunction)
Button(30, 140, 400, 100, 'Button Two (multiPress)', myFunction, True)
Основной игровой цикл
Сначала заполняем экран темно-серым цветом в основной петле. После этого мы даем возможность пользователю остановить игру с помощью маленького крестика в правом верхнем углу окна.

В цикле объектов мы перебираем каждый объект и вызываем его функцию process(). В нашем примере этот список будет иметь два объекта кнопки. После этого мы просто переворачиваем дисплей и вызываем метод tick() на объекте clock из pygame.

while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in objects:
        object.process()
    pygame.display.flip()
    fpsClock.tick(fps)
Результат
В следующем GIF-файле показано, как работает кнопка:

Результирующие кнопкиЗамечательно! Теперь вы знаете, как сделать кнопку в , посмотрите, как вы можете настроить кнопки, отредактировав переменные, которые мы установили в этом учебнике.pygame