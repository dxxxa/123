# [How to Extract Chrome Cookies in Python](https://www.thepythoncode.com/article/extract-chrome-cookies-python)
To run this:
- `pip3 install -r requirements.txt`
- Simply run the script:
```
python chrome_cookie_extractor.py
```
##
# [[] / []]()
Как вы, возможно, уже знаете, браузер Chrome сохраняет много данных о просмотре локально на вашем компьютере. Несомненно, самым опасным является возможность извлекать пароли и расшифровывать пароли из Chrome. Кроме того, одним из интересных сохраненных данных являются файлы cookie. Однако большинство значений файлов cookie шифруются.

Из этого туториала Вы узнаете, как извлекать файлы cookie Chrome и расшифровывать их на вашем компьютере с Windows с помощью Python.

Связанные с: Как извлечь пароли Chrome в Python.

Чтобы начать работу, давайте установим необходимые библиотеки:

$ pip3 install pycryptodome pypiwin32
Откройте новый файл Python и импортируйте необходимые модули:

import os
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
import win32crypt # pip install pypiwin32
from Crypto.Cipher import AES # pip install pycryptodome
Ниже приведены две удобные функции, которые помогут нам позже для извлечения файлов cookie (взятых из учебника по извлечению паролей Chrome):

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove 'DPAPI' str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
Related: Build 24 Ethical Hacking Scripts & Tools with Python Book

get_chrome_datetime() function converts the datetimes of chrome format into a Python datetime format.

get_encryption_key() extracts and decodes the AES key that was used to encrypt the cookies, which is stored in "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Local State" file in JSON format.

def decrypt_data(data, key):
    try:
        # get the initialization vector
        iv = data[3:15]
        data = data[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""
The above function accepts the data and the AES key as parameters and uses the key to decrypt the data to return it.

Now that we have everything we need, let's dive into the main function:

def main():
    # local sqlite Chrome cookie database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    # copy the file to current directory
    # as the database will be locked if chrome is currently open
    filename = "Cookies.db"
    if not os.path.isfile(filename):
        # copy file when does not exist in the current directory
        shutil.copyfile(db_path, filename)
The file that contains the cookies data is located as defined in db_path variable, we need to copy it to the current directory, as the database will be locked when the Chrome browser is currently open.

Connecting to the SQLite database:

    # connect to the database
    db = sqlite3.connect(filename)
    # ignore decoding errors
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()
    # get the cookies from `cookies` table
    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
    FROM cookies""")
    # you can also search by domain, e.g thepythoncode.com
    # cursor.execute("""
    # SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value
    # FROM cookies
    # WHERE host_key like '%thepythoncode.com%'""")
After we connect to the database, we ignore decoding errors in case there are any, we then query the cookies table with cursor.execute() function to get all cookies stored in this file. You can also filter cookies by a domain name as shown in the commented code.

Now let's get the AES key and iterate over the rows of cookies table and decrypt all encrypted data:

    # get the AES key
    key = get_encryption_key()
    for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            # already decrypted
            decrypted_value = value
        print(f"""
        Host: {host_key}
        Cookie name: {name}
        Cookie value (decrypted): {decrypted_value}
        Creation datetime (UTC): {get_chrome_datetime(creation_utc)}
        Last access datetime (UTC): {get_chrome_datetime(last_access_utc)}
        Expires datetime (UTC): {get_chrome_datetime(expires_utc)}
        ===============================================================
        """)
        # update the cookies table with the decrypted value
        # and make session cookie persistent
        cursor.execute("""
        UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
        WHERE host_key = ?
        AND name = ?""", (decrypted_value, host_key, name))
    # commit changes
    db.commit()
    # close connection
    db.close()
Get: Build 24 Ethical Hacking Scripts & Tools with Python Book

We use our previously defined decrypt_data() function to decrypt encrypted_value column, we print the results and set the value column to the decrypted data. We also make the cookie persistent by setting is_persistent to 1 and also is_secure to 0 to indicate that it is not encrypted anymore.

Finally, let's call the main function:

if __name__ == "__main__":
    main()
Once you execute the script, it'll print all the cookies stored in your Chrome browser including the encrypted ones, here is a sample of the results:

        ===============================================================
        Host: www.example.com
        Cookie name: _fakecookiename
        Cookie value (decrypted): jLzIxkuEGJbygTHWAsNQRXUaieDFplZP
        Creation datetime (UTC): 2021-01-16 04:52:35.794367
        Last access datetime (UTC): 2021-03-21 10:05:41.312598
        Expires datetime (UTC): 2022-03-21 09:55:48.758558
        ===============================================================
...
Conclusion
Awesome, now you know how to extract your Chrome cookies and use them in Python.

Чтобы защитить себя от этого, мы можем просто удалить все файлы cookie в браузере Chrome или использовать команду DELETE в SQL в исходном файле cookie для удаления файлов cookie.

Другим альтернативным решением является использование режима инкогнито. В этом случае браузер Chrome не сохраняет историю просмотров, файлы cookie, данные сайта или любую информацию о пользователе.

Кроме того, вы также можете извлекать и расшифровывать пароли Chrome таким же образом, и в этом учебнике показано, как это сделать.

Однако стоит отметить: если вы хотите использовать свои файлы cookie в Python напрямую, не извлекая их, как мы сделали здесь, есть классная библиотека, которая поможет вам сделать это.