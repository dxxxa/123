# [How to Generate and Read QR Code in Python](https://www.thepythoncode.com/article/generate-read-qr-code-python)
To run this:
- `pip3 install -r requirements.txt`
- If you want to generate a QR code, run `generate_qrcode.py`.

    For instance, if you want to generate a QR code that contains the data: "https://www.thepythoncode.com" to a file named `site.png`, you can:
    ```
    python generate_qrcode.py https://www.thepythoncode.com site.png
    ```
- If you want to read a QR code, run `read_qrcode.py`.

    For instance, if you want to read a QR code from a file named `site.png`, you can run:
    ```
    python read_qrcode.py site.png
    ```
    A new window will appear that contains the QR code surrounded by a blue square.
    and **outputs**:
    ```
    QRCode data:
    https://www.thepythoncode.com
    ```
- If you want to read QR codes live using your cam, just run:
    ```
    python read_qrcode_live.py
    ```

If you want to know how these are created, head to this tutorial: [How to Generate and Read QR Code in Python](https://www.thepythoncode.com/article/generate-read-qr-code-python).
##
# [[] / []]()
QR-код - это тип матричного штрих-кода, который представляет собой машиночитаемую оптическую этикетку, содержащую информацию о товаре, к которому он прикреплен. На практике QR-коды часто содержат данные для локатора, идентификатора или трекера, который указывает на веб-сайт или приложение и т. Д.

В этом уроке вы узнаете, как генерировать и читать QR-коды на Python с помощью библиотек qrcode и OpenCV.

Установка необходимых зависимостей:

pip3 install opencv-python qrcode numpy
Генерация QR-кода
Во-первых, давайте начнем с генерации QR-кодов, это в основном просто с использованием библиотеки qrcode:

import qrcode
# example data
data = "https://www.thepythoncode.com"
# output file name
filename = "site.png"
# generate qr code
img = qrcode.make(data)
# save img to a file
img.save(filename)
Это сгенерирует новый файл изображения в текущем каталоге с именем «site.png», который содержит изображение QR-кода указанных данных (в данном случае url этого сайта), будет выглядеть примерно так:

Автоматически сгенерированный QR-код в Python

Вы также можете использовать эту библиотеку, чтобы иметь полный контроль над генерацией QR-кода с помощью qrcode. Класс QRCode(), в котором можно создать экземпляр и указать размер, цвет заливки, задний цвет и исправление ошибок, например:

import qrcode
import numpy as np
# data to encode
data = "https://www.thepythoncode.com"
# instantiate QRCode object
qr = qrcode.QRCode(version=1, box_size=10, border=4)
# add data to the QR code
qr.add_data(data)
# compile the data into a QR code array
qr.make()
# print the image shape
print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
# transfer the array into an actual image
img = qr.make_image(fill_color="white", back_color="black")
# save it to a file
img.save("site_inversed.png")
Поэтому при создании класса QRCode мы указываем параметр version, который представляет собой целое число от 1 до 40, которое управляет размером изображения QR-кода (1 — маленький, матрица 21x21, 40 — матрица 185x185), но это будет перезаписано, когда данные не соответствуют указанному вами размеру. В нашем случае он будет автоматически масштабироваться до версии 3.

box_size параметр управляет количеством пикселей каждого поля QR-кода, в то время как параметр border определяет, сколько полей должно быть толщиной границы.

Затем мы добавляем данные с помощью метода qr.add_data(), компилируем их в массив с помощью метода qr.make(), а затем создаем фактическое изображение с помощью метода qr.make_image(). Мы указали белый цвет в качестве fill_color и черный в качестве back_color, что является полной противоположностью QR-коду по умолчанию, проверьте его:

Генерация пользовательского QR-кода с помощью PythonИ форма изображения действительно была увеличена и не была 21x21:

The shape of the QR image: (37, 37)
Связанные с: Как сделать считыватель штрих-кодов в Python.

Чтение QR-кода
Есть много инструментов, которые считывают QR-коды. Тем не менее, мы будем использовать OpenCV для этого, так как он популярен и легко интегрируется с веб-камерой или любым видео.

Хорошо, откройте новый файл Python и следуйте вместе со мной, let's прочитайте изображение, которое мы только что сгенерировали:

import cv2
# read the QRCODE image
img = cv2.imread("site.png")
К счастью для нас, OpenCV уже имеет встроенный детектор QR-кодов:

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
У нас есть изображение и детектор, давайте обнаружим и декодируем эти данные:

# detect and decode
data, bbox, straight_qrcode = detector.detectAndDecode(img)
Функция detectAndDecode() принимает изображение в качестве входных данных и декодирует его для возврата кортежа из 3 значений: данных, декодированных из QR-кода, выходного массива вершин найденного четырехугольника QR-кода и выходного изображения, содержащего выпрямленный и бинаризованный QR-код.

Нам просто нужны данные и bbox здесь, bbox поможет нам нарисовать четырехугольник на изображении, и данные будут напечатаны на консоли!

Давайте сделаем:

# if there is a QR code
if bbox is not None:
    print(f"QRCode data:\n{data}")
    # display the image with lines
    # length of bounding box
    n_lines = len(bbox)
    for i in range(n_lines):
        # draw all lines
        point1 = tuple(bbox[i][0])
        point2 = tuple(bbox[(i+1) % n_lines][0])
        cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)
Функция cv2.line() рисует отрезок линии, соединяющий две точки, мы извлекаем эти точки из массива bbox, который был декодирован detectAndDecode() ранее. мы указали синий цвет ( (255, 0, 0) - синий, так как OpenCV использует цвета BGR ) и толщину 2.

Наконец, давайте покажем изображение и завершим работу при нажатии клавиши:

# display the result
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
После этого декодированные данные будут напечатаны:

QRCode data:
https://www.thepythoncode.com
И показано следующее изображение:

The read QRCode using OpenCV in Python

Как видите, синие линии нарисованы в точных границах QR-кода. Потрясающе, мы закончили с этим скриптом, попробуйте запустить его с разными данными и увидеть свои собственные результаты!

Обратите внимание, что это идеально подходит для QR-кодов, а не для штрих-кодов, если вы хотите читать штрих-коды, проверьте этот учебник, который посвящен этому!

Если вы хотите обнаружить и декодировать QR-коды в прямом эфире с помощью веб-камеры (и я уверен, что вы это сделаете), вот код для этого:

import cv2
# initalize the cam
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
while True:
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if bbox is not None:
        # display the image with lines
        for i in range(len(bbox)):
            # draw all lines
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data:
            print("[+] QR Code detected, data:", data)
    # display the result
    cv2.imshow("img", img)    
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
Потрясающе, мы закончили с этим учебником, теперь вы можете интегрировать это в свои собственные приложения!

Проверьте официальную документацию qrcode.