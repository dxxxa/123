#Connection
# Выбор способа подключения
print("Выбор способа подключения"
      "\n1. Connection URLs-"
      "\n2. Connection 2-"
      "\n3. Connection 3+\n")

userChoice = input("Enter Option: ")
if userChoice == "1":  # Connection URLs
    try:
        # пытаемся подключиться к базе данных
        connection = psycopg2.connect('postgresql://user:password@host:port/database_name')
    except:
        # в случае сбоя подключения будет выведено сообщение  в STDOUT
        print('Can`t establish connection to database')

elif userChoice == "2":
    try:
        # пытаемся подключиться к базе данных
        connection = psycopg2.connect(dbname='test', user='postgres', password='secret', host='host')
    except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')

elif userChoice == "3":
    try:
        # пытаемся подключиться к базе данных
        # connection = psycopg2.connect(dbname=DB_NAME, user=DB_UNAME, password=DB_PWD, host='5432')
        connection = psycopg2.connect(user="postgres",
                                      password="Qwerty123456!",  # пароль, который указали при установке PostgreSQL
                                      host="127.0.0.1",
                                      port="5432")
    except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')
else:
    print("Invalid Option!")

cursor = connection.cursor()  # Курсор для выполнения операций с базой данных
################################################################################