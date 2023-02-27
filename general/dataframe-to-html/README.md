# [How to Convert Pandas Dataframes to HTML Tables in Python](https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Есть много случаев, когда вам нужно преобразовать фрейм данных Pandas в таблицу HTML. Две основные причины заключаются в том, что вы хотите лучше просматривать свой набор данных в качестве аналитика данных или интегрировать его в веб-сайт своей организации.

В этом уроке мы преобразуем любой фрейм данных Pandas в интерактивную таблицу с разбивкой на страницы, и мы можем выполнить сортировку по столбцам и поиск.

Чтобы начать, конечно, у вас должны быть установлены панды:

$ pip install pandas
Импорт необходимых библиотек:

import pandas as pd
import webbrowser
Мы будем использовать модуль webbrowser для автоматического открытия результирующей HTML-таблицы в новой вкладке браузера по умолчанию.

Давайте создадим функцию, которая принимает кадр данных в качестве аргумента и возвращает html-содержимое для этого:

def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table")
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                // paging: false,    
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html
К счастью, Pandas имеет встроенный метод to_html(), который генерирует HTML-содержимое этого фрейма данных в виде тега таблицы. После этого мы создаем полную HTML-страницу и добавляем расширение таблиц данных jQuery, чтобы оно было интерактивным.

По умолчанию разбиение на страницы, сортировка по столбцам и поиск включены; вы можете отключить их, если хотите. Например, если вы хотите отключить разбиение на страницы и показать весь фрейм данных, вы можете раскомментировать paging: false (помните, что комментирование в Javascript — это «//», а не «#», как в Python).

Я использую этот набор данных в демонстрационных целях. Давайте попробуем:

if __name__ == "__main__":
    # read the dataframe dataset
    df = pd.read_csv("Churn_Modelling.csv")
    # take only first 1000, otherwise it'll generate a large html file
    df = df.iloc[:1000]
    # generate the HTML from the dataframe
    html = generate_html(df)
    # write the HTML content to an HTML file
    open("index.html", "w").write(html)
    # open the new HTML file with the default browser
    webbrowser.open("index.html")
После того, как мы получаем наш HTML-контент, мы записываем его в новый индексный файл.html и открываем его с помощью функции webbrowser.open(). Вот как это выглядит:

Результирующая HTML-таблицаСамое классное, что мы можем искать на столе:

Поиск в результирующей HTML-таблицеИли выполните сортировку по определенному столбцу:

Сортировка по столбцам в результирующей HTML-таблицеИли отредактируйте параметры разбиения на страницы, например, показывая 50 записей на странице:

Редактирование параметров разбиения на страницы в результирующей HTML-таблицеВы также можете увидеть страницы под таблицей:

Редактирование параметров разбиения на страницы в результирующей HTML-таблицеЗаключение
Хорошо! Вот и все для учебника. Я надеюсь, что вам будет полезно легко лучше просматривать свой набор данных или интегрировать его в качестве HTML-контента на свой сайт.

Если вы хотите наоборот, извлекая HTML-таблицы и преобразуя их в CSV-файлы, проверьте этот учебник.

Набор данных, используемый в этом учебнике, взят из Kaggle. Вы можете получить его здесь, если у вас нет учетной записи Kaggle.

Обратите внимание, что стиль таблицы будет работать только при наличии подключения к Интернету. Если вы хотите, чтобы он работал в автономном режиме, вы можете просто загрузить файлы JS / CSS и поместить их в текущий каталог, чтобы он загружал их с вашего локального компьютера, а не с CDN.