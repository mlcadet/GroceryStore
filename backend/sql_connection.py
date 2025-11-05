import mysql.connector
from mysql.connector import Error
import time

# Keep a global connection but reconnect when needed to avoid
# "MySQL Connection not available." OperationalError caused by
# stale connections.
cnx = None

def get_sql_connection(retries=3, delay=0.5):
    """Return a live MySQL connection. If an existing global connection
    is closed or not available, try to reconnect. Retries will back off
    exponentially (delay * 2^attempt).

    NOTE: Credentials are read from this file for simplicity; for
    production consider using environment variables or a secure vault.
    """
    global cnx
    try:
        if cnx is None or not getattr(cnx, 'is_connected', lambda: False)():
            cnx = mysql.connector.connect(
                user='root',
                password='Steelbed@386',
                host='127.0.0.1',
                database='gs',
                autocommit=False
            )
    except Error as e:
        if retries > 0:
            time.sleep(delay)
            return get_sql_connection(retries=retries-1, delay=delay*2)
        # re-raise the last error to let caller decide how to handle it
        raise
    return cnx
