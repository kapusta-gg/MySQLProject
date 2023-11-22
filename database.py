import mysql.connector


def create_connection(user="user", password="user", host="localhost", db="test3"):
    con = mysql.connector.connect(user=user, password=password,
                                  host=host,
                                  database=db)
    return con


if __name__ == "__main__":
    cnx = create_connection()
    cur = cnx.cursor()

    data = cur.execute("SELECT * FROM student")
    row = cur.fetchall()

    for r in row:
        print(r)

    data = cur.execute("SELECT * FROM teacher")
    row = cur.fetchall()

    for r in row:
        print(r)

