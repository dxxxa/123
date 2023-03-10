# [How to Make an Image Classifier in Python using TensorFlow and Keras](https://www.thepythoncode.com/article/image-classification-keras-python)
To run this:
- `pip3 install -r requirements.txt`
- First, you need to train the model using `python train.py`
- Edit the code in `test.py` for you optimal model weights in `results` folder ( currently does not because you need to train first ) and run:
    ```
    python test.py
    ```
    **Output:**
    ```
    10000/10000 [==============================] - 3s 331us/step
    Test accuracy: 81.17999999999999 %
    frog
    ```
##
# [[] / []]()
Классификация изображений относится к процессу в компьютерном зрении, который может классифицировать изображение в соответствии с его визуальным содержанием. Например, алгоритм классификации изображений может быть разработан, чтобы определить, содержит ли изображение кошку или собаку. Хотя обнаружение объекта является тривиальным для людей, надежная классификация изображений по-прежнему является проблемой в приложениях компьютерного зрения.

В этом учебнике вы узнаете, как успешно классифицировать изображения в наборе данных CIFAR-10 (который состоит из самолетов, собак, кошек и других 7 объектов) с помощью Tensorflow в Python.

Обратите внимание, что существует разница между классификацией изображений и обнаружением объектов, классификация изображений заключается в классификации изображения в некоторую категорию, как в этом примере, входом является изображение, а выводом является одна метка класса (10 классов). Обнаружение объектов — это обнаружение, классификация и локализация объектов в реальных изображениях, одним из основных алгоритмов является обнаружение объектов YOLO.

Мы предварительно обработаем изображения и метки, а затем обучим сверточную нейронную сеть на всех обучающих образцах. Изображения должны быть нормализованы, а метки должны быть закодированы одним горячим способом.

Во-первых, давайте установим требования для этого проекта:

pip3 install numpy matplotlib tensorflow==2.0.0 tensorflow_datasets
Например, откройте пустой файл python и назовите его train.py и следуйте за ним. Импорт Tensorflow:

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import tensorflow as tf
import tensorflow_datasets as tfds
import os
Как и следовало ожидать, мы будем использовать tf.data API для загрузки набора данных CIFAR-10.

Гиперпараметры
Я экспериментировал с различными параметрами и нашел это как оптимальные:

# hyper-parameters
batch_size = 64
# 10 categories of images (CIFAR-10)
num_classes = 10
# number of training epochs
epochs = 30
num_classes просто относится к количеству категорий для классификации, в этом случае CIFAR-10 имеет только 10 категорий изображений.

Понимание и загрузка набора данных CIFAR-10
Набор данных состоит из 10 классов изображений, которые его метки варьируются от 0 до 9:
0: самолет.
1: автомобиль.
2: птица.
3: кат.
4: олень.
5: собака.
6: лягушка.
7: лошадь.
8: корабль.
9: грузовик.
50000 образцов для обучающих данных и 10000 образцов для тестовых данных.
Каждый образец представляет собой изображение размером 32x32x3 пикселей (ширина и высота 32 и глубина 3, что является значениями RGB).
Давайте загрузим это:

def load_data():
    """
    This function loads CIFAR-10 dataset, and preprocess it
    """
    def preprocess_image(image, label):
        # convert [0, 255] range integers to [0, 1] range floats
        image = tf.image.convert_image_dtype(image, tf.float32)
        return image, label
    # loading the CIFAR-10 dataset, splitted between train and test sets
    ds_train, info = tfds.load("cifar10", with_info=True, split="train", as_supervised=True)
    ds_test = tfds.load("cifar10", split="test", as_supervised=True)
    # repeat dataset forever, shuffle, preprocess, split by batch
    ds_train = ds_train.repeat().shuffle(1024).map(preprocess_image).batch(batch_size)
    ds_test = ds_test.repeat().shuffle(1024).map(preprocess_image).batch(batch_size)
    return ds_train, ds_test, info
Эта функция загружает набор данных с помощью модуля Tensorflow Datasets, мы устанавливаем with_info значение True, чтобы получить некоторую информацию об этом наборе данных, вы можете распечатать его и посмотреть, какие разные поля и их значения, мы будем использовать информацию для получения количества образцов в обучающих и тестовых наборах.

После этого мы:

Повторите набор данных вечно, используя метод repeat(), это позволит нам многократно генерировать образцы данных (мы укажем условия остановки на этапе обучения).
Перетасуйте его.
Нормализуйте изображения между 0 и 1, это поможет нейронной сети обучаться намного быстрее, мы использовали метод map(), который принимает функцию обратного вызова, которая принимает изображение и метку в качестве аргументов, мы просто использовали встроенный метод Tensorflow convert_image_dtype(), который делает это.
Наконец, мы пакетируем наш набор данных по 64 образцам с помощью функции batch(), поэтому каждый раз, когда мы генерируем новые точки данных, он будет возвращать 64 изображения и их 64 метки.
Построение модели
Будет использоваться следующая модель:

def create_model(input_shape):
    # building the model
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="same", input_shape=input_shape))
    model.add(Activation("relu"))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    # flattening the convolutions
    model.add(Flatten())
    # fully-connected layer
    model.add(Dense(1024))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))
    # print the summary of the model architecture
    model.summary()
    # training the model using adam optimizer
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model
Это 3 слоя из 2 ConvNets с функцией максимального пулирования и активации ReLU, а затем полностью связанные с 1024 единицами. Это относительно небольшая модель по сравнению с ResNet50 или Xception, которые являются самыми современными. Если вы считаете, что используете модели, созданные экспертами по глубокому обучению, вам нужно использовать трансферное обучение.

Обучение модели
Теперь давайте обучим модель:

if __name__ == "__main__":
    # load the data
    ds_train, ds_test, info = load_data()
    # constructs the model
    model = create_model(input_shape=info.features["image"].shape)
    # some nice callbacks
    logdir = os.path.join("logs", "cifar10-model-v1")
    tensorboard = TensorBoard(log_dir=logdir)
    # make sure results folder exist
    if not os.path.isdir("results"):
        os.mkdir("results")
    # train
    model.fit(ds_train, epochs=epochs, validation_data=ds_test, verbose=1,
              steps_per_epoch=info.splits["train"].num_examples // batch_size,
              validation_steps=info.splits["test"].num_examples // batch_size,
              callbacks=[tensorboard])
    # save the model to disk
    model.save("results/cifar10-model-v1.h5")
После загрузки данных и создания модели я использовал Tensorboard, который будет отслеживать точность и потери в каждую эпоху и предоставлять нам хорошую визуализацию.

Мы будем использовать папку «результаты» для сохранения наших моделей, если вы не уверены, как вы можете обрабатывать файлы и каталоги в Python, проверьте этот учебник.

Поскольку ds_train и ds_test будут генерировать образцы данных партиями неоднократно, нам нужно указать количество шагов на эпоху, и это количество выборок, деленное на размер пакета, и оно одинаково для validation_steps.

Запустите это, это займет несколько минут для завершения обучения, в зависимости от вашего CPU / GPU.

Вы получите аналогичный результат:

Epoch 1/30
781/781 [==============================] - 20s 26ms/step - loss: 1.6503 - accuracy: 0.3905 - val_loss: 1.2835 - val_accuracy: 0.5238
Epoch 2/30
781/781 [==============================] - 16s 21ms/step - loss: 1.1847 - accuracy: 0.5750 - val_loss: 0.9773 - val_accuracy: 0.6542
Вплоть до последней эпохи:

Epoch 29/30
781/781 [==============================] - 16s 21ms/step - loss: 0.4094 - accuracy: 0.8570 - val_loss: 0.5954 - val_accuracy: 0.8089
Epoch 30/30
781/781 [==============================] - 16s 21ms/step - loss: 0.4130 - accuracy: 0.8563 - val_loss: 0.6128 - val_accuracy: 0.8060
Теперь, чтобы открыть tensorboard, все, что вам нужно сделать, это ввести эту команду в терминале или командной строке в текущем каталоге:

tensorboard --logdir="logs"
Open up a browser tab and type localhost:6006, you'll be redirected to tensorboard, here is my result:

Потеря валидацииТочность проверки

Очевидно, что мы на правильном пути, потери при проверке уменьшаются, а точность увеличивается примерно до 81%. Это здорово!

Тестирование модели
Как только обучение будет завершено, оно сохранит окончательную модель и веса в папке результатов, таким образом, мы можем тренироваться только один раз и делать прогнозы, когда захотим.

Откройте новый файл python под названием test.py и следуйте за ним.

Импорт необходимых утилит:

from train import load_data, batch_size
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
Давайте создадим словарь Python, который сопоставляет каждое целое значение с соответствующей меткой в наборе данных:

# CIFAR-10 classes
categories = {
    0: "airplane",
    1: "automobile",
    2: "bird",
    3: "cat",
    4: "deer",
    5: "dog",
    6: "frog",
    7: "horse",
    8: "ship",
    9: "truck"
}
Загрузка тестовых данных и модели:

# load the testing set
ds_train, ds_test, info = load_data()
# load the model with final model weights
model = load_model("results/cifar10-model-v1.h5")
Оценка:

# evaluation
loss, accuracy = model.evaluate(ds_test, steps=info.splits["test"].num_examples // batch_size)
print("Test accuracy:", accuracy*100, "%")
Возьмем случайное изображение и сделаем прогноз:

# get prediction for this image
data_sample = next(iter(ds_test))
sample_image = data_sample[0].numpy()[0]
sample_label = categories[data_sample[1].numpy()[0]]
prediction = np.argmax(model.predict(sample_image.reshape(-1, *sample_image.shape))[0])
print("Predicted label:", categories[prediction])
print("True label:", sample_label)
Мы использовали next(iter(ds_test)) для получения следующего тестового пакета, а затем извлекли первое изображение и метку в этом пакете и сделали прогнозы по модели, вот результат:

156/156 [==============================] - 3s 20ms/step - loss: 0.6119 - accuracy: 0.8063
Test accuracy: 80.62900900840759 %
Predicted label: frog
True label: frog
Модель говорит, что это лягушка, давайте проверим это:

# show the image
plt.axis('off')
plt.imshow(sample_image)
plt.show()
Результат:ЛягушкаКрошечная лягушка! Модель была права!

Заключение
Хорошо, мы закончили с этим учебником, 81% неплохо для этого маленького CNN, я настоятельно рекомендую вам настроить модель или проверить ResNet50, Xception или другие современные модели, чтобы получить более высокую производительность!

Если вы не знаете, как использовать эти модели, у меня есть учебник по этому вопросу: Как использовать transfer Learning для классификации изображений с помощью Keras в Python.

Вы можете задаться вопросом, что эти изображения настолько просты, сетка 32x32 не такая, как реальный мир, изображения не такие простые, они часто содержат много объектов, сложных узоров и так далее. В результате часто обычной практикой является использование методов сегментации изображений, таких как обнаружение контуров или сегментация кластеризации K-Средних, прежде чем переходить к каким-либо методам классификации.

Наконец, если вы хотите расширить свои навыки в области машинного обучения (или даже если вы новичок), я бы посоветовал вам пройти специализированные курсы по машинному обучению и глубокому обучению. Удачи!

Счастливое обучение ♥