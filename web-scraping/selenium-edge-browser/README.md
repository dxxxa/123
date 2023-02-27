# [Automated Browser Testing with Edge and Selenium in Python](https://www.thepythoncode.com/article/automated-browser-testing-with-edge-and-selenium-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Run `main1.py` or `main2.py`
##
# [[] / []]()
По состоянию на сентябрь 2020 года Microsoft Edge занимает 8,84% рынка браузеров и занимает вторую позицию после Chrome. Но все же, при выполнении кросс-браузерного тестирования, наше основное внимание, как правило, вращается вокруг браузеров, таких как Chrome, Firefox или Safari. Но как насчет других браузеров, таких как Edge?

При тестировании веб-сайта очень важно, чтобы он отображался плавно и точно во всех браузерах, устройствах и машинах. Предположим, вы создали веб-сайт и протестировали его в браузерах, таких как Chrome, Firefox и Safari, вручную, и решили развернуть его. Но что, если пользователи открывают веб-сайт в Microsoft Edge или в версии браузеров, отличных от протестированных?

Поэтому очень важно выполнить автоматическое тестирование браузера, протестировать ваш сайт в нескольких комбинациях версий браузера, чтобы обеспечить эффективный пользовательский опыт с помощью Selenium. В этом уроке мы подробно рассмотрим, как выполнять автоматизированное тестирование браузера с помощью Edge и Selenium в Python. Мы будем использовать Edge WebDriver, чтобы помочь нам запустить наши сценарии автоматизации тестирования Selenium через браузер Edge.

Скачать Selenium Edge WebDriver
При выполнении автоматического тестирования браузера важно, чтобы тестовые скрипты взаимодействовали с браузером. Без WebDriver это может быть невозможно. Selenium Edge WebDriver работает как посредник между вашим кодом и браузером, что помогает обеспечить программируемое дистанционное управление браузером.

Вы можете скачать последнюю версию Selenium Edge WebDriver по этой ссылке.

Выполнение автоматизации браузера с помощью Edge и Selenium в Python
Давайте посмотрим, каковы предпосылки для использования Edge с Selenium и Python для автоматизации браузера:

Загрузите последнюю версию Python, если она еще не установлена, отсюда.
Далее нам нужен браузер Microsoft Edge. Вы можете использовать эту ссылку, чтобы скачать его. Обратите внимание на версию, которую вы загружаете, для целей WebDriver. Если у вас уже установлен Edge, вы можете узнать его версию, введя следующую команду в адресной строке Edge:
edge://version/
Вы также можете узнать версию браузера Edge, выполнив следующие действия:
Откройте браузер Microsoft Edge.
Выберите Настройки и многое другое в правом верхнем углу браузера и перейдите в Настройки.
В нижней части вкладки параметров отображается раздел О Программе Microsoft Edge, содержащий сведения о версии Edge.
Теперь, когда базовая установка готова, давайте перейдем к следующим шагам, чтобы загрузить и установить следующее:

Selenium framework для Python - Выполните следующую команду в терминале, после того, как вы уже установили язык Python, чтобы установить последнюю версию Selenium framework для языка Python:
pip3 install selenium
Edge WebDriver for Selenium — загрузите исполняемый файл Edge WebDriver по этой ссылке, который соответствует конфигурации вашей системы. Обязательно загрузите версию драйвера, основанную на версии Edge, установленной в вашей системе. Распакуйте файл и скопируйте расположение msedgedriver.exe.
Средства Selenium для Microsoft Edge — выполните следующую команду из терминала, чтобы загрузить инструменты Selenium для Microsoft Edge напрямую:
pip install msedge-selenium-tools selenium==3.141
Мы все готовы. Теперь мы можем выполнять автоматизированное тестирование с помощью Edge и Selenium в Python. Рассмотрим несколько примеров.

Запуск первого сценария автоматического тестирования браузера
В этом примере мы увидим, как написать первый скрипт, который инициирует автоматическое тестирование браузера с помощью Edge и Selenium:

# importing required package of webdriver
from selenium import webdriver
# Just Run this to execute the below script
if __name__ == '__main__':
   # Instantiate the webdriver with the executable location of MS Edge web driver
   browser = webdriver.Edge(r"C:\Users\LenovoE14\Downloads\edgedriver\msedgedriver.exe")
   # Simply just open a new Edge browser and go to lambdatest.com
   browser.get('https://www.lambdatest.com')
В этом приведенном выше коде мы просто создаем экземпляр WebDriver для Microsoft Edge, передавая путь к исполняемому edge WebDriver в качестве параметра. В данном случае это C:\Users\LenovoE14\Downloads\edgedriver\msedgedriver.exe. Затем мы открываем новый экземпляр Edge с предоставленным URL-адресом. Вы можете настроить URL-адрес в соответствии с вашим выбором.

Выполните приведенный выше код, и вы увидите экземпляр Microsoft Edge, начинающий работу с 'https://www.lambdatest.com' в адресной строке (потому что мы предоставили этот адрес экземпляру webdriver и попросили браузер открыть его):

Первый выполненный скрипт

Performing Browser Automation Using Web Locators
Let us now look at another example, to perform some specific actions, with the help of web locators. In this example, we will try to insert the email address at the home page of www.lambdatest.com and click on the button Start Free Testing, as shown in the below image:

Начать бесплатное тестированиеСкопируйте и вставьте приведенный ниже код в среду IDE/текстовый редактор и запустите его:

# importing required package of webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    # Instantiate the webdriver with the executable location of MS Edge
    browser = webdriver.Edge(r"C:\Users\LenovoE14\Downloads\edgedriver\msedgedriver.exe")
    # Simply just open a new Edge browser and go to lambdatest.com
    browser.maximize_window()
    browser.get('https://www.lambdatest.com')
    try:
        # Get the text box to insert Email using selector ID
        myElem_1 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'useremail')))
        # Entering the email address
        myElem_1.send_keys("rishabhps@lambdatest.com")
        myElem_1.click()
        # Get the Submit button to click and start free testing using selector CSS_SELECTOR
        myElem_2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#testing_form > div")))
        # Starting free testing on LambdaTest
        myElem_2.click()
        sleep(10)
    except TimeoutException:
        print("No element found")
    sleep(10)
    browser.close()
В приведенном выше коде мы вставили адрес электронной почты в текстовое поле, показанное выше, и нажали кнопку Начать бесплатное тестирование. Для этого мы использовали идентификатор селекторов и CSS SELECTOR. После выполнения откроется новый экземпляр Microsoft Edge и выполнит следующие действия в заданном порядке:

Будет запущен новый экземпляр Microsoft Edge:

Экземпляр Microsoft Edge, запущенный с помощью SeleniumБраузер будет максимизирован (по мере выполнения browser.maximize_window()):

Браузер развернут

Откроется домашняя страница LambdaText:

Открыта домашняя страница

Данное письмо будет вставлено в текстовое поле и кнопка Начать бесплатное тестирование будет нажата:

Вставленный адрес электронной почты

Вы будете перенаправлены на страницу входа в систему, чтобы настроить свою учетную запись и начать кросс-браузерное тестирование с помощью LambdaText:

Перенаправлено на страницу входаЗаключение
В этой статье мы успешно увидели:

Что такое Edge WebDriver и как его получить.
Как настроить автоматическое тестирование браузера с помощью Edge и Selenium в Python.
Написание первого автоматизированного теста браузера.
Использование селекторов для автоматизации браузера с помощью Edge и Selenium в Python.
Популярность Microsoft Edge постоянно растет. Мы выполнили автоматизацию браузера с помощью установленной версии. Но что, если нам нужно выполнить это в какой-то другой версии или какой-то другой версии ОС Windows?

В таком случае загрузка и тестирование каждой версии может оказаться невозможным, что приведет к определенным недостаткам или некоторым проблемам с пользовательским интерфейсом позже. Чтобы преодолеть это, мы можем использовать LambdaTest для кросс-браузерного тестирования. LambdaTest не только позволит вам протестировать ваш сайт в нескольких браузерах и комбинациях операционных систем, но и позволит вам выполнять параллельное тестирование, а также в облаке Selenium Grid.

LambdaTest предоставляет платформу для проведения интерактивного тестирования совместимости браузеров в реальном времени ваших общедоступных или локально размещенных веб-сайтов и веб-приложений в более чем 2000 реальных мобильных и настольных браузерах, работающих на реальных операционных системах.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!