# [How to Blur Faces in Images using OpenCV in Python](https://www.thepythoncode.com/article/blur-faces-in-images-using-opencv-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To blur faces of the image `father-and-daughter.jpg`:
    ```
    python blur_faces.py father-and-daughter.jpg
    ```
    This should show the blurred image and save it of the name `image_blurred.jpg` in your current directory.

- To blur faces using your live camera:
    ```
    python blur_faces_live.py
    ```
- To blur faces of a video:
    ```
    python blur_faces_video.py video.3gp
    ```
##
# [[] / []]()
Во многих случаях вы хотите загрузить видео или изображение публично в Интернете, и вы можете захотеть анонимизировать случайных людей, показанных на этом видео или изображении. В этом уроке вы узнаете, как можно размыть лица в изображениях и видео с помощью библиотеки OpenCV на Python.

Для того, чтобы размыть лица, показанные на изображениях, вам нужно сначала обнаружить эти лица и их положение на изображении. К счастью для нас, я уже написал учебник по распознаванию лиц, мы будем использовать только его исходный код, не стесняйтесь проверить его для получения дополнительной информации о том, как работает код распознавания лиц.

Чтобы начать установку необходимых зависимостей:

pip3 install opencv-python numpy
Откройте новый файл и импортируйте:

import cv2
import numpy as np
Как объясняется в учебнике по распознаванию лиц, поскольку нам нужно инициализировать нашу модель глубокого обучения для обнаружения лиц, нам нужно получить архитектуру модели вместе с ее предварительно обученными весами, загрузить их и поместить в папку весов:

# https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
prototxt_path = "weights/deploy.prototxt.txt"
# https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel 
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
# load Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
Приведенный ниже код считывает это изображение, подготавливает его и передает в нейронную сеть:

# read the desired image
image = cv2.imread("father-and-daughter.jpg")
# get width and height of the image
h, w = image.shape[:2]
# gaussian blur kernel size depends on width and height of original image
kernel_width = (w // 7) | 1
kernel_height = (h // 7) | 1
# preprocess the image: resize and performs mean subtraction
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
# set the image into the input of the neural network
model.setInput(blob)
# perform inference and get the result
output = np.squeeze(model.forward())
Теперь выходной объект представляет собой массив NumPy, в котором обнаружены все грани, давайте пересмотрим этот массив и размымем только те части, где мы уверены, что это лицо:

for i in range(0, output.shape[0]):
    confidence = output[i, 2]
    # get the confidence
    # if confidence is above 40%, then blur the bounding box (face)
    if confidence > 0.4:
        # get the surrounding box cordinates and upscale them to original image
        box = output[i, 3:7] * np.array([w, h, w, h])
        # convert to integers
        start_x, start_y, end_x, end_y = box.astype(np.int)
        # get the face image
        face = image[start_y: end_y, start_x: end_x]
        # apply gaussian blur to this face
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        # put the blurred face into the original image
        image[start_y: end_y, start_x: end_x] = face
В отличие от учебника по распознаванию лиц, где мы нарисовали ограничительные рамки для каждого обнаруженного лица. Вместо этого здесь мы получаем координаты коробки и применяем к ней размытие гаусса.

cv2. Метод GaussianBlur() размывает изображение с помощью гауссовского фильтра, применяя медианное значение к центральному пикселю в пределах размера ядра. Он принимает входное изображение в качестве первого аргумента, размер ядра Гаусса в качестве кортежа во втором аргументе и параметр sigma в качестве третьего.

Мы вычислили размер ядра Гаусса из исходного изображения, в документации говорится, что это должно быть нечетное и положительное целое число, я разделил исходное изображение на 7, чтобы оно зависело от формы изображения и выполнило побитовое ИЛИ, чтобы убедиться, что результирующее значение является нечетным числом, вы, конечно, можете установить свой собственный размер ядра, чем он выше, тем размытее изображение.

После того, как мы размываем каждое лицо, мы возвращаем его к исходному изображению, таким образом, мы получим изображение, в котором все лица размыты, вот результат:

Размытое изображение с помощью OpenCV в Python

Прекрасно! Хорошая вещь в этом заключается в том, что вы можете размыть лица в прямом эфире с помощью камеры, а также читать внешние видео по вашему выбору, проверить полную кодовую страницу для всего этого.

Я взял видео на YouTube и размыл все лица, проверьте это:

Размытие лиц в видео с помощью OpenCV в Python

Если вы хотите узнать, как работает распознавание лиц, обратитесь к этому руководству для объяснения.

Вы можете получить все ресурсы для этого учебника на этой странице Github.

Хотите узнать больше?
Наконец, я собрал несколько полезных ресурсов и курсов для вас для дальнейшего обучения, вот вам:

Специализированный курс глубокого обучения
Курс по сверточным нейронным сетям
Введение в компьютерное зрение и обработку изображений