# [Handling Imbalanced Datasets: A Case Study with Customer Churn](https://www.thepythoncode.com/article/handling-imbalanced-datasets-sklearn-in-python)
##
# [[] / []]()
Знакомство
Набор данных с неравными классами — это популярный вызов науки о данных и интересный вопрос интервью. Из этого туториала Вы узнаете, как эффективно оптимизировать модель и обрабатывать несбалансированные данные.

Проблемы классификации, такие как фильтрация спама, обнаружение мошенничества с кредитными картами, проблемы с медицинской диагностикой, такие как обнаружение рака кожи, и прогнозирование оттока являются одними из наиболее распространенных областей, где вы можете найти несбалансированные данные.

Почти каждый набор данных имеет неравномерное представление класса. Это не проблема, пока разница незначительна. Однако многие модели не могут обнаружить классы меньшинств, когда один или несколько классов очень редки.

Этот учебник будет предполагать двухклассовый выпуск (один класс большинства и один класс меньшинства).

Как правило, мы проверяем точность валидационного разделения, чтобы увидеть, насколько хорошо функционирует наша модель. Тем не менее, когда данные искажены, точность может быть обманчивой.

Содержание:

Знакомство
Описание данных
Кодирование категориальных переменных
Выполнение визуализации данных
Запуск логистической регрессии
Борьба с дисбалансом классов с использованием веса класса
Устранение дисбаланса классов с помощью ресамплинга
Борьба с дисбалансом классов с помощью SMOTE
Заключение
Описание данных
Эти данные содержат информацию о фирме, предоставляющей услуги потокового видео, которая хочет оценить, будет ли клиент оттокаться.

CSV-файл содержит около 2000 строк и 16 столбцов. Набор данных можно скачать здесь.

Прежде чем мы начнем, давайте установим необходимые библиотеки для этого учебника:

$ pip install numpy sklearn imblearn pandas statsmodels seaborn
Установим gdown для автоматической загрузки набора данных:

$ pip install --upgrade gdown
Загрузка набора данных:

$ gdown --id 12vfq3DYFId3bsXuNj_PhsACMzrLTfObs
Выпуск:

Downloading...
From: https://drive.google.com/uc?id=12vfq3DYFId3bsXuNj_PhsACMzrLTfObs
To: /content/data_regression.csv
100% 138k/138k [00:00<00:00, 72.5MB/s]
Теперь у нас все готово, начнем с импорта необходимых библиотек:

import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.utils import resample
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
Загрузка набора данных:

data=pd.read_csv("data_regression.csv")
# get the first 5 rows
data.head()
╔═══╤══════╤═════════════╤══════════╤════════╤═════╤═══════════════════════╤══════════════╤═════════════════╤═════════════════════╤════════════════════╤════════════════════╤═══════════════════════╤════════════════╤═══════════════════════╤════════════════════════╤═══════╗
║   │ year │ customer_id │ phone_no │ gender │ age │ no_of_days_subscribed │ multi_screen │ mail_subscribed │ weekly_mins_watched │ minimum_daily_mins │ maximum_daily_mins │ weekly_max_night_mins │ videos_watched │ maximum_days_inactive │ customer_support_calls │ churn ║
╠═══╪══════╪═════════════╪══════════╪════════╪═════╪═══════════════════════╪══════════════╪═════════════════╪═════════════════════╪════════════════════╪════════════════════╪═══════════════════════╪════════════════╪═══════════════════════╪════════════════════════╪═══════╣
║ 0 │ 2015 │ 100198      │ 409-8743 │ Female │ 36  │ 62                    │ no           │ no              │ 148.35              │ 12.2               │ 16.81              │ 82                    │ 1              │ 4.0                   │ 1                      │ 0.0   ║
╟───┼──────┼─────────────┼──────────┼────────┼─────┼───────────────────────┼──────────────┼─────────────────┼─────────────────────┼────────────────────┼────────────────────┼───────────────────────┼────────────────┼───────────────────────┼────────────────────────┼───────╢
║ 1 │ 2015 │ 100643      │ 340-5930 │ Female │ 36  │ 149                   │ no           │ no              │ 294.45              │ 7.7                │ 33.37              │ 87                    │ 3              │ 3.0                   │ 2                      │ 0.0   ║
╟───┼──────┼─────────────┼──────────┼────────┼─────┼───────────────────────┼──────────────┼─────────────────┼─────────────────────┼────────────────────┼────────────────────┼───────────────────────┼────────────────┼───────────────────────┼────────────────────────┼───────╢
║ 2 │ 2015 │ 100756      │ 372-3750 │ Female │ 36  │ 126                   │ no           │ no              │ 87.30               │ 11.9               │ 9.89               │ 91                    │ 1              │ 4.0                   │ 5                      │ 1.0   ║
╟───┼──────┼─────────────┼──────────┼────────┼─────┼───────────────────────┼──────────────┼─────────────────┼─────────────────────┼────────────────────┼────────────────────┼───────────────────────┼────────────────┼───────────────────────┼────────────────────────┼───────╢
║ 3 │ 2015 │ 101595      │ 331-4902 │ Female │ 36  │ 131                   │ no           │ yes             │ 321.30              │ 9.5                │ 36.41              │ 102                   │ 4              │ 3.0                   │ 3                      │ 0.0   ║
╟───┼──────┼─────────────┼──────────┼────────┼─────┼───────────────────────┼──────────────┼─────────────────┼─────────────────────┼────────────────────┼────────────────────┼───────────────────────┼────────────────┼───────────────────────┼────────────────────────┼───────╢
║ 4 │ 2015 │ 101653      │ 351-8398 │ Female │ 36  │ 191                   │ no           │ no              │ 243.00              │ 10.9               │ 27.54              │ 83                    │ 7              │ 3.0                   │ 1                      │ 0.0   ║
╚═══╧══════╧═════════════╧══════════╧════════╧═════╧═══════════════════════╧══════════════╧═════════════════╧═════════════════════╧════════════════════╧════════════════════╧═══════════════════════╧════════════════╧═══════════════════════╧════════════════════════╧═══════╝
Приведенная ниже функция поможет в осмотре и очистке кадра данных:

# check for the missing values and dataframes
def datainspection(dataframe):
  print("Types of the variables we are working with:")
  print(dataframe.dtypes)
  
  print("Total Samples with missing values:")

  print(data.isnull().any(axis=1).sum()) # null values

  print("Total Missing Values per Variable")
  print(data.isnull().sum())
  print("Map of missing values")
  sns.heatmap(dataframe.isnull())
datainspection(data)
age                         int64
no_of_days_subscribed       int64
multi_screen               object
mail_subscribed            object
weekly_mins_watched       float64
minimum_daily_mins        float64
maximum_daily_mins        float64
weekly_max_night_mins       int64
videos_watched              int64
maximum_days_inactive     float64
customer_support_calls      int64
churn                     float64
dtype: object
Total Samples with missing values:
82
Total Missing Values per Variable
year                       0
customer_id                0
phone_no                   0
gender                    24
age                        0
no_of_days_subscribed      0
multi_screen               0
mail_subscribed            0
weekly_mins_watched        0
minimum_daily_mins         0
maximum_daily_mins         0
weekly_max_night_mins      0
videos_watched             0
maximum_days_inactive     28
customer_support_calls     0
churn                     35
dtype: int64
Map of missing values
Мы удалим все нулевые значения:

data = data.dropna() # cleaning up null values
Кодирование категориальных переменных
Класс OrdinalEncoder() будет использоваться для кодирования категориальных объектов в виде целочисленного массива:

# function for encoding categorical variables
def encode_cat(data, vars):
  ord_en = OrdinalEncoder() 
  for v in vars:
    name = v+'_code' # add _code for encoded variables
    data[name] = ord_en.fit_transform(data[[v]])
    print('The encoded values for '+ v + ' are:')
    print(data[name].unique())
  return data
# check for the encoded variables
data = encode_cat(data, ['gender', 'multi_screen', 'mail_subscribed'])
The encoded values for gender are:
[0. 1.]
The encoded values for multi_screen are:
[0. 1.]
The encoded values for mail_subscribed are:
[0. 1.]
Выполнение визуализации данных
Приведенная ниже функция вернет парный график всех переменных в наборе данных. Функция select_dtypes() извлекает подмножество столбцов в DataFrame в зависимости от типов столбцов. Передаем столбцы для исключения в виде списка разностному методу:

def full_plot(data, class_col, cols_to_exclude):
  cols = data.select_dtypes(include=np.number).columns.tolist() # finding all the numerical columns from the dataframe
  X = data[cols] # creating a dataframe only with the numerical columns
  X = X[X.columns.difference(cols_to_exclude)] # columns to exclude
  X = X[X.columns.difference([class_col])]
  sns.pairplot(data, hue=class_col)
Чтобы отобразить парные графики, мы должны вызвать функцию выше:

full_plot(data,class_col='churn', cols_to_exclude=['customer_id','phone_no', 'year'])
Мы позволим вам выполнить эту операцию и увидеть результат, так как для ее завершения требуется от нескольких секунд до нескольких минут.

Тем не менее, функция ниже поможет нам, если мы хотим создать графики для выборочных столбцов:

# function for creating plots for selective columns only
def selected_diagnotic(data,class_col, cols_to_eval):
  cols_to_eval.append(class_col) 
  X = data[cols_to_eval] # only selective columns
  sns.pairplot(X, hue=class_col) # plot
selected_diagnotic(data, class_col='churn', cols_to_eval=['videos_watched', 'no_of_days_subscribed'])


Запуск логистической регрессии
Приведенная ниже функция выполняет задачу логистической регрессии с помощью statsmodels, который представляет собой модуль Python, предоставляющий классы и методы для оценки широкого спектра статистических моделей, выполнения статистических тестов и изучения статистических данных.

Logit() — метод, предоставляемый statsmodels для выполнения логистической регрессии. Он принимает два входных сигнала, y и X, и возвращает объект Logit.

После этого модель подгоняется к данным. В приведенной ниже таблице приводится описательное резюме результатов регрессии.

def logistic_regression(data, class_col, cols_to_exclude):
  cols = data.select_dtypes(include=np.number).columns.tolist() 
  X = data[cols]
  X = X[X.columns.difference([class_col])] 
  X = X[X.columns.difference(cols_to_exclude)] # unwanted columns 

  y = data[class_col] # the target variable 
  logit_model = sm.Logit(y,X) 
  result = logit_model.fit() # fit the model 
  print(result.summary2()) # check for summary 
logistic_regression(data, class_col='churn', cols_to_exclude=['customer_id', 'phone_no', 'year'])
Optimization terminated successfully.
         Current function value: 0.336585
         Iterations 7
                            Results: Logit
=======================================================================
Model:                Logit              Pseudo R-squared:   0.137     
Dependent Variable:   churn              AIC:                1315.1404 
Date:                 2022-04-01 12:22   BIC:                1381.8488 
No. Observations:     1918               Log-Likelihood:     -645.57   
Df Model:             11                 LL-Null:            -748.02   
Df Residuals:         1906               LLR p-value:        7.1751e-38
Converged:            1.0000             Scale:              1.0000    
No. Iterations:       7.0000                                           
-----------------------------------------------------------------------
                        Coef.  Std.Err.    z    P>|z|   [0.025   0.975]
-----------------------------------------------------------------------
age                    -0.0208   0.0068 -3.0739 0.0021  -0.0340 -0.0075
customer_support_calls  0.4246   0.0505  8.4030 0.0000   0.3256  0.5237
gender_code            -0.2144   0.1446 -1.4824 0.1382  -0.4979  0.0691
mail_subscribed_code   -0.7529   0.1798 -4.1873 0.0000  -1.1053 -0.4005
maximum_daily_mins     -3.7125  25.2522 -0.1470 0.8831 -53.2058 45.7809
maximum_days_inactive  -0.7870   0.2473 -3.1828 0.0015  -1.2716 -0.3024
minimum_daily_mins      0.2075   0.0727  2.8555 0.0043   0.0651  0.3499
multi_screen_code       1.9511   0.1831 10.6562 0.0000   1.5923  2.3100
no_of_days_subscribed  -0.0045   0.0018 -2.5572 0.0106  -0.0080 -0.0011
videos_watched         -0.0948   0.0317 -2.9954 0.0027  -0.1569 -0.0328
weekly_max_night_mins  -0.0169   0.0032 -5.3119 0.0000  -0.0231 -0.0107
weekly_mins_watched     0.4248   2.8619  0.1484 0.8820  -5.1844  6.0340
Некоторые из концепций в сводной таблице определены следующим образом:

Итерации: количество итераций модели, пытающихся оптимизировать модель. Максимальное количество итераций, выполняемых по умолчанию, составляет 33, за которыми завершается сбой оптимизации. Некоторые из концепций в сводной таблице определены следующим образом:
coef: Коэффициенты независимых переменных уравнения регрессии.
Log-Probability: Натуральный логарифм функции MLE. MLE - это процесс определения набора параметров, который приводит к наилучшему соответствию.
LL-Null: значение логарифмической вероятности модели, если независимая переменная не включена.
Псевдо-R-квадрат: значение, используемое для замены R-квадрата в линейной регрессии наименьших квадратов. Это отношение логарифмической вероятности нулевой модели к логарифмической вероятности всей модели.
P-значение: p-значение относится к проверке гипотезы, и чем ниже p-значение, тем больше важность переменной в модели.
Две функции, приведенные ниже, помогут подготовить и запустить модель. Первая функция будет обрабатывать секцию, а вторая отобразит отчет о классификации и область под кривой:

def prepare_model(data, class_col, cols_to_exclude):
  # Split in training and test set
  # Selecting only the numerical columns and excluding the columns we specified in the function
  cols = data.select_dtypes(include=np.number).columns.tolist() 
  X = data[cols]
  X = X[X.columns.difference([class_col])] 
  X = X[X.columns.difference(cols_to_exclude)]
  # Selecting y as a column
  y = data[class_col]
  return train_test_split(X, y, test_size=0.3, random_state=0) # perform train test split
def run_model(X_train, X_test, y_train, y_test):
  # Fitting the logistic regression
  logreg = LogisticRegression(random_state=13)
  logreg.fit(X_train, y_train) # fit the model
  # Predicting y values
  y_pred = logreg.predict(X_test) # make predictions on th test data
  logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
  print(classification_report(y_test, y_pred)) # check for classification report 
  print("The area under the curve is:", logit_roc_auc)  # check for AUC
  return y_pred
X_train, X_test, y_train, y_test = prepare_model(data, class_col='churn', cols_to_exclude=['customer_id', 'phone_no', 'year'])
y_pred = run_model(X_train, X_test, y_train, y_test)
    precision    recall  f1-score   support

         0.0       0.90      0.98      0.94       513
         1.0       0.47      0.13      0.20        63

    accuracy                           0.89       576
   macro avg       0.69      0.55      0.57       576
weighted avg       0.85      0.89      0.86       576

The area under the curve is: 0.55
Цитата из sklearn:

Точность — это отношение tp / (tp + fp), где tp — число истинных положительных результатов, а fp — количество ложных срабатываний.
Точность интуитивно заключается в способности классификатора не маркировать как положительный образец, который является отрицательным.
Отзыв — это отношение tp / (tp + fn), где tp — число истинных положительных результатов, а fn — количество ложноотрицательных.
Отзыв – это интуитивно способность классификатора находить все положительные образцы.
Оценка F-beta может быть интерпретирована как взвешенное гармоническое среднее точности и запоминания, где оценка F-beta достигает своего наилучшего значения при 1 и худшего балла при 0.
Стоит отметить, что оценка Формулы-1 здесь слишком низкая.

Давайте выполним матрицу путаницы. Матрица путаницы, которая иллюстрирует точные и неправильные прогнозы каждого класса, является захватывающим инструментом для анализа результата.

def confusion_m(y_test, y_pred):
  cm = confusion_matrix(y_test, y_pred)
  print(cm)
  tn, fp, fn, tp = cm.ravel()
  print("TN:", tn)
  print("TP:", tp)
  print("FN:", fn)
  print("FP:", fp)
## Call the function
confusion_m(y_test, y_pred)
[[504   9]
 [ 55   8]]
TN: 504
TP: 8
FN: 55
FP: 9
Первый столбец в первой строке показывает, сколько классов 0 было успешно предсказано, в то время как второй столбец показывает, сколько классов 0 было точно предсказано как 1.

Для класса меньшинства модель, упомянутая выше, может правильно предсказать 8 из 63 выборок. Только девять прогнозов оказались неверными для класса большинства. Поэтомумодель не очень хорошо предсказывает классы меньшинств.

Борьба с дисбалансом классов с использованием веса класса
Многие классификаторы Scikit-Learn имеют параметр class_weights, который можно задать для балансировки или задать пользовательский словарь, чтобы указать, как расставить приоритеты в релевантности несбалансированных данных.

Это сравнимо с передискретизацией. Вместо того, чтобы фактически перебирать (поскольку более обширный набор данных был бы вычислительно более дорогостоящим), мы можем поручить оценщику скорректировать способ расчета потерь.

Мы можем заставить оценщика учиться, используя веса в зависимости от того, какую релевантность (вес) мы придаем конкретному классу.

Мы определили class_weight="balanced" для репликации меньшего класса до тех пор, пока не получим такое же количество выборок, как и более крупный.

# class imbalance method 1 
def run_model_bweights(X_train, X_test, y_train, y_test):
    logreg = LogisticRegression(random_state=13, class_weight='balanced') # define class_weight parameter
    logreg.fit(X_train, y_train) # fit the model 
    y_pred = logreg.predict(X_test) # predict on test data
    logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test)) # ROC AUC score
    print(classification_report(y_test, y_pred)) 
    print("The area under the curve is:", logit_roc_auc) # AUC curve
run_model_bweights(X_train, X_test, y_train, y_test)
              precision    recall  f1-score   support

         0.0       0.96      0.75      0.84       513
         1.0       0.27      0.78      0.40        63

    accuracy                           0.75       576
   macro avg       0.62      0.76      0.62       576
weighted avg       0.89      0.75      0.79       576

The area under the curve is: 0.76
Можно отметить небольшое улучшение отзыва и оценки Формулы-1. Давайте продолжим, присвоив больший вес классу большинства (Случайный вес) и посмотрим, что произойдет:

# class imbalance method 2
def run_model_aweights(X_train, X_test, y_train, y_test, w):
    logreg = LogisticRegression(random_state=13, class_weight=w) # define class_weight parameter
    logreg.fit(X_train, y_train) # fit the model 
    y_pred = logreg.predict(X_test) # predict on test data
    logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))  # ROC AUC score
    print(classification_report(y_test, y_pred))
    print("The area under the curve is: %0.2f"%logit_roc_auc)  # AUC curve
run_model_aweights(X_train,X_test,y_train,y_test,{0:90, 1:10})
              precision    recall  f1-score   support

         0.0       0.89      1.00      0.94       513
         1.0       1.00      0.02      0.03        63

    accuracy                           0.89       576
   macro avg       0.95      0.51      0.49       576
weighted avg       0.90      0.89      0.84       576

The area under the curve is: 0.51
Мы отмечаем резкое падение с результатом Формулы-1. Поэтому вместо этого мы должны придавать больший вес классу меньшинства. Классам меньшинств должен быть придан больший вес, чтобы предположить, что модель должна отдавать приоритет этим классам. Мы должны уменьшить известность классов большинства, присвоив им более низкие веса.

Устранение дисбаланса классов с помощью ресамплинга
Этого можно достичь, импортировав модуль ресамплинга из scikit-learn. sklearn.resample не добавляет больше точек данных в наборы данных. Яnstead, он выполняет случайную ресамплинг (с / без замены) вашего набора данных.

Такой подход к выравниванию не позволяет модели машинного обучения отдавать приоритет классу большинства в наборе данных:

# class imbalance method 3
def adjust_imbalance(X_train, y_train, class_col):
  X = pd.concat([X_train, y_train], axis=1)
  # separate the 2 classes. Here we divide majority and minority classes
  class0 = X[X[class_col] == 0]
  class1 = X[X[class_col] == 1]
  # Case 1 - bootstraps from the minority class
  if len(class1)<len(class0):
    resampled = resample(class1,
                              replace=True, # Upsampling with replacement
                              n_samples=len(class0), ## Number to match majority class
                              random_state=10) 
    resampled_data = pd.concat([resampled, class0]) ## # Combination of majority and upsampled minority class
  # Case 1 - resamples from the majority class
  else:
    resampled = resample(class1,
                              replace=False, ## false instead of True like above
                              n_samples=len(class0), 
                              random_state=10) 
    resampled_data = pd.concat([resampled, class0])
  return resampled_data
## Call the function
resampled_data = adjust_imbalance(X_train, y_train, class_col='churn')
X_train, X_test, y_train, y_test = prepare_model(resampled_data, class_col='churn', cols_to_exclude=['customer_id', 'phone_no', 'year'])
run_model(X_train, X_test, y_train, y_test)
              precision    recall  f1-score   support

         0.0       0.69      0.75      0.72       339
         1.0       0.74      0.68      0.71       353

    accuracy                           0.71       692
   macro avg       0.71      0.71      0.71       692
weighted avg       0.71      0.71      0.71       692

The area under the curve is: 0.71
Мы отмечаем улучшение результатов Формулы-1.

Борьба с дисбалансом классов с помощью SMOTE
SMOTE (Synthetic Minority Oversampling Technique) - это метод создания элементов для класса меньшинства на основе тех, которые существуют в настоящее время.

Он работает, выбирая точку случайным образом из класса меньшинства и вычисляя k-ближайших соседей для этой точки.

Синтетические точки — это точки, которые вставляются между указанной точкой и ее соседями. Алгоритм SMOTE реализуется в соответствии со следующими шагами:

Выберите входной вектор из класса меньшинства.
Найдите k ближайших соседей (k соседей — это входные данные метода SMOTE()).
Выберите одного из этих соседей и вставьте синтетическую точку где-нибудь на линии, соединяющей рассматриваемую точку и ее выбранного соседа.
Повторяйте процесс до тех пор, пока данные не будут сбалансированы.
def prepare_data_smote(data,class_col,cols_to_exclude):
  # Synthetic Minority Oversampling Technique. 
  # Generates new instances from existing minority cases that you supply as input. 
  cols = data.select_dtypes(include=np.number).columns.tolist() 
  X = data[cols]
  X = X[X.columns.difference([class_col])]
  X = X[X.columns.difference(cols_to_exclude)]
  y = data[class_col]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
  sm = SMOTE(random_state=0, sampling_strategy=1.0)
  # run SMOTE on training set only
  X_train, y_train = sm.fit_resample(X_train, y_train)
  return X_train, X_test, y_train, y_test
X_train, X_test, y_train, y_test = prepare_data_smote(data,class_col='churn', cols_to_exclude=['customer_id', 'phone_no', 'year'])
run_model(X_train, X_test, y_train, y_test)
              precision    recall  f1-score   support

         0.0       0.96      0.75      0.84       513
         1.0       0.26      0.71      0.38        63

    accuracy                           0.75       576
   macro avg       0.61      0.73      0.61       576
weighted avg       0.88      0.75      0.79       576

The area under the curve is: 0.73
Заключение
Несбалансированный набор данных не обязательно означает, что эти два класса непредсказуемы.

Хотя большинство алгоритмов предназначены для работы с равным распределением классов, повышающая выборка (например, SMOTE) не является единственным методом для решения проблемы дисбаланса классов. В случае логистической регрессии и многих других моделей машинного обучения веса классов могут быть изменены на ошибку весовой модели в соответствии с распределением классов.

Вы можете проверить записную книжку Colab здесь.