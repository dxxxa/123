import string

path_data = "C:\\Users\\user\\PycharmProjects\\ssssssssssort\\data.txt"
path_sort = "C:\\Users\\user\\PycharmProjects\\ssssssssssort\\sort\\"


def create_digits():  # Ascii_Digits = '0123456789'
    print("\nDigits")
    for i in string.digits:
        print("[", i, "]", end=" ")
        open(i + ".txt", "w")


def ascii_uppercase():  # Ascii_Uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print("\nUpper Case Alphabets")
    for i in string.ascii_uppercase:
        print("[", i, "]", end=" ")
        open(i + ".txt", "w")


def ascii_lowercase():  # Ascii_Lowercase = 'abcdefghijklmnopqrstuvwxyz'
    print("\nLower Case Alphabets")
    for i in string.ascii_lowercase:
        print("[", i, "]", end=" ")
