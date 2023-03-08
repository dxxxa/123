import shutil
#with open('output_file.txt', 'wb') as wfd:
#    for f in file:
#        with open(f, 'rb') as fd:
#            shutil.copyfileobj(fd, wfd)


import os

path_data = "C:\\Users\\nUser\\PycharmProjects\\pythonProject4\\data.txt"
path = "C:\\Users\\nUser\\PycharmProjects\\pythonProject4"  # Каталог текстовых файлов
line_count = 0

# Вывести список всех файлов каталога и количество строк
for file in os.listdir(path):
    if file.endswith(".txt"):  # Паттерн поиска файлов по расширению
        if (file == 'data.txt'):
            continue
        else:
            local_count = 0
            # Вариант подсчета строк без загрузки файла в память целиком
            with open(file) as f:
                quantity = sum(1 for line in f)

            print(f'{os.path.join(path, file)} - {quantity} строк')
            line_count += quantity
print("=====================================")
print(f"Всего строк - {line_count}")



if os.path.exists(path_data):
    print("Файл найден")
    with open('data.txt') as f:
        n = 0
        for line in f:
            n += 1
    print("Data.txt = ", n)
    line_count_d = line_count - n
    print(f"Всего строк - Data.txt {line_count_d}")
    print("=====================================")
else:
    print("Файл data.txt не найден")
