# [How to Make a Planet Simulator with PyGame in Python](https://www.thepythoncode.com/article/make-a-planet-simulator-using-pygame-in-python)
##
# [[] / []]()
В этом уроке мы собираемся сделать небольшую симуляцию планеты с помощью Python и библиотеки игр PyGame. PyGame имеет удобный векторный класс, который может помочь нам при моделировании планет и их направления.

Импорт
Все модули, которые мы импортируем, встроены, за исключением библиотеки pygame, которую мы должны установить с pip install pygame. Нам также нужен sys, но он будет просто использоваться для остановки игры при нажатии на x в левом верхнем углу окна.

После этого мы получаем класс Vector2 из pygame.math, который предлагает некоторые интересные методы для использования, когда мы хотим работать с векторами.

Функция randrange() из случайного будет просто использоваться, когда мы создадим некоторые планеты. Мы также получаем ctypes для обеспечения высокого DPI. Это часто используется с tkinter, но мы также можем использовать его здесь, хотя это не имеет такого большого эффекта.

# Imports
import pygame
import sys

# We will work with Vector2 because it has some useful functions.
from pygame.math import Vector2

from random import randrange

import ctypes

# Enable High Dots Per Inch so the image displayed on the window is sharper.
ctypes.windll.shcore.SetProcessDpiAwareness(1)
Настройка Pygame
Далее мы настроили pygame. Для этого мы начнем с pygame.init(), который должен быть вызван, чтобы все модули работали. После этого мы определяем fps игры, и мы делаем объект часов, который будет обрабатывать скорость игры в сочетании с определенными fps:

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
Мы продолжаем, определяя размер окна и делая окно с этими размерами.

# Window Size
windowdim = Vector2(800, 800)
screen = pygame.display.set_mode((int(windowdim.x), int(windowdim.y)))
Планетарный класс
Давайте перейдем к классу планет, это основная часть кода этой программы, потому что она позволяет нам создавать бесконечное количество планет, которые будут реагировать друг на друга.

Вне класса нам нужно определить список, который содержит все планеты. Затем в главном цикле мы зацикливаемся на этом списке и вызываем метод для всех этих объектов.

# all the Planets are stored here
# They will append themselves.
planets = []
Функция конструктора
Сначала поговорим о конструкторе класса. Мы предоставляем каждой планете начальную позицию, и у нас есть следующие необязательные аргументы; дельта, которая является скоростью, радиусом планеты, и если планета неподвижна. Мы устанавливаем все эти входные данные в качестве атрибутов объектов.

# The Planet Class which will handle drawing and calculating planets.
class Planet():
    def __init__(self, position, delta=Vector2(0, 0), radius=10, imovable=False):

        # Where the planet is at the moment
        self.position = position

        # The Radius determines how much this planet affects others
        self.radius = radius

        # The Velocity
        self.delta = delta

        # If this planet is moving
        self.imovable = imovable

        # If this planet can be eaten by others.
        self.eatable = False
В конце конструктора мы добавляем сам объект в список планет, поэтому нам не нужно делать это вручную.

        # Appending itself to the list so its process
        # function will later be called in a loop.
        planets.append(self)
Функция процесса
Функция process() будет вызываться для каждой планеты в каждом кадре. Код перемещения будет пропущен, если для свойства imovable задано значение True. Если планета может двигаться, она будет петлять через любую другую планету, и если планета не является самим объектом, мы продолжаем.

Если планета находится слишком близко к этой, она будет съедена, это делается путем добавления радиуса этой планеты к другой и удаления этой планеты из списка.

Если это не так, мы вычисляем вектор на другую планету, а затем добавляем его к дельте. Теперь весь этот код находится в блоке try-except, потому что он не будет работать, если планеты находятся друг над другом. После этого добавляем дельту в позицию:

    def process(self):
        # This function will be called once every frame 
        # and it is responsible for calculating where the planet will go.

        # No Movement Calculations will happen if the planet doesnt move at all.
        # it also wont be eaten.
        if not self.imovable:
            for i in planets:
                if not i is self:
                    try:
                        if self.eatable:
                            if self.position.distance_to(i.position) < self.radius + i.radius:
                                print('Eaten')
                                i.radius += self.radius
                                planets.remove(self)
                        dir_from_obj  = (i.position - self.position).normalize() * 0.01 * (i.radius / 10)
                        self.delta += dir_from_obj
                    except:
                        print('In the same spot')

            self.position += self.delta
В конце концов, мы рисуем планету в ее положении, это делается даже в том случае, если планета неподвижна:

        # Drawing the planet at the current position.
        pygame.draw.circle(
            screen,
            [255, 255, 255],
            self.position,
            self.radius,
        )
Главная петля
И последнее, но не менее важное: у нас есть основной цикл, который будет охлаждать функцию процесса на каждой планете в списке планет в каждом кадре.

# Game loop.
while  True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for p in planets:
        p.process()

    pygame.display.flip()
    fpsClock.tick(fps)
Теперь этот код не будет порождать планеты сам по себе. В следующей части мы рассмотрим некоторые примеры.

Примеры
Солнце и две противоположные планеты
Этот код запускается прямо перед основным циклом, и он порождает три планеты. После кода вы увидите его в действии.

# Sun and two opposing Planets
Planet(Vector2(400, 400), radius=50, imovable=True)

Planet(Vector2(400, 200), delta=Vector2(3, 0), radius=10)
Planet(Vector2(400, 600), delta=Vector2(-3, 0), radius=10)
Солнце и две противоположные планеты

Солнце и четыре противоположные планеты
# Sun and four opposing Planets
Planet(Vector2(400, 400), radius=50, imovable=True)

Planet(Vector2(400, 200), delta=Vector2(3, 0), radius=10)
Planet(Vector2(400, 600), delta=Vector2(-3, 0), radius=10)
Planet(Vector2(600, 400), delta=Vector2(0, 3), radius=10)
Planet(Vector2(200, 400), delta=Vector2(0, -3), radius=10)
Солнце и четыре противоположные планеты

Два Солнца и Две Планеты
# Two Suns and two planets
Planet(Vector2(600, 400), radius=20, imovable=True)
Planet(Vector2(200, 400), radius=20, imovable=True)

Planet(Vector2(400, 200), delta=Vector2(0, 0), radius=10)
Planet(Vector2(400, 210), delta=Vector2(1, 2), radius=5)
Два Солнца и две планеты

Сетка

# Grid
gridDimension = 10
gridgap = 80
for x in range(gridDimension):
    for y in range(gridDimension):
        Planet(Vector2(gridgap * x + 40, gridgap * y + 40), radius=3, imovable=True)

Planet(Vector2(200, 200), delta=Vector2(randrange(-3, 3), 2), radius=5)
Сетка

Заключение
Отлично! Вы успешно создали программу моделирования планет с помощью Python! Вы всегда можете поэкспериментировать с различными настройками планет и увидеть результаты сами.