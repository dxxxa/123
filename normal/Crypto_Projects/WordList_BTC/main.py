# https://github.com/j4rj4r/Bitcoin-Brainwallet-Bruteforce

# Проект для брутфорса биткойн-мозгового кошелька.
# На вход берет словарь и для каждой строки генерирует приватный ключ и проверяет есть ли баланс.

import argparse
import sys


# from file_management import FileManagement
# from scan import Scan

class FileManagement:
    def __init__(self, outputfile, inputfile=None):
        self.inputfile = inputfile
        self.outputfile = outputfile

    def read_dictionary(self):
        f = open(self.inputfile, "r")
        lines = f.read().splitlines()
        f.close()
        return lines

    def write_discovery(self, address, password, wif, balance):
        f = open(self.outputfile, "a")
        f.write(address + "|" + password + "|" + wif + "|" + balance + "\n")
        f.close()


import hashlib
import binascii
import base58


class PrivateKey:
    def __init__(self, _privatekey=None):
        self._privatekey = _privatekey
        self._passphrase = None
        self.wif = None

    def from_passphrase(self, passphrase):
        hex_private_key = hashlib.sha256(passphrase.encode('utf-8')).hexdigest()
        self._privatekey = hex_private_key
        self._passphrase = passphrase
        self.wif = None
        return self._privatekey

    def privatekey_to_wif(self, _privatekey=None, compressed=False):
        if _privatekey is None:
            privatekey = self._privatekey
        else:
            privatekey = _privatekey
        if compressed:
            extented_key = "80" + privatekey + "01"
        else:
            extented_key = "80" + privatekey
        first_sha256 = hashlib.sha256(binascii.unhexlify(extented_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
        final_key = extented_key + second_sha256[:8]
        wif = base58.b58encode(binascii.unhexlify(final_key))
        wif = wif.decode("utf-8")
        self.wif = wif
        return wif


# from privatekey import PrivateKey
from bit import Key


class Scan:
    def __init__(self, file, wordlist):
        self.file = file
        self.wordlist = wordlist
        self.pkey = PrivateKey()
        self.discoveries = []
        self.balancetotal = 0
        self.noemptyaddr = 0

    def launch(self, compressed=False):
        for password in self.wordlist:
            self.pkey.from_passphrase(password)
            if compressed:
                wif = self.pkey.privatekey_to_wif(compressed=True)
            else:
                wif = self.pkey.privatekey_to_wif()
            key = Key(wif)
            balance = key.get_balance('btc')
            # If the balance is not empty
            if balance != "0":
                if key.address not in self.discoveries:
                    print(f'{key.address} : {balance}')
                    self.discoveries.append(key.address)
                    self.file.write_discovery(key.address, password, self.pkey.wif, balance)
                    self.balancetotal += float(balance)
                    self.noemptyaddr += 1
            else:
                print(f'Empty balance for : {password}')

        print(f'You have found a total of  {self.balancetotal} btc')
        print(f'Addresses with btc : {self.noemptyaddr}')
        return self.discoveries


if __name__ == '__main__':

    inputfile = 'default_wordlist.txt'
    outputfile = 'output.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Words dictionary file (e.g. dictionary.txt)',
                        type=str, required=False)
    parser.add_argument('-o', '--output', help='output file (e.g. output.txt)',
                        type=str, required=False)
    parser.add_argument('-c', '--compressed', help="Use compressed addresses", action='store_true', required=False)
    parser.add_argument('--version', action='version', version='Version : 1.01')

    args = parser.parse_args()

    if args.input:
        inputfile = args.input
    if args.output:
        outputfile = args.output

    # We initialize file management
    file = FileManagement(outputfile, inputfile)
    # A list with the contents of the dictionary is retrieved.
    wordlist = file.read_dictionary()
    # The scan object is initialized with the list of dictionary contents.
    scan = Scan(file, wordlist)
    # Start the scan and get the result.
    try:

        if args.compressed:
            print('Compressed Addresses : ON')
            result = scan.launch(compressed=True)
        else:
            result = scan.launch()
        # We write the result in a output file
        if not result:
            print('We didn\'t find anything !')

    except KeyboardInterrupt:
        print('Exit...')
        sys.exit(0)
