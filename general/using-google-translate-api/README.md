# [How to Translate Text in Python](https://www.thepythoncode.com/article/translate-text-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Tutorial code is in `translator.py`.
- If you want to translate a document, you can use `translate_doc.py`:
    ```
    python3 translate_doc.py --help
    ```
    **Output:**
    ```
    usage: translate_doc.py [-h] [-s SOURCE] [-d DESTINATION] target

    Simple Python script to translate text using Google Translate API (googletrans
    wrapper)

    positional arguments:
    target                Text/Document to translate

    optional arguments:
    -h, --help            show this help message and exit
    -s SOURCE, --source SOURCE
                            Source language, default is Google Translate's auto
                            detection
    -d DESTINATION, --destination DESTINATION
                            Destination language, default is English
    ```
- For instance, if you want to translate text in the document `wonderland.txt` from english (`en` as language code) to arabic (`ar` as language code):
    ```
    python translate_doc.py wonderland.txt --source en --destination ar
    ```
    A new file `wonderland_ar.txt` will appear in the current directory that contains the translated document.
- You can also translate text and print in the stdout using `translate_doc.py`:
    ```
    python translate_doc.py 'Bonjour' -s fr -d en
    ```
    **Output:**
    ```
    'Hello'
    ```
##
# [[] / []]()
Google Translate - это бесплатный сервис, который переводит слова, фразы и целые веб-страницы на более чем 100 языков. Вы, вероятно, уже знаете это, и вы использовали его много раз в своей жизни.

Из этого туториала Вы узнаете, как выполнять языковой перевод на Python с помощью библиотеки Googletrans. Googletrans - это бесплатная и неограниченная библиотека Python, которая делает неофициальные Ajax-вызовы к Google Translate API для обнаружения языков и перевода текста.

Эта библиотека предназначена не только для перевода; у нас есть учебник по обнаружению языков с использованием именно этой библиотеки, среди прочих.

Вот основные особенности этой библиотеки:

Автоматическое определение языка (оно также предлагает определение языка)
Массовые переводы
Быстрый
Поддержка HTTP/2
Пул подключений
Обратите внимание, что Googletrans выполняет вызовы API к API перевода Google. Если вы хотите надежного использования, рассмотрите возможность использования официального API или создания собственной модели машинного перевода.

Во-первых, давайте установим его с помощью pip:

pip3 install googletrans
Узнайте также: Как выполнять суммирование текста с помощью transformers в Python.

Перевод текста
Импорт необходимых библиотек:

from googletrans import Translator, constants
from pprint import pprint
Googletrans предоставляет нам удобный интерфейс. Давайте инициализируем наш экземпляр переводчика:

# init the Google API translator
translator = Translator()
Обратите внимание, что класс Translator имеет несколько необязательных аргументов:

service_urls: это должен быть список строк, которые являются URL-адресами API google translate; примером является ["translate.google.com", "translate.google.co.uk"]..
user_agent: строка, которая будет включена в заголовок User-Agent в запросе.
прокси (словарь): Словарь Python, который сопоставляет протокол или протокол и хост с URL-адресом прокси-сервера; Примером может служить {'http': 'example.com:3128', 'http://domain.example': 'example.com:3555'}, подробнее о прокси в этом учебнике.
timeout: время ожидания каждого запроса, которое вы делаете, выраженное в секундах.
Теперь мы просто используем метод translate(), чтобы получить переведенный текст:

# translate a spanish text to english text (by default)
translation = translator.translate("Hola Mundo")
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
Это приведет к печати оригинального текста и языка вместе с переведенным текстом и языком:

Hola Mundo (es) --> Hello World (en)
Если приведенный выше код приводит к ошибке, подобной этой:

AttributeError: 'NoneType' object has no attribute 'group'
Затем вы должны удалить текущую версию googletrans и установить новую, используя следующие команды:

$ pip3 uninstall googletrans
$ pip3 install googletrans==3.1.0a0
Возвращаясь к коду, он автоматически определяет язык и переводит на английский по умолчанию, давайте переведем на другой язык, арабский, например:

# translate a spanish text to arabic for instance
translation = translator.translate("Hola Mundo", dest="ar")
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
"ar" - это код языка для арабского языка. Вот выходные данные:

Hola Mundo (es) --> مرحبا بالعالم (ar)
Теперь давайте установим исходный язык и переведем его на английский:

# specify source language
translation = translator.translate("Wie gehts ?", src="de")
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
Выпуск:

Wie gehts ? (de) --> How are you ? (en)
Вы также можете проверить другие переводы и некоторые другие дополнительные данные:

# print all translations and other data
pprint(translation.extra_data)
Смотрите выходные данные:

{'all-translations': [['interjection',
                       ['How are you doing?', "What's up?"],
                       [['How are you doing?', ["Wie geht's?"]],
                        ["What's up?", ["Wie geht's?"]]],
                       "Wie geht's?",
                       9]],
 'confidence': 1.0,
 'definitions': None,
 'examples': None,
 'language': [['de'], None, [1.0], ['de']],
 'original-language': 'de',
 'possible-mistakes': None,
 'possible-translations': [['Wie gehts ?',
                            None,
                            [['How are you ?', 1000, True, False],
                             ["How's it going ?", 1000, True, False],
                             ['How are you?', 0, True, False]],
                            [[0, 11]],
                            'Wie gehts ?',
                            0,
                            0]],
 'see-also': None,
 'synonyms': None,
 'translation': [['How are you ?', 'Wie gehts ?', None, None, 1]]}
Много данных, из которых можно извлечь выгоду; у вас есть все возможные переводы, уверенность, определения и даже примеры.

Связанные с: Как перефразировать текст с помощью трансформеров в Python.

Перевод списка фраз
Вы также можете передать список текста для перевода каждого предложения в отдельности:

# translate more than a phrase
sentences = [
    "Hello everyone",
    "How are you ?",
    "Do you speak english ?",
    "Good bye!"
]
translations = translator.translate(sentences, dest="tr")
for translation in translations:
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
Выпуск:

Hello everyone (en) --> herkese merhaba (tr)
How are you ? (en) --> Nasılsın ? (tr)
Do you speak english ? (en) --> İngilizce biliyor musunuz ? (tr)
Good bye! (en) --> Güle güle! (tr)
Определение языка
API Google Translate также предлагает нам вызовы обнаружения языка:

# detect a language
detection = translator.detect("नमस्ते दुनिया")
print("Language code:", detection.lang)
print("Confidence:", detection.confidence)
Это приведет к печати кода обнаруженного языка вместе с коэффициентом достоверности (1,0 означает 100% уверенность):

Language code: hi
Confidence: 1.0
Это вернет код языка, чтобы получить полное имя языка, вы можете использовать словарь LANGUAGES, предоставленный Googletrans:

print("Language:", constants.LANGUAGES[detection.lang])
Выпуск:

Language: hindi
Читайте также: Разговорный чат-бот AI с трансформерами на Python.

Поддерживаемые языки
Как вы, возможно, знаете, Google Translate поддерживает более 100 языков. Давайте напечатаем их все:

# print all available languages
print("Total supported languages:", len(constants.LANGUAGES))
print("Languages:")
pprint(constants.LANGUAGES)
Вот усеченные выходные данные:

Total supported languages: 107
{'af': 'afrikaans',
 'sq': 'albanian',
 'am': 'amharic',
 'ar': 'arabic',
 'hy': 'armenian',
...
<SNIPPED>
...
 'vi': 'vietnamese',
 'cy': 'welsh',
 'xh': 'xhosa',
 'yi': 'yiddish',
 'yo': 'yoruba',
 'zu': 'zulu'}
Заключение
Вот оно. Эта библиотека отлично подходит для всех, кто хочет быстрый способ перевода текста в приложении. Однако эта библиотека является неофициальной, как упоминалось ранее; автор отметил, что максимальная длина символа на одном тексте составляет 15K.

Это также не гарантирует, что библиотека будет работать должным образом в любое время; если вы хотите использовать стабильный API, вы должны использовать официальный API Google Translate.

Если вы получаете ошибки HTTP 5xx с этой библиотекой, то Google заблокировал ваш IP-адрес; это потому, что используя эту библиотеку часто, Google Translate может заблокировать ваш IP-адрес; Вам нужно будет рассмотреть возможность использования прокси-серверов, передав прокси-словарь параметру proxies в классе Translator() или использовать официальный API, как обсуждалось.

Кроме того, я написал быстрый скрипт Python, который позволит вам переводить текст в предложения и документы в командной строке. Проверьте это здесь.