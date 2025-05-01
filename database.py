import mysql.connector
import os


def mydb_connection():
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    if mydb.is_connected():
        print("Connected to MySQL Server..")
    else:
        print("Something went wrong!!")
    return mydb
