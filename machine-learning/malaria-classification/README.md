# [How to Perform Malaria Cells Classification using TensorFlow 2 and Keras in Python](https://www.thepythoncode.com/article/malaria-cells-classification)
To run this:
- `pip3 install -r requirements.txt`
##
# [[] / []]()
Примеры использования глубокого обучения в медицине в последние годы знают большой скачок, от автоматической диагностики пациентов до компьютерного зрения, многие передовые модели разрабатываются в этой области.

В этом уроке мы реализуем модель глубокого обучения с использованием TensorFlow (Keras API) для двоичной задачи классификации, которая состоит из маркировки изображений клеток на инфицированных или не зараженных малярией.

Установка необходимых библиотек и фреймворков:

pip install numpy tensorflow opencv-python sklearn matplotlib
См. также: Как создать классификатор изображений в Python с помощью Tensorflow 2 и Keras.

Загрузка набора данных
Мы собираемся использовать Malaria Cell Images Dataset из Kaggle,fter загрузка и распаковка папки, вы увидите, cell_images, эта папка будет содержать две подпапки: Parasitized, Uninfected и еще один дублированный cell_images папке, не стесняйтесь удалять эту папку.

Я также предлагаю вам переместить изображение из обоих классов в другую папку test-samples, чтобы мы могли сделать выводы по нему, когда закончим обучение нашей модели.

Изображение инфицированных и неинфицированных клетокПредварительная обработка изображений с помощью OpenCV
OpenCV - это оптимизированная библиотека с открытым исходным кодом для обработки изображений и компьютерного зрения. Мы будем использовать его для предварительной обработки наших изображений и преобразования их в оттенки серого в виде массива NumPy (числовой формат) и изменения его размера до формы (70x70):

import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Activation
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# after you extract the dataset, 
# put cell_images folder in the working directory
img_dir="cell_images"  
img_size=70

def load_img_data(path):
    image_files = glob.glob(os.path.join(path, "Parasitized/*.png")) + \
                  glob.glob(os.path.join(path, "Uninfected/*.png"))
    X, y = [], []
    for image_file in image_files:
        # 0 for uninfected and 1 for infected
        label = 0 if "Uninfected" in image_file else 1
        # load the image in gray scale
        img_arr = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        # resize the image to (70x70)
        img_resized = cv2.resize(img_arr, (img_size, img_size))
        X.append(img_resized)
        y.append(label)
    return X, y
Мы использовали встроенный модуль glob для получения всех изображений в этом формате (заканчивая .png в определенной папке).

Затем мы перебираем эти имена файлов изображений и загружаем каждое изображение в оттенках серого, изменяем его размер и добавляем его в наш массив, мы также делаем то же самое для меток (0 для незараженных и 1 для паразитированных).

Связанные с: Распознавание лиц с помощью OpenCV в Python.

Подготовка и нормализация набора данных
Теперь, когда у нас есть наша функция для загрузки набора данных, давайте вызовем ее и выполним некоторую подготовку:

# load the data
X, y = load_img_data(img_dir)
# reshape to (n_samples, 70, 70, 1) (to fit the NN)
X = np.array(X).reshape(-1, img_size, img_size, 1)
# scale pixels from the range [0, 255] to [0, 1] 
# to help the neural network learn much faster
X = X / 255 

# shuffle & split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y)
print("Total training samples:", X_train.shape)
print("Total validation samples:", X_test.shape[0])
После того, как мы загрузим наш набор данных предварительно обработанным, мы расширяем форму массива изображений до (n_samples, 70, 70, 1), чтобы соответствовать входу нейронной сети.

Кроме того, чтобы помочь сети быстрее конвергенции, мы должны выполнить нормализацию данных. Существуют методы масштабирования из этого в sklearn, такие как:

StandardScaler: x_norm = (x - среднее) / std (где std - стандартное отклонение)
MinMaxScaler: x_norm = (x - x_min) / (x_max - x_min) это приводит к x_norm в диапазоне от 0 до 1.
В нашем случае мы не будем их использовать. Вместо этого мы разделим на 255, так как наибольшее значение, которое может достичь пиксель, составляет 255, это приведет к пикселям в диапазоне от 0 до 1 после применения масштабирования.

Затем мы будем использовать метод train_test_split() из sklearn для разделения набора данных на обучающие и тестовые наборы, мы использовали 10% от общего объема данных для его проверки позже. Параметр stratify сохранит долю цели, как и в исходном наборе данных, а также в обучающих и тестовых наборах данных.

train_test_split() метод перетасовывает данные по умолчанию (shuffle имеет значение True), мы хотим это сделать, так как исходное упорядочение состоит из прямых меток 0s в первой половине и прямых меток 1s во второй половине, что может привести к плохой тренировке сети в дальнейшем.

Реализация архитектуры модели CNN
Наша архитектура нейронной сети будет каким-то образом следовать той же архитектуре, что и на рисунке:



В нашем случае мы добавим 3 слоя свертки, затем сгладим, чтобы затем последовали полностью соединенные слои, состоящие из плотных слоев.

Определим эти слои и свойства:

Слои свертки: Роль сверточных слоев заключается в том, чтобы уменьшить изображения в более легкие формы, сохраняя только самые важные признаки. Матричный фильтр будет проходить по изображениям для применения операций свертки.
Слои пулинга: Их роль заключается в уменьшении пространственного объема, возникающего в результате операций свертки. Существует два типа слоев пулинга; средние слои пулинга и максимальные слои пулинга (в нашем случае мы будем использовать последние).
Сплющить: Слой, ответственный за преобразование результатов из свертки и опроса в 1D-форму, которая затем передается в полностью соединенный слой.
model = Sequential()
model.add(Conv2D(64, (3, 3), input_shape=X_train.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(64))
model.add(Activation("relu"))

model.add(Dense(64))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# train the model with 3 epochs, 64 batch size
model.fit(X_train, np.array(y_train), batch_size=64, epochs=3, validation_split=0.2)
# if you already trained the model, uncomment below and comment above
# so you can only load the previously trained model
# model.load_weights("malaria-cell-cnn.h5")
Поскольку выходные данные являются двоичными (либо заражены, либо не заражены), мы использовали Sigmoid (1/(1+exp(-x)) в качестве функции активации выходного слоя.

Вот мои результаты обучения:

Train on 19840 samples, validate on 4960 samples
Epoch 1/3
19840/19840 [==============================] - 14s 704us/sample - loss: 0.5067 - accuracy: 0.7135 - val_loss: 0.1949 - val_accuracy: 0.9300
Epoch 2/3
19840/19840 [==============================] - 12s 590us/sample - loss: 0.1674 - accuracy: 0.9391 - val_loss: 0.1372 - val_accuracy: 0.9482
Epoch 3/3
19840/19840 [==============================] - 12s 592us/sample - loss: 0.1428 - accuracy: 0.9495 - val_loss: 0.1344 - val_accuracy: 0.9518
Как вы, возможно, заметили, мы достигли точности 95% на обучающем наборе данных и его разделении проверки.

Оценка модели
Теперь давайте используем evaluate() из KERAS API для оценки модели на тестовом наборе данных:

loss, accuracy = model.evaluate(X_test, np.array(y_test), verbose=0)
print(f"Testing on {len(X_test)} images, the results are\n Accuracy: {accuracy} | Loss: {loss}")
Testing on 2756 images, the results are
 Accuracy: 0.9444847702980042 | Loss: 0.15253388267470028
Модель показала хорошие результаты и в тестовых данных с точностью, достигающей 94%.

Теперь давайте используем эту модель для выполнения выводов из двух изображений, которые мы поместили в папку testing-samples ранее в этом учебнике. Во-первых, давайте построим их график:

# testing some images
uninfected_cell = "cell_images/testing-samples/C1_thinF_IMG_20150604_104919_cell_82.png"
infected_cell = "cell_images/testing-samples/C38P3thinF_original_IMG_20150621_112116_cell_204.png"

_, ax = plt.subplots(1, 2)
ax[0].imshow(plt.imread(uninfected_cell))
ax[0].title.set_text("Uninfected Cell")
ax[1].imshow(plt.imread(infected_cell))
ax[1].title.set_text("Parasitized Cell")
plt.show()
Выпуск:

Инфицированные малярией и неинфицированные клетки

Отлично, теперь давайте загрузим эти изображения и выполним предварительную обработку:

img_arr_uninfected = cv2.imread(uninfected_cell, cv2.IMREAD_GRAYSCALE)
img_arr_infected = cv2.imread(infected_cell, cv2.IMREAD_GRAYSCALE)
# resize the images to (70x70)
img_arr_uninfected = cv2.resize(img_arr_uninfected, (img_size, img_size))
img_arr_infected = cv2.resize(img_arr_infected, (img_size, img_size))
# scale to [0, 1]
img_arr_infected = img_arr_infected / 255
img_arr_uninfected = img_arr_uninfected / 255
# reshape to fit the neural network dimensions
# (changing shape from (70, 70) to (1, 70, 70, 1))
img_arr_infected = img_arr_infected.reshape(1, *img_arr_infected.shape)
img_arr_infected = np.expand_dims(img_arr_infected, axis=3)
img_arr_uninfected = img_arr_uninfected.reshape(1, *img_arr_uninfected.shape)
img_arr_uninfected = np.expand_dims(img_arr_uninfected, axis=3)
Все, что нам нужно сделать сейчас, это использовать метод predict(), чтобы сделать вывод:

# perform inference
infected_result = model.predict(img_arr_infected)[0][0]
uninfected_result = model.predict(img_arr_uninfected)[0][0]
print(f"Infected: {infected_result}")
print(f"Uninfected: {uninfected_result}")
Выпуск:

Infected: 0.9827326536178589
Uninfected: 0.005085020791739225
Удивительно, модель на 98% уверена, что инфицированная клетка на самом деле инфицирована, и он уверен в 99,5% случаев, что неинфицированная клетка не инфицирована.

Сохранение модели
Наконец, мы завершим весь этот процесс сохранением нашей модели.

# save the model & weights
model.save("malaria-cell-cnn.h5")
Заключение:

В этом уроке вы узнали:

Как обрабатывать необработанные изображения, конвертировать их в оттенки серого и в массив NumPy (числовой формат) с помощью OpenCV.
Архитектура, лежащая в основе сверточной нейронной сети с ее различными компонентами.
Реализация CNN в Tensorflow/Keras.
Оценить и сохранить модель глубокого обучения, а также выполнить вывод по ней.
Я рекомендую вам настроить параметры модели, или вы можете использовать трансферное обучение, чтобы вы могли работать намного лучше. Вы также можете тренироваться на цветных изображениях вместо оттенков серого, это может помочь!

Есть и другие метрики, помимо точности, такие как чувствительность и специфичность, которые широко используются в медицинской сфере, я предлагаю вам добавить их и здесь. Если вы не уверены, как есть учебник по обнаружению рака кожи, в котором мы все это сделали!

Хотите узнать больше?
Наконец, я собрал несколько полезных ресурсов и курсов для вас для дальнейшего обучения, вот вам:

Курс «Глубокое обучение в компьютерном зрении»
Курс глубокого обучения
Курс по сверточным нейронным сетям
Введение в компьютерное зрение с Watson и курсом OpenCV