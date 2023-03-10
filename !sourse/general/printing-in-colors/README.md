# [How to Change Text Color in Python](https://www.thepythoncode.com/article/change-text-color-in-python)
##
# [[] / []]()
Печать на консоли в разных цветах довольно удобна и довольно практична, от создания причудливых сценариев сканирования до различения различных типов сообщений журнала (отладочный, информационный или критический и т. Д.) В ваших программах. В этом учебнике вы узнаете, как печатать цветной текст на Python с помощью библиотеки colorama.

Мы будем использовать colorama, давайте сначала установим его:

$ pip install colorama
Затем откройте новый файл Python и напишите следующее:

from colorama import init, Fore, Back, Style

# essential for Windows environment
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
Во-первых, мы вызываем функцию init(), которая необходима в среде Windows для правильной работы colorama, она ничего не делает на других платформах, поэтому вы можете удалить ее.

Во-вторых, мы определяем все доступные цвета переднего плана в списке FORES и фоновые цвета в списке BACKS, мы также определяем список ЯРКОСТИ для разных настроек яркости.

Далее давайте сделаем функцию, которая обертывает обычную функцию Python print(), но с возможностью установки цвета и яркости:

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)
Мы просто используем print() внутри, но предваряя текст с яркостью и цветовыми кодами и добавляя Style.RESET_ALL в конце концов, чтобы сбросить цвет и яркость по умолчанию каждый раз, когда мы используем функцию.

Мы также передаем **kwargs, чтобы мы могли использовать другие аргументы ключевых слов функции print(), такие как end и sep.

Теперь, когда у нас есть наша функция, давайте использовать все цвета переднего плана и напечатать один и тот же текст с разными цветами и каждый с разной яркостью:

# printing all available foreground colors with different brightness
for fore in FORES:
    for brightness in BRIGHTNESS:
        print_with_color("Hello world!", color=fore, brightness=brightness)
Это будет выглядеть так, как показано на следующем рисунке:

Один и тот же текст с разными цветами в PythonЧерный не отображается, так как цвет фона терминала также черный, вот с другим цветом фона:

Один и тот же текст с разными цветами в PythonТеперь давайте использовать цвета фона:

# printing all available foreground and background colors with different brightness
for fore in FORES:
    for back in BACKS:
        for brightness in BRIGHTNESS:
            print_with_color("A", color=back+fore, brightness=brightness, end=' ')
    print()
Вы можете изменить фон и цвет переднего плана одновременно, поэтому мы также перебираем цвета переднего плана, вот как это будет выглядеть:

Различные цвета фона с Colorama в Python

Заключение
Ну вот! Теперь вы знаете все доступные цвета переднего плана и фона, а также значения яркости в библиотеке colorama в Python. Я надеюсь, что это было полезно для вас, чтобы быстро понять информацию и скопировать код для ваших проектов.