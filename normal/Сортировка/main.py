#!/usr/bin/python
# -*- coding: cp1251 -*-

#

# https://ru.stackoverflow.com/questions/1193403/%D0%A1%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D1%81%D1%82%D1%80%D0%BE%D0%BA-%D0%B2-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%BC-%D1%84%D0%B0%D0%B9%D0%BB%D0%B5?ysclid=l6dntdmveq996744519


from random import choices
from tqdm.auto import tqdm
import os
import shutil

class LetterFile:
    def __init__(self, letter, max_lines):
        self.letter = letter
        self.number = 0
        self.line_count = 0
        self.max_lines = max_lines
        os.chdir(path3)
        self.create()

    def create(self):
        self.open('w')

    def open(self, mode='w+'):
        self.file = open(self.letter + "(" + str(self.number) + ")" + '.txt', mode)

    def close(self):
        self.file.close()

    def append(self, line):
        self.file.write(line)
        self.line_count += 1
        if self.line_count >= self.max_lines:
            self.close()
            self.number += 1
            self.line_count = 0
            self.open()


def get_big_letters():
    for ch in range(ord('A'), ord('Z') + 1):
        yield chr(ch)


def get_small_letters():
    for ch1 in range(ord('a'), ord('z') + 1):
        yield chr(ch1)


def digits():
    for ch2 in range(ord('0'), ord('9') + 1):
        yield chr(ch2)


input_file_name = 'data.txt'
# input_file_rows = 15_000_000
max_lines = 300000_000
# str_len = 15
alphabet0 = list(get_big_letters())
alphabet1 = list(get_small_letters())
alphabet2 = list(digits())
print("\nBig_Letters:  [", *alphabet0, "]"
      "\nSmall_Letters:[", *alphabet1, "]"
      "\nNumbers:      [", *alphabet2, "]"
      "\n#####################################")

# print('[0] Generating input File ### ��������� �����')
# with open(input_file_name, 'w') as f:
#    for i in tqdm(range(input_file_rows)):
#        s = ''.join(choices(alphabet, k=str_len))
#        f.write(s)
#        f.write('\n')

path_data = "C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\data.txt"
path = "C:\\Users\\nUser\\PycharmProjects\\pythonProject5"  # ������� ��������� ������
path3 = "C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\test"

line_count = 0

# input("Press Enter to continue1...")
# print("������� ����������:", os.getcwd())
# os.chdir(path3)

if os.path.exists(path_data):
    print("���� ������")
    files = {}

    #os.mkdir(path3)

    #directory_folder = r"C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\test"
    #folder_path = os.path.dirname(directory_folder)  # ���� � ����� � ������
    #if not os.path.exists(folder_path):  # ���� ���� �� ���������� ������� ���
    #    os.makedirs(folder_path)

    print('[1] Create Files')
    os.chdir(path3)

    for ch in alphabet0:
        f = LetterFile(ch, max_lines)
        files[ch] = f

    for ch1 in alphabet1:
        f = LetterFile(ch1, max_lines)
        files[ch1] = f

    for ch2 in alphabet2:
        f = LetterFile(ch2, max_lines)
        files[ch2] = f

    print('[2] Process input File')
    os.chdir("..")

    try:
        with open(input_file_name) as fr:
            i = 0
            for s in tqdm(fr.readlines()):
                try:
                    fw = files[s[0].upper()]
                except:
                    i += 1
                    my_file = open("Symbol.txt", "a")
                    my_file.write(s)
                    my_file.close()
                fw.append(s)
            print("Error: ������ � ��������!!!", i)

        print('[3] Closing Files')
        os.chdir(path3)

        for ch in alphabet0:
            f = files[ch]
            f.close()

        for ch1 in alphabet1:
            f = files[ch1]
            f.close()

        for ch2 in alphabet2:
            f = files[ch2]
            f.close()

        print('[4] Counting rows Files')
        input("(Press Enter to continue...)")
        print("=====================================")
        os.chdir("..")

        with open('data.txt') as f:
            n = 0
            for line in f:
                n += 1
        print("Data.txt = ", n)
        line_count_d = line_count - n
        print(f"����� ����� - Data.txt {line_count_d}")
        print("=====================================")

        os.chdir(path3)
        # ������� ������ ���� ������ �������� � ���������� �����
        for file in os.listdir(path3):
            if file.endswith(".txt"):  # ������� ������ ������ �� ����������
                if (file == 'data.txt'):
                    continue
                else:
                    local_count = 0
                    # ������� �������� ����� ��� �������� ����� � ������ �������
                    with open(file) as f:
                        quantity = sum(1 for line in f)

                    print(f'{os.path.join(path, file)} - {quantity} �����')
                    line_count += quantity
        print("=====================================")
        print(f"����� ����� - {line_count}")
    except:
        print('[Error!]�������� ������ ������.txt')
        src_dir = "C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\test"
        shutil.rmtree(src_dir)
else:
    print("���� data.txt �� ������")
