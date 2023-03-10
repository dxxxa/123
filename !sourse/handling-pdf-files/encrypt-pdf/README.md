# [How to Encrypt and Decrypt PDF Files in Python](https://www.thepythoncode.com/article/encrypt-pdf-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    $ python encrypt_pdf.py --help
    ```
    **Output:**
    ```
    usage: encrypt_pdf.py [-h] [-a {encrypt,decrypt}] [-l {1,2}] -p [PASSWORD] [-o OUTPUT_FILE] file

    These options are available

    positional arguments:
    file                  Input PDF file you want to encrypt

    optional arguments:
    -h, --help            show this help message and exit
    -a {encrypt,decrypt}, --action {encrypt,decrypt}
                            Choose whether to encrypt or to decrypt
    -l {1,2}, --level {1,2}
                            Choose which protection level to apply
    -p [PASSWORD], --password [PASSWORD]
                            Enter a valid password
    -o OUTPUT_FILE, --output_file OUTPUT_FILE
                            Enter a valid output file
    ```
- For instance, to encrypt `bert-paper.pdf` file and output as bert-paper-encrypted.pdf:
    ```
    $ python encrypt_pdf.py bert-paper.pdf -a encrypt -l 1 -p -o bert-paper-encrypted.pdf
    ```
- To decrypt it:
    ```
    $ python encrypt_pdf.py bert-paper-encrypted.pdf -a decrypt -l 1 -p -o bert-paper-decrypted.pdf
    ```
    This will spawn the original PDF file under the name `bert-paper-decrypted.pdf`. The password must be the same for encryption and decryption.
##
# [[] / []]()
Есть много целей, когда вы хотите зашифровать свой PDF-файл, одна из которых - помешать кому-то скопировать ваш PDF на свой компьютер и сделать его пригодным для использования только с помощью ключа расшифровки. С помощью зашифрованного PDF-файла можно запретить нежелательным лицам просматривать личные сведения или учетные данные в PDF-файле.

В этом учебнике вы узнаете, как шифровать PDF-файлы, применяя два уровня защиты:

Уровень 1: Ограничение доступа к PDF-файлу путем добавления пароля для открытия документа. Пароль открытия документа (также известный как пароль пользователя) требует, чтобы пользователь ввел пароль, чтобы открыть PDF-файл.
Уровень 2: Шифрование файла с помощью библиотеки pyAesCrypt и алгоритма шифрования AES256-CBC.
Целью этого учебника является разработка легкой утилиты на основе командной строки с помощью модулей на основе Python, не полагаясь на внешние утилиты за пределами экосистемы Python (например, qpdf) для защиты PDF-файлов на Python.

Прежде чем начать, давайте установим необходимые библиотеки:

$ pip install PyPDF4==1.27.0 pyAesCrypt==6.0.0
Давайте импортируем необходимые библиотеки в наш файл Python:

# Import Libraries
from PyPDF4 import PdfFileReader, PdfFileWriter, utils
import os
import argparse
import getpass
from io import BytesIO
import pyAesCrypt
Во-первых, давайте определим функцию, которая проверяет, зашифрован ли PDF-файл:

# Size of chunck
BUFFER_SIZE = 64*1024

def is_encrypted(input_file: str) -> bool:
    """Checks if the inputted file is encrypted using PyPDF4 library"""
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file, strict=False)
        return pdf_reader.isEncrypted
Во-вторых, давайте сделаем основную функцию, которая заключается в шифровании PDF-файла:

def encrypt_pdf(input_file: str, password: str):
    """
    Encrypts a file using PyPDF4 library.
    Precondition: File is not encrypted.
    """
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
    if pdf_reader.isEncrypted:
        print(f"PDF File {input_file} already encrypted")
        return False, None, None
    try:
        # To encrypt all the pages of the input file, you need to loop over all of them
        # and to add them to the writer.
        for page_number in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_number))
    except utils.PdfReadError as e:
        print(f"Error reading PDF File {input_file} = {e}")
        return False, None, None
    # The default is 128 bit encryption (if false then 40 bit encryption).
    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
    return True, pdf_reader, pdf_writer
Функция encrypt_pdf() выполняет следующие действия:

Он проверяет, что входной PDF-файл не зашифрован с помощью библиотеки PyPDF4.
Он выполняет итерацию по страницам и добавляет их в объект pdf_writer.
Шифрует объект pdf_writer с помощью заданного пароля.
Теперь, когда у нас есть функция, которая отвечает за шифрование, давайте сделаем обратное, это расшифровка:

def decrypt_pdf(input_file: str, password: str):
    """
    Decrypts a file using PyPDF4 library.
    Precondition: A file is already encrypted
    """
    pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
    if not pdf_reader.isEncrypted:
        print(f"PDF File {input_file} not encrypted")
        return False, None, None
    pdf_reader.decrypt(password=password)
    pdf_writer = PdfFileWriter()
    try:
        for page_number in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_number))
    except utils.PdfReadError as e:
        print(f"Error reading PDF File {input_file} = {e}")
        return False, None, None
    return True, pdf_reader, pdf_writer
Эта функция выполняет следующие функции:

Он проверяет, что входной PDF-файл зашифрован с помощью библиотеки PyPDF4.
Он расшифровывает pdf_reader объект с помощью пароля (должен быть правильным).
Он выполняет итерацию по страницам и добавляет их в объект pdf_writer.
Давайте перейдем к уровню 2, шифруя фактический файл:

def cipher_stream(inp_buffer: BytesIO, password: str):
    """Ciphers an input memory buffer and returns a ciphered output memory buffer"""
    # Initialize output ciphered binary stream
    out_buffer = BytesIO()
    inp_buffer.seek(0)
    # Encrypt Stream
    pyAesCrypt.encryptStream(inp_buffer, out_buffer, password, BUFFER_SIZE)
    out_buffer.seek(0)
    return out_buffer
Используя библиотеку pyAesCrypt, приведенная выше функция шифрует входной буфер памяти и возвращает зашифрованный буфер памяти в качестве выходных данных.

Давайте сделаем функцию расшифровки файла сейчас:

def decipher_file(input_file: str, output_file: str, password: str):
    """
    Deciphers an input file and returns a deciphered output file
    """
    inpFileSize = os.stat(input_file).st_size
    out_buffer = BytesIO()
    with open(input_file, mode='rb') as inp_buffer:
        try:
            # Decrypt Stream
            pyAesCrypt.decryptStream(
                inp_buffer, out_buffer, password, BUFFER_SIZE, inpFileSize)
        except Exception as e:
            print("Exception", str(e))
            return False
        inp_buffer.close()
    if out_buffer:
        with open(output_file, mode='wb') as f:
            f.write(out_buffer.getbuffer())
        f.close()
    return True
В decipher_file() мы используем метод decryptStream() из модуля pyAesCrypt, который принимает входной и выходной буфер, пароль, размер буфера и размер файла в качестве параметров и записывает расшифрованный поток в выходной буфер.

Для более удобного использования шифрования и расшифровки файлов я предлагаю вам прочитать этот учебник, в котором используется модуль криптографии, более удобный для разработчиков Python.

Теперь объединим наши функции в одну:

def encrypt_decrypt_file(**kwargs):
    """Encrypts or decrypts a file"""
    input_file = kwargs.get('input_file')
    password = kwargs.get('password')
    output_file = kwargs.get('output_file')
    action = kwargs.get('action')
    # Protection Level
    # Level 1 --> Encryption / Decryption using PyPDF4
    # Level 2 --> Encryption and Ciphering / Deciphering and Decryption
    level = kwargs.get('level')
    if not output_file:
        output_file = input_file
    if action == "encrypt":
        result, pdf_reader, pdf_writer = encrypt_pdf(
            input_file=input_file, password=password)
        # Encryption completed successfully
        if result:
            output_buffer = BytesIO()
            pdf_writer.write(output_buffer)
            pdf_reader.stream.close()
            if level == 2:
                output_buffer = cipher_stream(output_buffer, password=password)
            with open(output_file, mode='wb') as f:
                f.write(output_buffer.getbuffer())
            f.close()
    elif action == "decrypt":
        if level == 2:
            decipher_file(input_file=input_file,
                          output_file=output_file, password=password)
        result, pdf_reader, pdf_writer = decrypt_pdf(
            input_file=input_file, password=password)
        # Decryption completed successfully
        if result:
            output_buffer = BytesIO()
            pdf_writer.write(output_buffer)
            pdf_reader.stream.close()
            with open(output_file, mode='wb') as f:
                f.write(output_buffer.getbuffer())
            f.close()
Приведенная выше функция принимает 5 аргументов ключевых слов:

input_file: Входной PDF-файл.
output_file: Выходной PDF-файл.
password: строка пароля, с помощью которой требуется зашифровать.
action: принимает действия "encrypt" или "decrypt" в качестве строки.
level: Какой уровень шифрования вы хотите использовать. Установка значения 1 означает только добавление пароля во время открытия PDF-файла, 2 добавляет шифрование файла в качестве еще одного уровня безопасности.
Теперь давайте создадим новый класс, который наследует от argparse. Действие для безопасного ввода пароля:

class Password(argparse.Action):
    """
    Hides the password entry
    """
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)
Он переопределяет метод __call__() и задает для параметра dest переменной объекта пространства имен пароль, который пользователь вводит с помощью модуля getpass.

Далее определим функции для синтаксического анализа аргументов командной строки:

def is_valid_path(path):
    """Validates the path inputted and checks whether it is a file path or a folder path"""
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")

def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="These options are available")
    parser.add_argument("file", help="Input PDF file you want to encrypt", type=is_valid_path)
    # parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
    #                     required=True, help="Enter the path of the file or the folder to process")
    parser.add_argument('-a', '--action', dest='action', choices=[
                        'encrypt', 'decrypt'], type=str, default='encrypt', help="Choose whether to encrypt or to decrypt")
    parser.add_argument('-l', '--level', dest='level', choices=[
                        1, 2], type=int, default=1, help="Choose which protection level to apply")
    parser.add_argument('-p', '--password', dest='password', action=Password,
                        nargs='?', type=str, required=True, help="Enter a valid password")
    parser.add_argument('-o', '--output_file', dest='output_file',
                        type=str, help="Enter a valid output file")
    args = vars(parser.parse_args())
    # To Display Command Arguments Except Password
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j)
          for i, j in args.items() if i != 'password'))
    print("######################################################################")
    return args
Наконец, написание основного кода:

if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    # Encrypting or Decrypting File
    encrypt_decrypt_file(
        input_file=args['file'], password=args['password'], 
        action=args['action'], level=args['level'], output_file=args['output_file']
    )
Хорошо, давайте протестируем нашу программу. Во-первых, давайте пройдем --help, чтобы увидеть аргументы:

$ python encrypt_pdf.py --help
Выпуск:

usage: encrypt_pdf.py [-h] [-a {encrypt,decrypt}] [-l {1,2}] -p [PASSWORD] [-o OUTPUT_FILE] file

These options are available

positional arguments:
  file                  Input PDF file you want to encrypt

optional arguments:
  -h, --help            show this help message and exit
  -a {encrypt,decrypt}, --action {encrypt,decrypt}
                        Choose whether to encrypt or to decrypt
  -l {1,2}, --level {1,2}
                        Choose which protection level to apply
  -p [PASSWORD], --password [PASSWORD]
                        Enter a valid password
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Enter a valid output file
Потрясающе, давайте зашифруем пример PDF-файла (получите его здесь):

$ python encrypt_pdf.py bert-paper.pdf -a encrypt -l 1 -p -o bert-paper-encrypted1.pdf
При этом дважды будет предложено ввести пароль:

Password: 
Password:
## Command Arguments #################################################
file:bert-paper.pdf
action:encrypt
level:1
output_file:bert-paper-encrypted1.pdf
######################################################################
Новый PDF-файл, защищенный паролем, появится в текущем рабочем каталоге, если вы попытаетесь открыть его с помощью любой программы для чтения PDF, вам будет предложен пароль, как показано на рисунке ниже:

Пример зашифрованного PDF-файла с паролем с помощью Python

Очевидно, что если вы введете неправильный пароль, вы не сможете получить доступ к PDF-файлу.

Теперь давайте расшифруем его:

$ python encrypt_pdf.py bert-paper-encrypted1.pdf -a decrypt -p -l 1 -o bert-paper-decrypted1.pdf
Выпуск:

Password: 
## Command Arguments #################################################
file:bert-paper-encrypted1.pdf
action:decrypt
level:1
output_file:bert-paper-decrypted1.pdf
######################################################################
Удивительно, вы заметите, что bert-paper-decrypted1.pdf появляются в вашем каталоге, который эквивалентен оригиналу (не зашифрован).

Заключение
Обратите внимание, что если вы выберете уровень 2, весь файл будет зашифрован, и поэтому вам нужно расшифровать его дважды, сначала используя уровень 2, а затем уровень 1.

Вы должны знать, что блокировка PDF-файла путем добавления пароля открытия документа может быть обойдена с помощью различных методов, одним из которых является взлом пароля PDF, проверьте этот учебник, чтобы узнать, как это сделать.

Вы можете проверить полный код этого учебника здесь.

Вот некоторые связанные учебные пособия в формате PDF:

Как выделить и отредактировать текст в PDF-файлах с помощью Python.
Как извлечь изображения из PDF на Python.
Как извлечь все ссылки PDF на Python.
Как подписывать PDF-файлы на Python.
Как извлечь текст из изображений в PDF-файлах с помощью Python.
Как извлечь метаданные PDF в Python.
Как сжимать PDF-файлы на Python.
Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!