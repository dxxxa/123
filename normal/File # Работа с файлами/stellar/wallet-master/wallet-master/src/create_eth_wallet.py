# create_eth_wallet.py

from pywallet import wallet

seed = wallet.generate_mnemonic()
w = wallet.create_wallet(network="ETH", seed=seed, children=1)

print(w)
