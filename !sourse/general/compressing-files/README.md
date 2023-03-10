# [How to Compress and Decompress Files in Python](https://www.thepythoncode.com/article/compress-decompress-files-tarfile-python)
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python tar.py --help
    ```
    **Output:**
    ```
    usage: tar.py [-h] [-t TARFILE] [-p PATH] [-f FILES] method

    TAR file compression/decompression using GZIP.

    positional arguments:
    method                What to do, either 'compress' or 'decompress'

    optional arguments:
    -h, --help            show this help message and exit
    -t TARFILE, --tarfile TARFILE
                            TAR file to compress/decompress, if it isn't specified
                            for compression, the new TAR file will be named after
                            the first file to compress.
    -p PATH, --path PATH  The folder to compress into, this is only for
                            decompression. Default is '.' (the current directory)
    -f FILES, --files FILES
                            File(s),Folder(s),Link(s) to compress/decompress
                            separated by ','.
    ```
- If you want to compress one or more file(s)/folder(s):
    ```
    python tar.py compress -f test_folder,test.txt
    ```
    This will compress the folder `test_folder` and the file `test.txt` into a single TAR compressed file named: `test_folder.tar.gz`
    If you want to name the TAR file yourself, consider using `-t` flag.
- If you want to decompress a TAR file named `test_folder.tar.gz` into a new folder called `extracted` for instance:
    ```
    python tar.py decompress -t test_folder.tar.gz -p extracted
    ```
    A new folder `extracted` will appear that contains everything on `test_folder.tar.gz` decompressed.
##
# [[] / []]()
Сжатый файл — это своего рода архив, содержащий один или несколько файлов, уменьшенных в размере. Сжатие файлов в современных операционных системах обычно довольно простое. Однако в этом учебнике вы узнаете, как сжимать и распаковывать файлы с помощью языка программирования Python.

Вы можете спросить, зачем мне учиться сжимать файлы в Python, где уже есть инструменты? Ну, десжатие файлов программным путем без каких-либо ручных щелчков чрезвычайно полезно. Например, при загрузке наборов данных машинного обучения, в которых требуется загрузить фрагмент кода, извлекайте и загружайте их в память автоматически.

Вы также можете добавить функцию сжатия / распаковки в свое приложение, или у вас есть тысячи сжатых файлов, и вы хотите распаковать их одним щелчком мыши, этот учебник может помочь.

Связанные с: Как шифровать и расшифровывать файлы в Python.

Давайте начнем, мы будем использовать встроенный модуль tarfile, поэтому нам не нужно ничего устанавливать, вы можете опционально установить tqdm только для печати индикаторов выполнения:

pip3 install tqdm
Откройте новый файл Python и:

import tarfile
from tqdm import tqdm # pip3 install tqdm
Сжатие
Начнем со сжатия, за сжатие файла/папки или списка файлов/папок отвечает следующая функция:

def compress(tar_file, members):
    """
    Adds files (`members`) to a tar_file and compress it
    """
    # open file for gzip compressed writing
    tar = tarfile.open(tar_file, mode="w:gz")
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        # add file/folder/link to the tar file (compress)
        tar.add(member)
        # set the progress description of the progress bar
        progress.set_description(f"Compressing {member}")
    # close the file
    tar.close()
Я назвал эти файлы / папки членами, ну, это то, что документация называет их в любом случае.

Сначала мы открыли и создали новый tar-файл для gzip-сжатой записи (это то, что означает mode='w:gz'), а затем для каждого участника добавьте его в архив, а затем, наконец, закройте tar-файл.

Я опционально обернул члены tqdm для печати индикаторов выполнения, это будет полезно при сжатии большого количества файлов за один раз.

Вот и все для сжатия, теперь давайте углубимся в декомпрессию.

Узнайте также: Как сжимать PDF-файлы на Python.

Декомпрессия
Приведенная ниже функция предназначена для распаковки заданного архивного файла:

def decompress(tar_file, path, members=None):
    """
    Extracts `tar_file` and puts the `members` to `path`.
    If members is None, all members on `tar_file` will be extracted.
    """
    tar = tarfile.open(tar_file, mode="r:gz")
    if members is None:
        members = tar.getmembers()
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        # set the progress description of the progress bar
        progress.set_description(f"Extracting {member.name}")
    # or use this
    # tar.extractall(members=members, path=path)
    # close the file
    tar.close()
Во-первых, мы открыли архивный файл как читаемый со сжатием gzip. После этого я сделал необязательный параметр 'member' на случай, если мы хотим извлечь определенные файлы (не все архивы), если 'members' не указан, мы получим все файлы в архиве с помощью метода getmembers(), который возвращает всех членов архива в виде списка Python.

А затем для каждого члена извлеките его с помощью метода extract(), который извлекает элемент из архива в указанный нами каталог 'path'.

Обратите внимание, что мы можем в качестве альтернативы использовать extractall() для этого (что предпочтительно в официальной документации).

Давайте проверим это:

compress("compressed.tar.gz", ["test.txt", "folder"])
Это сжимает тест.txt файл и папку в текущем каталоге в новый файл архива tar, называемый compressed.tar.gz как показано на следующем рисунке:

Сжатый файл с помощью модуля tarfile в PythonЕсли вы хотите распаковать:

decompress("compressed.tar.gz", "extracted")
Это распакует предыдущий архив, который мы только что сжали в новую папку под названием extracted:

Распакованный архивный файл tar с помощью модуля tarfile в PythonХорошо, мы закончили! Вы можете быть креативными с этим, вот несколько идей:

Передача папок по сети после их сжатия.
Загрузка архивных файлов и их распаковка.
В этом уроке мы изучили сжатие и распаковку с помощью модуля tarfile, вы также можете использовать модуль zipfile для работы с ZIP-архивами, модуль bz2 для сжатия bzip2, модули gzip или zlib для файлов gzip.