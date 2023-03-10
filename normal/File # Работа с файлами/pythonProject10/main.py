import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

# Путь к web-driver
EXE_PATH = 'chromedriver.exe'
# Логин и пароль от вашей почты
EMAIL = "yershchipu@bk.ru"
PASSWORD = "qweqweqwe!qwe"

# запускаем браузер
browser = webdriver.Chrome(executable_path=EXE_PATH)
# Переходим на страницу шаблонов mail.ru
# Сайт выдаст форму авторизации
browser.get('https://e.mail.ru/templates/')

# Выставляем тайминги задержки чтобы браузер успел прогрузить страницу
time.sleep(5)

# Теперь нам надо авторизоваться
# заполняем поле логин
emailElem = browser.find_element_by_name('username')
emailElem.send_keys(EMAIL)
emailElem.submit()
time.sleep(1)

# заполняем поле пароль
passwordElem = browser.find_element_by_name('password')
passwordElem.send_keys(PASSWORD)
passwordElem.submit()
time.sleep(5)

# Мы авторизовались, теперь тащим адреса из файла.csv
# Содержание файла
# ФИО,Email

with open('email_list.csv', encoding="utf-8") as file:
    EMAIL_LIST = csv.reader(file)

    # Запускаем цикл
    for row in EMAIL_LIST:
        # Если mail что то заподозрит, то выкинет капчу,
        # мы получаем except, ждем некоторое время, и снова отправлем письмо
        try:
            # ФИО <Email>
            email_to = row[0] + "<" + row[1] + ">"

            # Нажимаем кнопку шаблоны (первый в списке шаблон настраиваем заранее)
            browser.find_element_by_xpath(
                '//*[@id="app-canvas"]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div[1]/div/div/div/div[1]/div/div/a[1]').click()
            time.sleep(3)

            # Заполняем поле кому
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div/label/div/div/input').send_keys(
                email_to)
            time.sleep(1)

            # Нажимаем кнопку отправить
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/span[1]/span/span').click()
            time.sleep(5)

            # После отправки открывается модальное окно, закрываем его
            browser.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div[2]/div/div/div[1]/span').click()
            time.sleep(10)

        except Exception:
            # Сообщаем пользователю, что скрипту необходимо переждать
            print('Error! Wait 1 hour\n')
            # Ждем час (можно меньше)
            time.sleep(3600)

            # Снова нажимаем кнопку отправить
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/span[1]/span/span').click()
            time.sleep(5)

            # Снова закрываем модальное окно
            browser.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div[2]/div/div/div[1]/span').click()
            time.sleep(10)

print('SUCCESS!')
time.sleep(500)