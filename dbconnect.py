# from flask.ext.mysql import MySQL
# from flask_mysql import MySQL
import MySQLdb

def Connection () :
    conn = MySQLdb.connect(host = "127.0.0.1" ,
                            user = "root",
                            passwd = "pankaj",
                            db = "flask")
    cursor = conn.cursor()
    return conn, cursor
