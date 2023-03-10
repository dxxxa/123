# ----- Example Python program that removes a PostgreSQL database -----
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
postgresConnection = psycopg2.connect(user="postgres",
                                  password="Qwerty123456!",
                                  host="127.0.0.1",
                                  port="5432")

postgresConnection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a database Cursor
cur_ob = postgresConnection.cursor()
name_db = "MyTestDatabase"

# Create database statement
sqlCreateDB = "create database " + name_db + ";"

# Create a database in PostgreSQL database
cur_ob.execute(sqlCreateDB)

# SQL statement for querying the list of databases
sqlQuery = "SELECT datname FROM pg_database WHERE datistemplate = false;"

# Execute the query statement
cur_ob.execute(sqlQuery)

# Retrieve all the rows from the cursor
rows = cur_ob.fetchall()

print("---List of databases before removing one:---")
for row in rows:
    print('%s' % (row[0]))

# Remove database statement
sqlRemDb = "DROP database " + name_db + ";"

cur_ob.execute(sqlRemDb)

# Remove the PostgreSQL database
cur_ob.execute(sqlQuery)

# Retrieve all the rows from the cursor
rows = cur_ob.fetchall()

print("---List of databases after removing one:---")

for row in rows:
    print('%s' % (row[0]))
