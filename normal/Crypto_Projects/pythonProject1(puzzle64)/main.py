# Испытайте удачу, найдя закрытый ключ для Puzzle64 16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN

# Закрытые ключи генерируются случайным образом в пространстве ключей 8000000000000000:ffffffffffffffff,
# закрытые ключи преобразуются в соответствующие открытые ключи для адреса.
# Если найден ключ, начинающийся с 16jY7qLJnx, он сохранит результат в текстовом файле boom.txt.


# Keyspace Puzzle 64 Random
# https://github.com/xh0st/keyspace64

try:
    import random
    from bitcoin import *
    from colorama import init, Fore, Back
    from termcolor import colored

# If required imports are unavailable, we will attempt to install them!

except ImportError:
    import subprocess

    subprocess.check_call(["python3", '-m', 'pip', 'install', 'bitcoin'])
    subprocess.check_call(["python3", '-m', 'pip', 'install', 'colorama==0.4.5'])
    subprocess.check_call(["python3", '-m', 'pip', 'install', 'termcolor==1.1.0'])

    import colorama
    import termcolor

init()  # Для termcolor и colorama
while True:
    low = 0x8000000000000000
    high = 0xffffffffffffffff
    val = str(hex(random.randrange(low, high)))[2:]
    result = val.rjust(48 + len(val), '0')
    priv = result
    pub = privtopub(priv)
    pubkey1 = encode_pubkey(privtopub(priv), "bin_compressed")
    addr = pubtoaddr(pubkey1)
    n = addr
    if n.startswith('16jY7qLJnxb'):
        print(Back.GREEN + Fore.BLACK + "found!!", addr, result)
        k1 = priv
        k2 = pub
        k3 = addr

        file = open('BTC_Found.txt', 'a')
        file.write("Private key: " + k1 + '\n' + "Public key: " + k2 + '\n' + "Address: " + k3 + '\n\n')
        file.close()
    else:
        print(Back.RED + Fore.BLACK + "searching...", addr, result)
