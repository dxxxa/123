# [How to Get the Size of Directories in Python](https://www.thepythoncode.com/article/get-directory-size-in-bytes-using-python)
To run this:
- `pip3 install -r requirements.txt`
- To get the size of subdirectories of `/root/home` directory:
    ```
    python get_directory_size.py /root/home
    ```
    This will show a pie chart that indicates the size of each subdirectory.
##
# [[] / []]()
Вы когда-нибудь задумывались, как вы можете получить размер папки в байтах с помощью Python? Как вы, возможно, уже знаете, функция os.path.get_size() возвращает только правильный размер нужных файлов, а не папок. В этом кратком руководстве вы узнаете, как создать простую функцию для вычисления общего размера каталога на Python.

Давайте начнем, откройте новый файл Python:

import os
Приведенная ниже основная функция вычисляет общий размер каталога с учетом его относительного или абсолютного пути:

def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                try:
                    total += get_directory_size(entry.path)
                except FileNotFoundError:
                    pass
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total
Обратите внимание, что я использовал функцию os.scandir(), которая возвращает итератор записей (файлов или каталогов) в указанном каталоге.

os.scandir() вызывает NotADirectoryError, если заданный путь не является папкой (файлом или ссылкой), поэтому мы поймали это исключение и возвращаем только фактический размер этого файла.

Он также вызывает PermissionError, если он не может открыть файл (например, системные файлы), в этом случае мы просто вернем 0.

Вышеуказанная функция вернет размер в байтах, который будет, конечно, нечитаемым для больших каталогов, в результате давайте сделаем функцию для масштабирования этих байтов до Kilo, Mega, Giga и т.д.:

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
Хорошо, я собираюсь протестировать это на моем диске C (я знаю, что он большой):

get_size_format(get_directory_size("C:\\"))
Это заняло около минуты и вернуло следующее:

'100.91GB'
Теперь, что, если я хочу знать, какие подкаталоги занимают большую часть этого пространства? Ну, следующий код не просто вычисляет размер каждого подкаталога, но строит пирог с помощью библиотеки matplotlib (в которую вы можете установить с помощью pip3 install matplotlib), которая показывает размер каждого из них:

import matplotlib.pyplot as plt

def plot_pie(sizes, names):
    """Plots a pie where `sizes` is the wedge sizes and `names` """
    plt.pie(sizes, labels=names, autopct=lambda pct: f"{pct:.2f}%")
    plt.title("Different Sub-directory sizes in bytes")
    plt.show()

if __name__ == "__main__":
    import sys
    folder_path = sys.argv[1]

    directory_sizes = []
    names = []
    # iterate over all the directories inside this path
    for directory in os.listdir(folder_path):
        directory = os.path.join(folder_path, directory)
        # get the size of this directory (folder)
        directory_size = get_directory_size(directory)
        if directory_size == 0:
            continue
        directory_sizes.append(directory_size)
        names.append(os.path.basename(directory) + ": " + get_size_format(directory_size))

    print("[+] Total directory size:", get_size_format(sum(directory_sizes)))
    plot_pie(directory_sizes, names)
Теперь каталог принимается в качестве аргумента в командной строке:

python get_directory_size.py C:\
Это покажет хороший пирог, который выглядит примерно так:

Размеры подкаталогов в PythonТеперь, увидев эту диаграмму, я знаю, что пользователи и папки Windows занимают большую часть моего диска C!