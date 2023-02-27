# [How to Make a Barcode Reader in Python](https://www.thepythoncode.com/article/making-a-barcode-scanner-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To detect barcodes of the images in this directory:
    ```
    python barcode_reader.py
    ```
- To detect barcodes live using your camera:
    ```
    python live_barcode_reader.py
    ```
##
# [[] / []]()
Штрих-код – это метод представления данных в визуальном и машиночитаемом виде, он состоит из полос и пробелов. Сегодня мы видим штрих-коды повсюду, особенно в продуктах в супермаркетах.

Штрих-коды могут быть считаны оптическим сканером штрих-кодов, но в этом уроке мы сделаем скрипт на Python, который способен считывать и декодировать штрих-коды, а также чертеж, где они расположены на данном изображении.

Связанные с: Как извлечь кадры из видео в Python.

Чтобы начать работу, нам нужно установить несколько библиотек:

pip3 install pyzbar opencv-python
После того, как вы установили их, откройте новый файл Python и импортируйте их:

from pyzbar import pyzbar
import cv2
У меня есть несколько изображений для тестирования, вы можете использовать любое изображение, которое вы хотите из Интернета или своего собственного диска, но вы можете получить мои тестовые изображения в этом каталоге.

Я обернул каждую функциональность в функцию, первая функция, которую мы собираемся обсудить, следующая:

def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        print("detected barcode:", obj)
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data)
        print()

    return image
Функция decode() принимает изображение в виде массива numpy и использует pyzbar.decode(), который отвечает за декодирование всех штрих-кодов из одного изображения и возвращает кучу полезной информации о каждом обнаруженном штрих-коде.

Затем мы перебираем все обнаруженные штрих-коды и рисуем прямоугольник вокруг штрих-кода и печатаем тип и данные штрих-кода.

Чтобы прояснить ситуацию, ниже приведено, как выглядел каждый obj, если мы его напечатаем:

Decoded(data=b'43770929851162', type='I25', rect=Rect(left=62, top=0, width=694, height=180), polygon=[Point(x=62, y=1), Point(x=62, y=179), Point(x=756, y=180), Point(x=756, y=0)])
Таким образом, функция pyzbar.decode() возвращает данные, содержащие штрих-код, тип штрих-кода, а также точки расположения в виде прямоугольника и многоугольника.

Это подводит нас к следующей функции, которую мы использовали, draw_barcode():

def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image
Эта функция принимает декодированный объект, который мы только что видели, и само изображение, оно рисует прямоугольник вокруг штрих-кода с помощью функции cv2.rectangle(), или вы можете раскомментировать другую версию функции; рисование полигона с помощью функции cv2.line(), выбор за вами. Я предпочел прямоугольную версию.

Наконец, он возвращает изображение, содержащее нарисованные штрих-коды. Теперь давайте используем эти функции для наших примеров изображений:

if __name__ == "__main__":
    from glob import glob

    barcodes = glob("barcode*.png")
    for barcode_file in barcodes:
        # load the image to opencv
        img = cv2.imread(barcode_file)
        # decode detected barcodes & get the image
        # that is drawn
        img = decode(img)
        # show the image
        cv2.imshow("img", img)
        cv2.waitKey(0)
В моем текущем каталоге у меня есть штрих-код1.png, штрих-код2.png и штрих-код3.png, которые являются примерами изображений отсканированного штрих-кода, я использовал glob, чтобы я мог получить все эти изображения в виде списка и перебирать их.

В каждый файл мы загружаем его с помощью функции cv2.imread() и используем ранее обсуждавшуюся функцию decode() для декодирования штрих-кодов, а затем показываем фактическое изображение.

Обратите внимание, что это также обнаружит QR-коды, и это нормально, но для более точных результатов я предлагаю вам проверить специальный учебник по обнаружению и генерации QR-кодов на Python.

Когда я запускаю скрипт, он показывает каждое изображение и печатает его тип и данные, нажмите любую клавишу, и вы получите следующее изображение, вот мой вывод:

detected barcode: Decoded(data=b'0036000291452', type='EAN13', rect=Rect(left=124, top=58, width=965, height=812), polygon=[Point(x=124, y=59), Point(x=124, y=869), Point(x=621, y=870), Point(x=1089, y=870), Point(x=1089, y=58)])
Type: EAN13
Data: b'0036000291452'

detected barcode: Decoded(data=b'Wikipedia', type='CODE128', rect=Rect(left=593, top=4, width=0, height=294), polygon=[Point(x=593, y=4), Point(x=593, y=298)])
Type: CODE128
Data: b'Wikipedia'

detected barcode: Decoded(data=b'43770929851162', type='I25', rect=Rect(left=62, top=0, width=694, height=180), polygon=[Point(x=62, y=1), Point(x=62, y=179), Point(x=756, y=180), Point(x=756, y=0)])
Type: I25
Data: b'43770929851162'
Вот последнее показанное изображение:

Штрих-код, обнаруженный с помощью Python

Заключение
Это потрясающе, теперь у вас есть отличный инструмент для создания собственного сканера штрих-кодов на Python. Я знаю, что вы все хотите читать прямо с камеры, в результате я подготовил код, который считывает с камеры и обнаруживает штрих-коды в прямом эфире, проверьте это здесь!

Вы также можете добавить какой-то звуковой сигнал при обнаружении каждого штрих-кода, как в супермаркетах, проверьте учебник для воспроизведения звуков, которые могут помочь вам в этом.

Для получения более подробной информации я приглашаю вас ознакомиться с документацией pyzbar.