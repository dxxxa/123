# [How to Encrypt and Decrypt Files in Python](https://www.thepythoncode.com/article/encrypt-decrypt-files-symmetric-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python crypt --help
    ```
    **Output:**
    ```
    usage: crypt.py [-h] [-g] [-e] [-d] file

    Simple File Encryptor Script

    positional arguments:
    file                File to encrypt/decrypt

    optional arguments:
    -h, --help          show this help message and exit
    -g, --generate-key  Whether to generate a new key or use existing
    -e, --encrypt       Whether to encrypt the file, only -e or -d can be
                        specified.
    -d, --decrypt       Whether to decrypt the file, only -e or -d can be
                        specified.
    ```
- If you want to encrypt `data.csv` using a new generated key:
    ```
    python crypt.py data.csv --generate-key --encrypt
    ```
- To decrypt it (must be same key, using `--generate-key` flag with decrypt won't be able to get the original file):
    ```
    python crypt.py data.csv --decrypt
    ```
- To encrypt another file using the same key generated previously:
    ```
    python crypt.py another_file --encrypt
    ```
##
# [[] / []]()
Шифрование — это процесс кодирования части информации таким образом, чтобы только уполномоченные стороны могли получить к ней доступ. Это критически важно, потому что это позволяет безопасно защитить данные, которые вы не хотите, чтобы кто-то видел или получал доступ.

В этом учебнике вы узнаете, как использовать Python для шифрования файлов или любого байтового объекта (также строковых объектов) с помощью библиотеки криптографии.

Мы будем использовать симметричное шифрование, что означает, что тот же ключ, который мы использовали для шифрования данных, также может использоваться для расшифровки. Существует множество алгоритмов шифрования. Библиотека, которую мы будем использовать, построена поверх алгоритма AES.

В реальном мире существует множество применений шифрования. На самом деле, если вы читаете это, то ваш браузер надежно подключен к этому веб-сайту (т. Е. Шифрование). Тем не менее, существуют вредоносные способы использования шифрования, такие как создание программ-вымогателей; у нас есть учебник о том, как построить такой инструмент. Проверьте это здесь.

Примечание: Важно понимать разницу между алгоритмами шифрования и хэширования. В шифровании вы можете получить исходные данные, как только у вас есть ключ, в то время как функции хэширования вы не можете; вот почему они называются односторонним шифрованием.

Содержание:

Генерация ключа
Шифрование текста
Шифрование файлов
Шифрование файлов паролем
СВЯЗАННЫЕ С: Как извлечь и расшифровать файлы cookie Chrome в Python.

Начнем с установки криптографии:

pip3 install cryptography
Откройте новый файл Python, и давайте начнем:

from cryptography.fernet import Fernet
Генерация ключа
Fernet является реализацией симметричной аутентифицированной криптографии; Давайте начнем с создания этого ключа и записи его в файл:

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
Функция Fernet.generate_key() генерирует свежий ключ fernet, вам действительно нужно хранить его в безопасном месте. Если вы потеряете ключ, вы больше не сможете расшифровать данные, которые были зашифрованы с помощью этого ключа.

Поскольку этот ключ уникален, мы не будем генерировать ключ каждый раз, когда мы что-либо шифруем, поэтому нам нужна функция для загрузки этого ключа для нас:

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()
Шифрование текста
Теперь, когда мы знаем, как генерировать, сохранять и загружать ключ, давайте начнем с шифрования строковых объектов, просто чтобы вы сначала ознакомились с ним.

Генерация и запись ключа в файл:

# generate and write a new key
write_key()
Давайте загрузим этот ключ:

# load the previously generated key
key = load_key()
Некоторые сообщения:

message = "some secret message".encode()
Поскольку строки имеют тип str в Python, нам нужно закодировать их и преобразовать в байты, чтобы они были пригодны для шифрования, метод encode() кодирует эту строку с помощью кодека utf-8. Инициализация класса Fernet с помощью этого ключа:

# initialize the Fernet class
f = Fernet(key)
Шифрование сообщения:

# encrypt the message
encrypted = f.encrypt(message)
Метод f.encrypt() шифрует передаваемые данные. Результат этого шифрования известен как «токен Fernet» и имеет сильные гарантии конфиденциальности и подлинности.

Давайте посмотрим, как это выглядит:

# print how it looks
print(encrypted)
Выпуск:

b'gAAAAABdjSdoqn4kx6XMw_fMx5YT2eaeBBCEue3N2FWHhlXjD6JXJyeELfPrKf0cqGaYkcY6Q0bS22ppTBsNTNw2fU5HVg-c-0o-KVqcYxqWAIG-LVVI_1U='
Расшифровка того, что:

decrypted_encrypted = f.decrypt(encrypted)
print(decrypted_encrypted)
b'some secret message'
Это действительно то же самое сообщение.

Метод f.decrypt() расшифровывает маркер Fernet. Это вернет исходный открытый текст в результате, когда он будет успешно расшифрован, в противном случае возникнет исключение.

Узнайте также: Как шифровать и расшифровывать PDF-файлы на Python.

Шифрование файлов
Теперь вы знаете, как в основном шифровать строки, давайте углубимся в шифрование файлов; нам нужна функция для шифрования файла с заданным именем файла и ключом:

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
После инициализации объекта Fernet заданным ключом давайте сначала прочитаем целевой файл:

    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
file_data содержит данные файла, шифруя его:

    # encrypt data
    encrypted_data = f.encrypt(file_data)
Запишите зашифрованный файл с тем же именем, чтобы он переопределил оригинал (пока не используйте это для конфиденциальной информации, просто протестируйте некоторые ненужные данные):

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
Хорошо, это сделано. Перейдя к функции расшифровки сейчас, это тот же процесс, за исключением того, что мы будем использовать функцию decrypt() вместо encrypt() для объекта Fernet:

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
Давайте проверим это. У меня есть файл data.csv и ключ в текущем каталоге, как показано на следующем рисунке:

Файл для шифрования

Это полностью читаемый файл. Чтобы зашифровать его, все, что нам нужно сделать, это вызвать функцию, которую мы только что написали:

# uncomment this if it's the first time you run the code, to generate the key
# write_key()
# load the key
key = load_key()
# file name
file = "data.csv"
# encrypt it
encrypt(file, key)
Как только вы выполните это, вы можете увидеть, что файл увеличен в размере, и он нечитаем; вы даже не можете прочитать ни одного слова!

Чтобы вернуть файл в исходную форму, просто вызовите функцию decrypt():

# decrypt the file
decrypt(file, key)
Ну вот! Вы увидите, что исходный файл появится вместо зашифрованного ранее.

Получите: Этический взлом с помощью электронной книги Python

Шифрование файлов паролем
Вместо того, чтобы случайным образом генерировать ключ, что, если мы можем сгенерировать ключ из пароля? Ну, чтобы иметь возможность сделать это, мы можем использовать алгоритмы, которые предназначены для этой цели.

Одним из таких алгоритмов является Scrypt. Это функция вывода ключа на основе пароля, которая была создана в 2009 году Колином Персивалем, мы будем использовать ее для генерации ключей из пароля.

Если вы хотите следить за этим, создайте новый файл Python и импортируйте следующее:

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64
import getpass
Во-первых, функции вывода ключей нуждаются в случайных битах, добавленных к паролю перед его хэшированием; эти биты называются солью, что помогает укрепить безопасность и защитить от словарных и переборных атак. Сделаем функцию для генерации этого с помощью модуля secrets:

def generate_salt(size=16):
    """Generate the salt used for key derivation, 
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)
У нас есть учебник по генерации случайных данных. Обязательно проверьте его, если вы не уверены в вышеуказанной ячейке.

Далее сделаем функцию для получения ключа из пароля и соли:

def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())
Инициализируем алгоритм Scrypt, передавая:

Соль.
Желаемая длина ключа (32 в данном случае).
n: Параметр стоимости ЦП/Памяти, должен быть больше 1 и иметь мощность 2.
r: Параметр размера блока.
p: Параметр распараллеливания.
Как упоминалось в документации, n, r и p могут регулировать стоимость вычислений и памяти алгоритма Scrypt. RFC 7914 рекомендует значения r=8, p=1, где оригинальная статья Scrypt предполагает, что n должно иметь минимальное значение 2**14 для интерактивных входов или 2**20 для более чувствительных файлов; Вы можете проверить документацию для получения дополнительной информации.

Далее делаем функцию загрузки ранее сгенерированной соли:

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()
Теперь, когда у нас есть функции генерации соли и вывода ключей, давайте создадим основную функцию, которая генерирует ключ из пароля:

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """
    Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt"
    """
    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)
Приведенная выше функция принимает следующие аргументы:

password: строка пароля, из которой создается ключ.
salt_size: целое число, указывающее размер генерируемой соли.
load_existing_salt: логическое значение, указывающее, загружаем ли мы ранее сгенерированную соль.
save_salt: Булев, указывающий, сохраняем ли мы сгенерированную соль.
После загрузки или генерации новой соли мы получаем ключ из пароля с помощью нашей функции derive_key() и, наконец, возвращаем ключ в виде текста в кодировке Base64.

Теперь мы можем использовать ту же функцию encrypt(), которую мы определили ранее:

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
Для функции decrypt() мы добавляем простой блок try-except для обработки исключения, когда пароль неправильный:

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("File decrypted successfully")
Замечательно! Давайте используем argparse, чтобы мы могли передавать аргументы из командной строки:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("-s", "--salt-size", help="If this is set, a new salt with the passed size is generated",
                        type=int)
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file, only -e or -d can be specified.")

    args = parser.parse_args()
    file = args.file

    if args.encrypt:
        password = getpass.getpass("Enter the password for encryption: ")
    elif args.decrypt:
        password = getpass.getpass("Enter the password you used for encryption: ")

    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
Давайте протестируем наш скрипт, зашифровав данные.csv как и ранее:

$ python crypt_password.py data.csv --encrypt --salt-size 16
Enter the password for encryption:
Вам будет предложено ввести пароль, get_pass() скрывает введенные символы, поэтому он более безопасен. Вы также заметите, что сгенерирован файл salt.salt.

Если вы откроете файл целевых данных.csv, вы увидите, что он зашифрован. Теперь попробуем расшифровать его неправильным паролем:

$ python crypt_password.py data.csv --decrypt           
Enter the password you used for encryption: 
Invalid token, most likely the password is incorrect
Данные.csv остаются как есть. Давайте передадим правильный пароль, который использовался при шифровании:

$ python crypt_password.py data.csv --decrypt 
Enter the password you used for encryption: 
File decrypted successfully
Удивительный! Вы увидите, что данные.csv возвращены в исходном виде.

Обратите внимание, что если вы генерируете другую соль (передавая -s или --salt-size) во время расшифровки, даже если это правильный пароль, вы не сможете восстановить файл, так как будет сгенерирована новая соль, которая переопределяет предыдущую, поэтому убедитесь, что при расшифровке не проходите -s или --salt-size.

Заключение
Проверьте официальную документацию криптографии для получения дополнительной информации и инструкций.

Обратите внимание, что вам нужно остерегаться больших файлов, так как файл должен быть полностью в памяти, чтобы быть пригодным для шифрования. Вам нужно рассмотреть возможность использования некоторых методов разделения данных или сжатия файлов для больших файлов!