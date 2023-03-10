# [How to Make a MAC Address Changer in Python](https://www.thepythoncode.com/article/make-a-mac-address-changer-in-python)
##
# [[] / []]()
MAC-адрес — это уникальный идентификатор, присваиваемый каждому сетевому интерфейсу в любом устройстве, которое подключается к сети. Изменение этого адреса имеет много преимуществ, включая предотвращение блокировки MAC-адресов; если ваш MAC-адрес заблокирован на точке доступа, вы просто измените его, чтобы продолжить использовать эту сеть.

Из этого туториала Вы узнаете, как изменить MAC-адрес в средах Windows и Linux с помощью Python.

Нам не нужно ничего устанавливать, так как мы будем использовать модуль подпроцесса в Python, взаимодействуя с командой ifconfig в Linux и командами getmac, reg и wmic в Windows.

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Изменение MAC-адреса в Linux
Чтобы начать работу, откройте новый файл Python и импортируйте библиотеки:

import subprocess
import string
import random
import re
У нас будет выбор: рандомизировать новый MAC-адрес или изменить его на указанный. В результате сделаем функцию для генерации и возврата MAC-адреса:

def get_random_mac_address():
    """Generate and return a MAC address in the format of Linux"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")
Мы используем строковый модуль для получения шестнадцатеричных цифр, используемых в MAC-адресах; мы удаляем строчные буквы и используем случайный модуль для выборки из этих символов.

Далее давайте сделаем еще одну функцию, которая использует команду ifconfig для получения текущего MAC-адреса нашей машины:

def get_current_mac_address(iface):
    # use the ifconfig command to get the interface details, including the MAC address
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()
Мы используем функцию check_output() из модуля подпроцесса, который запускает команду в оболочке по умолчанию и возвращает выходные данные команды.

MAC-адрес находится сразу после слова «эфир», мы используем метод re.search(), чтобы захватить его.

Теперь, когда у нас есть наши утилиты, давайте сделаем основную функцию для изменения MAC-адреса:

def change_mac_address(iface, new_mac_address):
    # disable the network interface
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    # change the MAC
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)
    # enable the network interface again
    subprocess.check_output(f"ifconfig {iface} up", shell=True)
Довольно просто, функция change_mac_address() принимает интерфейс и новый MAC-адрес в качестве параметров, отключает интерфейс, изменяет MAC-адрес и снова включает его.

Теперь, когда у нас есть все, давайте используем модуль argparse, чтобы завершить наш скрипт:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python Mac Changer on Linux")
    parser.add_argument("interface", help="The network interface name on Linux")
    parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    iface = args.interface
    if args.random:
        # if random parameter is set, generate a random MAC
        new_mac_address = get_random_mac_address()
    elif args.mac:
        # if mac is set, use it instead
        new_mac_address = args.mac
    # get the current MAC address
    old_mac_address = get_current_mac_address(iface)
    print("[*] Old MAC address:", old_mac_address)
    # change the MAC address
    change_mac_address(iface, new_mac_address)
    # check if it's really changed
    new_mac_address = get_current_mac_address(iface)
    print("[+] New MAC address:", new_mac_address)
У нас есть в общей сложности три параметра для передачи этому скрипту:

интерфейс: имя сетевого интерфейса, которое вы хотите изменить MAC-адрес, вы можете получить его с помощью команд ifconfig или ip в Linux.
-r или --random: генерируем ли мы случайный MAC-адрес вместо указанного.
-m или --mac: новый MAC-адрес, который мы хотим изменить, не используйте его с параметром -r.
В основном коде мы используем функцию get_current_mac_address() для получения старого MAC, мы меняем MAC, а затем снова запускаем get_current_mac_address(), чтобы проверить, изменился ли он. Вот прогон:

$ python mac_address_changer_linux.py wlan0 -r
Имя моего интерфейса — wlan0, и я выбрал -r для рандомизации MAC-адреса. Вот выходные данные:

[*] Old MAC address: 84:76:04:07:40:59
[+] New MAC address: ee:52:93:6e:1c:f2
Давайте перейдем на указанный MAC-адрес:

$ python mac_address_changer_linux.py wlan0 -m 00:FA:CE:DE:AD:00
Выпуск:

[*] Old MAC address: ee:52:93:6e:1c:f2
[+] New MAC address: 00:fa:ce:de:ad:00
Изменение отражается на машине и других машинах в той же сети и маршрутизаторе.

Читайте также: Как сделать HTTP прокси в Python

Изменение MAC-адреса в Windows
В Windows мы будем использовать три основные команды, а именно:

getmac: эта команда возвращает список сетевых интерфейсов, их MAC-адреса и имя транспорта; последний не отображается, когда интерфейс не подключен.
reg: Это команда, используемая для взаимодействия с реестром Windows. Мы можем использовать модуль winreg для той же цели. Однако я предпочел использовать команду reg.
wmic: Мы будем использовать эту команду для отключения и включения сетевого адаптера, чтобы изменение MAC-адреса отражалось.
Давайте начнем:

import subprocess
import regex as re
import string
import random

# the registry path of network interfaces
network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
# the transport name regular expression, looks like {AF1B45DB-B5D4-46D0-B4EA-3E18FA49BF5F}
transport_name_regex = re.compile("{.+}")
# the MAC address regular expression
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")
network_interface_reg_path — это путь в реестре, где расположены сведения о сетевом интерфейсе. Мы используем transport_name_regex и mac_address_regex регулярные выражения для извлечения имени транспорта и MAC-адреса каждого подключенного адаптера соответственно из команды getmac.

Далее давайте сделаем две простые функции, одну для генерации случайных MAC-адресов (как раньше, но в формате Windows), а другую для очистки MAC-адресов, когда пользователь указывает это:

def get_random_mac_address():
    """Generate and return a MAC address in the format of WINDOWS"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 2, 4, A, or E
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10))
    

def clean_mac(mac):
    """Simple function to clean non hexadecimal characters from a MAC address
    mostly used to remove '-' and ':' from MAC addresses and also uppercase it"""
    return "".join(c for c in mac if c in string.hexdigits).upper()  
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

По какой-то причине только 2, 4, A и E символы работают в качестве второго символа на MAC-адресе в Windows 10. Я пробовал других даже персонажей, но безуспешно.

Ниже приведена функция, отвечающая за получение MAC-адресов доступных адаптеров:

def get_connected_adapters_mac_address():
    # make a list to collect connected adapter's MAC addresses along with the transport name
    connected_adapters_mac = []
    # use the getmac command to extract 
    for potential_mac in subprocess.check_output("getmac").decode().splitlines():
        # parse the MAC address from the line
        mac_address = mac_address_regex.search(potential_mac)
        # parse the transport name from the line
        transport_name = transport_name_regex.search(potential_mac)
        if mac_address and transport_name:
            # if a MAC and transport name are found, add them to our list
            connected_adapters_mac.append((mac_address.group(), transport_name.group()))
    return connected_adapters_mac
Он использует команду getmac в Windows и возвращает список MAC-адресов вместе с их транспортным именем.

Когда вышеуказанная функция возвращает более одного адаптера, нам нужно предложить пользователю выбрать, какой адаптер изменить MAC-адрес. Приведенная ниже функция делает это:

def get_user_adapter_choice(connected_adapters_mac):
    # print the available adapters
    for i, option in enumerate(connected_adapters_mac):
        print(f"#{i}: {option[0]}, {option[1]}")
    if len(connected_adapters_mac) <= 1:
        # when there is only one adapter, choose it immediately
        return connected_adapters_mac[0]
    # prompt the user to choose a network adapter index
    try:
        choice = int(input("Please choose the interface you want to change the MAC address:"))
        # return the target chosen adapter's MAC and transport name that we'll use later to search for our adapter
        # using the reg QUERY command
        return connected_adapters_mac[choice]
    except:
        # if -for whatever reason- an error is raised, just quit the script
        print("Not a valid choice, quitting...")
        exit()
Теперь давайте сделаем нашу функцию для изменения MAC-адреса данного транспортного имени адаптера, которое извлекается из команды getmac:

def change_mac_address(adapter_transport_name, new_mac_address):
    # use reg QUERY command to get available adapters from the registry
    output = subprocess.check_output(f"reg QUERY " +  network_interface_reg_path.replace("\\\\", "\\")).decode()
    for interface in re.findall(rf"{network_interface_reg_path}\\\d+", output):
        # get the adapter index
        adapter_index = int(interface.split("\\")[-1])
        interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
        if adapter_transport_name in interface_content:
            # if the transport name of the adapter is found on the output of the reg QUERY command
            # then this is the adapter we're looking for
            # change the MAC address using reg ADD command
            changing_mac_output = subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
            # print the command output
            print(changing_mac_output)
            # break out of the loop as we're done
            break
    # return the index of the changed adapter's MAC address
    return adapter_index
Функция change_mac_address() использует команду reg QUERY в Windows для запроса network_interface_reg_path мы указали в начале скрипта, она вернет список всех доступных адаптеров, и мы различим целевой адаптер по его транспортному имени.

После того, как мы находим целевой сетевой интерфейс, мы используем команду reg add, чтобы добавить новую запись NetworkAddress в реестр, указывающую новый MAC-адрес. Функция также возвращает индекс адаптера, который нам понадобится позже для команды wmic.

Конечно, изменение MAC-адреса не отражается сразу при добавлении новой записи реестра. Нам нужно отключить адаптер и включить его снова. Следующие функции делают это:

def disable_adapter(adapter_index):
    # use wmic command to disable our adapter so the MAC address change is reflected
    disable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()
    return disable_output


def enable_adapter(adapter_index):
    # use wmic command to enable our adapter so the MAC address change is reflected
    enable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()
    return enable_output
Системный номер адаптера требуется командой wmic, и, к счастью, мы получаем его из нашей предыдущей функции change_mac_address().

И все готово! Давайте сделаем наш основной код:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python Windows MAC changer")
    parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    if args.random:
        # if random parameter is set, generate a random MAC
        new_mac_address = get_random_mac_address()
    elif args.mac:
        # if mac is set, use it after cleaning
        new_mac_address = clean_mac(args.mac)
    
    connected_adapters_mac = get_connected_adapters_mac_address()
    old_mac_address, target_transport_name = get_user_adapter_choice(connected_adapters_mac)
    print("[*] Old MAC address:", old_mac_address)
    adapter_index = change_mac_address(target_transport_name, new_mac_address)
    print("[+] Changed to:", new_mac_address)
    disable_adapter(adapter_index)
    print("[+] Adapter is disabled")
    enable_adapter(adapter_index)
    print("[+] Adapter is enabled again")
Поскольку выбор сетевого интерфейса запрашивается после запуска скрипта (всякий раз, когда обнаруживаются два или более интерфейсов), нам не нужно добавлять аргумент интерфейса.

Основной код прост:

Мы получаем все подключенные адаптеры с помощью функции get_connected_adapters_mac_address().
Мы получаем входные данные от пользователя, указывающие, на какой адаптер ориентироваться.
Мы используем функцию change_mac_address() для изменения MAC-адреса транспортного имени данного адаптера.
Мы отключаем и включаем адаптер с помощью функций disable_adapter() и enable_adapter() соответственно, поэтому изменение MAC-адреса отражается.
Хорошо, мы закончили со сценарием. Прежде чем попробовать, необходимо убедиться, что вы работаете от имени администратора. Я назвал сценарий mac_address_changer_windows.py:

$ python mac_address_changer_windows.py --help
Выпуск:

usage: mac_address_changer_windows.py [-h] [-r] [-m MAC]

Python Windows MAC changer

optional arguments:
  -h, --help         show this help message and exit
  -r, --random       Whether to generate a random MAC address
  -m MAC, --mac MAC  The new MAC you want to change to
Давайте попробуем со случайным MAC:

$ python mac_address_changer_windows.py --random
Выпуск:

#0: EE-9C-BC-AA-AA-AA, {0104C4B7-C06C-4062-AC09-9F9B977F2A55}
#1: 02-00-4C-4F-4F-50, {DD1B45DA-B5D4-46D0-B4EA-3E07FA35BF0F}
Please choose the interface you want to change the MAC address:0
[*] Old MAC address: EE-9C-BC-AA-AA-AA
The operation completed successfully.

[+] Changed to: 5A8602E9CF3D

[+] Adapter is disabled

[+] Adapter is enabled again
Мне было предложено выбрать адаптер, я выбрал первый, и MAC-адрес изменен на случайный MAC-адрес. Давайте подтвердим с помощью команды getmac:

$ getmac
Выпуск:

Physical Address    Transport Name
=================== ==========================================================
5A-86-02-E9-CF-3D   \Device\Tcpip_{0104C4B7-C06C-4062-AC09-9F9B977F2A55}
02-00-4C-4F-4F-50   \Device\Tcpip_{DD1B45DA-B5D4-46D0-B4EA-3E07FA35BF0F}
Операция действительно прошла успешно! Давайте попробуем с указанным MAC:

$ python mac_address_changer_windows.py -m EE:DE:AD:BE:EF:EE
Выпуск:

#0: 5A-86-02-E9-CF-3D, {0104C4B7-C06C-4062-AC09-9F9B977F2A55}
#1: 02-00-4C-4F-4F-50, {DD1B45DA-B5D4-46D0-B4EA-3E07FA35BF0F}
Please choose the interface you want to change the MAC address:0
[*] Old MAC address: 5A-86-02-E9-CF-3D
The operation completed successfully.

[+] Changed to: EEDEADBEEFEE

[+] Adapter is disabled

[+] Adapter is enabled again
Заключение
Замечательно! В этом учебнике вы узнали, как изменить MAC-адрес на любом компьютере Linux или Windows.

Если у вас не установлена команда ifconfig, вы должны установить ее через apt install net-tools на Debian/Ubuntu или yum установить net-tools на Fedora/CentOS.