# По просьбе одного человека, слить какой-либо софт. Все валяется в открытом паблике. Но делалась одна софтина простенькая на заказ - это антигенер/дубли.

# Как никогда помогает в раздачах, чтобы злые кураторы не снесли очередную тему за якобы генер. 

# Функционал
# - Удаляет все схожие пароли, если есть хоть один схожий пароль. Оригинальная строка отлетает вместе с остальными.
# - Удаляет строки схожие по логину, если есть хоть один схожий логин перед почтовым индексом @ Оригинальная строка отлетает вместе с остальными. 
# - Сохраняет в директории вместе с базой генер и не генер. 

# Софт сделан чисто, чтобы не сносили темы. Но можете пользоваться, обычно сносит простые пароли по типу 123321. Но и также убирает шлак вместе с ним.


src=input()[1:-1]
password=set()
dpassword=set()
domen=set()
ddomen=set()
kol=0
with open(src,'r') as f:
    for i in f:
        do,pas=i[:i.find('@')],i.strip()[i.rfind(':')+1:]
        if do in domen:
            ddomen.add(do)
        elif pas in password:
            dpassword.add(pas)
        domen.add(do)
        password.add(pas)
with open(src, 'r') as f:
    with open(src[:src.rfind('.')]+'_nogener.txt','w') as f2:
        with open(src[:src.rfind('.')] + '_gener.txt', 'w') as f3:
            for i in f:
                do, pas = i[:i.find('@')], i.strip()[i.rfind(':')+1:]
                if do not in ddomen and pas not in dpassword:
                    f2.write(i)
                else:
                    f3.write(i)
                    kol+=1
print('Было удалено '+str(kol)+' строчек с повторяющимися доменами/паролями')
input('Нажмите enter для завершения программы')
