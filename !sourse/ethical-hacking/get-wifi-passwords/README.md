# [How to Extract Saved WiFi Passwords in Python](https://www.thepythoncode.com/article/extract-saved-wifi-passwords-in-python)
##
# [[] / []]()
Как вы, возможно, уже знаете, Wi-Fi используется для подключения к нескольким сетям в разных местах, у вашей машины определенно есть способ сохранить пароль Wi-Fi где-то, поэтому при следующем подключении вам не придется повторно вводить его снова.

В этом учебнике вы узнаете, как создать быстрый скрипт Python для извлечения сохраненных паролей Wi-Fi на компьютерах Windows или Linux.

Нам не понадобится установка какой-либо сторонней библиотеки, так как мы будем использовать взаимодействие с netsh в Windows и папкой NetworkManager в Linux. Импорт библиотек:

import subprocess
import os
import re
from collections import namedtuple
import configparser
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Получение паролей Wi-Fi в Windows
В Windows, чтобы получить все имена Wi-Fi (ssids), мы используем команду netsh wlan show profiles, ниже функция использует подпроцесс для вызова этой команды и анализирует ее в Python:

def get_windows_saved_ssids():
    """Returns a list of saved SSIDs in a Windows machine using netsh command"""
    # get all saved profiles in the PC
    output = subprocess.check_output("netsh wlan show profiles").decode()
    ssids = []
    profiles = re.findall(r"All User Profile\s(.*)", output)
    for profile in profiles:
        # for each SSID, remove spaces and colon
        ssid = profile.strip().strip(":").strip()
        # add to the list
        ssids.append(ssid)
    return ssids
Мы используем регулярные выражения для поиска сетевых профилей. Затем мы можем использовать show profile [ssid] key=clear, чтобы получить пароль этой сети:

def get_windows_saved_wifi_passwords(verbose=1):
    """Extracts saved Wi-Fi passwords saved in a Windows machine, this function extracts data using netsh
    command in Windows
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "ciphers", "key"]
    """
    ssids = get_windows_saved_ssids()
    Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
    profiles = []
    for ssid in ssids:
        ssid_details = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode()
        # get the ciphers
        ciphers = re.findall(r"Cipher\s(.*)", ssid_details)
        # clear spaces and colon
        ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
        # get the Wi-Fi password
        key = re.findall(r"Key Content\s(.*)", ssid_details)
        # clear spaces and colon
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "None"
        profile = Profile(ssid=ssid, ciphers=ciphers, key=key)
        if verbose >= 1:
            print_windows_profile(profile)
        profiles.append(profile)
    return profiles

def print_windows_profile(profile):
    """Prints a single profile on Windows"""
    print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")
Во-первых, мы вызываем наш get_windows_saved_ssids(), чтобы получить все SSID, к которым мы подключались раньше, затем мы инициализируем наш nametuple, чтобы включить ssid, шифры и ключ. Мы вызываем профиль show [ssid] key=clear для каждого извлеченного SSID, анализируем шифры и ключ (пароль) и печатаем его с помощью простой функции print_windows_profile().

Назовем эту функцию сейчас:

def print_windows_profiles(verbose):
    """Prints all extracted SSIDs along with Key on Windows"""
    print("SSID                     CIPHER(S)      KEY")
    print("-"*50)
    get_windows_saved_wifi_passwords(verbose)
Поэтому print_windows_profiles() печатает все SSID вместе с шифром и ключом (паролем).

Связанные с: Создание 24 этических хакерских скриптов и инструментов с помощью Python Book

Получение паролей Wi-Fi в Linux
В Linux все по-другому, в каталоге /etc/NetworkManager/system-connections/ все ранее подключенные сети расположены здесь как INI-файлы, нам просто нужно прочитать эти файлы и распечатать их в хорошем формате:

def get_linux_saved_wifi_passwords(verbose=1):   
    """Extracts saved Wi-Fi passwords saved in a Linux machine, this function extracts data in the
    `/etc/NetworkManager/system-connections/` directory
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "auth-alg", "key-mgmt", "psk"]
    """
    network_connections_path = "/etc/NetworkManager/system-connections/"
    fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
    Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
    profiles = []
    for file in os.listdir(network_connections_path):
        data = { k.replace("-", "_"): None for k in fields }
        config = configparser.ConfigParser()
        config.read(os.path.join(network_connections_path, file))
        for _, section in config.items():
            for k, v in section.items():
                if k in fields:
                    data[k.replace("-", "_")] = v
        profile = Profile(**data)
        if verbose >= 1:
            print_linux_profile(profile)
        profiles.append(profile)
    return profiles


def print_linux_profile(profile):
    """Prints a single profile on Linux"""
    print(f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}") 
Связанные с: Как создать генератор паролей в Python.

Как уже упоминалось, мы используем os.listdir() в этом каталоге, чтобы перечислить все файлы, затем мы используем configparser для чтения INI-файла и перебираем элементы, если мы находим интересующие нас поля, мы просто включаем их в наши данные.

Есть и другая информация, но мы придерживаемся SSID, auth-alg, key-mgmt и psk (пароль). Далее вызовем функцию сейчас:

def print_linux_profiles(verbose):
    """Prints all extracted SSIDs along with Key (PSK) on Linux"""
    print("SSID                     AUTH KEY-MGMT  PSK")
    print("-"*50)
    get_linux_saved_wifi_passwords(verbose)
Наконец, давайте сделаем функцию, которая вызывает либо print_linux_profiles(), либо print_windows_profiles() на основе нашей ОС:

def print_profiles(verbose=1):
    if os.name == "nt":
        print_windows_profiles(verbose)
    elif os.name == "posix":
        print_linux_profiles(verbose)
    else:
        raise NotImplemented("Code only works for either Linux or Windows")
    
    
if __name__ == "__main__":
    print_profiles()
Запуск скрипта:

$ python get_wifi_passwords.py
Вывод на моем компьютере с Windows:

SSID                     CIPHER(S)      KEY
--------------------------------------------------
OPPO F9                  CCMP/GCMP      0120123489@
TP-Link_83BE_5G          CCMP/GCMP      0xxxxxxx
Access Point             CCMP/GCMP      super123
HUAWEI P30               CCMP/GCMP      00055511
ACER                     CCMP/GCMP      20192019
HOTEL VINCCI MARILLIA    CCMP           01012019
Bkvz-U01Hkkkkkzg         CCMP/GCMP      00000011
nadj                     CCMP/GCMP      burger010
Griffe T1                CCMP/GCMP      110011110111111
BIBLIO02                 None           None
AndroidAP                CCMP/GCMP      185338019mbs
ilfes                    TKIP           25252516
Point                    CCMP/GCMP      super123
А вот вывод Linux:

SSID                     AUTH KEY-MGMT  PSK
--------------------------------------------------
KNDOMA                   open wpa-psk   5060012009690
TP-LINK_C4973F           None None      None
None                     None None      None
Point                    open wpa-psk   super123
Point                    None None      None
Заключение
Хорошо, вот и все для этого урока. Я уверен, что это полезный код для вас, чтобы быстро получить сохраненные пароли Wi-Fi на вашем компьютере.