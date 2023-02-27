# [How to Perform DNS Enumeration in Python](https://www.thepythoncode.com/article/dns-enumeration-with-python)
##
# [[] / []]()
Перечисление DNS — это процесс сбора информации о конфигурации DNS конкретного домена. Это один из наиболее распространенных методов разведки, который может быть полезен для многих целей, таких как идентификация серверов доменных имен, изучение служб электронной почты, используемых в определенном домене, и многое другое.

Вы также можете извлечь информацию о доменном имени с помощью базы данных WHOIS, но это не является целью этого учебника, так как мы будем взаимодействовать с DNS.

Мы будем использовать библиотеку dnspython на Python, чтобы помочь нам выполнять DNS-запросы и удобно анализировать ответы. Давайте установим его:

$ pip install dnspython
После установки библиотеки откройте новый файл Python dns_enumeration.py и добавьте следующее:

import dns.resolver

# Set the target domain and record type
target_domain = "thepythoncode.com"
record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
# Create a DNS resolver
resolver = dns.resolver.Resolver()
for record_type in record_types:
    # Perform DNS lookup for the specified domain and record type
    try:
        answers = resolver.resolve(target_domain, record_type)
    except dns.resolver.NoAnswer:
        continue
    # Print the answers
    print(f"{record_type} records for {target_domain}:")
    for rdata in answers:
        print(f" {rdata}")
Мы указываем наиболее распространенные записи DNS: A, AAAA, CNAME, MX, NS, SOA и TXT. Вы можете посмотреть на эту страницу Википедии, чтобы увидеть все доступные записи DNS и их функции.

Мы создаем объект Resolver и используем метод resolve(), который принимает целевой домен и тип записи для извлечения информации DNS.

Вот мой вывод:

$ python dns_enumeration.py
 
DNS records for thepythoncode.com (A):
99.81.207.218
52.19.6.38    
34.247.123.251
DNS records for thepythoncode.com (MX):
0 thepythoncode-com.mail.protection.outlook.com.
DNS records for thepythoncode.com (NS):
sparrow.ezoicns.com.
siamese.ezoicns.com.
giraffe.ezoicns.com.
manatee.ezoicns.com.
DNS records for thepythoncode.com (SOA):
giraffe.ezoicns.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400
DNS records for thepythoncode.com (TXT):
"v=spf1 include:spf.protection.outlook.com -all"
"NETORGFT5410317.onmicrosoft.com"
"google-site-verification=yJTOgIk39vl3779N3QhPF-mAR36QE00J6LdXHeID4fM"
Замечательно! Много полезной информации здесь:

Мы видим, что thepythoncode.com сопоставляется с тремя разными IP-адресами (запись A); затем мы можем использовать такие службы, как IPInfo, чтобы узнать больше об этих IP-адресах.
Запись MX (Mail Exchange) используется для идентификации серверов, ответственных за обработку входящих сообщений электронной почты для домена. В нашем случае мы четко видим, что этот домен использует сервис Outlook.
Для записи NS thepythoncode.com имеет четыре разных сервера доменных имен от ezoicns.com. Записи NS идентифицируют DNS-серверы, ответственные за обработку DNS-запросов для домена. Другими словами, когда клиент хочет найти IP-адрес (например, обычный веб-браузер) для thepythoncode.com, он запросит информацию на одном из этих DNS-серверов.
Записи SOA содержат административную информацию о зоне и другие сведения о конфигурации DNS, такие как срок жизни (TTL) для записей DNS.
Наконец, записи TXT хранят произвольные текстовые данные, связанные с доменом. В нашем случае записи TXT содержат различные проверочные коды и другую информацию, используемую различными службами для проверки того, что у них есть разрешение на доступ к доменному имени. Например, запись "google-site-verification=yJTOgIk39vl3779N3QhPF-mAR36QE00J6LdXHeID4fM" используется Google для проверки того, что владелец веб-сайта имеет разрешение на доступ к службам Google для своего домена.
Запись SPF (Sender Policy Framework) в записях TXT используется для защиты от нежелательной почты и спуфинга, поскольку они содержат инструкции по получению почтовых серверов о том, каким серверам разрешено отправлять электронную почту для определенного домена.
Хорошо! Вот и все для учебника; Я надеюсь, что вам будет полезно извлечь ИНФОРМАЦИЮ DNS о доменном имени.
