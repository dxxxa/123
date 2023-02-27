# [How to Connect to a Remote MySQL Database in Python](https://www.thepythoncode.com/article/connect-to-a-remote-mysql-server-in-python)
##
# [[] / []]()
Как разработчик программного обеспечения, вы можете столкнуться с необходимостью подключения к удаленному серверу MySQL в вашем приложении. Однако параметр MySQL по умолчанию не разрешает удаленные подключения. Из этого туториала Вы узнаете, как подключиться к удаленному серверу MySQL на Python.

Мы будем использовать библиотеку коннекторов Python MySQL, давайте установим ее:

pip3 install mysql-connector-python
Приведенный ниже код отвечает за подключение к серверу MySQL:

import mysql.connector as mysql

# enter your server IP address/domain name
HOST = "x.x.x.x" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "database"
# this is the user you create
USER = "python-user"
# user password
PASSWORD = "Password1$"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
# enter your code here!
Метод mysql.connect() требует 4 аргументов:

host: это ваш удаленный сервер MySQL, вы можете использовать его IP-адрес или доменное имя.
database: имя базы данных, к которой вы хотите получить доступ, вы можете оставить ее пустой, если вы хотите подключиться только к серверу MySQL.
user: это имя пользователя, которого вы будете создавать для удаленного доступа, через минуту мы увидим, как его создать.
password: пароль этого пользователя.
Если вы измените эти параметры на данные вашего сервера (даже если они правильные данные), вы столкнетесь с ошибкой путаницы, подобной этой:

mysql.connector.errors.ProgrammingError: 1045 (28000): Access denied for user 'python-user'@'your ip address' (using password: YES)
Это потому, что просто MySQL не разрешает удаленные соединения, давайте посмотрим, сможем ли мы это исправить.

Разрешение удаленных подключений на сервере MySQL
Во-первых, вам нужно будет найти файл mysqld.cnf в вашей системе (my.ini в Windows), размещение этого файла может отличаться в зависимости от вашей версии MySQL и операционной системы. Самый простой способ найти файл конфигурации MySQL, это найти его, давайте выполним следующую команду:

$ locate mysqld.cnf
После того, как я выполнил вышеуказанную команду на Ubuntu 18.04, был напечатан следующий путь:

/etc/mysql/mysql.conf.d/mysqld.cnf
Поэтому перейдите к этому файлу и найдите строку, которая начинается с bind-address. По умолчанию он установлен на 127.0.0.1, что означает, что сервер будет принимать только локальные соединения, вам нужно установить его на свой внешний общедоступный IP-адрес или вы хотите установить его на 0.0.0.0, если ваш IP-адрес не является статическим (может измениться при перезагрузке и т. Д.). Яне могу найти строку в этом файле, просто добавьте ее:

Разрешение удаленных подключений на сервере MySQL

Secondly, you need to allow your client/remote IP address the access to the MySQL port on the firewall:

$ sudo ufw allow from <Remote_IP_Address> to any port 3306
If your remote IP address changes or you may want to allow it from all over the world (maybe a little bit dangerous), you can allow that port for everyone:

$ sudo ufw allow 3306
Создание пользователя для удаленного доступа
Наконец, перейдите на свой сервер MySQL и создайте пользователя:

/* '%' means from any where in the world*/
mysql> CREATE USER 'python-user'@'%' IDENTIFIED BY 'Password1$';
Вы можете быть знакомы с созданием пользователей для localhost, в этом случае мы использовали символ '%', что означает, что к этому пользователю можно получить доступ с любого удаленного хоста.

Опять же, если вам нужен определенный удаленный IP-адрес вместо всех, вы можете изменить «%» на «<Remote_IP_Address>», будет выглядеть примерно так:

mysql> CREATE USER 'python-user'@'<Remote_IP_Address>' IDENTIFIED BY 'password';
Вам необходимо заменить <Remote_IP_Address> фактическим IP-адресом машины, к которой вы планируете подключиться.

Если вы вернетесь к своему сценарию и запустите его, на этот раз вы получите другую ошибку:

mysql.connector.errors.ProgrammingError: 1044 (42000): Access denied for user 'python-user'@'%' to database 'database'
Это легко исправить, нам нужно предоставить вновь созданному пользователю все привилегии, вернуться на свой сервер MySQL и выполнить следующую команду:

/* grant all privileges to the user on all databases & tables available in the server */
mysql> GRANT ALL ON *.* TO 'python-user'@'%';
С помощью этой команды мы предоставили этому пользователю все привилегии на все базы данных и все таблицы, вы можете настроить это любым способом.

Наконец, давайте удалим привилегии, чтобы MySQL начал их использовать:

mysql> FLUSH PRIVILEGES;
Заключение
Удивительно, теперь, следуя этому руководству, вы можете подключаться к своему удаленному серверу MySQL не только с Python, но и с любого языка программирования.

Если вы не знаете, как использовать коннектор MySQL Python, ознакомьтесь с этим учебником, который научит вас, как вы можете создавать базу данных, таблицы, добавлять строки в эту таблицу, извлекать данные и т. Д.

Рекомендуемые курсы
Наконец, многие концепции баз данных здесь подробно не обсуждаются. Если вы чувствуете, что хотите больше узнать о базах данных с помощью Python, я настоятельно рекомендую вам пройти следующие курсы:

Курс Python для всех
Курс "Использование баз данных с Python"