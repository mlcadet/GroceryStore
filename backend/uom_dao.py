from sql_connection import get_sql_connection


class UOMDAO:
    def __init__(self, connection=None):
        # Keep for backwards compatibility but do not rely on it for live
        # connections. All methods will acquire a connection via
        # get_sql_connection() to avoid stale connection issues.
        self._initial_connection = connection

    def get_all_uoms(self):
        conn = get_sql_connection()
        with conn.cursor() as cursor:
            query = "SELECT uom_id, uom_name FROM gs.uom"
            cursor.execute(query)
            result = cursor.fetchall()
            return [
                {"uom_id": uom_id, "uom_name": uom_name}
                for uom_id, uom_name in result
            ]

    def insert_uom(self, uom):
        """Insert a UOM. Expects a dict with key 'uom_name'. Returns new id."""
        if not isinstance(uom, dict) or 'uom_name' not in uom:
            raise ValueError("Missing 'uom_name' in uom data")
        conn = get_sql_connection()
        with conn.cursor() as cursor:
            query = "INSERT INTO gs.uom (uom_name) VALUES (%s)"
            cursor.execute(query, (uom['uom_name'],))
            conn.commit()
            return cursor.lastrowid

    def delete_uom(self, uom_id):
        """Delete a UOM by id. Returns number of rows deleted."""
        conn = get_sql_connection()
        with conn.cursor() as cursor:
            query = "DELETE FROM gs.uom WHERE uom_id = %s"
            cursor.execute(query, (uom_id,))
            conn.commit()
            return cursor.rowcount

# # Optional test block
if __name__ == "__main__":
    from sql_connection import get_sql_connection

    connection = get_sql_connection()
    dao = UOMDAO(connection)
    uoms = dao.get_all_uoms()
    print(uoms)
    connection.close()