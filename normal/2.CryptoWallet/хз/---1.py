# Из модуля random импортируем функцию
# random(), которая генерирует случайное
# вещественное число, и функцию randint(),
# которая генерирует случайное целое.

from random import random, randint
#############################################
# Запрашиваем нижнюю и верхнюю границы
# диапазона, в пределах которого будет
# генерироваться случайное целое число.

print("Range of integers: ")
imin = int(input("Input Starting Range :> "))
imax = int(input("Input Ending Range   :> "))

qwe = int(input("Input Range   :> "))
#############################################
# Функция randint() генерирует случайное
# число n, которое не меньше imin и не
# больше imax.

for i in range(0,qwe):
    n = randint(imin, imax)

    print("%d" % n)





########################################

# Из модуля random импортируем функцию
# random(), которая генерирует случайное
# вещественное число, и функцию randint(),
# которая генерирует случайное целое.

#from random import random, randint

# Запрашиваем нижнюю и верхнюю границы
# диапазона, в пределах которого будет
# генерироваться случайное целое число.

#print("Range of integers: ")
#imin = int(input())
#imax = int(input())

# Функция randint() генерирует случайное
# число n, которое не меньше imin и не
# больше imax.

#n = randint(imin, imax)

#print("%d" % n)




from random import random, randint



def main():
	print("""                                                                                                                                                                                                 

[1] Generate a List of Wallets with a Range [with Balances]
[2] Generate a List of Wallets with a Range [without Balances]
[3] Guess a Number List to Generate a Wallet
[4] Random DEC
[5] Conventor

"q" for quit
	 """)

	x = input(">>> ")
	if x == "q":
		try:
			quit()
		except:
			exit()



	elif x == "1":
		r1  = int(input("Input Starting Range :> "))
		r2 = int(input("Input Ending Range   :> "))
		for x in range(r1,r2):
			int_to_address(x)



	elif x == "2":
		r1  = int(input("Input Starting Range :> "))
		r2 = int(input("Input Ending Range   :> "))
		for x in range(r1,r2):
			btcwb(x)



	elif x == "3":
		print("Enter your lucky number in the following format:")
		print("ex: 1 2 456 788 123 657 11 66 234 68 23\n")
		array = map(int, input("Enter Numbers by Keeping Space : ").split())
		for i in array:
			int_to_address(i)
			i += 1



	elif x == "4":
        # Запрашиваем нижнюю и верхнюю границы диапазона, в пределах которого будет генерироваться случайное целое число.
		print("Range of integers: ")
		imin = int(input("Input Starting Range :> "))
		imax = int(input("Input Ending Range   :> "))

		qwe = int(input("Input Range          :> "))

		# Функция randint() генерирует случайное число n, которое не меньше imin и не больше imax.
		for i in range(0,qwe):
			n = randint(imin, imax)
        
			print("%d" % n)



	elif x == "5":
		print("""   Conventor:                                                                                                                                                                                              

[1] BIN to DEC
[2] DEC to
[3] 
[4] 

"q" for quit
	""")
		x = input(">>> ")
		if x == "q":
			try:
				quit()
			except:
				exit()





	else:
		print("Command not Recognized")
        
main()

