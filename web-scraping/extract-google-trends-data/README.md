# [How to Extract Google Trends Data in Python](https://www.thepythoncode.com/article/extract-google-trends-data-in-python)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Google Trends - это веб-сайт, созданный Google, который анализирует популярность поисковых запросов в поиске Google практически по всем регионам, языкам и категориям.

В этом уроке вы узнаете, как извлечь данные Google Trends с помощью Pytrends, неофициальной библиотеки на Python, чтобы извлечь почти все, что доступно на веб-сайте Google Trends.

Вот оглавление:

Начало работы
Проценты со временем
Интересы по регионам
Связанные темы и запросы
Трендовые поиски
Заключение
Начало работы
Чтобы начать работу, давайте установим необходимые зависимости:

$ pip install pytrends seaborn
Мы будем использовать Seaborn только для красивых сюжетов, ничего больше:

from pytrends.request import TrendReq
import seaborn
# for styling
seaborn.set_style("darkgrid")
Для начала с pytrends необходимо создать объект TrendReq:

# initialize a new Google Trends Request Object
pt = TrendReq(hl="en-US", tz=360)
Параметр hl — это язык хоста для доступа к Google Trends, а tz — смещение часового пояса.

Существуют и другие параметры, такие как повторные попытки, указывающие количество повторных попыток в случае сбоя запроса, или использование прокси-серверов путем передачи списка параметру прокси-серверов.

Проценты со временем
Чтобы получить относительное количество поисков по списку ключевых слов, мы можем использовать метод interest_over_time() после построения полезной нагрузки:

# set the keyword & timeframe
pt.build_payload(["Python", "Java"], timeframe="all")

# get the interest over time
iot = pt.interest_over_time()
iot
Выпуск:

		Python	Java	isPartial
date			
2004-01-01	8	92	False
2004-02-01	8	100	False
2004-03-01	7	96	False
2004-04-01	7	98	False
2004-05-01	8	85	False
...	...	...	...
2021-10-01	14	11	False
2021-11-01	14	11	False
2021-12-01	13	11	False
2022-01-01	13	10	False
2022-02-01	15	11	True
218 rows × 3 columns
Значения варьируются от 0 (мало или нет поисков) до 100 (максимально возможные поиски).

Метод build_payload() принимает несколько параметров помимо списка ключевых слов:

cat: Вы можете указать идентификатор категории; если поисковый запрос может означать более одного значения, установка категории устранит путаницу. Вы можете проверить эту страницу на наличие списка идентификаторов категорий или просто вызвать метод pytrends.categories() для их получения.
geo: двухбуквенная аббревиатура страны для поиска определенной страны, такой как США, FR, ES, DZ и т. Д. Вы также можете получить данные по провинциям, указав дополнительные аббревиатуры, такие как «GB-ENG» или «US-AL».
таймфрейм: это временной диапазон данных, которые мы хотим извлечь, «все» означает все данные, которые доступны в Google с самого начала, вы можете пройти определенные даты времени, или минусовые паттерны, такие как «сегодня 6-м» вернут последние данные за шесть месяцев, «сегодня 3-d» вернет последние три дня, и так далее. Значение по умолчанию для этого параметра — «сегодня 5-й», означающее последние пять лет.
Давайте построим относительную разницу в поиске между Python и Java с течением времени:

# plot it
iot.plot(figsize=(10, 6))
Выпуск:

Интерес языков программирования Java и Python с течением времениВ качестве альтернативы мы можем использовать метод, который захватывает почасовые данные. Однако это бесполезно, если вы ищете долгосрочные тенденции. Подходит для коротких периодов:get_historical_interest()

# get hourly historical interest
data = pt.get_historical_interest(
    ["data science"], 
    year_start=2022, month_start=1, day_start=1, hour_start=0,
    year_end=2022, month_end=2, day_end=10, hour_end=23,
)
data
Мы устанавливаем дату и время начала и окончания и получаем результаты. Вы также можете передать cat и geo, как упоминалось ранее. Вот выходные данные:

			data science	isPartial
date		
2022-01-01 00:00:00	28	False
2022-01-01 01:00:00	34	False
2022-01-01 02:00:00	42	False
2022-01-01 03:00:00	44	False
2022-01-01 04:00:00	52	False
...	...	...
2022-02-10 19:00:00	69	False
2022-02-10 20:00:00	70	False
2022-02-10 21:00:00	69	False
2022-02-10 22:00:00	73	False
2022-02-10 23:00:00	68	False
989 rows × 2 columns
Если что-то быстро появляется, этот метод, безусловно, будет полезен. Обратите внимание, что этот метод может привести к тому, что Google заблокирует ваш IP-адрес, так как он захватывает много данных, если вы указываете расширенный период времени, поэтому имейте это в виду.

Интересы по регионам
Давайте получим интерес к конкретному ключевому слову по регионам:

# the keyword to extract data
kw = "python"
pt.build_payload([kw], timeframe="all")
# get the interest by country
ibr = pt.interest_by_region("COUNTRY", inc_low_vol=True, inc_geo_code=True)
Мы передаем "COUNTRY" в метод interest_by_region(), чтобы получить интерес по странам. Другими возможными значениями являются «CITY» для данных на уровне города, «DMA» для данных уровня metro и «REGION» для данных регионального уровня.

Мы устанавливаем inc_low_vol значение True, поэтому мы включаем страны с низким объемом поиска, мы также устанавливаем inc_geo_code значение True, чтобы включить геокод каждой страны.

Отсортируем страны по интересу к Python:

# sort the countries by interest
ibr[kw].sort_values(ascending=False)
Выпуск:

geoName
British Indian Ocean Territory    100
St. Helena                         38
China                              25
South Korea                        25
Singapore                          22
                                 ... 
Pitcairn Islands                    0
Guinea-Bissau                       0
São Tomé & Príncipe                 0
British Virgin Islands              0
Svalbard & Jan Mayen                0
Name: python, Length: 250, dtype: int64
Вы также можете построить топ-10, если хотите, используя ibr[kw].sort_values(ascending=False)[:10].plot.bar().

Связанные темы и запросы
Еще одна интересная функция - извлекать связанные темы из вашего ключевого слова:

# get related topics of the keyword
rt = pt.related_topics()
rt[kw]["top"]
Метод related_topics() возвращает словарь Python каждого ключевого слова; этот словарь имеет два фрейма данных, один для растущих тем и один для общих топовых тем. Ниже приведены выходные данные:


value	formattedValue		hasData	link						topic_mid	topic_title		topic_type
0	100		100	True	/trends/explore?q=/m/05z1_&date=all		/m/05z1_	Python			Programming language
1	7		7	True	/trends/explore?q=/m/01dlmc&date=all		/m/01dlmc	List			Abstract data type
2	6		6	True	/trends/explore?q=/m/06x16&date=all		/m/06x16	String			Computer science
3	6		6	True	/trends/explore?q=/m/020s1&date=all		/m/020s1	Computer file		Topic
4	5		5	True	/trends/explore?q=/m/0cv6_m&date=all		/m/0cv6_m	Pythons			Snake
5	3		3	True	/trends/explore?q=/m/0nk18&date=all		/m/0nk18	Associative array	Topic
6	3		3	True	/trends/explore?q=/m/026sq&date=all		/m/026sq	Data			Topic
...
20	2		2	True	/trends/explore?q=/m/021plb&date=all		/m/021plb	NumPy			Software
21	2		2	True	/trends/explore?q=/m/016r48&date=all		/m/016r48	Object			Computer science
22	2		2	True	/trends/explore?q=/m/0fpzzp&date=all		/m/0fpzzp	Linux			Operating system
23	1		1	True	/trends/explore?q=/m/0b750&date=all		/m/0b750	Subroutine		Topic
24	1		1	True	/trends/explore?q=/m/02640pc&date=all		/m/02640pc	Import			Topic
Или связанные поисковые запросы:

# get related queries to previous keyword
rq = pt.related_queries()
rq[kw]["top"]
Выпуск:

query	value
0	python for	100
1	python list	97
2	python file	74
3	python string	73
4	monty python	44
5	install python	42
6	python if	41
7	python function	39
8	python download	34
9	python windows	33
10	python array	31
11	dictionary python	30
12	ball python	30
13	pandas	29
14	pandas python	29
15	python tutorial	26
16	python script	24
17	python class	23
18	python import	23
19	numpy	22
20	python set	22
21	python programming	21
22	python online	20
23	python time	19
24	python pdf	19
Кроме того, существует метод suggestions(keyword), который возвращает предложенные поисковые запросы:

# get suggested searches
pt.suggestions("python")
Выпуск:

[{'mid': '/m/05z1_', 'title': 'Python', 'type': 'Programming language'},
 {'mid': '/m/05tb5', 'title': 'Python family', 'type': 'Snake'},
 {'mid': '/m/0cv6_m', 'title': 'Pythons', 'type': 'Snake'},
 {'mid': '/m/01ny0v', 'title': 'Ball python', 'type': 'Reptiles'},
 {'mid': '/m/02_2hl', 'title': 'Python', 'type': 'Film'}]
Вот еще один пример:

# another example of suggested searches
pt.suggestions("America")
Выпуск:

[{'mid': '/m/09c7w0',
  'title': 'United States',
  'type': 'Country in North America'},
 {'mid': '/m/01w6dw',
  'title': 'American Express',
  'type': 'Credit card service company'},
 {'mid': '/m/06n3y', 'title': 'South America', 'type': 'Continent'},
 {'mid': '/m/03lq2', 'title': 'Halloween', 'type': 'Celebration'},
 {'mid': '/m/01yx7f',
  'title': 'Bank of America',
  'type': 'Financial services company'}]
Трендовые поиски
Еще одной особенностью Google Trends является возможность извлекать текущие трендовые поисковые запросы в каждом регионе:

# trending searches per region
ts = pt.trending_searches(pn="united_kingdom")
ts[:5]
Выпуск:

0	Championship
1	Super Bowl
2	Sheffield United
3	Kodak Black
4	Atletico Madrid
Другой альтернативой является realtime_trending_searches():

# real-time trending searches
pt.realtime_trending_searches()
Выпуск:

title	entityNames
0	Jared Cannonier, Derek Brunson, Mixed martial ...	[Jared Cannonier, Derek Brunson, Mixed martial...
1	Christian Nodal, Belinda	[Christian Nodal, Belinda]
2	Vladimir Putin, Russia	[Vladimir Putin, Russia]
3	River Radamus, Slalom skiing, Giant slalom, Wi...	[River Radamus, Slalom skiing, Giant slalom, W...
4	California State University, Fullerton, Cal St...	[California State University, Fullerton, Cal S...
...	...	...
81	Javier Bardem, Minority group, Desi Arnaz, Aar...	[Javier Bardem, Minority group, Desi Arnaz, Aa...
82	Marvel Cinematic Universe, Thanos, Avengers: E...	[Marvel Cinematic Universe, Thanos, Avengers: ...
83	Siena Saints, College basketball, Rider Broncs...	[Siena Saints, College basketball, Rider Bronc...
84	Chicago Blackhawks, St. Louis Blues, National ...	[Chicago Blackhawks, St. Louis Blues, National...
85	New York Islanders, Calgary Flames, National H...	[New York Islanders, Calgary Flames, National ...
86 rows × 2 columns
Заключение
Хорошо, теперь вы знаете, как удобно извлекать данные Google Trends с помощью Python и с помощью библиотеки pytrends. Вы можете проверить репозиторий Pytrends Github для получения более подробной информации о методах, которые мы использовали в этом учебнике.