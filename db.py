import mysql.connector

def db_connect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlacc",
        database="pos_app"
    )
    return db
def display():
    print("Conection Successful")