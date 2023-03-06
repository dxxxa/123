#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os


with open('Output.txt', 'w') as file:
    subprocess.run('netsh wlan show profiles', stdout=file, check=True)

with open('Output.txt', encoding = 'cp866') as file:
    lines = file.readlines()
    with open('SSID.txt', 'a') as f:
        for line in lines:
            if 'Все профили пользователей' in line:
                f.write(line)
            else:
                pass

with open('SSID.txt') as file:
    lines = file.readlines()
    for line in lines:
        line = line.split()
        # print(f'netsh wlan show profile name={line[-1]} key=clear')
        with open('BAD_Wifi.txt', 'a') as f:
            try:
                subprocess.run(f'netsh wlan show profile name={line[-1]} key=clear', stdout=f, check=True)
            except:
                pass

a = open('BAD_Wifi.txt', 'w')
a.close()

with open('BAD_Wifi.txt', encoding = 'cp866') as file:
    lines = file.readlines()
    with open('WIFI_Passwords.txt', 'a') as f:
        for line in lines:
            if 'Имя SSID               :' in line:
                f.write(line)
            if 'Содержимое ключа            :' in line:
                f.write(line.replace('     :', ':') + '\n')

os.system('del Output.txt')
os.system('del SSID.txt')
os.system('del BAD_Wifi.txt')