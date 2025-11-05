import mysql.connector
from mysql.connector import Error
import time

def get_sql_connection(retries=3, delay=0.5):
    """Create and return a new MySQL connection.

    Previously we cached a global connection which caused "commands out
    of sync" and lost-connection errors when multiple cursors were used
    concurrently. Returning a fresh connection per call avoids those
    issues in this small app.

    The function will retry a few times with exponential backoff on
    connection errors.
    """
    attempt = 0
    while True:
        try:
            conn = mysql.connector.connect(
                user='root',
                password='Steelbed@386',
                host='127.0.0.1',
                database='gs',
                autocommit=False
            )
            return conn
        except Error:
            attempt += 1
            if attempt > retries:
                raise
            time.sleep(delay * (2 ** (attempt - 1)))
