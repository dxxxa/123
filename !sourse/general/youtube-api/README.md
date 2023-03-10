# [How to Use YouTube API in Python](https://www.thepythoncode.com/article/using-youtube-api-in-python)
To run this:
- `pip3 install -r requirements.txt`
- For complete code, use `youtube-api.ipynb`
- To get video details: `video_details.py`
- To get channel details: `channel_details.py`
- To search by keyword: `search_by_keyword.py`
- To extract comments: `comments.py`
##
# [[] / []]()
YouTube, без сомнения, является крупнейшим сайтом для обмена видео в Интернете. Это один из основных источников образования, развлечений, рекламы и многих других областей. Поскольку это веб-сайт с большим количеством данных, доступ к его API позволит вам получить почти все данные YouTube.

В этом уроке мы рассмотрим, как получить подробную информацию о видео YouTube и статистику, выполнить поиск по ключевому слову, получить информацию о канале YouTube и извлечь комментарии как из видео, так и из каналов, используя API YouTube с Python.

Вот оглавление:

Включение API YouTube
Получение сведений о видео
Поиск по ключевому слову
Получение сведений о канале YouTube
Извлечение комментариев YouTube
Включение API YouTube
Чтобы включить API данных YouTube, выполните следующие действия:

Перейдите в консоль API Google и создайте проект или используйте существующий.
На панели библиотеки найдите API данных YouTube версии 3, нажмите на него и нажмите Включить.Включение API YouTube
На панели учетных данных щелкните Создать учетные данные и выберите Идентификатор клиента OAuth.Создание учетных данных
Выберите Классическое приложение в качестве типа приложения и продолжите.Классическое приложение как тип приложения в клиенте OAuth
Вы увидите окно, подобное этому:Создан клиент OAuth
Нажмите кнопку ОК, загрузите файл учетных данных и переименуйте его в :credentials.jsonЗагрузка учетных данных
Заметка: Если вы впервые используете API Google, вам может потребоваться просто создать экран согласия OAuth и добавить свой адрес электронной почты в качестве тестирующего пользователя.

Теперь, когда вы настроили API YouTube, получите свой credentials.json в текущем каталоге вашей записной книжки / файла Python, и давайте начнем.

Во-первых, установите необходимые библиотеки:

$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
Теперь давайте импортируем необходимые модули, которые нам понадобятся:

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import re
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
SCOPES — это список областей использования Api YouTube; мы используем его для просмотра всех данных YouTube без каких-либо проблем.

Теперь давайте сделаем функцию, которая аутентифицируется с помощью YouTube API:

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

# authenticate to YouTube API
youtube = youtube_authenticate()
youtube_authenticate() ищет файл credentials.json, который мы загрузили ранее, и пытается аутентифицироваться с помощью этого файла, это откроет браузер по умолчанию при первом запуске, поэтому вы принимаете разрешения. После этого он сохранит новый файл token.pickle, содержащий авторизованные учетные данные.

Это должно выглядеть знакомо, если вы использовали Google API раньше, например, Gmail API, Google Drive API или что-то еще. Запрос в браузере по умолчанию — принять разрешения, необходимые для приложения. Если вы видите окно, указывающее, что приложение не проверено, вы можете просто перейти в раздел Дополнительно и щелкнуть имя приложения.

Получение сведений о видео
Теперь, когда у вас все настроено, давайте начнем с извлечения сведений о видео YouTube, таких как заголовок, описание, время загрузки и даже статистика, такая как количество просмотров и количество лайков.

Следующая функция поможет нам извлечь идентификатор видео (который нам понадобится в API) из URL-адреса видео:

def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")
Мы просто использовали модуль urllib.parse для получения идентификатора видео из URL-адреса.

Приведенная ниже функция получает объект сервиса YouTube (возвращаемый из функции), а также любой аргумент ключевого слова, принятый API, и возвращает ответ API для конкретного видео:youtube_authenticate()

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()
Обратите внимание, что мы указали часть фрагмента, contentDetails и статистику, так как это наиболее важные части ответа в API.

Мы также передаем kwargs в API напрямую. Далее определим функцию, которая принимает ответ, возвращаемый из приведенной выше функции get_video_details(), и выводит наиболее полезную информацию из видео:

def print_video_infos(video_response):
    items = video_response.get("items")[0]
    # get the snippet, statistics & content details from the video response
    snippet         = items["snippet"]
    statistics      = items["statistics"]
    content_details = items["contentDetails"]
    # get infos from the snippet
    channel_title = snippet["channelTitle"]
    title         = snippet["title"]
    description   = snippet["description"]
    publish_time  = snippet["publishedAt"]
    # get stats infos
    comment_count = statistics["commentCount"]
    like_count    = statistics["likeCount"]
    view_count    = statistics["viewCount"]
    # get duration from content details
    duration = content_details["duration"]
    # duration in the form of something like 'PT5H50M15S'
    # parsing it to be something like '5:50:15'
    parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
    duration_str = ""
    for d in parsed_duration:
        if d:
            duration_str += f"{d[:-1]}:"
    duration_str = duration_str.strip(":")
    print(f"""\
    Title: {title}
    Description: {description}
    Channel Title: {channel_title}
    Publish time: {publish_time}
    Duration: {duration_str}
    Number of comments: {comment_count}
    Number of likes: {like_count}
    Number of views: {view_count}
    """)
Наконец, давайте используем эти функции для извлечения информации из демонстрационного видео:

video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw&ab_channel=jawed"
# parse video ID from URL
video_id = get_video_id_by_url(video_url)
# make API call to get video info
response = get_video_details(youtube, id=video_id)
# print extracted video infos
print_video_infos(response)
Сначала мы получаем идентификатор видео из URL-адреса, затем получаем ответ от вызова API и, наконец, печатаем данные. Вот выходные данные:

    Title: Me at the zoo
    Description: The first video on YouTube. Maybe it's time to go back to the zoo?
    Channel Title: jawed
    Publish time: 2005-04-24T03:31:52Z
    Duration: 19
    Number of comments: 11018071
    Number of likes: 5962957
    Number of views: 138108884
Видите ли, мы использовали параметр id для получения сведений о конкретном видео, вытакже можете установить несколько идентификаторов видео, разделенных запятыми, поэтому вы делаете один вызов API, чтобы получить подробную информацию о нескольких видео, проверьте документацию для получения более подробной информации.

Поиск по ключевому слову
Поиск с помощью YouTube API прост; мы просто передаем параметр q для запроса, тот же запрос, который мы используем в строке поиска YouTube:

def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()
На этот раз мы заботимся о сниппете, и мы используем search() вместо videos(), как в ранее определенной функции get_video_details().

Давайте, например, найдем «python» и ограничим результаты только 2:

# search for the query 'python' and retrieve 2 items only
response = search(youtube, q="python", maxResults=2)
items = response.get("items")
for item in items:
    # get the video ID
    video_id = item["id"]["videoId"]
    # get the video details
    video_response = get_video_details(youtube, id=video_id)
    # print the video details
    print_video_infos(video_response)
    print("="*50)
Мы устанавливаем maxResults равным 2, поэтому мы извлекаем первые два элемента, вот часть выходных данных:

Title: Learn Python - Full Course for Beginners [Tutorial]
    Description: This course will give you a full introduction into all of the core concepts in python...<SNIPPED>
    Channel Title: freeCodeCamp.org
    Publish time: 2018-07-11T18:00:42Z
    Duration: 4:26:52
    Number of comments: 30307
    Number of likes: 520260
    Number of views: 21032973
==================================================
    Title: Python Tutorial - Python for Beginners [Full Course]
    Description: Python tutorial - Python for beginners
  Learn Python programming for a career in machine learning, data science & web development...<SNIPPED>
    Channel Title: Programming with Mosh
    Publish time: 2019-02-18T15:00:08Z
    Duration: 6:14:7
    Number of comments: 38019
    Number of likes: 479749
    Number of views: 15575418
Вы также можете указать параметр order в функции search(), чтобы упорядочить результаты поиска, которые могут быть «дата», «рейтинг», «viewCount», «релевантность» (по умолчанию), «заголовок» и «videoCount».

Другим полезным параметром является тип, который может быть «канал», «плейлист» или «видео», по умолчанию это все они.

Пожалуйста, проверьте эту страницу для получения дополнительной информации о методе search().list().

Получение сведений о канале YouTube
В этом разделе будет взят URL-адрес канала и извлечена информация о канале с помощью API YouTube.

Во-первых, нам нужны вспомогательные функции для синтаксического анализа URL-адреса канала. Следующие функции помогут нам в этом:

def parse_channel_url(url):
    """
    This function takes channel `url` to check whether it includes a
    channel ID, user ID or channel name
    """
    path = p.urlparse(url).path
    id = path.split("/")[-1]
    if "/c/" in path:
        return "c", id
    elif "/channel/" in path:
        return "channel", id
    elif "/user/" in path:
        return "user", id

def get_channel_id_by_url(youtube, url):
    """
    Returns channel ID of a given `id` and `method`
    - `method` (str): can be 'c', 'channel', 'user'
    - `id` (str): if method is 'c', then `id` is display name
        if method is 'channel', then it's channel id
        if method is 'user', then it's username
    """
    # parse the channel URL
    method, id = parse_channel_url(url)
    if method == "channel":
        # if it's a channel ID, then just return it
        return id
    elif method == "user":
        # if it's a user ID, make a request to get the channel ID
        response = get_channel_details(youtube, forUsername=id)
        items = response.get("items")
        if items:
            channel_id = items[0].get("id")
            return channel_id
    elif method == "c":
        # if it's a channel name, search for the channel using the name
        # may be inaccurate
        response = search(youtube, q=id, maxResults=1)
        items = response.get("items")
        if items:
            channel_id = items[0]["snippet"]["channelId"]
            return channel_id
    raise Exception(f"Cannot find ID:{id} with {method} method")
Теперь мы можем разобрать URL канала. Давайте определим наши функции для вызова YouTube API:

def get_channel_videos(youtube, **kwargs):
    return youtube.search().list(
        **kwargs
    ).execute()


def get_channel_details(youtube, **kwargs):
    return youtube.channels().list(
        part="statistics,snippet,contentDetails",
        **kwargs
    ).execute()
We'll be using get_channel_videos() to get the videos of a specific channel, and get_channel_details() will allow us to extract information about a specific youtube channel.

Now that we have everything, let's make a concrete example:

channel_url = "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ"
# get the channel ID from the URL
channel_id = get_channel_id_by_url(youtube, channel_url)
# get the channel details
response = get_channel_details(youtube, id=channel_id)
# extract channel infos
snippet = response["items"][0]["snippet"]
statistics = response["items"][0]["statistics"]
channel_country = snippet["country"]
channel_description = snippet["description"]
channel_creation_date = snippet["publishedAt"]
channel_title = snippet["title"]
channel_subscriber_count = statistics["subscriberCount"]
channel_video_count = statistics["videoCount"]
channel_view_count  = statistics["viewCount"]
print(f"""
Title: {channel_title}
Published At: {channel_creation_date}
Description: {channel_description}
Country: {channel_country}
Number of videos: {channel_video_count}
Number of subscribers: {channel_subscriber_count}
Total views: {channel_view_count}
""")
# the following is grabbing channel videos
# number of pages you want to get
n_pages = 2
# counting number of videos grabbed
n_videos = 0
next_page_token = None
for i in range(n_pages):
    params = {
        'part': 'snippet',
        'q': '',
        'channelId': channel_id,
        'type': 'video',
    }
    if next_page_token:
        params['pageToken'] = next_page_token
    res = get_channel_videos(youtube, **params)
    channel_videos = res.get("items")
    for video in channel_videos:
        n_videos += 1
        video_id = video["id"]["videoId"]
        # easily construct video URL by its ID
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_response = get_video_details(youtube, id=video_id)
        print(f"================Video #{n_videos}================")
        # print the video details
        print_video_infos(video_response)
        print(f"Video URL: {video_url}")
        print("="*40)
    print("*"*100)
    # if there is a next page, then add it to our parameters
    # to proceed to the next page
    if "nextPageToken" in res:
        next_page_token = res["nextPageToken"]
We first get the channel ID from the URL, and then we make an API call to get channel details and print them.

After that, we specify the number of pages of videos we want to extract. The default is ten videos per page, and we can also change that by passing the  maxResults parameter.

We iterate on each video and make an API call to get various information about the video, and we use our predefined print_video_infos() to print the video information.

Here is a part of the output:

================Video #1================
    Title: Async + Await in JavaScript, talk from Wes Bos
    Description: Flow Control in JavaScript is hard! ...
    Channel Title: freeCodeCamp.org
    Publish time: 2018-04-16T16:58:08Z
    Duration: 15:52
    Number of comments: 52
    Number of likes: 2353
    Number of views: 74562
Video URL: https://www.youtube.com/watch?v=DwQJ_NPQWWo
========================================
================Video #2================
    Title: Protected Routes in React using React Router
    Description: In this video, we will create a protected route using...
    Channel Title: freeCodeCamp.org
    Publish time: 2018-10-16T16:00:05Z
    Duration: 15:40
    Number of comments: 158
    Number of likes: 3331
    Number of views: 173927
Video URL: https://www.youtube.com/watch?v=Y0-qdp-XBJg
...<SNIPPED>
You can get other information; you can print the response dictionary for further information or check the documentation for this endpoint.

Extracting YouTube Comments
YouTube API allows us to extract comments; this is useful if you want to get comments for your text classification project or something similar.

The below function takes care of making an API call to commentThreads():

def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()
The below code extracts comments from a YouTube video:

# URL can be a channel or a video, to extract comments
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw&ab_channel=jawed"
if "watch" in url:
    # that's a video
    video_id = get_video_id_by_url(url)
    params = {
        'videoId': video_id, 
        'maxResults': 2,
        'order': 'relevance', # default is 'time' (newest)
    }
else:
    # should be a channel
    channel_id = get_channel_id_by_url(url)
    params = {
        'allThreadsRelatedToChannelId': channel_id, 
        'maxResults': 2,
        'order': 'relevance', # default is 'time' (newest)
    }
# get the first 2 pages (2 API requests)
n_pages = 2
for i in range(n_pages):
    # make API call to get all comments from the channel (including posts & videos)
    response = get_comments(youtube, **params)
    items = response.get("items")
    # if items is empty, breakout of the loop
    if not items:
        break
    for item in items:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        updated_at = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
        like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        comment_id = item["snippet"]["topLevelComment"]["id"]
        print(f"""\
        Comment: {comment}
        Likes: {like_count}
        Updated At: {updated_at}
        ==================================\
        """)
    if "nextPageToken" in response:
        # if there is a next page
        # add next page token to the params we pass to the function
        params["pageToken"] =  response["nextPageToken"]
    else:
        # must be end of comments!!!!
        break
    print("*"*70)
Вы также можете изменить переменную url на URL-адрес канала YouTube, чтобы он передавал allThreadsRelatedToChannelId вместо videoId в качестве параметра в API commentThreads().

Мы извлекаем два комментария на страницу и две страницы, так что всего четыре комментария. Вот выходные данные:

        Comment: We&#39;re so honored that the first ever YouTube video was filmed here!
        Likes: 877965
        Updated At: 2020-02-17T18:58:15Z
        ==================================        
        Comment: Wow, still in your recommended in 2021? Nice! Yay
        Likes: 10951
        Updated At: 2021-01-04T15:32:38Z
        ==================================        
**********************************************************************
        Comment: How many are seeing this video now
        Likes: 7134
        Updated At: 2021-01-03T19:47:25Z
        ==================================        
        Comment: The first youtube video EVER. Wow.
        Likes: 865
        Updated At: 2021-01-05T00:55:35Z
        ==================================        
**********************************************************************
Мы извлекаем сам комментарий, количество лайков и дату последнего обновления; Вы можете изучить словарь ответов, чтобы получить другую полезную информацию.

Вы можете редактировать переданные нами параметры, такие как увеличение maxResults или изменение порядка. Проверьте страницу этой конечной точки API.

Заключение
Api данных YouTube предоставляет гораздо больше, чем то, что мы рассмотрели здесь. Если у вас есть канал YouTube, вы можете загружать, обновлять и удалять видео и многое другое.

Я приглашаю вас изучить больше в документации по API YouTube для расширенных методов поиска, получения сведений о плейлистах, участниках и многом другом.

Если вы хотите извлечь данные YouTube, но не хотите использовать API, то у нас также есть учебник по получению данных YouTube с помощью веб-парсинга (больше похоже на неофициальный способ сделать это).