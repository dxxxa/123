# [How to Use Gmail API in Python](https://www.thepythoncode.com/article/use-gmail-api-in-python)
To use the scripts here:
- Create your credentials file in Google API dashboard and putting it in the current directory, follow [this tutorial](https://www.thepythoncode.com/article/use-gmail-api-in-python) for detailed information.
- `pip3 install -r requirements.txt`
- Change `our_email` variable in `common.py` to your gmail address.
- To send emails, use the `send_emails.py` script:
    ```
    python send_emails.py --help
    ```
    **Output:**
    ```
    usage: send_emails.py [-h] [-f FILES [FILES ...]] destination subject body

    Email Sender using Gmail API

    positional arguments:
    destination           The destination email address
    subject               The subject of the email
    body                  The body of the email

    optional arguments:
    -h, --help            show this help message and exit
    -f FILES [FILES ...], --files FILES [FILES ...]
                            email attachments
    ```
    For example, sending to example@domain.com:
    ```
    python send_emails.py example@domain.com "This is a subject" "Body of the email" --files file1.pdf file2.txt file3.img
    ```
- To read emails, use the `read_emails.py` script. Downloading & parsing emails for Python related emails:
    ```
    python read_emails.py "python"
    ```
    This will output basic information on all matched emails and creates a folder for each email along with attachments and HTML version of the emails.
- To mark emails as **read** or **unread**, consider using `mark_emails.py`:
    ```
    python mark_emails.py --help
    ```
    **Output**:
    ```
    usage: mark_emails.py [-h] [-r] [-u] query

    Marks a set of emails as read or unread

    positional arguments:
    query         a search query that selects emails to mark

    optional arguments:
    -h, --help    show this help message and exit
    -r, --read    Whether to mark the message as read
    -u, --unread  Whether to mark the message as unread
    ```
    Marking emails from **Google Alerts** as **Read**:
    ```
    python mark_emails.py "Google Alerts" --read
    ```
    Marking emails sent from example@domain.com as **Unread**:
    ```
    python mark_emails.py "example@domain.com" -u
    ```
- To delete emails, consider using `delete_emails.py` script, e.g: for deleting emails about Bitcoin:
    ```
    python delete_emails.py "bitcoin"
    ```
- If you want the full code, consider using `tutorial.ipynb` file.
- Or if you want a all-in-one script, `gmail_api.py` is here as well!
##
# [[] / []]()
Gmail на сегодняшний день является самым популярным почтовым сервисом. Частные лица и организации используют его. Многие из его функций улучшены с помощью ИИ, включая его безопасность (и обнаружение мошеннических электронных писем) и его предложения при написании электронных писем.

В предыдущих руководствах мы объяснили, как вы можете отправлять электронные письма и читать электронные письма с помощью Python. Если вы еще не читали их, я настоятельно рекомендую вам проверить их.

В то время как предыдущие учебники были посвящены непосредственному использованию протоколов IMAP / SMTP, в этом мы будем использовать API Google для отправки и чтения электронных писем; таким образом, мы можем использовать функции, специфичные для Google Mail, например; добавлять ярлыки к некоторым электронным письмам, помечать письма как непрочитанные / прочитанные и так далее.

В этом руководстве мы рассмотрим некоторые из основных функций API Gmail и напишем несколько скриптов Python, которые могут отправлять электронные письма, искать электронные письма, удалять и помечать их как прочитанные или непрочитанные. Они будут использоваться следующим образом:

$ python send_emails.py destination@gmail.com "Subject" "Message body" --files file1.txt file2.pdf file3.png
$ python read_emails.py "search query"
$ python delete_emails.py "search query"
$ python mark_emails.py --read "search query"
$ python mark_emails.py --unread "search query"
Вот оглавление:

Включение API Gmail
Отправка электронных писем
Поиск сообщений электронной почты
Чтение электронных писем
Пометка писем как прочитанных
Пометка писем как непрочитанных
Удаление электронных писем
Чтобы начать работу, давайте установим необходимые зависимости:

$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
Включение API Gmail
Чтобы использовать API Gmail, нам нужен токен для подключения к API Gmail. Мы можем получить его из панели инструментов Google API.

Сначала мы включаем API почты Google, переходим на панель инструментов и используем строку поиска для поиска API Gmail, нажимаем на него, а затем включаем:

Включение почтового API Google

Затем мы создаем идентификатор клиента OAuth 2.0, создав учетные данные (перейдя к кнопке Создать учетные данные):

Щелчок учетных данных

Щелкните Создать учетные данные, а затем выберите Идентификатор клиента OAuth в раскрывающемся меню:



Вы перейдете на эту страницу:

Создание учетных данныхВыберите Классическое приложение в качестве типа приложения и продолжите. Вы увидите окно, подобное этому:

Учетные данные OAuth

Продолжайте и нажмите СКАЧАТЬ JSON; он загрузит файл JSON с длинным именем. Переименуйте его в credentials.json и поместите в текущий каталог проекта.

Кроме того, если вы пропустили это окно, вы можете нажать на кнопку значка загрузки в правой части страницы:

Загрузка учетных данных


Заметка: Если вы впервые используете API Google, вам может потребоваться просто создать экран согласия OAuth и добавить свой адрес электронной почты в качестве тестирующего пользователя.

Теперь мы закончили с настройкой API, начнем с импорта необходимых модулей:

import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'your_gmail@gmail.com'
Очевидно, что вам нужно изменить our_email на ваш адрес. Убедитесь, что вы используете адрес электронной почты, с помощью которого вы создали аутентификацию API.

Прежде всего, давайте сделаем функцию, которая загружает credentials.json, выполняет аутентификацию с помощью API Gmail и возвращает объект сервиса, который можно будет использовать позже во всех наших предстоящих функциях:

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()
Вы должны увидеть это знакомо, если вы уже использовали Google API раньше, например Google Drive API; это в основном чтение credentials.json и сохранение его в файл token.pickle после аутентификации в Google в вашем браузере, мы сохраняем токен, поэтому при втором запуске кода мы не должны аутентифицироваться снова.

Это предложит вам в вашем браузере по умолчанию принять разрешения, необходимые для этого приложения. Если вы видите окно, указывающее, что приложение не проверено, вы можете просто перейти в «Дополнительно» и нажать «Перейти к Gmail API Python (небезопасный)»:

Это приложение не проверено

Отправка электронных писем
Во-первых, давайте начнем с функции, которая отправляет электронные письма; мы знаем, что электронные письма могут содержать вложения, поэтому мы определим функцию, которая добавляет вложение в сообщение. Сообщение является экземпляром MIMEMultipart (или MIMEText, если оно не содержит вложений):

# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
Во-вторых, мы пишем функцию, которая принимает некоторые параметры сообщения, строит и возвращает сообщение электронной почты:

def build_message(destination, obj, body, attachments=[]):
    if not attachments: # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
И, наконец, мы создаем функцию, которая принимает параметры сообщения и использует почтовый API Google для отправки сообщения, построенного с помощью build_message(), который мы ранее определили:

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body, attachments)
    ).execute()
Вот и все для отправки сообщений. Воспользуемся функцией для отправки примера письма:

# test send email
send_message(service, "destination@domain.com", "This is a subject", 
            "This is the body of the email", ["test.txt", "anyfile.png"])
Укажите свой адрес электронной почты в качестве адреса назначения и реальные пути к файлам, и вы увидите, что сообщение действительно отправлено!

Узнайте также: Как отправлять электронные письма на Python с помощью smtplib.

Поиск сообщений электронной почты
def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages
Нам пришлось извлекать сообщения страницу за страницей, потому что они разбиты на страницы. Эта функция будет возвращать идентификаторы электронных писем, которые соответствуют запросу. Мы будем использовать его для удаления, пометки как прочитанного, пометки как непрочитанного и функций поиска. Хорошей новостью является то, что вы можете использовать поисковые операторы Gmail, такие как от, до, тема, имя файла, до и после (для дат) и многие другие. Посетите эту страницу для получения дополнительной информации.

Чтение электронных писем
В этом разделе мы создадим код Python, который принимает поисковый запрос в качестве входных данных и считывает все соответствующие электронные письма; печать основной информации электронной почты (Кому, От адресов, Тема и Дата) и простых/текстовых частей.

Мы также создадим папку для каждого электронного письма на основе темы и загрузим текстовое / html-содержимое, а также любой файл, который вложен в электронное письмо и сохранит его в созданной папке.

Прежде чем мы углубимся в функцию, которая читает электронные письма с заданным поисковым запросом, мы определим две служебные функции, которые мы будем использовать:

# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
Функция get_size_format() будет просто печатать байты в хорошем формате (взятом из этого учебника), и нам понадобится функция clean(), чтобы создать имя папки, которое не содержит пробелов и специальных символов.

Далее определим функцию, которая анализирует содержимое раздела электронной почты:

def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:
                # attachment other than a plain text or HTML
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            # we get the attachment ID 
                            # and make another request to get the attachment itself
                            print("Saving the file:", filename, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                        .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))
Теперь давайте напишем нашу основную функцию для чтения электронной почты:

def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                folder_name = clean(value)
                # we will also handle emails with the same subject name
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    # we have the same folder name, add a number next to it
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("="*50)
Поскольку ранее определенная функция search_messages() возвращает список идентификаторов совпадающих писем, read_message() загружает содержимое электронного письма и делает то, что уже упоминалось выше.

Функция read_message() использует parse_parts() для разбора различных разделов электронной почты, если это текст/равнина, то мы просто декодируем его и печатаем на экране; если это text/html, то мы просто сохраняем его в той папке, которая создана с индексом имени.html, а если это файл (вложение), то загружаем вложение по его attachment_id и сохраняем его в созданной папке.

Кроме того, если два письма имеют одну и ту же тему, то нам нужно добавить простой счетчик к имени папки, и это то, что мы сделали с folder_counter.

Давайте используем это в действии:

# get emails that match the query you specify
results = search_messages(service, "Python Code")
print(f"Found {len(results)} results.")
# for each email matched, read it (output plain/text to console & save HTML and attachments)
for msg in results:
    read_message(service, msg)
Это загрузит и разберет все электронные письма, содержащие ключевое слово Python Code. Вот часть выходных данных:

Found 19 results.
==================================================
From: Python Code <email@domain.com>
To: "email@gmail.com" <email@gmail.com>
Subject: How to Play and Record Audio in Python
Date: Fri, 21 Feb 2020 09:24:58 +0000

Hello !

I have no doubt that you already encountered with an application that uses sound (either recording or playing) and you know how useful is that !
<...SNIPPED..>

Saving HTML to How_to_Play_and_Record_Audio_in_Python\index.html
==================================================
From: Python Code <email@domain.com>
To: "email@gmail.com" <email@gmail.com>
Subject: Brute-Forcing FTP Servers in Python
Date: Tue, 25 Feb 2020 21:31:09 +0000‌ ‌ ‌ ‌  ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌

Hello,
A brute-force attack consists of an attack that submits many passwords with the hope of guessing correctly.
<...SNIPPED...>

Saving HTML to Brute_Forcing_FTP_Servers_in_Python_1\index.html
==================================================
<...SNIPPED...>
Вы также увидите папки, созданные в текущем каталоге для каждого соответствующего электронного письма:

Проанализированные электронные письма

Внутри каждой папки находится соответствующая HTML-версия электронного письма и любые вложения, если таковые имеются.

Расширенные фильтры можно использовать в функции search_messages(). Например, если вы хотите получать электронные письма, содержащие вложение PDF, вы можете использовать search_messages (сервис, «имя файла: pdf»). Опять же, проверьте эту страницу для расширенной фильтрации.

Связанные с: Как читать электронные письма в Python с помощью imaplib.

Пометка писем как прочитанных
def mark_as_read(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_mark ],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()
Мы используем этот метод и устанавливаем значение в параметре body, чтобы удалить непрочитанную метку из соответствующих писем. batchModify()removeLabelIds["UNREAD"]

Например, давайте пометим все электронные письма Google следующим образом:

mark_as_read(service, "Google")
Пометка писем как непрочитанных
Пометка сообщений как непрочитанных может быть выполнена аналогичным образом, на этот раз путем добавления метки ["UNREAD"]:

def mark_as_unread(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    # add the label UNREAD to each of the search results
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'addLabelIds': ['UNREAD']
        }
    ).execute()
Пример запуска:

# make unread emails from email@domain.com
mark_as_unread(service, "from: email@domain.com")
Удаление электронных писем
Теперь для функции удаления сообщений:

def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()
На этот раз мы используем метод batchDelete() для удаления всех совпадающих писем, давайте, например, удалим все электронные письма Google Alerts:

delete_messages(service, "Google Alerts")
Связанные с: Как удалить электронные письма в Python с помощью imaplib.

Заключение
Запросы Gmail поддерживают фильтры, которые можно использовать для выбора определенных сообщений. Некоторые из этих фильтров показаны ниже, и это диалоговое окно, которое отображается при поиске электронных писем; мы можем заполнить его и получить соответствующий поисковый запрос:

Поисковые запросы Gmail

Gmail не только предлагает отличный и дружественный пользовательский интерфейс со многими функциями для требовательных пользователей, но также предлагает мощный API для разработчиков для использования и взаимодействия с Gmail. Мы пришли к выводу, что манипулировать электронными письмами из почты Google программно очень просто.

Если вы хотите узнать больше об API, я рекомендую вам проверить официальную страницу API Gmail.