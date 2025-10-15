from sql_connection import get_sql_connection

class ProductsDAO:
    def __init__(self, connection):
        self.connection = connection

    #Fetch all products
    def get_all_products(self):
        with self.connection.cursor() as cursor:
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
            cursor.execute(query)
            response = []
            for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
                print(f"Product ID: {product_id}, Name: {name}, UOM ID: {uom_id}, Price per Unit: {price_per_unit}, UOM Name: {uom_name}")
                response.append({
                    "product_id": product_id,
                    "name": name,
                    "uom_id": uom_id,
                    "price_per_unit": price_per_unit,
                    "uom_name": uom_name
                })
            return response

    #Validate and insert a new product
    def insert_product(self, product):
        required_keys = ['product_name', 'uom_id', 'price_per_unit']
        if not all(key in product for key in required_keys):
            raise ValueError(f"Missing keys in product: {product}")

        with self.connection.cursor() as cursor:
            query = ("INSERT INTO gs.products"
                     "(name, uom_id, price_per_unit) "
                     "VALUES (%s, %s, %s)")
            data = (product['product_name'], product['uom_id'], product['price_per_unit'])
            cursor.execute(query, data)
            self.connection.commit()
            return cursor.lastrowid

    #Delete a product
    def delete_product(self, product_id):
        with self.connection.cursor() as cursor:
            query = "DELETE FROM gs.products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
            return cursor.rowcount

# Optional: test block
if __name__ == "__main__":
    connection = get_sql_connection()
    dao = ProductsDAO(connection)
    products = dao.get_all_products()
    print(products)
    # print(dao.insert_product({"product_name": "cabbage", "uom_id": 1, "price_per_unit": "1.50"}))
    # print(dao.delete_product(11))


