# create_child_wallet.py

from pywallet import wallet

WALLET_PUBKEY = 'tpubDCxTwu5rUgWdjyQuHocwmqhJuxL2WnFRDhxP9j4YK2KMkKrys3Bk2nUsjoBdxi8fxVKB4Ye6mDTrFYisX5vgvSbisDnv3aCTX8eV2UavyLx'

# generate address for specific user (id = 10)
user_addr = wallet.create_address(
    network='btctest', xpub=WALLET_PUBKEY, child=10)

# or generate a random address, based on timestamp
rand_addr = wallet.create_address(network='btctest', xpub=WALLET_PUBKEY)

print('User Address\n', user_addr)
print('Random Address\n', rand_addr)
