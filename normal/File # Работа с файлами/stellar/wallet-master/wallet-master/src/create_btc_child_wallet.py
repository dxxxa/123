from pywallet import wallet

WALLET_PUBKEY = 'xpub661MyMwAqRbcEtt23sScv8tGQB4qMaJkgYRoRTtmcpJ8K6XsZw7Tjp2feauhmBZvdWEN8WrE5ghe5BFwwT4y72nSPkKiUko23Fa9C2nZ7X7'

# generate address for specific user (id = 10)
user_addr = wallet.create_address(network="BTC", xpub=WALLET_PUBKEY, child=10)

# or generate a random address, based on timestamp
rand_addr = wallet.create_address(network="BTC", xpub=WALLET_PUBKEY)

print("User Address\n", user_addr)
print("Random Address\n", rand_addr)
