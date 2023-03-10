>>> import random
>>> private_key = ''.join(['%x' % random.randrange(16) for x in range(0, 64)])
>>> private_key
'9ceb87fc34ec40408fd8ab3fa81a93f7b4ebd40bba7811ebef7cbc80252a9815'
>>> # or
>>> import os
>>> private_key = os.urandom(32).encode('hex')
>>> private_key
'0a56184c7a383d8bcce0c78e6e7a4b4b161b2f80a126caa48bde823a4625521f'
------------------------------
Python, ECDSA

>>> import binascii
>>> import ecdsa # sudo pip install ecdsa
>>> private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
>>> binascii.hexlify(private_key.to_string()).decode('ascii').upper()
u'CE47C04A097522D33B4B003B25DD7E8D7945EA52FA8931FD9AA55B315A39DC62'
------------------------------
Bitcoin-cli

$ bitcoin-cli getnewaddress
14RVpC4su4PzSafjCKVWP2YBHv3f6zNf6U
$ bitcoin-cli dumpprivkey 14RVpC4su4PzSafjCKVWP2YBHv3f6zNf6U
L3SPdkFWMnFyDGyV3vkCjroGi4zfD59Wsc5CHdB1LirjN6s2vii9
------------------------------
Python, ECDSA

>>> import binascii
>>> import ecdsa
>>> private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
>>> public_key = private_key.get_verifying_key()
>>> binascii.hexlify(public_key.to_string()).decode('ascii').upper()
u'D5C08F1BFC9C26A5D18FE9254E7923DEBBD34AFB92AC23ABFC6388D2659446C1F04CCDEBB677EAABFED9294663EE79D71B57CA6A6B76BC47E6F8670FE759D746'