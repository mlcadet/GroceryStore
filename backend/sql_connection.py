import mysql.connector

cnx = None

def get_sql_connection():
    global cnx
    if cnx is None:
        cnx = mysql.connector.connect(
            user='root',
            password='Steelbed@386',
            host='127.0.0.1',
            database='gs'
        )
    return cnx
