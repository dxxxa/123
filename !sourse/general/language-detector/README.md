# [How to Make a Language Detector Using Python](https://www.thepythoncode.com/article/language-detector-in-python)
##
# [[] / []]()
Python является универсальным языком, который имеет множество приложений в разных областях. В этой статье мы будем использовать Python для создания детектора языка.

Детектор языка - это инструмент, который может автоматически идентифицировать язык данного текста. Это может быть полезно в нескольких ситуациях. Например, предположим, что вы хотите классифицировать или фильтровать статьи в блоге на основе их языков или чистых данных в проектах обработки и анализа данных. В этом случае вы можете легко сделать все это с помощью инструмента детектора языка.

Python предоставляет множество пакетов для обнаружения языков, но в этой статье будут рассмотрены четыре различных пакета Python, которые используются для обнаружения языков: langdetect, langid, googletrans и language_detector.

Вот оглавление:

Установка необходимых пакетов
Создание средства командной строки детектора языка с помощью
langdetect
лангид
гуглтранс
language_detector
Заключение
На протяжении всей этой статьи мы будем использовать эти предложения для обнаружения языков:

I love programming, Python is my favorite language.
أحب البرمجة ، بايثون هي لغتي المفضلة.
我喜欢编程，Python 是我最喜欢的语言。
Me encanta programar, Python es mi lenguaje favorito.
Eu amo programar, Python é minha linguagem favorita.
Это одно и то же предложение, переведенное на разные языки. Чтобы получить доступ ко всем языковым кодам, которые мы будем использовать в этой статье, посетите эту страницу.

Установка необходимых пакетов
Прежде всего, первой задачей является установка всех необходимых пакетов, так как их нет в стандартных пакетах утилит Python. Мы, прежде всего, создадим виртуальную среду, а затем установим в нее все необходимые пакеты:

$ python -m venv project
И активируйте его с помощью команды на Windows:

$ .\project\Scripts\activate
или Linux/macOS:

$ source project/bin/activate
Теперь, когда виртуальная среда запущена и работает, давайте установим все пакеты, которые мы собираемся использовать:

$ pip install langdetect langid googletrans==3.1.0a0 language-detector
Создание средства командной строки детектора языка
В этом разделе мы создадим инструмент командной строки детектора языка, используя по одному пакету за раз. Поэтому внутри виртуальной среды создайте два файла и назовите их language_detector_cli_1.py и предложениями.txt соответственно:



Обратите внимание, что вы можете называть файлы как угодно в соответствии с вашими предпочтениями, но убедитесь, что имена имеют смысл. В файлах предложений.txt у нас будут предложения, которые мы хотим обнаружить, поэтому откройте и вставьте эти строки:

I love programming, Python is my favorite language.
أحب البرمجة ، بايثون هي لغتي المفضلة.
我喜欢编程，Python 是我最喜欢的语言。
Me encanta programar, Python es mi lenguaje favorito.
Eu amo programar, Python é minha linguagem favorita.
В этот файл можно добавить столько предложений, сколько захотите.

langdetect
Наша первая реализация инструмента командной строки детектора языка будет использовать пакет langdetect. Как упоминалось в документации, он поддерживает 55 языков и является частью библиотеки обнаружения языков Google.

Откройте .py файл, который мы только что создали, и вставьте следующий код:

# import the detect function from langdetect
from langdetect import detect
# openning the txt file in read mode
sentences_file = open('sentences.txt', 'r')
# creating a list of sentences using the readlines() function
sentences = sentences_file.readlines()
Здесь мы импортируем функцию detect() из пакета langdetect, мы будем использовать ее для обнаружения слов или предложений. Затем открываем предложения.txt файл в режиме чтения, после успешного открытия получаем из него все предложения.

Создадим теперь функцию обнаружения языков; мы назовем его detect_language() и вставим следующий код:

# a function for detection language
def detect_langauage(sentence, n):
    """try and except block for catching exception errors"""
    # the try will run when everything is ok
    try:
        # checking if the sentence[n] exists
        if sentences[n]:
            # creating a new variable, the strip() function removes newlines
            new_sentence = sentences[n].strip('\n')
            print(f'The language for the sentence "{new_sentence}" is {detect(new_sentence)}')
    # this will catch all the errors that occur  
    except:
        print(f'Sentence does not exist')
Давайте немного разобьем код внутри функции detect_language(), чтобы мы были на одной странице. Функция принимает два аргумента, предложение и n, предложение имеет тип str, а n - тип int, и внутри этой функции у нас есть блок try/except для обработки любых ошибок.

Внутри оператора try у нас есть оператор if, проверяющий, существует ли предложение. Если это предложение существует, мы удаляем из него символы новой строки и обнаруживаем язык. Внутри этого мы просто ловим любые ошибки, которые могут возникнуть. Наконец, чуть ниже функции вставьте следующий код:

# printing the the number of sentences in the sentences.txt   
print(f'You have {len(sentences)} sentences')
# this will prompt the user to enter an integer
number_of_sentence = int(input('Which sentence do you want to detect?(Provide an integer please):'))
# calling the detect_langauage function
detect_langauage(sentences_file, number_of_sentence)
У нас есть функция print(), функция input() для получения данных от пользователя и вызов функции. Давайте теперь протестируем программу; мы определим язык первого предложения из файла sentences_file.txt, число которого равно 0.

Теперь давайте запустим его:

$ python language_detector_cli_1.py
Выходные данные будут выглядеть следующим образом после предоставления 0 в качестве входных данных:

You have 5 sentences
Which sentence do you want to detect?(Provide an integer please):0
The language for the sentence "I love programming, Python is my favorite language." is en
Если вы проверяете коды языков, en — это английский язык.

Примечание: Как упоминалось в документации, пакет langdetect использует недетерминированный алгоритм, что означает, что вы можете получать разные результаты каждый раз, когда пытаетесь обнаружить короткий или неоднозначный текст.

лангид
Второй пакет, который мы можем использовать для определения языка, — это пакет langid. Откройте еще один новый файл Python, назовите его language_detector_cli_2.py и сделайте так, чтобы он выглядел следующим образом:

import langid

# opening the txt file in read mode
sentences_file = open('sentences.txt', 'r')
# creating a list of sentences using the readlines() function
sentences = sentences_file.readlines()
# looping through all the sentences in thesentences.txt file
for sentence in sentences:
    # detecting the languages for the sentences
    lang = langid.classify(sentence)
    # formatting the sentence by removing the newline characters
    formatted_sentence = sentence.strip('\n')
    print(f'The sentence "{formatted_sentence}" is in {lang[0]}')
В приведенном выше фрагменте кода мы импортируем langid, затем открываем предложения.txt файл и читаем пять предложений.

После этого мы перебираем все эти предложения и, в то же время, определяем язык каждого предложения с помощью функции langid.classify(), эта функция принимает предложение в качестве аргумента, и, наконец, мы печатаем отформатированный результат.

Давайте запустим его:

$ python langauage_detector_cli_2.py
Результат, который мы получаем, выглядит следующим образом:

The sentence "I love programming, Python is my favorite language." is in en
The sentence "أحب البرمجة ، بايثون هي لغتي المفضلة." is in ar
The sentence "我喜欢编程，Python 是我最喜欢的语言。" is in zh
The sentence "Me encanta programar, Python es mi lenguaje favorito." is in es
The sentence "Eu amo programar, Python é minha linguagem favorita." is in gl
Все прогнозы верны, кроме последнего, где должно быть pt.

гуглтранс
Третьим в списке является пакет googletrans, этот пакет можно использовать для переводов и определения языка. Мы использовали его в учебнике по переводу текста, если вы хотите проверить его.

Согласно документации, он бесплатный и неограниченный. Теперь давайте использовать его для обнаружения языков; откройте новый файл Python, назовите его language_detector_cli_3.py и добавьте следующее:

# importing the Translator function from googletrans
from googletrans import Translator
# translator object
translator = Translator()
Мы импортируем объект Translator из googletrans, а затем инициализируем его. Теперь, поскольку мы будем получать предложения из файлов предложений.txt, нам нужно открыть его и получить предложения:

# openning the txt file in read mode
sentences_file = open('sentences.txt', 'r')
# creating a list of sentences using the readlines() function
sentences = sentences_file.readlines()
А для обнаружения языков воспользуемся этой функцией:

# a function for detection language
def detect_langauage(sentence, n):
    """try and except block for catching exception errors"""
    # the try will run when everything is ok
    try:
        # checking if the sentence[n] exists
        if sentences[n]:
            # creating a new variable, the strip() function removes newlines
            new_sentence = sentences[n].strip('\n')
            # detecting the sentence language using the translator.detect()
            # .lang extract the language code
            detected_sentence_lang = translator.detect(new_sentence).lang 
            print(f'The language for the sentence "{new_sentence}" is {detected_sentence_lang}')
    # this will catch all the errors that occur  
    except:
        print(f'Make sure the sentence exists or you have internet connection')
Приведенная выше функция похожа на другую функцию, которую мы использовали для пакета langdetect, но разница заключается в этой строке кода внутри оператора if.

Мы используем translator.detect() для обнаружения языка и извлечения кода языка с помощью атрибута lang.

И, наконец, вставьте следующие строки кода после функции:

print(f'You have {len(sentences)} sentences')
# this will prompt the user to enter an integer
number_of_sentence = int(input('Which sentence do you want to detect?(Provide an integer please):'))
# calling the detect_langauage function
detect_langauage(sentences_file, number_of_sentence)
Чтобы запустить программу, используйте следующую команду:

$ python langauage_detector_cli_3.py
Вам будет предложено выбрать предложение для обнаружения, и это результат, который вы получите после предоставления допустимого ввода:

You have 5 sentences
Which sentence do you want to detect?(Provide an integer please):1
The language for the sentence "أحب البرمجة ، بايثون هي لغتي المفضلة." is ar
language_detector
Наш окончательный пакет для определения языка - это language_detector, без лишних слов, открыть новый файл Python, назвать его language_detector_cli_4.py и импортировать пакет:

from language_detector import detect_language
Теперь мы создадим функцию для обработки обнаружения языка и назовем ее detectLanguage().

Здесь следует отметить, что мы импортировали detect_language из language_detector; это не должно противоречить имени функции; вот почему мы назвали функцию detectLanguage(). Функция примет текст в качестве аргумента:

def detectLanguage(text):
    # detecting the language using the detect_language function
    language = detect_language(text)
    print(f'"{text}" is written in {language}')
В приведенной выше функции текст, переданный функции detectLanguage(), также передается в detect_language().

Сразу после обнаружения функцииLanguage() вставьте следующий код:

# an infinite while while loop
while True:
    # this will prompt the user to enter options
    option = input('Enter 1 to detect language or 0 to exit:')
    if option == '1':
        # this will prompt the user to enter the text
        data = input('Enter your sentence or word here:')
        # calling the detectLanguage function
        detectLanguage(data)
    # if option is 0 break the loop   
    elif option == '0':
        print('Quitting........\nByee!!!')
        break
    # if option isnt 1 or 0 then its invalid 
    else:
        print('Wrong input, try again!!!')
В приведенном выше фрагменте кода у нас есть бесконечный цикл while; пользователю будет предложено ввести два варианта, 1 и 0. Если параметр равен 1, пользователю будет предложено ввести текст для обнаружения, если параметр равен 0, цикл будет разорван, а если параметры не являются ни 1, ни 0, пользователь будет уведомлен о неправильном вводе.

Чтобы протестировать эту программу, выполните:

$ python langauage_detector_cli_4.py
Результат:

Enter 1 to detect language or 0 to exit:1
Enter your sentence or word here:J'adore programmer, Python est mon langage préféré
"J'adore programmer, Python est mon langage préféré" is written in French
Enter 1 to detect language or 0 to exit:0
Quitting........
Byee!!!
Заключение 
В этой статье показано, как сделать детектор языка с помощью Python. Мы не исчерпали весь список пакетов, которые можно использовать для обнаружения языков, но надеемся, что теперь вы знаете, как обнаруживать языки с помощью Python.

Некоторые пакеты, которые мы использовали, были недостаточно точными, но хорошо, что Python поставляется с другими, более точными пакетами для работы. Я приглашаю вас поэкспериментировать с библиотеками и посмотреть, какая из них подходит вам лучше всего.