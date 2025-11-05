from sql_connection import get_sql_connection
import mysql.connector
from mysql.connector import errors as mysql_errors


class ProductsDAO:
    def __init__(self, connection=None):
        # Do not rely on a long-lived connection; acquire per method
        self._initial_connection = connection

    # Fetch all products
    def get_all_products(self):
        # Acquire a fresh connection for this method and retry once on lost-connection
        conn = get_sql_connection()
        cursor = None
        query = """
            SELECT 
              products.product_id, 
              products.name, 
              products.uom_id, 
              products.price_per_unit, 
              uom.uom_name
            FROM gs.products
            INNER JOIN gs.uom ON products.uom_id = uom.uom_id;
            """

        try:
            cursor = conn.cursor()
            cursor.execute(query)
        except mysql_errors.OperationalError as oe:
            # Lost connection during query — attempt one reconnect and retry
            try:
                conn = get_sql_connection(retries=2)
                if cursor:
                    try:
                        cursor.close()
                    except Exception:
                        pass
                cursor = conn.cursor()
                cursor.execute(query)
            except Exception:
                # Re-raise so caller gets a proper error (and server can return 500)
                if cursor:
                    try:
                        cursor.close()
                    except Exception:
                        pass
                raise

        response = []
        try:
            for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
                print(f"Product ID: {product_id}, Name: {name}, UOM ID: {uom_id}, Price per Unit: {price_per_unit}, UOM Name: {uom_name}")
                response.append({
                    "product_id": product_id,
                    "name": name,
                    "uom_id": uom_id,
                    "price_per_unit": price_per_unit,
                    "uom_name": uom_name
                })
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
        return response

    # Validate and insert a new product
    def insert_product(self, product):
        required_keys = ['product_name', 'uom_id', 'price_per_unit']
        if not all(key in product for key in required_keys):
            raise ValueError(f"Missing keys in product: {product}")

        conn = get_sql_connection()
        with conn.cursor() as cursor:
            query = ("INSERT INTO gs.products"
                     "(name, uom_id, price_per_unit) "
                     "VALUES (%s, %s, %s)")
            data = (product['product_name'], product['uom_id'], product['price_per_unit'])
            cursor.execute(query, data)
            conn.commit()
            return cursor.lastrowid

    # Delete a product
    def delete_product(self, product_id):
        conn = get_sql_connection()
        with conn.cursor() as cursor:
            query = "DELETE FROM gs.products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount

# Optional: test block
if __name__ == "__main__":
    connection = get_sql_connection()
    dao = ProductsDAO(connection)
    products = dao.get_all_products()
    print(products)
    # print(dao.insert_product({"product_name": "cabbage", "uom_id": 1, "price_per_unit": "1.50"}))
    # print(dao.delete_product(11))