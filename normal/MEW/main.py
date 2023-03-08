import os  # cleaning the terminal   # os.system('cls')
# import sys
# import pytz
# from datetime import datetime
from time import time, strftime, localtime  # time для счетчика

# GENERATE ETH
import random  # 1   #   random number generation   # [4] Random Check
import secp256k1Crypto  # 2   # pip install secp256k1Crypto
from Crypto.Hash import keccak  # 3   # pip install pycryptodome
import hashlib

# PARSING #
import requests

# GENERATE #
# PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + ("\\" if sys.platform == "win32" else "/")

MAX_PRIVATE_KEY = "115792089237316195423570985008687907852837564279074904382605163141518161494336"


def info():
    print("Max BINary  : \n"
          "Max DECimal : 115792089237316195423570985008687907852837564279074904382605163141518161494336\n"
          "Max HEXadec : \n"
          "Max Text    : ... symbol\n"
          "Max PRIV-Key: fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140\n"
          "Max PUB-Key : 0x80C0dbf239224071c59dD8970ab9d542E3414aB2\n")


file_name = "Output_" + str(strftime("%d%b_%H-%M-%S", localtime())) + ".txt"


def set_file_name(new_file_name):
    global file_name
    file_name = new_file_name


##################################################################################################
# ######################################## [1] Check One #########################################
# [1] Check One /// [1] BINary to WIF #
def bin_convert(arg):
    bin0 = arg
    # bin0 = input("BINary to WIF\n>>>")
    bin_to_dec = int(bin0, 2)
    bin_to_hex = hex(int(bin0, 2))
    print("DECimal  : ", bin_to_dec, "\nHEXadecimal : ", bin_to_hex, "\nBINary : ", bin0)
    print("----------------")
    return bin_to_dec


# [1] Check One /// [2] DECimal to WIF #
def dec_convert(arg):
    dec = arg
    # dec = int(input("DECimal to WIF\n>>>"))
    dec_to_hex = hex(int(dec))
    dec_to_bin = bin(int(dec))
    print("DECimal  : ", dec, "\nHEXadecimal : ", dec_to_hex, "\nBINary : ", dec_to_bin)
    print("----------------")
    return dec


# [1] Check One /// [3] HEXadecimal to WIF #
def hex_convert(arg):
    hex0 = arg
    # hex0 = input("HEXadecimal to WIF\n>>>")
    hex_to_dec = int(hex0, 16)
    hex_to_bin = bin(int(hex0, 16))
    print("DECimal  : ", hex_to_dec, "\nHEXadecimal : ", hex0, "\nBINary : ", hex_to_bin)
    print("----------------")
    return hex_to_dec


# [1] Check One / CONVERTING / [4] Text to WIF #
def text_convert(text):
    # text = input("Text to WIF\n>>>")
    text2 = text.encode('utf-8')
    hash_object = hashlib.sha256(text2)
    hex_dig = hash_object.hexdigest()
    # print(hex_dig)  # bitcoin is awesome   to   23d4a09295be678b21a5f1dceae1f634a69c1b41775f680ebf8165266471401b
    return hex_dig


# [1] Check One / GENERATE ETH / [5] PRIV-Key #
def private_to_dec(priv_k):
    return int(priv_k, 16)


# [1] Check One / GENERATE ETH / [5] PRIV-Key #
def dec_to_eth_address(arg):
    global PRIV_Key
    PRIV_Key = arg.to_bytes(32, byteorder='big').hex()
    global priv_key_to_dec
    priv_key_to_dec = int(PRIV_Key, 16)
    # 1)secp256k1Crypto используется для генерации открытого ключа
    # 2)Затем преобразуйте закрытый ключ в открытый ключ
    private_key = bytes.fromhex(PRIV_Key)
    privkey = secp256k1Crypto.PrivateKey(private_key)
    privkey.pubkey.serialize(compressed=False).hex()
    # 04dfa13518ff965498743f3a01439dd86bc34ff9969c7a3f0430bbf8865734252953c9884af787b2cadd45f92dff2b81e21cfdf98873e492e5fdc07e9eb67ca74d

    # 3 Вычислить хеш-значение открытого ключа # Использовать алгоритм хеширования keccak256
    # Удалите 04 из начала открытого ключа,
    # преобразуйте оставшуюся часть в байтовую строку и используйте алгоритм keccak256 для хеширования:
    keccak_hash = keccak.new(digest_bits=256)
    public_key = privkey.pubkey.serialize(compressed=False).hex()[2:]
    # '04dfa13518ff965498743f3a01439dd86bc34ff9969c7a3f0430bbf8865734252953c9884af787b2cadd45f92dff2b81e21cfdf98873e492e5fdc07e9eb67ca74d'[2:]
    public_key = bytes.fromhex(public_key)
    keccak_hash.update(public_key)  # <Crypto.Hash.keccak.Keccak_Hash object at 0x102960588>
    h = keccak_hash.hexdigest()  # 39c0eb3b26d4838930b1f34babcd68033a72978c1084e2d44d1fa06ddc4a2d57

    # 4 Получить окончательный адрес Ethereum:
    # Берутся последние 40 букв шестнадцатеричной строки хеш-значения и добавьте 0x в начале
    eth_address = "0x" + h[-40:]
    print("Ethereum Address\nPRIV-Key :", PRIV_Key, "\nPUB-Key  :", eth_address)  # ВЫВОД в ЛОГ
    print("----------------")
    return eth_address


# [1] Check One / [6] PUB-Key #
def pub_key(pub_k):
    inp = pub_k
    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={inp}")
    tr = r.text[13:-4].split("\"},{\"")
    for i in tr:
        print(i[11:53], int(i[66:], 16))


##################################################################################################
# ########################################### PARSING ############################################
def network(arg, arg2):  # Controller   PARSING #
    eth_net_mew(arg, arg2)  # PARSING   ETHEREUM   NETWORK #
    bsc_net_mew(arg, arg2)  # PARSING   Binance Smart Chain   NETWORK #
    matic_net_mew(arg, arg2)  # PARSING   Polygon (MATIC)   NETWORK #
    # all_net_mew(arg, arg2)  # PARSING   ALL   NETWORK #


# PARSING   ETHEREUM   NETWORK #
def eth_net_mew(arg, arg2):
    address = arg
    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={address}")
    tr = r.text[13:-4].split("\"},{\"")
    print("[Ethereum (Eth)]  Contracts :")
    wsum = 0
    for i in tr:
        print(i[11:53], int(i[66:], 16))
        value = int(i[66:], 16)
        wsum += value
    if wsum != 0:
        if arg2 == 1:
            txt_name = "[1]One_Output.txt"
        elif arg2 == 2:
            txt_name = f"[2]List_{file_name}.txt"
        elif arg2 == 3:
            txt_name = f"[3]Range_{file_name}.txt"
        elif arg2 == 4:
            txt_name = f"[4]Random_{file_name}.txt"
        file = open(txt_name, "a")
        file.write(f"DECimal  : {priv_key_to_dec}\nPRIV-Key : {PRIV_Key}\nPUB-Key  : {address}\n\n")
        file.write("[Ethereum (Eth)]  Contracts :\n")
        for i in tr:
            wallet = i[11:53]
            value = int(i[66:], 16)
            wsum += value
            if value > 0:
                file.write(wallet + " " + str(value) + "\n")
        file.write("---------------------------------------------------------------\n\n")
    print("---------------------------------------------------------------")


# PARSING   Binance Smart Chain   NETWORK #
def bsc_net_mew(arg, arg2):
    address = arg
    r = requests.get(f"https://tokenbalance.mewapi.io/bsc?address={address}")
    tr = r.text[13:-4].split("\"},{\"")
    print("[Binance Smart Chain (BSC)]  Contracts :")
    wsum = 0
    for i in tr:
        print(i[11:53], int(i[66:], 16))
        value = int(i[66:], 16)
        wsum += value
    if wsum != 0:
        if arg2 == 1:
            txt_name = "[1]One_Output.txt"
        elif arg2 == 2:
            txt_name = f"[2]List_{file_name}.txt"
        elif arg2 == 3:
            txt_name = f"[3]Range_{file_name}.txt"
        elif arg2 == 4:
            txt_name = f"[4]Random_{file_name}.txt"
        file = open(txt_name, "a")
        file.write(f"DECimal  : {priv_key_to_dec}\nPRIV-Key : {PRIV_Key}\nPUB-Key  : {address}\n\n")
        file.write("[Binance Smart Chain (BSC)]  Contracts :\n")
        for i in tr:
            wallet = i[11:53]
            value = int(i[66:], 16)
            wsum += value
            if value > 0:
                file.write(wallet + " " + str(value) + "\n")
        file.write("---------------------------------------------------------------\n\n")
    print("---------------------------------------------------------------")


# PARSING   Polygon (MATIC)   NETWORK #
def matic_net_mew(arg, arg2):
    address = arg
    r = requests.get(f"https://tokenbalance.mewapi.io/matic?address={address}")
    tr = r.text[13:-4].split("\"},{\"")
    print("[Polygon (Matic)]  Contracts :")
    wsum = 0
    for i in tr:
        print(i[11:53], int(i[66:], 16))
        value = int(i[66:], 16)
        wsum += value
    if wsum != 0:
        if arg2 == 1:
            txt_name = "[1]One_Output.txt"
        elif arg2 == 2:
            txt_name = f"[2]List_{file_name}.txt"
        elif arg2 == 3:
            txt_name = f"[3]Range_{file_name}.txt"
        elif arg2 == 4:
            txt_name = f"[4]Random_{file_name}.txt"
        file = open(txt_name, "a")
        file.write(f"DECimal  : {priv_key_to_dec}\nPRIV-Key : {PRIV_Key}\nPUB-Key  : {address}\n\n")
        file.write("[Polygon (Matic)]  Contracts :\n")
        for i in tr:
            wallet = i[11:53]
            value = int(i[66:], 16)
            wsum += value
            if value > 0:
                file.write(wallet + " " + str(value) + "\n")
        file.write("---------------------------------------------------------------\n\n")
    print("---------------------------------------------------------------")


# PARSING   ALL   NETWORK #
def all_net_mew(arg, arg2):
    address = arg
    my_list = ['eth', 'bsc', 'matic']
    my_listt = my_list
    my_listt = ['Ethereum', 'Binance Smart Chain', 'Polygon (Matic)']
    for ii in range(0, 3):
        third_elem = my_list[ii]
        r = requests.get(f"https://tokenbalance.mewapi.io/{third_elem}?address={address}")
        tr = r.text[13:-4].split("\"},{\"")
        if ii == 0:
            print("[Ethereum (Eth)]  Contracts :")
        elif ii == 1:
            print("[Binance Smart Chain (BSC)]  Contracts :")
        elif ii == 2:
            print("[Polygon (Matic)]  Contracts :")
        wsum = 0
        for i in tr:
            # print(i[11:53], int(i[66:], 16))
            value = int(i[66:], 16)
            wsum += value
        if wsum != 0:
            if arg2 == 1:
                txt_name = "[1]One_Output.txt"
            elif arg2 == 2:
                txt_name = f"[2]List_{file_name}.txt"
            elif arg2 == 3:
                txt_name = f"[3]Range_{file_name}.txt"
            elif arg2 == 4:
                txt_name = f"[4]Random_{file_name}.txt"
            file = open(txt_name, "a")
            file.write(f"DECimal  : {priv_key_to_dec}\nPRIV-Key : {PRIV_Key}\nPUB-Key  : {address}\n\n")
            file.write(f"{my_listt[ii]} :\n")
            for i in tr:
                wallet = i[11:53]
                value = int(i[66:], 16)
                wsum += value
                if value > 0:
                    file.write(wallet + " " + str(value) + "\n")
            file.write("---------------------------------------------------------------\n")
        print("---------------------------------------------------------------")


##################################################################################################
# ####################################### [2] Check List #########################################
def check_list_inp():
    try:
        f = open("[2]List_INPUT.txt")
        f.close()
    except FileNotFoundError:
        print("[2]List_INPUT.txt ОТСУТСТВУЕТ!")
        main()
    print("[2]List_INPUT.txt СУЩЕСТВУЕТ!")
    # file2 = open(PROJECT_PATH + "input.txt", "r")
    file2 = open("[2]List_INPUT.txt", "r")
    for line in file2.readlines():
        # file = open(PROJECT_PATH + "output.txt", "a")
        dec = int(line.strip())
        dec_convert(dec)
        addr = dec_to_eth_address(dec)
        prename_write_file = 2
        network(addr, prename_write_file)


##################################################################################################
# ##################################### [5] Delete Output ########################################
def clear_files():
    # clear_files()
    print("Delete all OUTPUT.txt files?")
    yes = 'y' in input("(Y)es/(N)o: ").lower().strip()
    if not yes:
        print("Not confirmed")
        main()
    print('Deleting all .txt files')
    files_in_directory = os.listdir()
    # files_in_directory = os.listdir(os.getcwd())
    # files_in_directory = os.listdir(PROJECT_PATH)
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        if file not in ("[2]List_INPUT.txt", "[3]Range_Check_CHANGE.txt"):
            path_to_file = os.path.join(file)
            # path_to_file = os.path.join(os.getcwd(), file)
            # path_to_file = os.path.join(PROJECT_PATH, file)
            os.remove(path_to_file)
    main()
##################################################################################################
##################################################################################################
# Добавить генерацию адреса из текста

# Добавить пункт проверки и вывода какие ововещения включены
# Добавить оповещение звуковое(сигнал),email,telegram,смс

# Добавить лого при запуске?

# Добавить цветной текст?

# 3 и 4 режимы нет кнопки назад и выход
##################################################################################################
# ########################################### MENU ###############################################


def main():
    print("\nChecker MEW"
          "\n[1] Check One"
          "\n[2] Check List"
          "\n[3] Check Range"
          "\n[4] Check Random"
          "\n"
          "\n[5] Delete Output"
          "\n[q] Quit\n")

    x = input(">>> ")
    if x == "q":  # [q] Quit
        exit(0)

# ##[1] Check One ########
    elif x == "1":
        # os.system('cls')
        print("\nCheck One"
              "\n[1] BINary to WIF"
              "\n[2] DECimal to WIF"
              "\n[3] HEXadecimal to WIF\n"
              "\n[4] Text to WIF\n"
              "\n[5] PRIV-Key"
              "\n[6] PUB-Key\n"
              "\n[b] Back"
              "\n[q] Quit\n")
        y = input(">>> ")
        if y == "q":  # [q] Quit
            exit(0)

        # ##### [1] Check One /// [1] BINary to WIF ########
        elif y == "1":
            bin0 = input("BINary to WIF\n>>>")
            deca = bin_convert(bin0)
            addr = dec_to_eth_address(deca)
            prename_write_file = 1
            network(addr, prename_write_file)
            main()

        # ##### [1] Check One /// [2] DECimal to WIF ########
        elif y == "2":
            dec = int(input("DECimal to WIF\n>>>"))
            t = time()
            dec_convert(dec)
            deca = dec
            addr = dec_to_eth_address(deca)
            prename_write_file = 1
            network(addr, prename_write_file)
            t2 = time()
            print(f"Time: {t2 - t}")
            main()

        # ##### [1] Check One /// [3] HEXadecimal to WIF ########
        elif y == "3":
            hex0 = input("HEXadecimal to WIF\n>>>")
            deca = hex_convert(hex0)
            addr = dec_to_eth_address(deca)
            prename_write_file = 1
            network(addr, prename_write_file)
            main()

        # ##### [1] Check One /// [4] Text to WIF ########
        elif y == "4":
            text = input("Text to WIF\n>>>")
            text_hex_dig = text_convert(text)
            deca = hex_convert(text_hex_dig)
            addr = dec_to_eth_address(deca)
            prename_write_file = 1
            network(addr, prename_write_file)
            main()

        # ##### [1] Check One /// [5] PRIV-Key ########
        elif y == "5":
            priv_k = input("PRIV-Key :>>> ").strip()  # 000000000000000000000000000000000000000000000000000000000000000a
            t = time()
            deca = private_to_dec(priv_k)  # 000000000000000000000000000000000000000000000000000000000000000a to 10
            dec_convert(deca)
            addr = dec_to_eth_address(deca)
            prename_write_file = 1
            network(addr, prename_write_file)
            t2 = time()
            print(f"Time: {t2 - t}")
            main()

        # ##### [1] Check One /// [6] PUB-Key ########
        elif y == "6":
            pub_k = input("PUB-Key :>>> ").strip()
            t = time()
            pub_key(pub_k)
            t2 = time()
            print(f"Time: {t2 - t}")
            main()

        elif y == "b":
            # os.system('cls')
            main()
        else:
            print("Command not Recognized")

    # [2] Check List #
    elif x == "2":
        os.system('cls')
        set_file_name("Output_" + str(strftime("%d-%b_%H-%M-%S", localtime())) + ".txt")
        print("MyEtherWallet | Check List")
        print("------------- the Starting of   [2] Checks List ---------------")
        t = time()
        check_list_inp()
        t2 = time()
        print("------------- the Completion of [2] Checks List ---------------")
        print(f"Time :>>> {t2 - t}")
        main()

    # [3] Check Range #
    elif x == "3":
        os.system('cls')
        print("MyEtherWallet | Check Ranges | 0 <---> 2^256\n")
        set_file_name("Output_" + str(strftime("%d-%b_%H-%M-%S", localtime())) + ".txt")
        while True:
            info()
            r1 = int(input("Input Starting Range :>>> "))
            r2 = int(input("Input Ending Range   :>>> "))
            print("------------- the Starting of   [3] Checks Ranges -------------")
            t = time()
            change_file = open("[3]Range_Check_CHANGE.txt", "a")
            change_file.write(f"{file_name}   Range: {r1} to {r2}\n")
            change_file.close()
            for x in range(r1, r2):
                dec_convert(x)
                addr = dec_to_eth_address(x)
                prename_write_file = 3
                network(addr, prename_write_file)
                if x == (r2 - 1):
                    print(f"------------ the Completion of   [3] Checks Ranges ------------"
                          f"\nStarting Range :>>> {r1}"
                          f"\nEnding Range   :>>> {r2}")
            t2 = time()
            print(f"Time :>>> {t2 - t}")
            main()

    # [4] Check Random #
    elif x == "4":
        os.system('cls')
        print("MyEtherWallet | [4] Check Random | 0 <---> 2^256")
        info()
        set_file_name("Output_" + str(strftime("%d-%b_%H-%M-%S", localtime())) + ".txt")
        while True:
            r1 = int(input("Input Starting Range :>>> "))
            r2 = int(input("Input Ending Range   :>>> "))
            r3 = int(input("Input Num Iteration  :>>> "))
            print("------------- the Starting of   [4] Checks Random -------------")
            t = time()
            for x in range(r3):
                i = random.randint(r1, r2)  # (0, 2 ** 256) default
                dec_convert(i)
                addr = dec_to_eth_address(i)
                prename_write_file = 4
                network(addr, prename_write_file)
                if x == (r3 - 1):
                    print(f"------------ the Completion of   [4] Checks Random ------------"
                          f"\nStarting Range Random :>>> {r1}"
                          f"\nEnding Range Random   :>>> {r2}"
                          f"\nNum Iteration         :>>> {r3}")
            t2 = time()
            print(f"Time :>>> {t2 - t}")
            main()

    # [5] Delete Output #
    elif x == "5":
        clear_files()

    else:
        print("Command not Recognized")
        main()


main()














# ######################################################################################################
#
# if __name__ == '__main__':
#    main()


# def private_to_public(private_key):
#    private_key = bytes.fromhex(private_key.strip())
#    privkey = secp256k1Crypto.PrivateKey(private_key)
#    privkey.pubkey.serialize(compressed=False).hex()
#    keccak_hash = keccak.new(digest_bits=256)
#    public_key = privkey.pubkey.serialize(compressed=False).hex()[2:]
#    public_key = bytes.fromhex(public_key)
#    keccak_hash.update(public_key)
#    h = keccak_hash.hexdigest()
#    public_key = '0x' + h[-40:]
#    return public_key


# def priv_check(PRIV_Key):
#    private_key = PRIV_Key
#    private_key = bytes.fromhex(private_key)
#    privkey = secp256k1Crypto.PrivateKey(private_key)
#    privkey.pubkey.serialize(compressed=False).hex()
#    keccak_hash = keccak.new(digest_bits=256)
#    public_key = privkey.pubkey.serialize(compressed=False).hex()[2:]
#    public_key = bytes.fromhex(public_key)
#    keccak_hash.update(public_key)
#    h = keccak_hash.hexdigest()
#    address = '0x' + h[-40:]

#    inp = (address).strip()
#    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={inp}")
#    tr = r.text[13:-4].split("\"},{\"")
#    wsum = 0
#    for i in tr:
#        value = int(i[66:], 16)
#        wsum += value
#    if wsum != 0:
#        print(f"PUB-Key : {inp}")
#        for i in tr:
#            wallet = i[11:53]
#            value = i
#            nt(i[66:], 16)
#            wsum += value
#            if value > 0:
#                print(wallet + " " + str(value))
#        print("\n")
#######################################################################################################
# with open(PROJECT_PATH + file_name, "a") as file:
#    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={public_key}")
#    tr = r.text[13:-4].split("\"},{\"")
#    wsum = 0
#    for i in tr:
#        print(i[11:53], int(i[66:], 16))  # ОТОБРАЖЕНИЕ БАЛАНСА
#        value = int(i[66:], 16)
#        wsum += value
#    if wsum != 0:
#        file.write(f"DECimal : {number}\nPRIV-Key : {private_key}\nPUB-Key : {public_key}\n")
#        for i in tr:
#            wallet = i[11:53]
#            value = int(i[66:], 16)
#            wsum += value
#            if value > 0:
#                file.write(wallet + " " + str(value) + "\n")
#        file.write("\n\n")
#########################################################################
# def test(public_key, key_number, private_key):
# with open(PROJECT_PATH + file_name, "a") as file:
#    with open(file_name, "a") as file:
#        r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={public_key}")
#        tr = r.text[13:-4].split("\"},{\"")
#        wsum = 0
#        for i in tr:
#            value = int(i[66:], 16)
#            wsum += value
#        if wsum != 0:
#            file.write(f"DECimal : {key_number}\nPRIV-Key : {private_key}\nPUB-Key : {public_key}\n")
#            for i in tr:
#                wallet = i[11:53]
#                value = int(i[66:], 16)
#                wsum += value
#                if value > 0:
#                    file.write(wallet + " " + str(value) + "\n")
#            file.write("\n\n")


#  [2] Check List
#    elif x == "2":
#        # os.system('cls')  # Clear scr
#        while True:
#            print("MyEtherWallet | Check List")
#            st_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#            t = time()
#            check_list_all_mew()
#            # dec_to_eth_address(x)
#            # eth_net_mew()
#            # bsc_net_mew()
#            # matic_net_mew()
#            t2 = time()
#            end_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#            print(f"\n"
#                  f"      Time : {t2 - t}\n"
#                  f"Start Time : {st_time}\n"
#                  f"End   Time : {end_time}\n"
#                  f"-----------------------------------------------\n")


#    # [3] Check Range
#    elif x == "3":
#        # os.system('cls')  # Clear scr
#        print("MyEtherWallet | Check Range")
#        r1 = int(input("Input Starting Range :>>> "))
#        r2 = int(input("Input Ending Range   :>>> "))
#        st_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#        t = time()
#        #change_file = open(PROJECT_PATH + "changes.txt", "a")
#        change_file = open("changes.txt", "a")
#        change_file.write(f"{file_name}   Range: {r1} to {r2}\n")
#        change_file.close()
#        for x in range(r1, r2):
#            dec_to_address(x)
#            # dec_to_eth_address(x)
#            # eth_net_mew()
#            # bsc_net_mew()
#            # matic_net_mew()
#        t2 = time()
#        end_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#        print(f"\n"
#              f"Start : {r1}\n"
#              f"End   : {r2}\n"
#              f"Subtraction : {r2 - r1}")  # Subtraction - Вычисление/вычитание
#        print(f"\n"
#              f"      Time : {t2 - t}\n"
#              f"Start Time : {st_time}\n"
#              f"End   Time : {end_time}\n"
#              f"-----------------------------------------------\n")
#        main()


# [4] Check Random
#    elif x == "4":
#        # os.system('cls')  # Clear scr
#        while True:
#            print("MyEtherWallet | Check Random | 0 <---> 2^256\n")
#            r1 = int(input("Input Starting Range :>>> "))
#            r2 = int(input("Input Ending Range   :>>> "))
#            r3 = int(input("Input Number         :>>> "))
#           #change_file = open(PROJECT_PATH + "changes.txt", "a")         # На компе неправильный путь использует!!!
#            change_file = open("changes.txt", "a")                         # На компе неправильный путь использует!!!
#            change_file.write(f"{file_name}   Random: {r1} to {r2}, count - {r3}\n")
#            change_file.close()
#            st_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#            t = time()
#            for x in range(r3):
#                i = random.randint(r1, r2)  # (0, 2 ** 256) default
#                dec_to_address(i)
#                # dec_to_eth_address(i)
#                # eth_net_mew()
#                # bsc_net_mew()
#                # matic_net_mew()
#            t2 = time()
#            end_time = datetime.fromtimestamp(time(), pytz.timezone("Europe/Moscow")).strftime("%A, %B %d, %Y %H:%M:%S")
#            print(f"\n"
#                  f"      Time : {t2 - t}\n"
#                  f"Start Time : {st_time}\n"
#                  f"End   Time : {end_time}\n"
#                  f"-----------------------------------------------\n")
#            main()
