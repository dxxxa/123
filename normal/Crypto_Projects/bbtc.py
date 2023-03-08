#Usage
#Private Keys
from pybitcoin import BitcoinPrivateKey

private_key = BitcoinPrivateKey()
private_key.to_hex()
#'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
private_key.to_wif()
#'5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
private_key_2 = BitcoinPrivateKey('91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d')
print (private_key.to_wif() == private_key_2.to_wif())




#Public Keys
#public_key = private_key.public_key()
#public_key.to_hex()
#'042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
#public_key_2 = BitcoinPublicKey(public_key.to_hex())
#print public_key.to_hex() == public_key_2.to_hex()




Addresses
#public_key.address()
#'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'
#public_key.hash160()
#'1e6db1e09b5e307847e5734864a79ea0113d0083'
