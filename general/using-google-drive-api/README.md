# [How to Use Google Drive API in Python](https://www.thepythoncode.com/article/using-google-drive--api-in-python)
To use the scripts, you should:
- `pip3 install -r requirements.txt`
- Enable Google Drive API to get `credentials.json` file, check [the tutorial](https://www.thepythoncode.com/article/using-google-drive--api-in-python) for more information.
##
# [[] / []]()
Google Диск позволяет хранить ваши файлы в облаке, к которым вы можете получить доступ в любое время и в любой точке мира. В этом уроке вы узнаете, как перечислить файлы вашего диска Google, искать по ним, загружать сохраненные файлы и даже загружать локальные файлы на ваш диск программно с помощью Python.

Вот оглавление:

Включение API диска
Список файлов и каталогов
Загрузка файлов
Поиск файлов и каталогов
Загрузка файлов
Чтобы начать работу, давайте установим необходимые библиотеки для этого учебника:

pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib tabulate requests tqdm
Включение API диска
Включение Api Google Диска очень похоже на другие API Google, такие как API Gmail, API YouTube или API поисковой системы Google. Во-первых, у вас должна быть учетная запись Google с включенным Google Диском. Перейдите на эту страницу и нажмите кнопку «Включить API диска», как показано ниже:

Включение API диска

Появится новое окно; выберите тип приложения. Я буду придерживаться «Настольного приложения», а затем нажму кнопку «Создать». После этого вы увидите еще одно окно, в котором говорится, что все готово:

Api диска включен

Загрузите свои учетные данные, нажав кнопку «Загрузить конфигурацию клиента», а затем «Готово».

Наконец, вам нужно поместить credentials.json, который загружается в ваши рабочие каталоги (т. Е. Где вы выполняете предстоящие скрипты Python).

Список файлов и каталогов
Прежде чем что-либо делать, нам необходимо аутентифицировать наш код в нашей учетной записи Google. Приведенная ниже функция делает это:

import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)
Мы импортировали необходимые модули. Приведенная выше функция была взята со страницы быстрого запуска Google Диска. Он в основном ищет файл token.pickle для аутентификации в вашей учетной записи Google. Если он не нашел его, он будет использовать credentials.json, чтобы запросить аутентификацию в вашем браузере. После этого он инициирует службу API Google Диска и возвращает ее.

Перейдя к главной функции, определим функцию, которая перечисляет файлы на нашем диске:

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 5 files the user has access to.
    """
    service = get_gdrive_service()
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
    # get the results
    items = results.get('files', [])
    # list all 20 files & folders
    list_files(items)
Поэтому мы использовали функцию service.files().list() для возврата первых пяти файлов/папок, к которым пользователь имеет доступ, указав pageSize=5, мы передали некоторые полезные поля параметру fields, чтобы получить подробную информацию о перечисленных файлах, таких как mimeType (тип файла), размер в байтах, идентификаторы родительского каталога и время последней измененной даты. Проверьте эту страницу, чтобы увидеть все остальные поля.

Обратите внимание, что мы использовали функцию list_files(items), мы еще не определили эту функцию. Поскольку результаты теперь представляют собой список словарей, он не так удобочитаем. Мы передаем элементы этой функции, чтобы распечатать их в удобочитаемом формате:

def list_files(items):
    """given items returned by Google Drive API, prints them in a tabular way"""
    if not items:
        # empty drive
        print('No files found.')
    else:
        rows = []
        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            rows.append((id, name, parents, size, mime_type, modified_time))
        print("Files:")
        # convert to a human readable table
        table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
        # print the table
        print(table)
Мы преобразовали эту переменную list of dictionaries items в переменную списка кортежей строк, а затем передали их в установленный ранее модуль табличирования, чтобы распечатать их в хорошем формате, назовем функцию main():

if __name__ == '__main__':
    main()
Смотрите мои выходные данные:

Files:
ID                                 Name                            Parents                  Size      Type                          Modified Time
---------------------------------  ------------------------------  -----------------------  --------  ----------------------------  ------------------------
1FaD2BVO_ppps2BFm463JzKM-gGcEdWVT  some_text.txt                   ['0AOEK-gp9UUuOUk9RVA']  31.00B    text/plain                    2020-05-15T13:22:20.000Z
1vRRRh5OlXpb-vJtphPweCvoh7qYILJYi  google-drive-512.png            ['0AOEK-gp9UUuOUk9RVA']  15.62KB   image/png                     2020-05-14T23:57:18.000Z
1wYY_5Fic8yt8KSy8nnQfjah9EfVRDoIE  bbc.zip                         ['0AOEK-gp9UUuOUk9RVA']  863.61KB  application/x-zip-compressed  2019-08-19T09:52:22.000Z
1FX-KwO6EpCMQg9wtsitQ-JUqYduTWZub  Nasdaq 100 Historical Data.csv  ['0AOEK-gp9UUuOUk9RVA']  363.10KB  text/csv                      2019-05-17T16:00:44.000Z
1shTHGozbqzzy9Rww9IAV5_CCzgPrO30R  my_python_code.py               ['0AOEK-gp9UUuOUk9RVA']  1.92MB    text/x-python                 2019-05-13T14:21:10.000Z
Это файлы на моем Google Диске. Обратите внимание, что столбцы Размер масштабируются в байтах; Это потому, что мы использовали функцию get_size_format() в функции list_files(), вот код для нее:

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
Приведенная выше функция должна быть определена перед запуском метода main(). В противном случае возникнет ошибка. Для удобства проверьте полный код.

Помните, что после запуска скрипта вам будет предложено в браузере по умолчанию выбрать свою учетную запись Google и разрешить приложение для областей, которые вы указали ранее, не волнуйтесь, это произойдет только при первом запуске, а затем token.pickle будет сохранен и вместо этого загрузит данные аутентификации оттуда.

Заметка: Иногда после выбора учетной записи Google вы увидите предупреждение "Это приложение не проверено" (так как Google не проверил ваше приложение). Это нормально, чтобы перейти в раздел «Дополнительно» и разрешить приложение в вашей учетной записи.

Загрузка файлов
Чтобы загрузить файлы на наш Google Диск, нам нужно изменить список SCOPES, который мы указали ранее, нам нужно добавить разрешение на добавление файлов / папок:

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']
Другая область означает разные привилегии, и необходимо удалить файл token.pickle в рабочем каталоге и повторно запустить код для проверки подлинности в новой области.

Мы будем использовать ту же функцию get_gdrive_service() для аутентификации нашей учетной записи, давайте сделаем функцию для создания папки и загрузки в нее примера файла:

def upload_files():
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": "TestFolder",
        "mimeType": "application/vnd.google-apps.folder"
    }
    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": "test.txt",
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload("test.txt", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))
Мы использовали метод service.files().create() для создания новой папки, мы передали словарь folder_metadata, который имеет тип и имя папки, которую мы хотим создать, мы передали fields="id" для извлечения идентификатора папки, чтобы мы могли загрузить файл в эту папку.

Затем мы использовали класс MediaFileUpload для загрузки примера файла и передачи его в тот же метод service.files().create(), убедитесь, что у вас есть тестовый файл по вашему выбору с именем test.txt, на этот раз мы указали атрибут «parents» в словаре метаданных, мы просто поместили папку, которую мы только что создали. Давайте запустим его:

if __name__ == '__main__':
    upload_files()
После запуска кода на моем Google Диске была создана новая папка:

Папка, созданная с помощью API Google Диска в PythonИ действительно, после того, как я войду в эту папку, я вижу файл, который мы только что загрузили:

Файл, загруженный с помощью API Google Диска в PythonМы использовали текстовый файл для демонстрации, но вы можете загрузить любой тип файла, который вы хотите. Проверьте полный код загрузки файлов на Google Диск.

Поиск файлов и каталогов
Google Диск позволяет нам искать файлы и каталоги с помощью ранее использовавшегося метода list(), просто передав параметр 'q', следующая функция принимает службу API диска и запрашивает и возвращает отфильтрованные элементы:

def search(service, query):
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result
Давайте посмотрим, как использовать эту функцию:

def main():
    # filter to text files
    filetype = "text/plain"
    # authenticate Google Drive API
    service = get_gdrive_service()
    # search for files that has type of text/plain
    search_result = search(service, query=f"mimeType='{filetype}'")
    # convert to table to print well
    table = tabulate(search_result, headers=["ID", "Name", "Type"])
    print(table)
Таким образом, мы фильтруем текстовые /простые файлы здесь, используя "mimeType='text/plain'" в качестве параметра запроса, если вы хотите фильтровать по имени, вы можете просто использовать "name='filename.ext'" в качестве параметра запроса. Более подробную информацию можно найти в документации по API Google Диска.

Давайте выполним это:

if __name__ == '__main__':
    main()
Выпуск:

ID                                 Name           Type
---------------------------------  -------------  ----------
15gdpNEYnZ8cvi3PhRjNTvW8mdfix9ojV  test.txt       text/plain
1FaE2BVO_rnps2BFm463JwPN-gGcDdWVT  some_text.txt  text/plain
Проверьте полный код здесь.

Связанные с: Как использовать API Gmail в Python.

Загрузка файлов
Чтобы загрузить файлы, нам нужно сначала получить файл, который мы хотим загрузить. Мы можем либо найти его, используя предыдущий код, либо вручную получить его идентификатор диска. В этом разделе мы будем искать файл по имени и загружать его на наш локальный диск:

import pickle
import os
import re
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import requests
from tqdm import tqdm

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]
Я добавил здесь две области. Это потому, что нам нужно создать разрешение, чтобы сделать файлы доступными для совместного использования и загрузки. Вот основная функция:

def download():
    service = get_gdrive_service()
    # the name of the file you want to download from Google Drive 
    filename = "bbc.zip"
    # search for the file by name
    search_result = search(service, query=f"name='{filename}'")
    # get the GDrive ID of the file
    file_id = search_result[0][0]
    # make it shareable
    service.permissions().create(body={"role": "reader", "type": "anyone"}, fileId=file_id).execute()
    # download file
    download_file_from_google_drive(file_id, filename)
Вы видели первые три строки в предыдущих рецептах. Мы просто аутентифицируемся с помощью нашей учетной записи Google и ищем нужный файл для загрузки.

После этого мы извлекаем идентификатор файла и создаем новое разрешение, которое позволит нам скачать файл, и это то же самое, что создать кнопку общей ссылки в веб-интерфейсе Google Диска.

Наконец, мы используем нашу определенную функцию download_file_from_google_drive() для загрузки файла, вот он:

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        # get the file size from Content-length response header
        file_size = int(response.headers.get("Content-Length", 0))
        # extract Content disposition from response headers
        content_disposition = response.headers.get("content-disposition")
        # parse filename
        filename = re.findall("filename=\"(.+)\"", content_disposition)[0]
        print("[+] File size:", file_size)
        print("[+] File name:", filename)
        progress = tqdm(response.iter_content(CHUNK_SIZE), f"Downloading {filename}", total=file_size, unit="Byte", unit_scale=True, unit_divisor=1024)
        with open(destination, "wb") as f:
            for chunk in progress:
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # update the progress bar
                    progress.update(len(chunk))
        progress.close()

    # base URL for download
    URL = "https://docs.google.com/uc?export=download"
    # init a HTTP session
    session = requests.Session()
    # make a request
    response = session.get(URL, params = {'id': id}, stream=True)
    print("[+] Downloading", response.url)
    # get confirmation token
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm':token}
        response = session.get(URL, params=params, stream=True)
    # download to disk
    save_response_content(response, destination)  
Я взял часть приведенного выше кода из учебника по загрузке файлов; он просто делает запрос GET к целевому URL-адресу, который мы создали, передавая идентификатор файла в качестве параметров в методе session.get().

Я использовал библиотеку tqdm для печати индикатора выполнения, чтобы увидеть, когда он закончится, что станет удобным для больших файлов. Давайте выполним его:

if __name__ == '__main__':
    download()
Это приведет к поиску файла bbc.zip, загрузке его и сохранению в вашем рабочем каталоге. Проверьте полный код.

Заключение
Хорошо, вот оно. Это в основном основные функции Google Диска. Теперь вы знаете, как делать их в Python без ручных щелчков мыши!

Помните, что при каждом изменении списка SCOPES необходимо удалить файл token.pickle для повторной проверки подлинности в учетной записи с новыми областями. Смотрите эту страницу для получения дополнительной информации, а также списка областей и их объяснений.

Не стесняйтесь редактировать код, чтобы принять имена файлов в качестве параметров для их загрузки или загрузки. Идите и попытайтесь сделать скрипт максимально динамичным, введя модуль argparse, чтобы сделать некоторые полезные скрипты. Давайте посмотрим, что вы построите!

Ниже приведен список других руководств по API Google, если вы хотите проверить их:

Как извлечь данные Google Trends в Python.
Как использовать API пользовательской поисковой системы Google в Python.
Как извлечь данные YouTube с помощью API YouTube в Python.
Как использовать API Gmail в Python.