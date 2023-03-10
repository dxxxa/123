# Email_Sorting_@Domen.py
# Email Sorting @Domen INPUT.txt

import os
import re
from time import time

filename = 'Email Sorting @Domen INPUT.txt'


xxx = str(len(re.findall(r"[\n']+?", open(filename).read())))  # выведет количество всех строк включая пустые
yyy = str(len(re.findall(r"[\n']+", open(filename).read())))  # выведет количество без пустых строк
print("File contains lines: " + xxx)
print("File contains lines: " + yyy)

start_time = time()

if not os.path.isdir("SORT"):
    os.makedirs('SORT')
    for mail in open(filename, 'r').readlines():
        # open('SORT/' + mail.split('@')[1].split(':')[0].split('.')[0] + '.txt', 'a').write(mail)
        try:
            open('SORT/' + '@' + mail.split('@')[1].split(':')[0] + '.txt', 'a').write(mail)
        except:
            print('Found wrong Email')
            open('SORT/' + 'OTHER.txt', 'a').write(mail)
    end_time = time()  # program end time
    tot_time = end_time - start_time
    # printing run time # Общее затраченное Время выполнения
    print("=========================================="
          "\nSorting is Done"
          "\nTotal Elapsed Runtime:", str(tot_time)[0:6] + "sec",
          "\n==========================================")

    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    # Список всех файлов в каталоге с помощью scandir() # List all files in a directory using scandir()
    basepath = 'SORT/'
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                # print('@' + entry.name, ':', len(re.findall(r"[\n']+?", open(entry).read())))
                abc = len(re.findall(r"[\n']+?", open(entry).read()))
                print(entry.name, ':', abc)

    # Считает сумму всех строк в файлах txt
    strings = 0
    files = os.listdir()
    for file in files:
        if os.path.isfile(file):
            if file.endswith('.txt'):
                with open(file) as f:
                    ss = f.read().split('\n')
                    for s in ss:
                        if s.strip() and not s.startswith('#') and not s.startswith(
                                '"') and not s.startswith("'"):
                            strings += 1

    print("\nFile contains lines: " + xxx,
          "\nFile contains lines: " + yyy,
          "\n=========================================="
          "\nВсего строк:", strings - 1)
else:
    print('Удалите папку SORT для работы скрипта!')
