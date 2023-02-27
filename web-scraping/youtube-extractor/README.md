# [How to Extract YouTube Data in Python](https://www.thepythoncode.com/article/get-youtube-data-python)
To run this:
- `pip3 install -r requirements.txt`
-
    ```
    python extract_video_info.py https://www.youtube.com/watch?v=jNQXAC9IVRw
    ```
    **Output:**
    ```
    Title: Me at the zoo
    Views: 172639597
    Published at: 2005-04-23
    Video Duration: 0:18
    Video tags: me at the zoo, jawed karim, first youtube video
    Likes: 8188077
    Dislikes: 191986

    Description: The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts


    Channel Name: jawed
    Channel URL: https://www.youtube.com/channel/UC4QobU6STFB0P71PMvOGN5A
    Channel Subscribers: 1.98M subscribers
    ```
##
# [[] / []]()
Веб-парсинг — это извлечение данных с веб-сайтов. Это форма копирования, при которой конкретные данные собираются и копируются из Интернета в центральную локальную базу данных или электронную таблицу для последующего анализа или извлечения.

Поскольку YouTube является крупнейшим веб-сайтом для обмена видео в Интернете, извлечение данных может быть очень полезным. Вы можете найти самые популярные каналы, следить за популярностью каналов, записывать лайки и просмотры на видео и многое другое. Из этого туториала Вы узнаете, как извлечь данные из видео YouTube с помощью requests_html и BeautifulSoup на Python.

Обратите внимание, что использование этого метода для извлечения данных YouTube ненадежно, так как YouTube продолжает изменять свой код. Код этого учебника может завершиться ошибкой в любое время. Поэтому для более надежного использования я предлагаю вам использовать YouTube API для извлечения данных.

Связанные с: Как извлечь комментарии YouTube на Python.

Установка необходимых зависимостей:

pip3 install requests_html bs4
Прежде чем мы углубимся в быстрый скрипт, нам нужно будет поэкспериментировать над тем, как извлечь такие данные с веб-сайтов с помощью BeautifulSoup, открыть интерактивную оболочку Python и написать следующие строки кода:

from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs # importing BeautifulSoup

# sample youtube video url
video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
# init an HTML Session
session = HTMLSession()
# get the html content
response = session.get(video_url)
# execute Java-script
response.html.render(sleep=1)
# create bs object to parse HTML
soup = bs(response.html.html, "html.parser")
Приведенный выше код запрашивает URL-адрес видео YouTube, визуализирует Javascript и, наконец, создает объект BeatifulSoup, обертывающий полученный HTML- код.

Отлично, теперь давайте попробуем найти все метатеги на странице:

In [10]: soup.find_all("meta")
Out[10]: 
[<meta content="IE=edge" http-equiv="X-UA-Compatible"/>,
 <meta content="rgba(255,255,255,0.98)" name="theme-color"/>,
 <meta content="Me at the zoo" name="title"/>,
 <meta content="The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts" name="description"/>,
 <meta content="me at the zoo, jawed karim, first youtube video" name="keywords"/>,
 <meta content="YouTube" property="og:site_name"/>,
 <meta content="https://www.youtube.com/watch?v=jNQXAC9IVRw" property="og:url"/>,
 <meta content="Me at the zoo" property="og:title"/>,
 <meta content="https://i.ytimg.com/vi/jNQXAC9IVRw/hqdefault.jpg" property="og:image"/>,
 <meta content="480" property="og:image:width"/>,
 <meta content="360" property="og:image:height"/>,
 <meta content="The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts" property="og:description"/>,
 <meta content="544007664" property="al:ios:app_store_id"/>,
 <meta content="YouTube" property="al:ios:app_name"/>,
 <meta content="vnd.youtube://www.youtube.com/watch?v=jNQXAC9IVRw&amp;feature=applinks" property="al:ios:url"/>,
 <meta content="vnd.youtube://www.youtube.com/watch?v=jNQXAC9IVRw&amp;feature=applinks" property="al:android:url"/>,
 <meta content="http://www.youtube.com/watch?v=jNQXAC9IVRw&amp;feature=applinks" property="al:web:url"/>,
 <meta content="video.other" property="og:type"/>,
 <meta content="https://www.youtube.com/embed/jNQXAC9IVRw" property="og:video:url"/>,
 <meta content="https://www.youtube.com/embed/jNQXAC9IVRw" property="og:video:secure_url"/>,
 <meta content="text/html" property="og:video:type"/>,
 <meta content="480" property="og:video:width"/>,
 <meta content="360" property="og:video:height"/>,
 <meta content="YouTube" property="al:android:app_name"/>,
 <meta content="com.google.android.youtube" property="al:android:package"/>,
 <meta content="me at the zoo" property="og:video:tag"/>,
 <meta content="jawed karim" property="og:video:tag"/>,
 <meta content="first youtube video" property="og:video:tag"/>,
 <meta content="87741124305" property="fb:app_id"/>,
 <meta content="player" name="twitter:card"/>,
 <meta content="@youtube" name="twitter:site"/>,
 <meta content="https://www.youtube.com/watch?v=jNQXAC9IVRw" name="twitter:url"/>,
 <meta content="Me at the zoo" name="twitter:title"/>,
 <meta content="The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts" name="twitter:description"/>,
 <meta content="https://i.ytimg.com/vi/jNQXAC9IVRw/hqdefault.jpg" name="twitter:image"/>,
 <meta content="YouTube" name="twitter:app:name:iphone"/>,
 <meta content="544007664" name="twitter:app:id:iphone"/>,
 <meta content="YouTube" name="twitter:app:name:ipad"/>,
 <meta content="544007664" name="twitter:app:id:ipad"/>,
 <meta content="vnd.youtube://www.youtube.com/watch?v=jNQXAC9IVRw&amp;feature=applinks" name="twitter:app:url:iphone"/>,
 <meta content="vnd.youtube://www.youtube.com/watch?v=jNQXAC9IVRw&amp;feature=applinks" name="twitter:app:url:ipad"/>,
 <meta content="YouTube" name="twitter:app:name:googleplay"/>,
 <meta content="com.google.android.youtube" name="twitter:app:id:googleplay"/>,
 <meta content="https://www.youtube.com/watch?v=jNQXAC9IVRw" name="twitter:app:url:googleplay"/>,
 <meta content="https://www.youtube.com/embed/jNQXAC9IVRw" name="twitter:player"/>,
 <meta content="480" name="twitter:player:width"/>,
 <meta content="360" name="twitter:player:height"/>,
 <meta content="Me at the zoo" itemprop="name"/>,
 <meta content="The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts" itemprop="description"/>,
 <meta content="False" itemprop="paid"/>,
 <meta content="UC4QobU6STFB0P71PMvOGN5A" itemprop="channelId"/>,
 <meta content="jNQXAC9IVRw" itemprop="videoId"/>,
 <meta content="PT0M19S" itemprop="duration"/>,
 <meta content="False" itemprop="unlisted"/>,
 <meta content="480" itemprop="width"/>,
 <meta content="360" itemprop="height"/>,
 <meta content="HTML5 Flash" itemprop="playerType"/>,
 <meta content="480" itemprop="width"/>,
 <meta content="360" itemprop="height"/>,
 <meta content="true" itemprop="isFamilyFriendly"/>,
 <meta content="AD,AE,AF,AG,AI,AL,AM,AO,AQ,AR,AS,AT,AU,AW,AX,AZ,BA,BB,BD,BE,BF,BG,BH,BI,BJ,BL,BM,BN,BO,BQ,BR,BS,BT,BV,BW,BY,BZ,CA,CC,CD,CF,CG,CH,CI,CK,CL,CM,CN,CO,CR,CU,CV,CW,CX,CY,CZ,DE,DJ,DK,DM,DO,DZ,EC,EE,EG,EH,ER,ES,ET,FI,FJ,FK,FM,FO,FR,GA,GB,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GR,GS,GT,GU,GW,GY,HK,HM,HN,HR,HT,HU,ID,IE,IL,IM,IN,IO,IQ,IR,IS,IT,JE,JM,JO,JP,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LT,LU,LV,LY,MA,MC,MD,ME,MF,MG,MH,MK,ML,MM,MN,MO,MP,MQ,MR,MS,MT,MU,MV,MW,MX,MY,MZ,NA,NC,NE,NF,NG,NI,NL,NO,NP,NR,NU,NZ,OM,PA,PE,PF,PG,PH,PK,PL,PM,PN,PR,PS,PT,PW,PY,QA,RE,RO,RS,RU,RW,SA,SB,SC,SD,SE,SG,SH,SI,SJ,SK,SL,SM,SN,SO,SR,SS,ST,SV,SX,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TR,TT,TV,TW,TZ,UA,UG,UM,US,UY,UZ,VA,VC,VE,VG,VI,VN,VU,WF,WS,YE,YT,ZA,ZM,ZW" itemprop="regionsAllowed"/>,
 <meta content="172826227" itemprop="interactionCount"/>,
 <meta content="2005-04-23" itemprop="datePublished"/>,
 <meta content="2005-04-23" itemprop="uploadDate"/>,
 <meta content="Film &amp; Animation" itemprop="genre"/>]
Все очень просто, здесь много ценных данных. Например, мы можем получить название видео:

In [11]: soup.find("meta", itemprop="name")["content"]
Out[11]: 'Me at the zoo'
Или количество просмотров:

In [12]: soup.find("meta", itemprop="interactionCount")['content']
Out[12]: '172826227'
Таким образом, вы сможете извлечь все, что хотите, с этой веб-страницы. Теперь давайте сделаем наш скрипт, который извлекает некоторую полезную информацию, которую мы можем получить со страницы видео YouTube, откроем новый файл Python и следуем за ним:

Импорт необходимых модулей:

from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
Прежде чем мы сделаем нашу функцию, которая извлекает все видеоданные, давайте инициализируем наш HTTP-сеанс:

# init session
session = HTMLSession()
Сделаем функцию; получив URL-адрес видео YouTube, он вернет все данные в словаре:

def get_video_info(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(sleep=1)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    result = {}
Обратите внимание, что после того, как мы загрузили HTML-содержимое веб-страницы, мы запустили метод render() для выполнения Javascript, чтобы данные, которые мы ищем, отображались в HTML.

Обратите внимание, что если вы получаете ошибку тайм-аута, то вы можете просто добавить параметр timeout и установить его на 60 секунд (по умолчанию 8 секунд) или что-то в этом роде:

response.html.render(sleep=1, timeout=60)
Получение названия видео:

    # video title
    result["title"] = soup.find("meta", itemprop="name")['content']
Количество представлений, преобразованных в целое число:

    # video views (converted to integer)
    result["views"] = result["views"] = soup.find("meta", itemprop="interactionCount")['content']
Получите описание видео:

    # video description
    result["description"] = soup.find("meta", itemprop="description")['content']
Дата публикации видео:

    # date published
    result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
Продолжительность видео:

    # get the duration of the video
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
Мы могли бы получить длительность из метатега, как и предыдущие поля, но это будет в другом формате, таком как PT0M19S, который переводится в 19 секунд или 00: 19 в формате, который находится в теге ytp-time-duration span.

Мы также можем извлечь теги видео:

    # get the video tags
    result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
Количество лайков:

    # Additional video and channel information (with help from: https://stackoverflow.com/a/68262735)
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_json = json.loads(data)
    videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
    videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
    # number of likes
    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] # "No likes" or "###,### likes"
    likes_str = likes_label.split(' ')[0].replace(',','')
    result["likes"] = '0' if likes_str == 'No' else likes_str
    # number of likes (old way) doesn't always work
    # text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    # result["likes"] = ''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ])
    # result["likes"] = 0 if result['likes'] == '' else int(result['likes'])
    # number of dislikes - YouTube does not publish this anymore...
    # result["dislikes"] = ''.join([ c for c in text_yt_formatted_strings[1].attrs.get("aria-label") if c.isdigit() ])	
    # result["dislikes"] = '0' if result['dislikes'] == '' else result['dislikes']
    result['dislikes'] = 'UNKNOWN'
Как вы можете заметить, есть два разных способа. Прокомментированный способ кажется непоследовательным и иногда вылетает после обновлений YouTube. Таким образом, новый метод, похоже, справляется с обновлениями (спасибо Мэтту за вклад). Кроме того, дизлайки больше не показываются публично в видео на YouTube; на данный момент они комментируются.

Поскольку в видео на YouTube вы можете увидеть детали канала, такие как имя и количество подписчиков, давайте также возьмем это:

    # channel details
    channel_tag = soup.find("meta", itemprop="channelId")['content']
    # channel name
    channel_name = soup.find("span", itemprop="author").next.next['content']
    # channel URL
    # channel_url = soup.find("span", itemprop="author").next['href']
    channel_url = f"https://www.youtube.com/{channel_tag}"
    # number of subscribers as str
    channel_subscribers = videoSecondaryInfoRenderer['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']
    # channel details (old way)
    # channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
    # # channel name (old way)
    # channel_name = channel_tag.text
    # # channel URL (old way)
    # channel_url = f"https://www.youtube.com{channel_tag['href']}"
    # number of subscribers as str (old way)
    # channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
    result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}
    return result
Поскольку функция soup.find() возвращает объект Tag. Вы по-прежнему можете найти теги HTML в других тегах. В результате принято вызывать find() более одного раза.

Теперь эта функция возвращает много видеоинформации в словаре. Давайте закончим наш сценарий:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Video Data Extractor")
    parser.add_argument("url", help="URL of the YouTube video")
    args = parser.parse_args()
    url = args.url
    # get the data
    data = get_video_info(url)
    # print in nice format
    print(f"Title: {data['title']}")
    print(f"Views: {data['views']}")
    print(f"Published at: {data['date_published']}")
    print(f"Video Duration: {data['duration']}")
    print(f"Video tags: {data['tags']}")
    print(f"Likes: {data['likes']}")
    print(f"Dislikes: {data['dislikes']}")
    print(f"\nDescription: {data['description']}\n")
    print(f"\nChannel Name: {data['channel']['name']}")
    print(f"Channel URL: {data['channel']['url']}")
    print(f"Channel Subscribers: {data['channel']['subscribers']}")
Здесь нет ничего особенного, так как нам нужен способ получения URL-адреса видео из командной строки. Вышесказанное делает именно это, а затем печатает его в формате. Вот мои выходные данные при запуске скрипта:

C:\youtube-extractor>python extract_video_info.py https://www.youtube.com/watch?v=jNQXAC9IVRw
Title: Me at the zoo
Views: 172639597
Published at: 2005-04-23
Video Duration: 0:18
Video tags: me at the zoo, jawed karim, first youtube video
Likes: 8188077
Dislikes: 191986

Description: The first video on YouTube. While you wait for Part 2, listen to this great song: https://www.youtube.com/watch?v=zj82_v2R6ts


Channel Name: jawed
Channel URL: https://www.youtube.com/channel/UC4QobU6STFB0P71PMvOGN5A
Channel Subscribers: 1.98M subscribers
Заключение
Вот и все! Вы знаете, как извлечь данные из тегов HTML, а затем продолжить и добавить другие поля, такие как качество видео и другие.

Если вы хотите извлечь комментарии youTube, есть много вещей, которые нужно сделать, кроме этого. Для этого есть отдельное учебное пособие.

Вы можете не только извлечь детали видео YouTube, но вы также можете применить этот навык к любому веб-сайту, который вы хотите. Если вы собираетесь извлекать страницы Википедии, для этого есть учебник! Или, может быть, вы хотите очистить данные о погоде из Google? Для этого также есть учебник.

Проверьте полный код этого учебника здесь.

Заметка: YouTube постоянно меняет HTML-структуру видеостраниц. Если код этого учебника не работает для вас, пожалуйста, ознакомьтесь с руководством по API YouTube.