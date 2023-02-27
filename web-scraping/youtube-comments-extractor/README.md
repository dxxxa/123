# [How to Extract YouTube Comments in Python](https://www.thepythoncode.com/article/extract-youtube-comments-in-python)
To run this:
- `pip3 install -r requirements.txt`
- ```
    python youtube_comment_extractor.py --help
    ```
    **Output:**
    ```
    usage: youtube_comment_extractor.py [-h] [-l LIMIT] [-o OUTPUT] url

    Simple YouTube Comment extractor

    positional arguments:
    url                   The YouTube video full URL

    optional arguments:
    -h, --help            show this help message and exit
    -l LIMIT, --limit LIMIT
                            Number of maximum comments to extract, helpful for
                            longer videos
    -o OUTPUT, --output OUTPUT
                            Output JSON file, e.g data.json
    ```
- To download the latest 50 comments from https://www.youtube.com/watch?v=jNQXAC9IVRw and save them to `data.json`:
    ```
    python youtube_comment_extractor.py https://www.youtube.com/watch?v=jNQXAC9IVRw --limit 50 --output data.json
    ```
##
# [[] / []]()
Возможность извлекать комментарии с крупнейшего веб-сайта обмена видео в Интернете - это удобный инструмент, вы можете извлекать комментарии для выполнения таких задач, как классификация текста, или вы можете захотеть извлечь комментарии к своим видео на YouTube для выполнения определенных задач, возможности бесконечны.

В этом уроке мы не только напишем скрипт Python для извлечения комментариев YouTube, но и будем экспериментировать с сетевой утилитой в инструментах разработчика браузера, чтобы захватить правильный запрос комментариев, чтобы он мог помочь нам в написании кода.

Заметка: Если код этого учебника не работает для вас, пожалуйста, ознакомьтесь с учебником по API YouTube.

Связанные с: Как извлечь данные YouTube в Python.

Прежде чем мы начнем, давайте установим требования:

pip3 install requests
Мониторинг сетевого трафика в браузере
Теперь, чтобы следовать вместе со мной, зайдите в любое видео YouTube по вашему выбору с помощью Chrome или любого другого браузера и щелкните правой кнопкой мыши и выберите Inspect Element и перейдите в раздел «Сеть»:

Мониторинг сетевого трафика в браузереОбратите внимание, что я написал в поле ввода фильтра, это поможет нам отфильтровать нежелательные HTTP-запросы, такие как изображения, файлы стиля и Javascript и т. Д."comment"

Теперь перейдите на страницу видео и прокрутите вниз, пока не увидите загруженные комментарии. Если вы вернетесь к сетевому инструменту, вы увидите что-то вроде этого:

Обнаружен новый запрос комментариев

Отлично, мы успешно захватили запрос комментария, если вы нажмете на него, вы увидите фактический URL-адрес запроса, метод и удаленный IP-адрес:

Комментарий запрос общих деталейПока это хорошо, помните, что цель здесь состоит в том, чтобы смоделировать этот HTTP-запрос на Python, но поскольку это запрос POST, нам понадобятся дополнительные детали, такие как тело POST и параметры URL.

Если мы прокрутим вниз вниз в том же разделе (Заголовки), мы увидим параметры строки запроса и данные формы, например:

Комментарий Запрос ДеталиПотрясающе, поэтому нам нужны , , , , и параметры. Примечание и параметры должны иметь значение , и иметь одно и то же значение. action_get_commentspbjctokencontinuationitctsession_tokenaction_get_commentspbj1ctokencontinuationВ следующем разделе мы увидим, как мы можем извлечь их из исходного кода страницы видео YouTube с помощью Python.

Кроме того, если вы продолжите прокручивать вниз, чтобы загрузить больше комментариев, вы увидите, что аналогичные запросы добавляются в список запросов:

2-й комментарий запрос деталейОбратите внимание, что некоторые параметры изменяют свое значение при каждом запросе загрузки комментария. Не волнуйтесь, мы рассмотрим это в следующем разделе.

Написание экстрактора комментариев на Python
Теперь, когда мы понимаем, как делается запрос на загрузку комментариев, попробуем смоделировать его в Python, импортируя необходимые модули:

import requests
import json
import time
Поскольку нам нужно будет проанализировать некоторые данные (параметры, показанные в последнем разделе) из содержимого страницы видео, мы не будем использовать синтаксический анализатор HTML, такой как BeautifulSoup, потому что большая часть данных находится в объекте Javascript в тегах скрипта. В результате следующие две функции помогут нам искать по контенту:

# from https://github.com/egbertbouman/youtube-comment-downloader
def search_dict(partial, key):
    """
    A handy function that searches for a specific `key` in a `partial` dictionary/list
    """
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                # found the key, return the value
                yield v
            else:
                # value of the dict may be another dict, so we search there again
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        # if the passed data is a list
        # iterate over it & search for the key at the items in the list
        for i in partial:
            for o in search_dict(i, key):
                yield o

# from https://github.com/egbertbouman/youtube-comment-downloader
def find_value(html, key, num_sep_chars=2, separator='"'):
    # define the start position by the position of the key + 
    # length of key + separator length (usually : and ")
    start_pos = html.find(key) + len(key) + num_sep_chars
    # the end position is the position of the separator (such as ")
    # starting from the start_pos
    end_pos = html.find(separator, start_pos)
    # return the content in this range
    return html[start_pos:end_pos]
Не пытайтесь понять их сейчас, они помогут нам во время извлечения токенов. Теперь давайте определим нашу основную функцию, которая принимает URL-адрес видео YouTube и возвращает комментарии в виде списка словарей:

def get_comments(url):
    session = requests.Session()
    # make the request
    res = session.get(url)
res имеет HTTP-ответ веб-страницы видео YouTube, теперь давайте получим маркер сеанса из возвращенного HTML-содержимого:

    # extract the XSRF token
    xsrf_token = find_value(res.text, "XSRF_TOKEN", num_sep_chars=3)
Токен XSRF - это session_token, который требуется в данных формы в запросе, если вы просмотрите источник страницы видео и выполните поиск по нему, вы найдете его там:

Маркер сеансаОтлично, давайте продолжим добычу других полей, которые являются и .ctokenitct

Приведенная ниже строка отвечает за извлечение объекта Javascript, который содержит все необходимые данные:

    # parse the YouTube initial data in the <script> tag
    data_str = find_value(res.text, 'window["ytInitialData"] = ', num_sep_chars=0, separator="\n").rstrip(";")
    # convert to Python dictionary instead of plain text string
    data = json.loads(data_str)
Вот как это выглядит в источнике страницы:

Исходные данные YouTube

Теперь данные представляют собой обычный словарь Python, который содержит все видеоданные YouTube, теперь нам нужно искать следующий словарьContinuationData, который имеет необходимые параметры:

    # search for the ctoken & continuation parameter fields
    for r in search_dict(data, "itemSectionRenderer"):
        pagination_data = next(search_dict(r, "nextContinuationData"))
        if pagination_data:
            # if we got something, break out of the loop,
            # we have the data we need
            break
    continuation_tokens = [(pagination_data['continuation'], pagination_data['clickTrackingParams'])]
Возвращаясь к источнику страницы, вот что мы ищем:

Ключи словаря для поискаПоэтому нас интересует область () и continuationctokenclickTrackingParams (itct)

Остальная часть кода делает запрос в /comment_service_ajax для получения и синтаксического анализа комментариев и сбора маркеров продолжения после каждого запроса, который мы делаем, пока не будет больше комментариев:

    while continuation_tokens:
        # keep looping until continuation tokens list is empty (no more comments)
        continuation, itct = continuation_tokens.pop()
        # construct params parameter (the ones in the URL)
        params = {
            "action_get_comments": 1,
            "pbj": 1,
            "ctoken": continuation,
            "continuation": continuation,
            "itct": itct,
        }
        # construct POST body data, which consists of the XSRF token
        data = {
            "session_token": xsrf_token,
        }
        # construct request headers
        headers = {
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20200731.02.01"
        }
        # make the POST request to get the comments data
        response = session.post("https://www.youtube.com/comment_service_ajax", params=params, data=data, headers=headers)
        # convert to a Python dictionary
        comments_data = json.loads(response.text)
        for comment in search_dict(comments_data, "commentRenderer"):
            # iterate over loaded comments and yield useful info
            yield {
                "commentId": comment["commentId"],
                "text": ''.join([c['text'] for c in comment['contentText']['runs']]),
                "time": comment['publishedTimeText']['runs'][0]['text'],
                "isLiked": comment["isLiked"],
                "likeCount": comment["likeCount"],
                # "replyCount": comment["replyCount"],
                'author': comment.get('authorText', {}).get('simpleText', ''),
                'channel': comment['authorEndpoint']['browseEndpoint']['browseId'],
                'votes': comment.get('voteCount', {}).get('simpleText', '0'),
                'photo': comment['authorThumbnail']['thumbnails'][-1]['url'],
                "authorIsChannelOwner": comment["authorIsChannelOwner"],
            }
        # load continuation tokens for next comments (ctoken & itct)
        continuation_tokens = [(next_cdata['continuation'], next_cdata['clickTrackingParams'])
                         for next_cdata in search_dict(comments_data, 'nextContinuationData')] + continuation_tokens
        # avoid heavy loads with popular videos
        time.sleep(0.1)
Отлично, давайте проверим это:

if __name__ == "__main__":
    from pprint import pprint
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    for count, comment in enumerate(get_comments(url)):
        if count == 3:
            break
        pprint(comment)
        print("="*50)
Это позволит извлечь первые 3 комментария и распечатать их:

{'author': 'wizard yt',
 'authorIsChannelOwner': False,
 'channel': 'UCNg8yS4kYFvvkOQFIwR5NqA',
 'commentId': 'UgwiWPPBdLMwnBSCPwJ4AaABAg',
 'isLiked': False,
 'likeCount': 0,
 'photo': 'https://yt3.ggpht.com/a/AATXAJyyoOqaBjwEGRqKzuykxNosYd76Tmj-AFUcgAzB=s48-c-k-c0xffffffff-no-rj-mo',
 'text': 'Sub2sub pls i request you i want 50 subs',
 'time': '2 seconds ago',
 'votes': '0'}
==================================================
{'author': 'Abdou Rockikz',
 'authorIsChannelOwner': False,
 'channel': 'UCA4FBhVyVNMO5LcRfJKwrEA',
 'commentId': 'UgzzD6ngnIFkLX_lnsx4AaABAg',
 'isLiked': False,
 'likeCount': 0,
 'photo': 'https://yt3.ggpht.com/a/AATXAJxXbUQXU551ZKsiQ2t_DF-4yLmvG-YrDnmArCuNZw=s48-c-k-c0xffffffff-no-rj-mo',
 'text': 'This is a fake comment',
 'time': '4 seconds ago',
 'votes': '0'}
==================================================
{'author': 'NIGHT Devil',
 'authorIsChannelOwner': False,
 'channel': 'UCA4FBhVyVNMO5LcRfJKwrEA',
 'commentId': 'UgxbTzFsW9wrD8qvuxJ4AaABAg',
 'isLiked': False,
 'likeCount': 0,
 'photo': 'https://yt3.ggpht.com/a/AATXAJxXbUQXU551ZKsiQ2t_DF-4yLmvG-YrDnmArCuNZw=s48-c-k-c0xffffffff-no-rj-mo',
 'text': 'CLICK <hidden> for a video',
 'time': '6 seconds ago',
 'votes': '0'}
Наконец, давайте используем модуль argparse для преобразования этого в инструмент командной строки, который может использоваться кем угодно:

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Simple YouTube Comment extractor")
    parser.add_argument("url", help="The YouTube video full URL")
    parser.add_argument("-l", "--limit", type=int, help="Number of maximum comments to extract, helpful for longer videos")
    parser.add_argument("-o", "--output", help="Output JSON file, e.g data.json")
    # parse passed arguments
    args = parser.parse_args()
    limit = args.limit
    output = args.output
    url = args.url
    from pprint import pprint
    for count, comment in enumerate(get_comments(url)):
        if limit and count >= limit:
            # break out of the loop when we exceed limit specified
            break
        if output:
            # write comment as JSON to a file
            with open(output, "a") as f:
                # begin writing, adding an opening brackets
                if count == 0:
                    f.write("[")
                f.write(json.dumps(comment, ensure_ascii=False) + ",")
        else:
            pprint(comment)
            print("="*50)
    print("total comments extracted:", count)
    if output:
        # remove the last comma ','
        with open(output, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()
        # add "]" to close the list in the end of the file
        with open(output, "a") as f:
            print("]", file=f)
Это инструмент командной строки, который принимает URL-адрес видео YouTube в качестве обязательного параметра, -l или --limit, чтобы ограничить количество комментариев для извлечения и -o или --output, чтобы указать выходной файл, в который комментарии будут записаны как JSON, вот пример выполнения:

$ python youtube_comment_extractor.py https://www.youtube.com/watch?v=jNQXAC9IVRw --limit 50 --output comments50.json
Это извлечет 50 комментариев из этого видео и запишет их в файл comments50.json.

Заметка: Если код этого учебника не работает для вас, пожалуйста, ознакомьтесь с учебником по API YouTube.

Заключение
Пройдя этот учебник, вы сможете создать простой скрипт извлечения комментариев YouTube. Однако следует отметить, что часть кода для этого учебника была взята из этого репозитория.

Есливы хотите скачать гораздо больше комментариев, я приглашаю вас сделать индикатор выполнения вручную или с помощью библиотеки tqdm, удачи в этом!