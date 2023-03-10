import time
import os
from bit import Key

key_count = 5000

path = os.path.dirname(os.path.abspath(__file__)) + "\\"
baseName = path + 'base.txt'
profit = path + 'out.txt'

print('Чтение base.txt', flush=True, end='')

start = time.time()
f = open(baseName, 'r')
t = set(f.read().split('\n'))
end = time.time()
f.close()
print('sec:', end - start, flush=True)
y = 0
print('Start generation...', flush=True)

while True:
    # генерация кошельков
    y += 1
    print('Generation', key_count, 'address wallets №', y, flush=True)
    mass = {}
    for _ in range(key_count):
        k = Key()
        mass[k.address] = k.to_wif()
        mass[k.segwit_address] = k.to_wif()

    # проверка сгенерированного
    print('проверка ...', flush=True)
    for key in mass:
        print(key, mass[key])
        if key in t:
            with open(profit, 'a') as out:
                out.write('{},{}\n'.format(key, mass[key]))
                print('что-то нашли ...', flush=True)
