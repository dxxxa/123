# [How to Delete Emails in Python](https://www.thepythoncode.com/article/deleting-emails-in-python)
To run this:
- Change `username` and `password` for real email credentials, edit the `imap.search()` line for your use case and run `delete_emails.py`:
    ```
    python delete_emails.py
    ```
##
# [[] / []]()
Вы когда-нибудь хотели удалить электронные письма в своем почтовом ящике, но вы знаете, что это займет много времени и усилий, чтобы сделать это вручную?

В этом уроке вы не только узнаете, как автоматически удалять электронные письма с помощью Python, но также узнаете, как фильтровать электронные письма по дате, теме, отправителю и т. Д., Чтобы удалить их за один снимок.

Мы будем использовать встроенный в Python модуль imaplib, но если вы хотите использовать какой-то API, у нас есть учебник о том, как использовать Api Gmail, где мы показываем, как читать, отправлять и удалять электронные письма на Python.

imaplib реализует протокол IMAP в Python, IMAP - это стандартный интернет-протокол, используемый почтовыми клиентами для извлечения, а также удаления сообщений электронной почты с почтового сервера.

Начнем с импорта необходимых модулей и указания учетных данных нашей учетной записи:

import imaplib
import email
from email.header import decode_header

# account credentials
username = "youremailaddress@provider.com"
password = "yourpassword"
Конечно, вы должны указать учетные данные своей учетной записи. Приведенный ниже код отвечает за подключение к IMAP-серверу почтового провайдера:

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)
Для демонстрации этого учебника я использую демо-аккаунт Gmail, поэтому я указываю imap.gmail.com сервере. Для других поставщиков проверьте эту ссылку, содержащую список серверов IMAP для наиболее часто используемых поставщиков услуг электронной почты.

Кроме того, если вы используете учетную запись Gmail и приведенный выше код вызывает ошибку, указывающую на то, что учетные данные неправильные, убедитесь, что вы разрешаете менее безопасные приложения в настройках своей учетной записи.

Теперь, когда мы вошли в нашу учетную запись электронной почты, давайте выберем наш целевой почтовый ящик:

# select the mailbox I want to delete in
# if you want SPAM, use imap.select("SPAM") instead
imap.select("INBOX")
Итак, мы используем выбор почтового ящика с помощью метода imap.select(), я выбрал папку INBOX для этого учебника, вы можете распечатать imap.list() для доступных почтовых ящиков в вашей учетной записи.

Теперь давайте сделаем поиск IMAP для поиска писем, которые мы хотим удалить:

# search for specific mails by sender
status, messages = imap.search(None, 'FROM "googlealerts-noreply@google.com"')
Приведенная выше строка ищет электронные письма, которые были отправлены из электронной почты Google Alerts, другим примером может быть поиск по ТЕМЕ:

# to get mails by subject
status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')
Или поиск по дате:

# to get mails after a specific date
status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
# to get mails before a specific date
status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')
Или если вы хотите удалить все электронные письма:

# to get all mails
status, messages = imap.search(None, "ALL")
Я дал вам много вариантов, вы должны выбрать только одну строку поиска в зависимости от вашего варианта использования. Список критериев поиска IMAP можно найти по этой ссылке.

Статус содержит строку, успешно ли выполнен поиск, сообщения возвращаются в виде списка однобайтовой строки почтовых идентификаторов, разделенных пробелом, преобразуем ее в список целых чисел:

# convert messages to a list of email IDs
messages = messages[0].split(b' ')
Теперь давайте переберем целевые письма и пометим их как удаленные:

for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    # you can delete the for loop for performance if you have a long list of emails
    # because it is only for printing the SUBJECT of target email to delete
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes type, decode to str
                subject = subject.decode()
            print("Deleting", subject)
    # mark the mail as deleted
    imap.store(mail, "+FLAGS", "\\Deleted")
Как сказано в комментариях выше, вы можете удалить внутреннюю часть для цикла, если вы хотите производительности, я взял его из учебника по чтению электронных писем, он там только для печати ТЕМЫ электронного письма, поэтому мы знаем, что мы удаляем.

Наконец, мы выполняем метод imap.expunge(), который навсегда удаляет письма, помеченные как удаленные, мы также закрываем почтовый ящик и выходим из учетной записи:

# permanently remove mails that are marked as deleted
# from the selected mailbox (in this case, INBOX)
imap.expunge()
# close the mailbox
imap.close()
# logout from the account
imap.logout()
Потрясающе, код завершен, для тестирования этого кода я собираюсь удалить все электронные письма, пришедшие из электронной почты Google Alerts:

Электронные письма для удаленияИ действительно, после того, как я запустил сценарий, я получил такой вывод:

Deleting Alerte Google – Bitcoin
Deleting Alerte Google – Bitcoin
Deleting Alerte Google – Bitcoin
...<SNIPPED>...
Deleting Alerte Google – Bitcoin
Для этой демонстрации все электронные письма имеют один и тот же заголовок, так как я отфильтровал его по электронной почте отправителя, но если вы запустите разные критерии поиска, вы, конечно, увидите разные выходные данные.

Заключение
Отлично, теперь у вас есть навыки автоматического удаления писем с помощью модуля imaplib в Python.

Я предлагаю вам создать новую учетную запись электронной почты и протестировать этот код на ней, так как вы можете сделать необратимые ошибки на своих основных учетных записях электронной почты.

Проверьте полный код здесь.

Вот другие учебники по электронной почте Python:

Как отправлять электронные письма на Python.
Как читать электронные письма на Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!

Счастливое кодирование ♥