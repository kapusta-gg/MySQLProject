import mysql.connector


def create_connection(user="user", password="user", host="localhost", db="test3"):
    con = mysql.connector.connect(user=user, password=password,
                                  host=host,
                                  database=db)
    return con

