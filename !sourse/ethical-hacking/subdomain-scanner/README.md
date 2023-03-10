# [How to Make a Subdomain Scanner in Python](https://www.thepythoncode.com/article/make-subdomain-scanner-python)
To run this:
- `pip3 install -r requirements.txt`
- To run the fast subdomain scanner:
    ```
    python fast_subdomain_scanner.py --help
    ```
    **Output:**
    ```
    usage: fast_subdomain_scanner.py [-h] [-l WORDLIST] [-t NUM_THREADS]       
                                 [-o OUTPUT_FILE]
                                 domain

    Faster Subdomain Scanner using Threads

    positional arguments:
    domain                Domain to scan for subdomains without protocol (e.g
                            without 'http://' or 'https://')

    optional arguments:
    -h, --help            show this help message and exit
    -l WORDLIST, --wordlist WORDLIST
                            File that contains all subdomains to scan, line by
                            line. Default is subdomains.txt
    -t NUM_THREADS, --num-threads NUM_THREADS
                            Number of threads to use to scan the domain. Default
                            is 10
    -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Specify the output text file to write discovered
                            subdomains
    ```
- If you want to scan hackthissite.org for subdomains using only 10 threads with a word list of 100 subdomains (`subdomains.txt`):
    ```
    python fast_subdomain_scanner.py hackthissite.org -l subdomains.txt -t 10
    ```
    After a while, it **outputs:**
    ```
    [+] Discovered subdomain: http://mail.hackthissite.org
    [+] Discovered subdomain: http://www.hackthissite.org
    [+] Discovered subdomain: http://forum.hackthissite.org
    [+] Discovered subdomain: http://admin.hackthissite.org
    [+] Discovered subdomain: http://stats.hackthissite.org
    [+] Discovered subdomain: http://forums.hackthissite.org
    ```
    If you want to output the discovered URLs to a file:
    ```
    python fast_subdomain_scanner.py hackthissite.org -l subdomains.txt -t 10 -o discovered_urls.txt
    ```
    This will create a new file `discovered_urls.txt` that includes the discovered subdomains.
- For bigger subdomain wordlists, check [this repository](https://github.com/rbsec/dnscan).
##
# [[] / []]()
Поиск поддоменов конкретного веб-сайта позволяет изучить его полную доменную инфраструктуру. Создание такого инструмента действительно удобно на этапе сбора информации в тестировании на проникновение для этических хакеров.

Поиск поддоменов вручную займет вечность. К счастью, нам не нужно этого делать. В этом уроке мы построим сканер поддоменов на Python, используя библиотеку запросов. Давайте начнем!

Связанные с: Как использовать Shodan API в Python.

Давайте установим его:

pip3 install requests
Метод, который мы будем использовать здесь, - это грубое принуждение. Другими словами, мы собираемся протестировать все общие имена поддоменов этого конкретного домена. Всякий раз, когда мы получаем ответ от сервера, это показатель для нас, что поддомен жив.

Откройте новый файл Python и следуйте за ним. Давайте использовать google.com в демонстрационных целях; и я использовал его, потому что у Google есть много поддоменов, хотя:

import requests

# the domain to scan for subdomains
domain = "google.com"
Получите: Создайте 24 этических хакерских скрипта и инструмента с помощью Python Book

Теперь нам понадобится большой список поддоменов для сканирования, я использовал список из 100 поддоменов только для демонстрации, но в реальном мире, если вы действительно хотите обнаружить все поддомены, вы должны использовать больший список. Проверьте этот репозиторий GitHub, который содержит до 10K поддоменов.

У меня есть файл "subdomains.txt" в текущем каталоге. Убедитесь, что вы тоже это сделали (возьмите список по вашему выбору в этом репозитории):

# read all subdomains
file = open("subdomains.txt")
# read all content
content = file.read()
# split by new lines
subdomains = content.splitlines()
Теперь список поддоменов содержит поддомены, которые мы хотим протестировать. Давайте переборщим:

# a list of discovered subdomains
discovered_subdomains = []
for subdomain in subdomains:
    # construct the url
    url = f"http://{subdomain}.{domain}"
    try:
        # if this raises an ERROR, that means the subdomain does not exist
        requests.get(url)
    except requests.ConnectionError:
        # if the subdomain does not exist, just pass, print nothing
        pass
    else:
        print("[+] Discovered subdomain:", url)
        # append the discovered subdomain to our list
        discovered_subdomains.append(url)
Сначала мы создаем URL-адрес, подходящий для отправки запроса, а затем используем функцию requests.get() для получения HTTP-ответа от сервера. Это вызовет исключение ConnectionError всякий раз, когда сервер не отвечает; вот почему мы завернули его в блок try/except.

Если исключение не было поднято, то поддомен существует. Запишем все обнаруженные поддомены в файл:

# save the discovered subdomains into a file
with open("discovered_subdomains.txt", "w") as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file=f)
Вот часть результата, когда я запускал скрипт:

Результат работы сканера поддоменов в Python

Как только он будет завершен, вы увидите новый файл, discovered_subdomains.txt появится, который включает в себя все обнаруженные поддомены!

При запуске скрипта вы заметите, что он довольно медленный, особенно когда вы используете более длинные списки, так как он использует один поток для сканирования. Однако если требуется ускорить процесс сканирования, для сканирования можно использовать несколько потоков. Я уже написал один. Проверьте это здесь.

Хорошо, мы закончили. Теперь вы знаете, как обнаружить поддомены любого сайта, который вы хотите!