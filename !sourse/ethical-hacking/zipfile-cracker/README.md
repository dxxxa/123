# [How to Crack Zip File Passwords in Python](https://www.thepythoncode.com/article/crack-zip-file-password-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Cracking `secret.zip` file with the password list in `wordlist.txt` file, use the following command:
    ```
    python zip_cracker.py secret.zip wordlist.txt
    ```
- For a bigger list, consider downloading [rockyou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) wordlist.
##
# [[] / []]()
Скажем, вам поручено исследовать компьютер подозреваемого, и вы находите ZIP-файл, который кажется очень полезным, но защищен паролем. В этом учебнике вы напишете простой скрипт Python, который пытается взломать пароль zip-файла с помощью атаки словаря.

Обратите внимание, что в Linux есть более удобные инструменты для взлома zip-файлов, такие как John the Ripper или fcrackzip (в этом уроке показано, как их использовать). Цель этого учебника - сделать то же самое, но с языком программирования Python.

Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python EBook

Мы будем использовать встроенный модуль zipfile Python и стороннюю библиотеку tqdm для быстрой печати индикаторов выполнения:

pip3 install tqdm
Как упоминалось ранее, мы будем использовать словарную атаку, что означает, что нам понадобится список слов для перебора силы этого защищенного паролем zip-файла. Для этого урока мы будем использовать большой список слов rockyou (размером около 133 МБ). Если вы используете Kali Linux, вы можете найти его в /usr/share/wordlists/rockyou.txt.gz пути. В противном случае вы можете скачать его здесь.

Вы также можете использовать инструмент crunch для создания пользовательского списка слов, как вы точно укажете.

Связанные с: Как взломать PDF-файлы в Python.

Откройте новый файл Python и следуйте инструкциям:

import zipfile
from tqdm import tqdm
Давайте укажем наш целевой zip-файл вместе с путем к списку слов:

# the password list path you want to use, must be available in the current directory
wordlist = "rockyou.txt"
# the zip file you want to crack its password
zip_file = "secret.zip"
Чтобы прочитать zip-файл в Python, мы используем zip-файл. Класс ZipFile, который имеет методы для открытия, чтения, записи, закрытия, перечисления и извлечения zip-файлов (здесь мы будем использовать только метод extractall():

# initialize the Zip File object
zip_file = zipfile.ZipFile(zip_file)
# count the number of words in this wordlist
n_words = len(list(open(wordlist, "rb")))
# print the total number of passwords
print("Total passwords to test:", n_words)
Обратите внимание, что мы читаем весь список слов, а затем получаем только количество паролей для тестирования. Это может оказаться полезным для tqdm, чтобы мы могли отслеживать, где мы находимся в процессе грубого форсирования. Вот остальная часть кода:

with open(wordlist, "rb") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit="word"):
        try:
            zip_file.extractall(pwd=word.strip())
        except:
            continue
        else:
            print("[+] Password found:", word.decode().strip())
            exit(0)
print("[!] Password not found, try other wordlist.")
Related: Build 24 Ethical Hacking Scripts & Tools with Python EBook

Since wordlist now is a Python generator, using tqdm won't give much progress information. That's why I introduced the total parameter to give tqdm insight into how many words are in the file.

We open the wordlist and read it word by word, and try it as a password to extract the zip file; reading the entire line will come with the new line character. As a result, we use the strip() method to remove white spaces.

The method extractall() will raise an exception whenever the password is incorrect, so we can proceed to the next password, in that case. Otherwise, we print the correct password and exit the program.

I have edited the code a little to accept the zip and wordlist files from command line arguments. Check it here.

Check my result:

root@rockikz:~# gunzip /usr/share/wordlists/rockyou.txt.gz
root@rockikz:~# python3 zip_cracker.py secret.zip /usr/share/wordlists/rockyou.txt
Total passwords to test: 14344395
  3%|▉                            | 435977/14344395 [01:15<40:55, 5665.23word/s]
[+] Password found: abcdef12345
ОТКАЗ от ответственности: Используйте этот сценарий для файла, к которому у вас есть разрешение на доступ. В противном случае мы не несем ответственности за любое неправомерное использование.

Как вы можете видеть, я нашел пароль после примерно 435 тысяч пробных испытаний, которые заняли около минуты на моей машине. Обратите внимание, что список слов rockyou содержит более 14 миллионов слов, которые являются наиболее часто используемыми паролями, отсортированными по частоте.

Хорошо, мы успешно создали простой, но полезный скрипт, который взламывает пароль zip-файла. Попробуйте использовать гораздо большие списки слов, если вы не смогли взломать его с помощью этого списка.

Если вы хотите создать надежный пароль, убедитесь, что вы используете генератор паролей.

Я настоятельно рекомендую вам использовать несколько потоков, чтобы взломать пароль намного быстрее. Если вам это удастся, пожалуйста, поделитесь своими результатами с нами в комментариях ниже!