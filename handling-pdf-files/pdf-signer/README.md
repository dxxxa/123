# [How to Sign PDF Files in Python](https://www.thepythoncode.com/article/sign-pdf-files-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Refer to [the tutorial](https://www.thepythoncode.com/article/sign-pdf-files-in-python) on how to run the script.
##
# [[] / []]()
Цифровая подпись, добавленная в PDF-документ, эквивалентна чернильной подписи на бумажном документе, однако первая гораздо более безопасна.

Цифровая подпись гарантирует целостность PDF-документа и удостоверяет, что этот документ не был изменен неизвестным лицом. Он может заменить вашу рукописную подпись, чтобы ускорить практически любой бумажный процесс ручной подписи и ускорить рабочие процессы.

В этом уроке вы узнаете:

Как создать самозаверяющий сертификат в Python.
Как добавить цифровую подпись в PDF-документ на Python.
Необходимы следующие компоненты:

PDFNetPython3: это оболочка для PDFTron SDK. С помощью компонентов PDFTron вы можете создавать надежные и быстрые приложения, которые могут просматривать, создавать, печатать, редактировать и комментировать PDF-файлы в различных операционных системах. Разработчики используют PDFTron SDK для чтения, записи и редактирования PDF-документов, совместимых со всеми опубликованными версиями спецификаций PDF (включая последнюю версию ISO32000). PDFTron не является бесплатным, он предлагает 2 типа лицензий в зависимости от того, разрабатываете ли вы внешний / коммерческий продукт или собственное решение. Для целей этого учебника мы будем использовать бесплатную пробную версию этого SDK.
pyOpenSSL: оболочка Python вокруг библиотеки OpenSSL. OpenSSL - это популярная библиотека безопасности, используемая многими продуктами, приложениями и поставщиками.
Целью этого учебника является разработка легкой утилиты на основе командной строки с помощью модулей на основе Python для цифровой подписи одного или коллекции PDF-файлов, расположенных по определенному пути.

Связанные с: Как добавить водяные знаки PDF-файлам в Python.

Чтобы начать работу, давайте установим библиотеки:

$ pip install PDFNetPython3==8.1.0 pyOpenSSL==20.0.1
В итоге структура наших папок будет выглядеть следующим образом:

Структура проектаФайл представляет собой образец подписи:signature.jpg

Пример подписиФайл представляет собой образец PDF-файла, подлежащий подписанию."Letter of confirmation.pdf"

Давайте начнем, откроем новый файл Python и назовем его sign_pdf.py или как-то еще:

# Import Libraries
import OpenSSL
import os
import time
import argparse
from PDFNetPython3.PDFNetPython import *
from typing import Tuple


def createKeyPair(type, bits):
    """
    Create a public/private key pair
    Arguments: Type - Key Type, must be one of TYPE_RSA and TYPE_DSA
               bits - Number of bits to use in the key (1024 or 2048 or 4096)
    Returns: The public/private key pair in a PKey object
    """
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey
Приведенная выше функция создает пару открытый/закрытый ключ для использования при создании самозаверяющего сертификата для выполнения асимметричного шифрования.

Далее создание функции для создания самозаверяющего сертификата:

def create_self_signed_cert(pKey):
    """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
    # Create a self signed certificate
    cert = OpenSSL.crypto.X509()
    # Common Name (e.g. server FQDN or Your Name)
    cert.get_subject().CN = "BASSEM MARJI"
    # Serial Number
    cert.set_serial_number(int(time.time() * 10))
    # Not Before
    cert.gmtime_adj_notBefore(0)  # Not before
    # Not After (Expire after 10 years)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    # Identify issue
    cert.set_issuer((cert.get_subject()))
    cert.set_pubkey(pKey)
    cert.sign(pKey, 'md5')  # or cert.sign(pKey, 'sha256')
    return cert
Эта функция создает самозаверяющий сертификат, который не требует подписи центра сертификации.

Эта функция присваивает сертификату следующие атрибуты:

Общее название: БАССЕМ МАРДЖИ.
Серийный номер: случайное число в зависимости от функции времени.
Не после: истечение срока действия через 10 лет.
Теперь давайте создадим функцию, которая использует обе функции для генерации сертификата:

def load():
    """Generate the certificate"""
    summary = {}
    summary['OpenSSL Version'] = OpenSSL.__version__
    # Generating a Private Key...
    key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
    # PEM encoded
    with open('.\static\private_key.pem', 'wb') as pk:
        pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
        pk.write(pk_str)
        summary['Private Key'] = pk_str
    # Done - Generating a private key...
    # Generating a self-signed client certification...
    cert = create_self_signed_cert(pKey=key)
    with open('.\static\certificate.cer', 'wb') as cer:
        cer_str = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        cer.write(cer_str)
        summary['Self Signed Certificate'] = cer_str
    # Done - Generating a self-signed client certification...
    # Generating the public key...
    with open('.\static\public_key.pem', 'wb') as pub_key:
        pub_key_str = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
        #print("Public key = ",pub_key_str)
        pub_key.write(pub_key_str)
        summary['Public Key'] = pub_key_str
    # Done - Generating the public key...
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    open('.\static\container.pfx', 'wb').write(p12.export())
    # You may convert a PKSC12 file (.pfx) to a PEM format
    # Done - Generating a container file of the private key and the certificate...
    # To Display A Summary
    print("## Initialization Summary ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("############################################################################")
    return True
Эта функция выполняет следующие функции:

Создает пару открытого и закрытого ключей.
Хранит закрытый ключ в файле "private_key.pem" в статической папке.
Создает самозаверяющий сертификат и сохраняет его в файл "certificate.cer" в статической папке.
Сохраняет открытый ключ в файле "public_key.pem" в статической папке.
Создает файл-контейнер "container.pfx", объединяющий закрытый ключ и сертификат, и помещает его в статическую папку.
Обратите внимание, что закрытый ключ не должен печататься в консоли. Тем не менее, он включен в сводный словарь (который будет напечатан) в демонстрационных целях, убедитесь, что вы удалили закрытый ключ из вывода консоли, если вы серьезно относитесь к этому.

Теперь, когда у нас есть основная функция для генерации сертификата, давайте создадим функцию для подписи PDF-файла:

def sign_file(input_file: str, signatureID: str, x_coordinate: int, 
            y_coordinate: int, pages: Tuple = None, output_file: str = None
              ):
    """Sign a PDF file"""
    # An output file is automatically generated with the word signed added at its end
    if not output_file:
        output_file = (os.path.splitext(input_file)[0]) + "_signed.pdf"
    # Initialize the library
    PDFNet.Initialize()
    doc = PDFDoc(input_file)
    # Create a signature field
    sigField = SignatureWidget.Create(doc, Rect(
        x_coordinate, y_coordinate, x_coordinate+100, y_coordinate+50), signatureID)
    # Iterate throughout document pages
    for page in range(1, (doc.GetPageCount() + 1)):
        # If required for specific pages
        if pages:
            if str(page) not in pages:
                continue
        pg = doc.GetPage(page)
        # Create a signature text field and push it on the page
        pg.AnnotPushBack(sigField)
    # Signature image
    sign_filename = os.path.dirname(
        os.path.abspath(__file__)) + "\static\signature.jpg"
    # Self signed certificate
    pk_filename = os.path.dirname(
        os.path.abspath(__file__)) + "\static\container.pfx"
    # Retrieve the signature field.
    approval_field = doc.GetField(signatureID)
    approval_signature_digsig_field = DigitalSignatureField(approval_field)
    # Add appearance to the signature field.
    img = Image.Create(doc.GetSDFDoc(), sign_filename)
    found_approval_signature_widget = SignatureWidget(
        approval_field.GetSDFObj())
    found_approval_signature_widget.CreateSignatureAppearance(img)
    # Prepare the signature and signature handler for signing.
    approval_signature_digsig_field.SignOnNextSave(pk_filename, '')
    # The signing will be done during the following incremental save operation.
    doc.Save(output_file, SDFDoc.e_incremental)
    # Develop a Process Summary
    summary = {
        "Input File": input_file, "Signature ID": signatureID, 
        "Output File": output_file, "Signature File": sign_filename, 
        "Certificate File": pk_filename
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True
Функция sign_file() выполняет следующие действия:

Итерация по страницам входного PDF-файла.
Вставляет виджет подписи на выбранные страницы этого файла в определенном месте.
Добавляет изображение подписи и подписывает файл с помощью самозаверяющего сертификата.
Убедитесь, что у вас есть сертификаты в статической папке (мы увидим, как это сгенерировать позже).

При необходимости следующая функция полезна для подписи всех PDF-файлов в определенной папке:

def sign_folder(**kwargs):
    """Sign all PDF Files within a specified path"""
    input_folder = kwargs.get('input_folder')
    signatureID = kwargs.get('signatureID')
    pages = kwargs.get('pages')
    x_coordinate = int(kwargs.get('x_coordinate'))
    y_coordinate = int(kwargs.get('y_coordinate'))
    # Run in recursive mode
    recursive = kwargs.get('recursive')
    # Loop though the files within the input folder.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # Check if pdf file
            if not filename.endswith('.pdf'):
                continue
            # PDF File found
            inp_pdf_file = os.path.join(foldername, filename)
            print("Processing file =", inp_pdf_file)
            # Compress Existing file
            sign_file(input_file=inp_pdf_file, signatureID=signatureID, x_coordinate=x_coordinate,
                      y_coordinate=y_coordinate, pages=pages, output_file=None)
        if not recursive:
            break
Эта функция предназначена для подписи PDF-файлов определенной папки.

Он зацикливается на файлах указанной папки либо рекурсивно, либо нет в зависимости от значения рекурсивного параметра и обрабатывает эти файлы один за другим. Он принимает следующие параметры:

input_folder: путь к папке, содержащей обрабатываемые PDF-файлы.
signatureID: идентификатор создаваемого виджета подписи.
x_coordinate и y_coordinate: координаты, указывающие местоположение подписи.
pages: диапазон подписываемых страниц.
рекурсивный: следует ли запускать этот процесс рекурсивно путем зацикливания по вложенным папкам или нет.
Хорошо, теперь у нас есть все, давайте сделаем необходимый код для разбора аргументов командной строки:

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
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-l', '--load', dest='load', action="store_true",
                        help="Load the required configurations and create the certificate")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
                        help="Enter the path of the file or the folder to process")
    parser.add_argument('-s', '--signatureID', dest='signatureID',
                        type=str, help="Enter the ID of the signature")
    parser.add_argument('-p', '--pages', dest='pages', type=tuple,
                        help="Enter the pages to consider e.g.: [1,3]")
    parser.add_argument('-x', '--x_coordinate', dest='x_coordinate',
                        type=int, help="Enter the x coordinate.")
    parser.add_argument('-y', '--y_coordinate', dest='y_coordinate',
                        type=int, help="Enter the y coordinate.")
    path = parser.parse_known_args()[0].input_path
    if path and os.path.isfile(path):
        parser.add_argument('-o', '--output_file', dest='output_file',
                            type=str, help="Enter a valid output file")
    if path and os.path.isdir(path):
        parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
            str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively")
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args
Функция is_valid_path() проверяет путь, введенный в качестве параметра, и проверяет, является ли он файлом или каталогом.

Функция parse_args() определяет и задает соответствующие ограничения для аргументов командной строки, которые будут указаны пользователем при запуске этой утилиты.

Ниже я опишу определенные аргументы:

--load или -l: инициализируйте параметры конфигурации, создав самозаверяющий сертификат. Этот шаг должен быть выполнен один раз или по необходимости.
--input_path или -i: используется для ввода пути к файлу или папке для обработки, этот параметр связан с функцией is_valid_path(), которая определена ранее.
--signatureID или -s: идентификатор, присваиваемый виджету подписи. (в случае, если нескольким подписантам необходимо подписать один и тот же PDF-документ).
--pages или -p: Страницы для подписи.
--x_coordinate или -x и --y_coordinate или -y: указывает расположение подписи на странице.
--output_file или -o: путь к выходному файлу. Заполнение этого аргумента ограничено выбором файла в качестве входных данных, а не каталога.
--recursive или -r: обрабатывать папку рекурсивно или нет. Заполнение этого аргумента ограничено выбором каталога.
Написание основного кода сейчас:

if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    if args['load'] == True:
        load()
    else:
        # If File Path
        if os.path.isfile(args['input_path']):
            sign_file(
                input_file=args['input_path'], signatureID=args['signatureID'],
                x_coordinate=int(args['x_coordinate']), y_coordinate=int(args['y_coordinate']), 
                pages=args['pages'], output_file=args['output_file']
            )
        # If Folder Path
        elif os.path.isdir(args['input_path']):
            # Process a folder
            sign_folder(
                input_folder=args['input_path'], signatureID=args['signatureID'], 
                x_coordinate=int(args['x_coordinate']), y_coordinate=int(args['y_coordinate']),
                pages=args['pages'], recursive=args['recursive']
            )
Вышесказанное представляет собой основную функцию нашей программы, которая вызывает соответствующие функции в зависимости от параметра загрузки или выбранного пути.

Давайте протестируем нашу программу:

Во-первых, давайте передадим --help, чтобы увидеть доступные аргументы командной строки для передачи:

$ python sign_pdf.py --help
Выпуск:

usage: sign_pdf.py [-h] [-l] [-i INPUT_PATH] [-s SIGNATUREID] [-p PAGES] [-x X_COORDINATE] [-y Y_COORDINATE]

Available Options

optional arguments:
  -h, --help            show this help message and exit
  -l, --load            Load the required configurations and create the certificate
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter the path of the file or the folder to process
  -s SIGNATUREID, --signatureID SIGNATUREID
                        Enter the ID of the signature
  -p PAGES, --pages PAGES
                        Enter the pages to consider e.g.: [1,3]
  -x X_COORDINATE, --x_coordinate X_COORDINATE
                        Enter the x coordinate.
  -y Y_COORDINATE, --y_coordinate Y_COORDINATE
                        Enter the y coordinate.
Хорошо, давайте сначала создадим самозаверяющий сертификат:

$ python sign_pdf.py --load
После выполнения вы заметите, что связанные файлы были созданы под статической папкой:

Сгенерированные файлы сигнатурКроме того, на консоли будет приведена следующая сводка:

## Command Arguments #################################################
load:True
input_path:None
signatureID:None
pages:None
x_coordinate:None
y_coordinate:None
######################################################################
## Initialization Summary ##################################################
OpenSSL Version:20.0.1
Private Key:b'-----BEGIN PRIVATE KEY-----\nMIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAM5HRS/5iLztVPxp\nnKUpjrECxVgqH+/BFh5A8v7KJcUsHY6ht6yL3D+vXxgiv170pOml2tGmW3zmvL/j\nEkWI/duMSyvPjc03SUp6rQqCnjw/dG2tSsOhzC51WwI8+bwDrdhNZ7x0UEdleeQw\n5NtwQ6MqwiLNLhJLT8V/dtVsK/LxAgMBAAECgYEAglt31cGUMBCrzHfRjm6cxjBC\nFl1IoXMcTzIsXefRxrECXMjGEjywi26AYfhTh+aC8UTm6+Z9mokWbw1I1rij85/y\nvx4CTSGFAkMGAzmRTkmliPZoQDUxjr2XmSZaRhipo0atLY5dQYhQcINXq80lLAxZ\nsS3Tl7mxnssRo0hcHCECQQDyTVQEE5YLKpAsLWYRqMP3L2EDKNmySycIvVKh9lKB\nSlaHWzUfdHgzONcTA5Egd2CQchifPLx9KrykkusXs4knAkEA2fCYpKaaDDY+CjUI\nrY5RsYYoh5v2tZZ3PB3ElbN5afZY+dHa+mXsI6eBZgaUmsHeT0/OyymfsxZk//mI\n85pCJwJBAI54h4kqFxSTv1gqjZSenjOO6UUZVP/wDpCl+ZuAIb0h/8TxDUhkjHTZ\n3CSy+TeU2fO1EuM2rEIQygEe3hr+lwsCQFMCgwFju5UfK+4zWQTSCme1k8ZjL0rm\n7q9lHzVt0Lb9b9JnjiKFo7XI3U6A/yUa5pQK79cOGZfa1clxwCoY/U0CQBu4vATn\nyWVfp6lgLgY9T9FsCp7wPIRJJA1sUfhDvNeNt7WK6ynhVDaD0bZ+lX0sYG2RxI3m\nVSgAaAyqkMcYl5Q=\n-----END PRIVATE KEY-----\n'
Self Signed Certificate:b'-----BEGIN CERTIFICATE-----\nMIIBoTCCAQoCBQPMisZRMA0GCSqGSIb3DQEBBAUAMBcxFTATBgNVBAMMDEJBU1NF\nTSBNQVJKSTAeFw0yMTA5MTQyMTI3NDhaFw0zMTA5MTIyMTI3NDhaMBcxFTATBgNV\nBAMMDEJBU1NFTSBNQVJKSTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAzkdF\nL/mIvO1U/GmcpSmOsQLFWCof78EWHkDy/solxSwdjqG3rIvcP69fGCK/XvSk6aXa\n0aZbfOa8v+MSRYj924xLK8+NzTdJSnqtCoKePD90ba1Kw6HMLnVbAjz5vAOt2E1n\nvHRQR2V55DDk23BDoyrCIs0uEktPxX921Wwr8vECAwEAATANBgkqhkiG9w0BAQQF\nAAOBgQBLqfxOdXkXO2nubqSTdLEZYKyN4L+BxlYm2ZuG8ki0tAOrAAVIcmCM6QYf\n0oWURShZko+a6YP5f4UmZh1DVO7WnnBOytDf+f+n3SErw5YEkfbCDQp5MSjz+79N\nvJtQOPr3RjtyuDFWvNlcit2q6JW2lsmfD2+CdG7iSbiKLC8Bag==\n-----END CERTIFICATE-----\n'
Public Key:b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDOR0Uv+Yi87VT8aZylKY6xAsVY\nKh/vwRYeQPL+yiXFLB2Oobesi9w/r18YIr9e9KTppdrRplt85ry/4xJFiP3bjEsr\nz43NN0lKeq0Kgp48P3RtrUrDocwudVsCPPm8A63YTWe8dFBHZXnkMOTbcEOjKsIi\nzS4SS0/Ff3bVbCvy8QIDAQAB\n-----END PUBLIC KEY-----\n'
############################################################################
Как видите, были успешно сгенерированы закрытый и открытый ключи, а также сертификат. Опять же, как отмечалось ранее. Если вы используете этот код, вы должны исключить закрытый ключ из сводного словаря, чтобы он не был напечатан на консоли.

Теперь подпишем документ под названием «Письмо-подтверждение.pdf», помещенный в статическую папку:

$ python sign_pdf.py -i ".\static\Letter of confirmation.pdf" -s "BM" -x 330 -y 280
На консоли отобразится следующая сводка:

## Command Arguments #################################################
load:False
input_path:static\Letter of confirmation.pdf
signatureID:BM
pages:None
x_coordinate:330
y_coordinate:280
output_file:None
######################################################################

PDFNet is running in demo mode.
Permission: read
Permission: write
## Summary ########################################################
Input File:static\Letter of confirmation.pdf
Signature ID:BM
Output File:static\Letter of confirmation_signed.pdf
Signature File:C:\pythoncode-tutorials\handling-pdf-files\pdf-signer\static\signature.jpg
Certificate File:C:\pythoncode-tutorials\handling-pdf-files\pdf-signer\static\container.pfx
###################################################################
Этот документ будет обновлен в "Письме о confirmation_signed.pdf" следующим образом:

Подписанный PDF-документ с помощью PythonКогда вы нажмете на выделенное поле подписи, вы заметите предупреждающее сообщение, отображаемое ниже:

Предупреждение о цифровой подписиПричина этого предупреждения заключается в том, что новый самозаверяющий сертификат еще не является доверенным для Acrobat Reader. Нажмите на кнопку Свойства подписи, и вы увидите сведения о самозаверяющем сертификате.

Примечание: Пожалуйста, обратитесь к прилагаемому приложению с подробным описанием инструкций по доверию самозаверяющему сертификату Adobe Reader.

Заключение
Можно также указать параметр -p для подписи нескольких страниц в PDF-файле, что-то вроде:

$ python sign_pdf.py -i pdf_file.pdf -s "BM" -x 330 -y 300 -p [1, 3]
Или подписание нескольких PDF-файлов, включенных в папку:

$ python sign_pdf.py -i pdf-files-folder -s "BM" -p [1] -x 330 -y 300 -r 0
Цифровая подпись документов экономит время, уменьшает потребность в бумажных процессах и обеспечивает гибкость для утверждения документа практически из любого места.

Надеюсь, вам понравилась эта статья и помогла вам создать свои инструменты!

Проверьте полный код здесь.

Связанные туториалы:

Как шифровать и расшифровывать PDF-файлы на Python.
Как сжимать PDF-файлы на Python.
Приложение
После подписания PDF-файла (т.е. «Письмо confirmation_signed.pdf») и последующего открытия его в Adobe Reader под панелью инструментов может появиться следующее сообщение («По крайней мере, одна подпись имеет проблемы»)

Предупреждающее сообщение в Adobe Acrobat

Действительно, это сообщение не указывает на то, что цифровая подпись недействительна или повреждена, но это означает, что цифровая подпись, добавленная с помощью самозаверяющего сертификата, не может быть автоматически проверена Adobe Reader, поскольку сертификат не входит в список доверенных удостоверений, которые Adobe использует для проверки подписи.

Выполните действия, показанные на следующих снимках экрана, чтобы добавить самозаверяющий сертификат в список доверенных удостоверений Adobe:

Перейдите в раздел «Изменить настройки >».Переход к редактированию / Настройкам в Adobe Acrobat
Выберите опцию Подписи и нажмите на кнопку Дополнительно, выделенную ниже:Перейти к Больше
Выберите опцию Доверенные сертификаты и нажмите кнопку Импорт:Выбор доверенных сертификатов и нажатие кнопки Импорт
Нажмите Обзор и импорт самозаверяющего сертификата из папки:staticИмпорт самозаверяющего сертификатаИмпорт сертификатаСертификат импортирован
Select the newly added certificate and press on Edit Trust:Editing Trust
Enable the checkbox "Use this certificate as a trusted root" and press OK:Using the certificate as a trusted root
Now close and re-open the PDF document:

Действительный сертификатНажмите на поле подписи:



И вот, это действительная подпись!

Проверьте полный код здесь.

Наконец, если вы новичок и хотите изучать Python, я предлагаю вам пройти курс Python For Everybody Coursera, в котором вы узнаете много нового о Python. Вы также можете проверить нашу страницу ресурсов и курсов, чтобы увидеть ресурсы Python, которые я рекомендую по различным темам!