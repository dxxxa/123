# [How to Automate Login using Selenium in Python](https://www.thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Get [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) and put it in the current directory.
- Edit credentials in `automate_login.py` and run it!
##
# [[] / []]()
Управление веб-браузером из программы может быть полезно во многих сценариях, примерами использования являются автоматизация текста веб-сайта и веб-парсинг, очень популярная платформа для такого рода автоматизации - Selenium WebDriver.

Selenium WebDriver - это библиотека управления браузерами, которая поддерживает все основные браузеры (Firefox, Edge, Chrome, Safari, Opera и т. Д.) И доступна для различных языков программирования, включая Python. В этом уроке мы будем использовать его привязки Python для автоматизации входа на веб-сайты.

Автоматизация процесса входа на веб-сайт оказывается удобной. Например, может потребоваться автоматическое изменение настроек учетной записи или извлечение некоторой информации, требующей входа в систему, например извлечение адресов электронной почты. Вы можете использовать Python для извлечения ссылок, которые доступны только после входа в систему, загрузки изображений внутри вашей учетной записи и многих других вариантов использования.

У нас также есть учебник по извлечению веб-форм с помощью библиотеки BeautifulSoup, поэтому вы можете объединить извлечение форм входа и их заполнение с помощью этого учебника.

Во-первых, давайте установим Selenium для Python:

$ pip3 install selenium
Следующим шагом является установка драйвера, специфичного для браузера, которым мы хотим управлять. Ссылки для скачивания доступны на этой странице. Я устанавливаю ChromeDriver, но вы можете использовать свой любимый.

Чтобы сделать вещи конкретными, я буду использовать страницу входа на GitHub, чтобы продемонстрировать, как вы можете автоматически входить в систему с помощью Selenium.

Откройте новый скрипт Python и инициализируйте WebDriver:

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Github credentials
username = "username"
password = "password"

# initialize the Chrome driver
driver = webdriver.Chrome("chromedriver")
После того, как вы скачаете и распакуете драйвер для вашей ОС, поместите его в текущий каталог или в известный путь, чтобы вы могли передать его в webdriver. Класс Chrome(). В моем случае chromedriver.exe находится в текущем каталоге, поэтому я просто передаю его имя конструктору.

Поскольку мы заинтересованы в автоматизации входа в Github, мы перейдем на страницу входа в GitHub и проверим страницу, чтобы определить ее HTML-элементы:

HTML-элементы страницы входа на GithubПоля ввода логина и пароля, а также имя кнопки Вход будут полезны нам для извлечения этих элементов в код и вставки их программным путем.id

Обратите внимание, что поле ввода имени пользователя / адреса электронной почты имеет login_field идентификатор, где поле ввода пароля имеет идентификатор пароля, см. также кнопка отправки имеет имя фиксации, приведенный ниже код переходит на страницу входа в GitHub, извлекает эти элементы, заполняет учетные данные и нажимает кнопку:

# head to github login page
driver.get("https://github.com/login")
# find username/email field and send the username itself to the input field
driver.find_element("id", "login_field").send_keys(username)
# find password input field and insert password as well
driver.find_element("id", "password").send_keys(password)
# click login button
driver.find_element("name", "commit").click()
Мы используем функцию find_element() и передаем "id" первому параметру для извлечения HTML-элемента по его идентификатору, а метод send_keys() имитирует нажатия клавиш. Приведенная выше ячейка кода заставит Chrome ввести электронное письмо и пароль, а затем нажать кнопку Войти.

Следующее, что нужно сделать, это определить, был ли наш вход в систему успешным, есть много способов обнаружить это, но в этом уроке мы сделаем это, обнаружив показанные ошибки при входе в систему (конечно, это изменится с одного веб-сайта на другой).

Страница входа в систему с ошибкой GithubНа рисунке выше показано, что происходит, когда мы вставляем неправильные учетные данные. Вы увидите новый HTML-элемент с классом с текстом "Неправильное имя пользователя или пароль".div"flash-error"

Приведенный ниже код отвечает за ожидание загрузки страницы после входа в систему с помощью WebDriverWait() и проверяет наличие ошибки:

# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
# get the errors (if there are)
errors = driver.find_elements("css selector", ".flash-error")
# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")
Мы используем WebDriverWait, чтобы дождаться завершения загрузки документа, метод execute_script() выполняет Javascript в контексте браузера, JS-код возвращает document.readyState === 'complete' возвращает True при загрузке страницы и False в противном случае.

Чтобы подтвердить, что мы вошли в систему, давайте извлечем общедоступные репозитории GitHub нашего вошедшего в систему пользователя:

# an example scenario, show me my public repositories
repos = driver.find_element("css selector", ".js-repos-container")
# wait for the repos container to be loaded
WebDriverWait(driver=driver, timeout=10).until((lambda x: repos.text != "Loading..."))
# iterate over the repos and print their names
for repo in repos.find_elements("css selector", "li.public"): # you can use "li.private" for private repos
    print(repo.find_element("css selector", "a").get_attribute("href"))
Вот выходные данные:

[+] Login successful
https://github.com/x4nth055/pythoncode-tutorials
https://github.com/x4nth055/ethical-hacking-tools-python
https://github.com/x4nth055/emotion-recognition-using-speech
Наконец, мы закрываем наш драйвер:

# close the driver
driver.close()
Заключение
Хорошо, теперь у вас есть навык автоматического входа на веб-сайт по вашему выбору. Обратите внимание, что GitHub будет блокировать вас, когда вы запускаете сценарий несколько раз с неправильными учетными данными, поэтому имейте это в виду.

Теперь вы можете делать то, что хотите, после входа в систему с помощью учетной записи; вы можете добавить код, который вы хотите после входа в систему.

Кроме того, если вы успешно вошли в систему, используя свою реальную учетную запись, вы можете столкнуться с подтверждением по электронной почте, если у вас включена двухфакторная аутентификация. Чтобы обойти это, вы можете либо отключить его, либо прочитать свою электронную почту программно с помощью Python и извлечь код подтверждения и вставить его в режиме реального времени с помощью Selenium, большая проблема, не так ли? Удачи вам в этом!

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Проверьте полный код здесь.

Узнайте также: Как использовать API GitHub в Python.