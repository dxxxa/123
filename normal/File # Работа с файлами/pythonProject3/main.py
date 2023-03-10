#!/usr/bin python3

import os
import BCompilationFilterBanner
from BCompilationFilterBanner import style

print(BCompilationFilterBanner.banner)


def emailFilter(file_path, filter_name):
    path = os.path.realpath(file_path)
    with open(path, "rb") as text:
        read = text.read().decode("ansi")
        split = read.split()
        for word in split:
            try:
                if filter_name in word:
                    email_pass = word.split(":")
                    email = email_pass[0]
                    password = email_pass[-1]
                    email_write = open(f"{SaveAs}.txt", "a")
                    email_write.write(f"{email}:{password} \n")
                    email_write.close()
                    print(f"{style.MAGENTA}{email}{style.RED}:{style.GREEN}{password} \n")
                else:
                    pass
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            except UnicodeEncodeError:
                print("UnicodeEncodeError")
            except Exception as e:
                print(e)
        CWD = os.getcwd()
        print(f"{style.CYAN}File saved in {CWD}\\{SaveAs}.txt")


FilePath = input(f"{style.CYAN}[+]Enter path for file to filter from: ")
print(f'{style.YELLOW}Filter Example: "email", "yahoo", "rambler","mail",<target name>, etc...')
FilterName = input(f"{style.CYAN}[+]Enter filter type: ")
SaveAs = input("SaveAs: ")
emailFilter(FilePath, FilterName)