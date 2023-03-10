#!/usr/bin/python
from pybitcoin import BitcoinPrivateKey
import requests
import json

FILE_PATH = r'C:\Temp.txt'

with open(FILE_PATH) as f:
    keys: List[str] = f.read().splitlines()

for key in keys:
    private_key = BitcoinPrivateKey(private_key=key)

public_key = private_key.public_key()
address = public_key.address()

r = requests.get('https://chain.so/api/v2/address/BTC/{}'.format(address))
print ('Address: {} Private Key: {} Balance: {}'.format(address, key, (json.loads(r.content)['data']['balance'])))
