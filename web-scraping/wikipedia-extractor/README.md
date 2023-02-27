# [How to Access Wikipedia in Python](https://www.thepythoncode.com/article/access-wikipedia-python)
To run this:
- `pip3 install -r requirements.txt`
- `python3 wikipedia_extractor.py`
##
# [[] / []]()
Википедия, без сомнения, является крупнейшей и самой популярной общей справочной работой в Интернете, это один из самых популярных веб-сайтов. Он содержит исключительно бесплатный контент. В результате возможность доступа к этому большому количеству информации на Python является удобной работой. В этом уроке вы сможете легко извлекать информацию из Википедии без какой-либо тяжелой работы.

СВЯЗАННЫЕ С: Как извлечь все ссылки на веб-сайты на Python.

Я должен отметить, что мы не собираемся очищать страницы Википедии вручную, модуль Википедии уже сделал тяжелую работу за нас. Давайте установим его:

$ pip3 install wikipedia
Откройте интерактивную оболочку Python или пустой файл и следуйте инструкциям.

Давайте получим краткое изложение того, что такое язык программирования Python:

import wikipedia
# print the summary of what python is
print(wikipedia.summary("Python Programming Language"))
Это извлечет резюме с этой страницы Википедии. Более конкретно, он будет печатать некоторые первые предложения, мы можем указать количество предложений для извлечения:

In [2]: wikipedia.summary("Python programming languag", sentences=2)
Out[2]: "Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace."
Обратите внимание, что я намеренно неправильно написал запрос, это все равно дает мне точный результат.

Поиск термина в поиске Википедии:

In [3]: result = wikipedia.search("Neural networks")
In [4]: print(result)
['Neural network', 'Artificial neural network', 'Convolutional neural network', 'Recurrent neural network', 'Rectifier (neural networks)', 'Feedforward neural network', 'Neural circuit', 'Quantum neural network', 'Dropout (neural networks)', 'Types of artificial neural networks']
Это вернуло список связанных заголовков страниц, let's получает всю страницу для «Нейронной сети», которая является результатом[0]:

# get the page: Neural network
page = wikipedia.page(result[0])
Извлечение заголовка:

# get the title of the page
title = page.title
Получение всех категорий этой страницы Википедии:

# get the categories of the page
categories = page.categories
Извлечение текста после удаления всех HTML-тегов (это делается автоматически):

# get the whole wikipedia page text (content)
content = page.content
Все ссылки:

# get all the links in the page
links = page.links
Ссылки:

# get the page references
references = page.references
Наконец, резюме:

# summary
summary = page.summary
Давайте распечатаем их:

# print info
print("Page content:\n", content, "\n")
print("Page title:", title, "\n")
print("Categories:", categories, "\n")
print("Links:", links, "\n")
print("References:", references, "\n")
print("Summary:", summary, "\n")
Попробуйте!

Вы также можете изменить язык в библиотеке википедии на Python с английского на другой по вашему выбору:

# changing language
# for a list of available languages, 
# check http://meta.wikimedia.org/wiki/List_of_Wikipedias link.
language = "es"
wikipedia.set_lang(language)
# get a page and print the summary in the new language
print(f"Summary of web scraping in {language}:", wikipedia.page("Web Scraping").summary)
Выше мы изменили язык, используя функцию wikipedia.set_lang(), а затем извлекли наши страницы в обычном режиме. Список доступных языков можно найти по этой ссылке.

Хорошо, мы закончили, это было краткое введение в то, как вы можете извлечь информацию из Википедии на Python. Это может быть полезно, если вы хотите автоматически собирать данные для языковых моделей, сделать чат-бота, отвечающего на вопросы, сделать приложение-оболочку вокруг этого и многое другое! Возможности безграничны, расскажите нам, что вы сделали с этим в комментариях ниже!

Если вы заинтересованы в извлечении данных из видео YouTube, ознакомьтесь с этим руководством.