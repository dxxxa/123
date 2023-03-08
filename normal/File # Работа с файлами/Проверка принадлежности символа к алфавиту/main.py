import string

#>>> help(string)
#DATA
#    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
#    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    digits = '0123456789'
#    hexdigits = '0123456789abcdefABCDEF'
#    octdigits = '01234567'
#    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
#    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
#    whitespace = ' \t\n\r\x0b\x0c'

#
# ascii_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
print(list(range(ord('A'), ord('Z')+1)) + list(range(ord('a'), ord('z')+1)))
# ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print(list(map(chr, range(ord('A'), ord('Z')+1))))
# ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
print(list(map(chr, range(ord('a'), ord('z')+1))))

print("\n\n\n")


# ascii_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def CaseAlphabets():
    print("\nCase Alphabets")
    for i in list(range(ord('A'), ord('Z') + 1)) + list(range(ord('a'), ord('z') + 1)):
        print(chr(i), end=" ")


print("Alphabets (65, 91) & (97, 123)")


# ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def upperCaseAlphabets():
    print("\nUpper Case Alphabets")
    for i in range(65, 91):
        print(chr(i), end=" ")


# ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
def lowerCaseAlphabets():
    print("\nLower Case Alphabets")
    for i in range(97, 123):
        print(chr(i), end=" ")


CaseAlphabets()
upperCaseAlphabets()
lowerCaseAlphabets()
print("\n\n\n")



# ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print("\nUpper Case Alphabets")
for i in string.ascii_uppercase:
    print(i, end=" ")

# ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
print("\nLower Case Alphabets")
for i in string.ascii_lowercase:
    print(i, end=" ")

print("\n\n\n")



# Generating a list of Alphabets in Python
print("\nGenerating a list of Alphabets in Python")
# initialize an empty list that will contain all the capital alphabets
alphabets_in_capital = []
for i in range(65, 91):
    alphabets_in_capital.append(chr(i))
print(alphabets_in_capital)

# initialize an empty list that will contain all the lowercase alphabets
alphabets_in_lowercase = []
for i in range(97, 123):
    alphabets_in_lowercase.append(chr(i))
print(alphabets_in_lowercase)



# Python Alphabet using list comprehension
print("\nPython Alphabet using list comprehension")
var = 'A'
alphabets = []
# starting from the ASCII value of 'A' and keep increasing the value by i
alphabets = [(chr(ord(var)+i)) for i in range(26)]
print(alphabets)

var = 'a'
alphabets = []
# starting from the ASCII value of 'a' and keep increasing the value by i
alphabets = [(chr(ord(var)+i)) for i in range(26)]
print(alphabets)



# Python Alphabet using map function
print("\nPython Alphabet using map function")
# make a list of numbers from 65-91 and then map(convert) it into # characters.
alphabet = list(map(chr, range(65, 91)))
print(alphabet)

alphabet = list(map(chr, range(97, 123)))
print(alphabet)

alphabets = list(map(chr, range(ord('A'), ord('Z')+1)))
print(alphabets)

alphabets = list(map(chr, range(ord('a'), ord('z')+1)))
print(alphabets)



# Importing the String Module
print("\nImporting the String Module")
# Импорт строкового модуля
import string
# [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
uppercase_alphabets = list(string.ascii_uppercase)
print(uppercase_alphabets)

# [abcdefghijklmnopqrstuvwxyz]
lowercase_alphabets = list(string.ascii_lowercase)
print(lowercase_alphabets)

# [abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]
alphabets = list(string.ascii_letters)
print(alphabets)

# [0123456789]
digits = list(string.digits)
print(digits)

# ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
punctuation = list(string.punctuation)
print(punctuation)





# Как проверить, является ли символ алфавитом или нет в Python
# Python Program to Check Alphabet
print("\nPython Program to Check Alphabet")
ch = input("Enter a character: ")
if ((ch>='A' and ch<= 'Z') or (ch>='a' and ch<='z')):
    print(ch, "is an Alphabet")
else:
    print(ch, "is not an Alphabet")



