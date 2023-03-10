from ethereum import utils
import os

#dec - bin

a= int(input("Enter a decimal number that you want to convert to hexadecimal: "))
def dec2hex (number2):
    b=hex(a)
    return b
r= dec2hex(a)
print("Hexadecimal conversion is: "+ str(r) )

private_key = utils.sha3(r)

#Адрес учетной записи
#Преобразуйте закрытый ключ в общий адрес.
raw_address = utils.privtoaddr(private_key)
account_address = utils.checksum_encode(raw_address)

print (raw_address)
print (account_address)