from bitcoinlib.wallets import HDWallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic


w = HDWallet.create('Wallet3')
key1 = w.get_key()
key1.address

print(key1)

w.scan()
w.info()

t = w.send_to('12ooWd8Xag7hsgP9PBPnmyGe36VeUrpMSH', 100000)
t.info
