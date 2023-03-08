import os

import random
import sys
from datetime import datetime
from time import time, strftime, localtime


import requests
import secp256k1Crypto
from Crypto.Hash import keccak

SAMPLE_OUTPUT = "MyEtherWallet | MEW\n" \
                "[1] Check One\n" \
                "[2] Check List\n" \
                "[3] Check Range\n" \
                "[4] Check Random\n\n" \
                "[5] Delete Output\n" \
                "[q] Quit\n"
MAX_PRIVATE_KEY = ("fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140",
                   "0x80C0dbf239224071c59dD8970ab9d542E3414aB2",
                   "115792089237316195423570985008687907852837564279074904382605163141518161494336")
PROJECT_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + ("\\" if sys.platform == "win32" else "/")
file_name = "Output_" + str(strftime("%d-%b_%H-%M-%S", localtime())) + ".txt"


def private_to_public(private_key):
    private_key = bytes.fromhex(private_key.strip())
    privkey = secp256k1Crypto.PrivateKey(private_key)
    privkey.pubkey.serialize(compressed=False).hex()
    keccak_hash = keccak.new(digest_bits=256)
    public_key = privkey.pubkey.serialize(compressed=False).hex()[2:]
    public_key = bytes.fromhex(public_key)
    keccak_hash.update(public_key)
    h = keccak_hash.hexdigest()
    public_key = '0x' + h[-40:]
    return public_key


def private_to_dec(private_key):
    return int(private_key, 16)


def dec_to_address(number):
    print("DECimal  :", number)
    private_key = number.to_bytes(32, byteorder='big').hex()
    # print("PRIV-Key :", private_key)
    public_key = private_to_public(private_key)
    # print("PUB-Key  :", public_key, '\n')
    test(public_key, number, private_key)


def get_request_time():
    time1 = time()
    r = requests.get(
        f"https://tokenbalance.mewapi.io/eth"
        f"?address=0000000000000000000000000000000000000000000000000000000000000001").text
    r2 = requests.get(
        f"https://tokenbalance.mewapi.io/eth"
        f"?address=6af0b900e08e30a56e4f26e3f467627af4206808670c53b75a729264ddb7d450").text
    time2 = time()
    return (time2 - time1) / 2


def test(public_key, key_number, private_key):
    with open(PROJECT_PATH + file_name, "a") as file:
        r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={public_key}")
        tr = r.text[13:-4].split("\"},{\"")
        wsum = 0
        for i in tr:
            value = int(i[66:], 16)
            wsum += value
        if wsum != 0:
            file.write(f"DECimal : {key_number}\nPRIV-Key : {private_key}\nPUB-Key : {public_key}\n")
            for i in tr:
                wallet = i[11:53]
                value = int(i[66:], 16)
                wsum += value
                if value > 0:
                    file.write(wallet + " " + str(value) + "\n")
            file.write("\n\n")


def private_check(private_key):
    t = time()
    public_key = private_to_public(private_key)
    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={public_key}")
    tr = r.text[13:-4].split("\"},{\"")
    wsum = 0
    for i in tr:
        value = int(i[66:], 16)
        wsum += value
    wallets = []
    values = []
    if wsum != 0:
        for i in tr:
            wallet = i[11:53]
            value = i
            wsum += int(value[66:], 16)
            if int(value[66:], 16) > 0:
                wallets.append(wallet)
                values.append(int(value[66:], 16))
    t2 = time()
    t_res = t2 - t
    return public_key, wallets, values, t_res


def single_mew(public_key):
    r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={public_key}")
    tr = r.text[13:-4].split("\"},{\"")
    for i in tr:
        print(i[11:53], int(i[66:], 16))


def check_list_all_mew():
    t = time()
    file2 = open(PROJECT_PATH + "input.txt", "r")
    for line in file2.readlines():
        file = open(PROJECT_PATH + "output.txt", "a")
        inp = line.strip()
        r = requests.get(f"https://tokenbalance.mewapi.io/eth?address={inp}")
        tr = r.text[13:-4].split("\"},{\"")
        wsum = 0
        for i in tr:
            value = int(i[66:], 16)
            wsum += value
        if wsum != 0:
            file.write(f"Wallet: {inp}" + "\n")
            for i in tr:
                wallet = i[11:53]
                value = int(i[66:], 16)
                wsum += value
                if value > 0:
                    file.write(wallet + " " + str(value) + "\n")
            file.write("\n\n")
    t2 = time()
    print(t2 - t)


def range_check(r_time):
    print("MyEtherWallet | Check Range")
    r1 = int(input("Input Starting Range :>>> "))
    r2 = int(input("Input Ending Range   :>>> "))
    t = time()
    h_time = datetime.fromtimestamp(r_time * (r2 - r1) + time()).strftime("%A, %B %d, %Y %I:%M:%S")
    print(f"Time Remaining: {h_time}")
    change_file = open(PROJECT_PATH + "changes.txt", "a")
    change_file.write(f"{file_name}   Range: {r1} to {r2}\n")
    change_file.close()
    for x in range(r1, r2):
        dec_to_address(x)
    print(datetime.fromtimestamp(time()).strftime("%A, %B %d, %Y %I:%M:%S"))
    t2 = time()
    print(t2 - t)


def random_check():
    print("MyEtherWallet | Check Random | 0<--->2^256")
    r1 = int(input("Input Starting Range :>>> "))
    r2 = int(input("Input Ending Range   :>>> "))
    r3 = int(input("Input Number         :>>> "))
    change_file = open(PROJECT_PATH + "changes.txt", "a")
    change_file.write(f"{file_name}   Random: {r1} to {r2}, count - {r3}\n")
    change_file.close()
    t = time()
    for x in range(r3):
        i = random.randint(r1, r2)  # (0, 2 ** 256) default
        dec_to_address(i)
    t2 = time()
    print(t2 - t)


def clear_files():
    yes = 'y' in input("(Y)es/(N)o: ").lower().strip()
    if not yes:
        print("Not confirmed")
    print('Deleting all .txt files')
    files_in_directory = os.listdir(PROJECT_PATH)
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        if file not in ("input.txt", "changes.txt"):
            path_to_file = os.path.join(PROJECT_PATH, file)
            os.remove(path_to_file)


def list_check():
    print("MyEtherWallet | Check List")
    t = time()
    check_list_all_mew()
    t2 = time()
    print(f"Time: {t2 - t}")


def single_pub(public_key):
    t = time()
    single_mew(public_key)
    t2 = time()
    print(f"Time: {t2 - t}")


def single_dec(dec_number):
    t = time()
    dec_to_address(dec_number)
    t2 = time()
    print(f"Time: {t2 - t}")
