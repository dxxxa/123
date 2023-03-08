#!/usr/bin/python
# -*- coding: cp1251 -*-

#
# https://ru.stackoverflow.com/questions/1193403/%D0%A1%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D1%81%D1%82%D1%80%D0%BE%D0%BA-%D0%B2-%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%BC-%D1%84%D0%B0%D0%B9%D0%BB%D0%B5?ysclid=l6dntdmveq996744519


from random import choices
from tqdm.auto import tqdm
import os
import shutil


# �������� ������ LetterFile
class LetterFile:  # �������� ����� class(������� �����) �� ������� ������� ������������ ������(LetterFile).
    #  ����� self ��� ������ �������� ������ �������
    def __init__(self, letter, max_lines):  # ����� __init__ � ��� ����������������, ���������� ��� �������� ������� ������, self ��� ��������� � ���������� � ������� �������
        self.letter = letter  # ������� �������
        self.number = 0  # ������� �������
        self.line_count = 0  # ������� �������
        self.max_lines = max_lines  # ������� �������
        #os.chdir(path_sort)  # �����?
        self.create()

    def create(self):  # ����� �������
        self.open('w')

    def open(self, mode='w+'):  # ����� �������
        self.file = open(self.letter + "(" + str(self.number) + ")" + '.txt', mode)

    def close(self):  # ����� �������
        self.file.close()

    def append(self, line):  # ����� �������
        self.file.write(line)
        self.line_count += 1
        if self.line_count >= self.max_lines:
            self.close()
            self.number += 1
            self.line_count = 0
            self.open()


# ��������� [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
def get_big_letters():
    # ������� ord() �������� chr().   >>> ord('A') # 65   >>> chr(65) # 'A'
    for ch in range(ord('A'), ord('Z') + 1):  # ������� ord() ������ �����/������� � ������� Unicode ��� �������� 'A-Z'
        # �������� ����� yield ������������ � �������� ��� ��, ��� � return � ��� ����������� ���������� ������.
        # ������� ����������� � ���, ��� yield ���������� ���������.
        yield chr(ch)  # ������� chr() ������ ������, �������������� ������, �� ������� Unicode


# ��������� [abcdefghijklmnopqrstuvwxyz]
def get_small_letters():
    # ������� ord() �������� chr().   >>> ord('a') # 97      >>> chr(97) # 'a'
    for ch1 in range(ord('a'), ord('z') + 1):  # ������� ord() ������ �����/������� � ������� Unicode ��� �������� 'a-z'
        # �������� ����� yield ������������ � �������� ��� ��, ��� � return � ��� ����������� ���������� ������.
        # ������� ����������� � ���, ��� yield ���������� ���������.
        yield chr(ch1)  # ������� chr() ������ ������, �������������� ������, �� ������� Unicode


# ��������� [0123456789]
def digits():
    # ������� ord() �������� chr().   >>> ord('0') # 48   >>> chr(48) # '0'
    for ch2 in range(ord('0'), ord('9') + 1):  # ������� ord() ������ �����/������� � ������� Unicode ��� �������� '0-9'
        # �������� ����� yield ������������ � �������� ��� ��, ��� � return � ��� ����������� ���������� ������.
        # ������� ����������� � ���, ��� yield ���������� ���������.
        yield chr(ch2)  # ������� chr() ������ ������, �������������� ������, �� ������� Unicode


input_file_name = 'data.txt'
# input_file_rows = 15_000_000
max_lines = 300000_000  # ������������ ���������� ����� � �����
# str_len = 15  # ������������ ���������� �������� � ������
alphabet0 = list(get_big_letters())  # ��������� [ABCDEFGHIJKLMNOPQRSTUVWXYZ] ��������� � ������
alphabet1 = list(get_small_letters())  # ��������� [abcdefghijklmnopqrstuvwxyz] ��������� � ������
alphabet2 = list(digits())  # ��������� [0123456789] ��������� � ������
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

path = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\"  # ������� ��������� ������
path_data = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\data.txt"  # ���� � ����� ���������� data.txt
path_sort = "C:\\Users\\nUser\\Desktop\\Sort_A-Z\\Sort"  # ������� ���������� � ������� 0-9.txt & A-Z.txt

line_count = 0

# input("Press Enter to continue1...")
# print("������� ����������:", os.getcwd())
# os.chdir(path_sort)

if os.path.exists(path_data):  # os.path.exists(path_data) ��������� ���������� �� ���� "C:\\Users\\path_data\\text.txt"
    print("���� data.txt ������")
    files = {}  # �������� ������: ������������ ��� ������ �������(dict), � ������� ������� �� ����� �������� ��� ������
                # dicts = [
                #    {'id': 123, 'name': 'L'},
                #    {'id': 234, 'name': 'K'},
                #    {'id': 345, 'name': 'P'}
                # ]
                # print(dicts[0]['name'])
                # 'L'

    #os.mkdir(path_sort)  # ������� ���������� "C:\\Users\\path_sort"

    #directory_folder = r"C:\\Users\\nUser\\PycharmProjects\\pythonProject5\\test"
    #folder_path = os.path.dirname(directory_folder)  # ���� � ����� � ������
    #if not os.path.exists(folder_path):  # ���� ���� �� ���������� ������� ���
    #    os.makedirs(folder_path)

    print('[1] Create Files')
    os.chdir(path_sort)  # ������� chdir() ������ os �������� ������� ������� ������� �� path_sort ("C:\\Users\\path_sort")

    for ch in alphabet0:  # ������ ���������� [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
        f = LetterFile(ch, max_lines)  # �������� A-Z � �����(LetterFile)
        files[ch] = f

    for ch1 in alphabet1:  # ������ ���������� [abcdefghijklmnopqrstuvwxyz]
        f = LetterFile(ch1, max_lines)  # �������� a-z � �����(LetterFile)
        files[ch1] = f

    for ch2 in alphabet2:  # ������ ���������� [0123456789]
        f = LetterFile(ch2, max_lines)  # �������� 0-9 � �����(LetterFile)
        files[ch2] = f

    print('[2] Process input File')
    os.chdir("..")  # ������� chdir() ������ os �������� ������� ������� ������� �� ".." (����������) ("C:\\Users")

    try:
        er = 0
        with open(input_file_name) as fr:
        #with open(input_file_name, encoding='ascii', errors='ignore') as fr:
            try:
            #    file = open('ok123.txt', 'r')
            except FileNotFoundError as e:
            #    print(e)

            i = 0  # ��� �������� ����� � Symbol
            for s in tqdm(fr.readlines()):
                try:
                    fw = files[s[0].upper()]  # ����� string upper() ����������� ��� ������� ������� �������� � ������ � ������� �������� ��������
                except:
                    i += 1  # ������� ������
                    my_file = open("Symbol.txt", "a")  # ������ ������ ������
                    my_file.write(s)
                    my_file.close()
                fw.append(s)
            print("Error: ����� � ��������!!!", i)
        print('[3] Closing Files')
        os.chdir(path_sort)  # ������� chdir() ������ os �������� ������� ������� ������� �� path_sort ("C:\\Users\\path_sort")

        for ch in alphabet0:
            f = files[ch]
            f.close()

        for ch1 in alphabet1:
            f = files[ch1]
            f.close()

        for ch2 in alphabet2:
            f = files[ch2]
            f.close()
    except:
        # ������� ������ �����
        # file1 = open("C:\\Users\\nUser\\Desktop\\Sort_A-Z\\data.txt", "r")
        # while True:
        #    line = file1.readline()  # ��������� ������
        #    if not line:  # ��������� ����, ���� ������ ������
        #        break
        #    print(line.strip())  # ������� ������
        # file1.close  # ��������� ����

        print("[Error!]�������� �������� Sort � ������.txt")  # ��������� !!! ������� �� ����� �������� ������ � �����, ��� ��� ���� ���� ����� ������ ���������: 'C:\\Users\\nUser\\Desktop\\Sort_A-Z\\Sort\\0(0).txt
        # shutil.rmtree(path_sort)  # ������� rmtree() ������ shutil ���������� ������� ��� ������ ��������� path_sort.



    print('[4] Counting rows Files')
    # input("(Press Enter to continue...)")
    print("=====================================")
    os.chdir(path)  # ������� chdir() ������ os �������� ������� ������� ������� �� ".." (����������) ("C:\\Users")

    with open('data.txt') as f:
        n = 0
        for line in f:
            n += 1
    # print("Data.txt = ", n)
    # line_count_d = line_count - n
    # abc = print(f"����� ����� - Data.txt {line_count_d}")
    # print("=====================================")

    os.chdir(path_sort)  # ������� chdir() ������ os �������� ������� ������� ������� �� path_sort ("C:\\Users\\path_sort")
    # ������� ������ ���� ������ �������� � ���������� ����� � ���
    for file in os.listdir(path_sort):  # ������� listdir() ������ os ���������� ������, ���������� ����� ������ � ���������� � ��������, �������� ����� path.
        if file.endswith(".txt"):  # ������� ������ ������ �� ����������
            if (file == 'data.txt'):  # ���� ��� ����� data.txt
                continue  # �� ��������� ���
            else:  # �����
                local_count = 0
                # ������� �������� ����� ��� �������� ����� � ������ �������
                with open(file) as f:
                    quantity = sum(1 for line in f)

                print(f'{os.path.join(path, file)} - {quantity} �����')
                line_count += quantity
    print("=====================================")
    print("Data.txt = ", n)
    print(f"����� ����� - {line_count}")

else:
    print("���� data.txt �� ������")
