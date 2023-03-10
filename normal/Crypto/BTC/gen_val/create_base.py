import os

path = os.path.dirname(os.path.abspath(__file__)) + "\\"
baseInName = path + 'blockchair_bitcoin_addresses_latest.tsv'
baseOutName = path + 'base.txt'

bsOut = open(baseOutName, 'w')

print('Преобразование:  blockchair_bitcoin_addresses_latest.tsv --> base.txt ... ', end='')

with open(baseInName, 'r') as bs:
    for i in bs.readlines():
        key, val = i.strip().split('\t')
        if key[0] in ["1", "3"]:
            bsOut.write('{}\n'.format(key))
bsOut.close()
bs.close()
print("COMPLETE")
