# [Named Entity Recognition using Transformers and Spacy in Python](https://www.thepythoncode.com/article/named-entity-recognition-using-transformers-and-spacy)
##
# [[] / []]()
Именованное распознавание сущностей (NER) — это типичная задача обработки естественного языка (NLP), которая автоматически идентифицирует и распознает предопределенные сущности в заданном тексте. Такие сущности, как имена людей, организации, даты и время, а также местоположения, являются ценной информацией для извлечения из неструктурированного и немаркированного необработанного текста.

В конце этого урока вы сможете выполнить распознавание именованных сущностей на любом заданном английском тексте с помощью HuggingFace Transformers и SpaCy на Python; Вот пример результирующего NER:

Распознавание именованных сущностей
SpaCy - это библиотека с открытым исходным кодом на Python для продвинутого НЛП. Он построен на последних исследованиях и предназначен для использования в реальных продуктах. Мы будем использовать две модели NER на SpaCy, а именно обычный en_core_web_sm и трансформатор en_core_web_trf. Мы также будем использовать удивительный визуализатор NER от spaCy.

Чтобы начать работу, давайте установим необходимые библиотеки для этого учебника. Во-первых, установка трансформаторов:

$ pip install --upgrade transformers sentencepiece
Далее нам нужно установить spacy и spacy-трансформаторы. Для этого я взял последний файл .whl из релизов spacy-models для установки:

$ pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.2.0/en_core_web_trf-3.2.0-py3-none-any.whl
Конечно, если вы читаете этот учебник в будущем, обязательно получите последнюю версию с этой страницы, если у вас возникнут какие-либо проблемы, связанные с вышеуказанной командой.

Далее мы должны скачать en_core_web_sm обычную модель spaCy:

$ python -m spacy download en_core_web_sm
en_core_web_sm — это конвейер моделей на английском языке, оптимизированный для ЦП. Он небольшой, размером всего 13 МБ и под лицензией MIT. Для больших моделей можно использовать en_core_web_md для средних и en_core_web_lg для больших.

После завершения установки давайте начнем с кода:

import spacy
from transformers import *
Для этого урока мы будем выполнять NER на этом тексте, который я взял из Википедии:

# sample text from Wikipedia
text = """
Albert Einstein was a German-born theoretical physicist, widely acknowledged to be one of the greatest and most influential physicists of all time. 
Einstein is best known for developing the theory of relativity, but he also made important contributions to the development of the theory of quantum mechanics.
Einstein was born in the German Empire, but moved to Switzerland in 1895, forsaking his German citizenship (as a subject of the Kingdom of Württemberg) the following year. 
In 1897, at the age of 17, he enrolled in the mathematics and physics teaching diploma program at the Swiss Federal polytechnic school in Zürich, graduating in 1900
"""
NER с трансформаторами
Мы будем использовать API конвейера HuggingFace Transformers для загрузки моделей:

# load BERT model fine-tuned for Named Entity Recognition (NER)
ner = pipeline("ner", model="dslim/bert-base-NER")
Мы используем модель BERT (bert-base-encased), которая была точно настроена на наборе данных CoNLL-2003 Named Entity Recognition. Вы можете использовать dslim/bert-large-NER для более крупной версии этого.

Давайте извлечем сущности для нашего текста с помощью этой модели:

# perform inference on the transformer model
doc_ner = ner(text)
# print the output
doc_ner
Выпуск:

[{'end': 7,
  'entity': 'B-PER',
  'index': 1,
  'score': 0.99949145,
  'start': 1,
  'word': 'Albert'},
 {'end': 16,
  'entity': 'I-PER',
  'index': 2,
  'score': 0.998417,
  'start': 8,
  'word': 'Einstein'},
 {'end': 29,
  'entity': 'B-MISC',
  'index': 5,
  'score': 0.99211043,
  'start': 23,
  'word': 'German'},
 {'end': 158,
  'entity': 'B-PER',
  'index': 28,
  'score': 0.99736506,
  'start': 150,
  'word': 'Einstein'},
 {'end': 318,
  'entity': 'B-PER',
  'index': 55,
  'score': 0.9977113,
  'start': 310,
  'word': 'Einstein'},
 {'end': 341,
  'entity': 'B-LOC',
  'index': 60,
  'score': 0.50242233,
  'start': 335,
  'word': 'German'},
 {'end': 348,
  'entity': 'I-LOC',
  'index': 61,
  'score': 0.95330054,
  'start': 342,
  'word': 'Empire'},
 {'end': 374,
  'entity': 'B-LOC',
  'index': 66,
  'score': 0.99978524,
  'start': 363,
  'word': 'Switzerland'},
 {'end': 404,
  'entity': 'B-MISC',
  'index': 74,
  'score': 0.9995827,
  'start': 398,
  'word': 'German'},
 {'end': 460,
  'entity': 'B-LOC',
  'index': 84,
  'score': 0.9994709,
  'start': 449,
  'word': 'Württemberg'},
 {'end': 590,
  'entity': 'B-MISC',
  'index': 111,
  'score': 0.9888771,
  'start': 585,
  'word': 'Swiss'},
 {'end': 627,
  'entity': 'B-LOC',
  'index': 119,
  'score': 0.9977405,
  'start': 621,
  'word': 'Zürich'}]
Как видите, выходные данные представляют собой список словарей, в котором указаны начальная и конечная позиции сущности в тексте, оценка прогнозирования, само слово, индекс и имя сущности.

Именованные сущности этих наборов данных:

O: Вне именованной сущности.
B-MIS: Начало разной сущности сразу после другой другой другой сущности.
I-MIS: Разное.
B-PER: Начало имени человека сразу после имени другого человека.
I-PER: Имя человека.
B-ORG: Начало организации сразу после другой организации.
I-ORG: Организация.
B-LOC: Начало местоположения сразу после другого местоположения.
I-LOC: Расположение.
Далее давайте создадим функцию, которая использует spaCy для визуализации этого словаря Python:

def get_entities_html(text, ner_result, title=None):
  """Visualize NER with the help of SpaCy"""
  ents = []
  for ent in ner_result:
    e = {}
    # add the start and end positions of the entity
    e["start"] = ent["start"]
    e["end"] = ent["end"]
    # add the score if you want in the label
    # e["label"] = f"{ent["entity"]}-{ent['score']:.2f}"
    e["label"] = ent["entity"]
    if ents and -1 <= ent["start"] - ents[-1]["end"] <= 1 and ents[-1]["label"] == e["label"]:
      # if the current entity is shared with previous entity
      # simply extend the entity end position instead of adding a new one
      ents[-1]["end"] = e["end"]
      continue
    ents.append(e)
  # construct data required for displacy.render() method
  render_data = [
    {
      "text": text,
      "ents": ents,
      "title": title,
    }
  ]
  spacy.displacy.render(render_data, style="ent", manual=True, jupyter=True)
Приведенная выше функция использует функцию spacy.displacy.render() для отображения извлеченного текста именованной сущности. Мы используем manual=True, указывая, что это ручная визуализация, а не документ spaCy. Мы также установили jupyter в True, так как в настоящее время мы находимся на ноутбуке Juypter или Colab.

Вся цель цикла for состоит в том, чтобы создать список словарей с начальной и конечной позициями и меткой сущности. Мы также проверяем, есть ли поблизости какие-то одинаковые сущности, поэтому мы объединяем их.

Назовем это так:

# get HTML representation of NER of our text
get_entities_html(text, doc_ner)
АльбертB-PER ЭйнштейнI-PER был немецким физиком-теоретиком, родившимся в B-MISC, широко признанным одним из величайших и самых влиятельных физиков всех времен. ЭйнштейнB-PER наиболее известен развитием теории относительности, но он также внес важный вклад в развитие теории квантовой механики. ЭйнштейнB-PER родился в немецкойимперии B-LOC I-LOC, но переехал в ШвейцариюB-LOC в 1895 году, отказавшись от своего немецкого гражданства B-MISC (как подданного Королевства ВюртембергB-LOC) в следующем году. В 1897 году, в возрасте 17 лет, он поступил на дипломную программу преподавания математики и физики в швейцарскую Федеральную политехническую школу B-MISC в ЦюрихеB-LOC, которую окончил в 1900 году.
Далее давайте загрузим еще одну относительно большую и лучшую модель, основанную на roberta-large:

# load roberta-large model
ner2 = pipeline("ner", model="xlm-roberta-large-finetuned-conll03-english")
Выполнение вывода:

# perform inference on this model
doc_ner2 = ner2(text)
Визуализации:

# get HTML representation of NER of our text
get_entities_html(text, doc_ner2)
Альберт ЭйнштейнI-PER был немецким физиком-теоретиком, родившимся в I-MISC, широко признанным одним из величайших и самых влиятельных физиков всех времен. ЭйнштейнI-PER наиболее известен развитием теории относительности, но он также внес важный вклад в развитие теории квантовой механики. ЭйнштейнI-PER родился в Германской империиI-LOC, но переехал в ШвейцариюI-LOC в 1895 году, отказавшись от своего немецкого гражданстваI-MISC (как субъект Королевства ВюртембергI-LOC) в следующем году. В 1897 году, в возрасте 17 лет, он поступил на дипломную программу преподавания математики и физики в швейцарской федеральной политехнической школе I-MISC I-ORG в Цюрихе I-LOC, которую окончил в 1900 году.
Как вы можете видеть, теперь он улучшен, называя Альберта Эйнштейна единым целым, а также Королевством Вюртемберг.

Есть много других моделей, которые были точно настроены на тот же набор данных. Вот еще один:

# load yet another roberta-large model
ner3 = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english")
# perform inference on this model
doc_ner3 = ner3(text)
# get HTML representation of NER of our text
get_entities_html(text, doc_ner3)
Альберт ЭйнштейнPER был немецким физиком-теоретикомMISC, широко признанным одним из величайших и самых влиятельных физиков всех времен. ЭйнштейнPER наиболее известен развитием теории относительности, но он также внес важный вклад в развитие теории квантовой механики. ЭйнштейнПЕР родился в Германской империиLOC, но переехал в ШвейцариюLOC в 1895 году, отказавшись от своего немецкого гражданстваMISC (как подданного Королевства ВюртембергLOC) в следующем году. В 1897 году, в возрасте 17 лет, он поступил на дипломную программу преподавания математики и физики в швейцарской политехнической школе MISC FederalORG в Цюрихе, которую окончил в 1900 году.
Однако эта модель имеет только сущности PER, MISC, LOC и ORG. SpaCy автоматически окрашивает знакомые сущности.

NER с SpaCy
Чтобы выполнить NER с помощью SpaCy, мы должны сначала загрузить модель с помощью функции spacy.load():

# load the English CPU-optimized pipeline
nlp = spacy.load("en_core_web_sm")
Мы загружаем загруженную модель. Убедитесь, что вы загрузили модель, которую хотите использовать, прежде чем загружать ее здесь. Далее, давайте создадим наш документ:

# predict the entities
doc = nlp(text)
А затем визуализировать его:

# display the doc with jupyter mode
spacy.displacy.render(doc, style="ent", jupyter=True)
Альберт ЭйнштейнБЫЛ немецким физиком-теоретиком, родившимся в NORP, широко признанным одним из величайших и самых влиятельных физиков всех времен. ЭйнштейнPERSON наиболее известен развитием теории относительности, но он также внес важный вклад в развитие теории квантовоймеханики ORG. ЭйнштейнПЕРСОН родился в Германской империиGPE, но переехал в ШвейцариюGPE в 1895году DATE, отказавшись от своего немецкого гражданстваNORP (как подданного Королевства ВюртембергGPE) в следующем годуDATE. В 1897году DATE, в возрасте 17лет, он поступил на дипломную программу преподавания математики и физики в швейцарской федеральной политехнической школе NORP в Цюрихе GPE, которую окончил в 1900году.
Этот выглядит намного лучше, и есть гораздо больше сущностей (18), чем предыдущие, а именно КАРДИНАЛ, ДАТА, СОБЫТИЕ, FAC, GPE, ЯЗЫК, ЗАКОН, LOC, ДЕНЬГИ, NORP, ПОРЯДКОВЫЙ номер, ORG, ПРОЦЕНТ, ЧЕЛОВЕК, ПРОДУКТ, КОЛИЧЕСТВО, ВРЕМЯ, WORK_OF_ART.

Однако квантовая механика была ошибочно обозначена как организация, поэтому давайте воспользуемся моделью Transformer, которую предлагает spaCy:

# load the English transformer pipeline (roberta-base) using spaCy
nlp_trf = spacy.load('en_core_web_trf')
Давайте выполним вывод и визуализируем текст:

# perform inference on the model
doc_trf = nlp_trf(text)
# display the doc with jupyter mode
spacy.displacy.render(doc_trf, style="ent", jupyter=True)
Альберт ЭйнштейнБЫЛ немецким физиком-теоретиком, родившимся в NORP, широко признанным одним из величайших и самых влиятельных физиков всех времен. ЭйнштейнPERSON наиболее известен развитием теории относительности, но он также внес важный вклад в развитие теории квантовой механики. ЭйнштейнПЕРСОН родился в Германской империиGPE, но переехал в ШвейцариюGPE в 1895году DATE, отказавшись от своего немецкого гражданстваNORP (как подданного Королевства ВюртембергGPE) в следующем годуDATE. В 1897году DATE, в возрасте 17лет DATE, он поступил на дипломную программу преподавания математики и физики в Политехническую школу Swiss FederalORG в Цюрихе GPE, окончив в 1900году DATE.
На этот раз Swiss Federal была помечена как организация, хотя она не была завершена (это должна быть Швейцарская федеральная политехническая школа), и квантовая механика больше не является организацией.

Модель en_core_web_trf работает намного лучше, чем предыдущие. Проверьте эту таблицу, которая показывает каждую английскую модель, предлагаемую spaCy, с их размером и оценкой метрик каждой из них:

Название модели	Размер модели	Точность	Вспоминать	F-Score
en_core_web_sm	13 МБ	0.85	0.84	0.84
en_core_web_md	43 МБ	0.85	0.84	0.85
en_core_web_lg	741 МБ	0.86	0.85	0.85
en_core_web_trf	438 МБ	0.90	0.90	0.90
 
Заключение
Обязательно попробуйте другие типы текстов и убедитесь сами, подтверждает ли ваш текст приведенную выше таблицу! Вы можете проверить эту страницу на spaCy, чтобы увидеть подробную информацию о каждой модели.

Для других языков spaCy стремится сделать эти модели доступными для каждого языка во всем мире. Вы можете проверить эту страницу, чтобы увидеть доступные модели для каждого языка.

Вот некоторые связанные учебники по НЛП, которые вы можете найти полезными:

Генерация текста с помощью трансформеров в Python
Как перефразировать текст с помощью трансформеров в Python
Распознавание речи с помощью трансформеров в Python
Машинный перевод с использованием трансформеров в Python