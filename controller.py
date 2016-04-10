from dbconnect import Connection

def Test() :
    conn, cursor = Connection()
    x = cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return data
