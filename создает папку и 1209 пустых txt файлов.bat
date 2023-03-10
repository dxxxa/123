@echo off
set "d=C:\1\
set n=1209
 
if not exist "%d%" md "%d%"
for /l %%n in (1 1 %n%) do rem:>"%d%\rockyou2021_%%n.txt"
pause