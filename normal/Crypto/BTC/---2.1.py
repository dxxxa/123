#from bipwallet import wallet
#from bipwallet.utils import *
import requests
import bit

wallet.generate_mnemonic()  # на выходе будет фраза из 12 слов


def generate(seed, index=1):
    master_key = HDPrivateKey.master_key_from_mnemonic(seed)

    root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()
    xpublic_key = root_keys

    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()
    rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

    xprivatekey = rootkeys_wif.to_b58check()
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()

    return address, wif


s = wallet.generate_mnemonic()
a = generate(s)

print("Секретная фраза:", s)
print("Адрес:", a[0])
print("Приватный ключ:", a[1])


def balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"
    response = requests.get(url).json()

    return response["final_balance"] / 10000000


def send(wif, address, money):
    key = bit.Key(wif)
    transaction_hash = key.create_transaction([(address, money, "btc")], fee=10000, absolute_fee=True)

    response = requests.post('https://blockchain.info/pushtx', data={'tx': transaction_hash}).text

    if response == "Transaction Submitted": return True
    return False