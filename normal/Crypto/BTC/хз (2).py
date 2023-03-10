import hashlib
import base58
import binascii


private_key_static = "0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D"
extended_key = "80"+private_key_static
first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

# add checksum to end of extended key
final_key = extended_key+second_sha256[:8]

# Wallet Import Format = base 58 encoded final_key
WIF = base58.b58encode(binascii.unhexlify(final_key))

print (WIF)