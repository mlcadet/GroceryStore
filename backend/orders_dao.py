# CLASS-BASED DAO VERSION
from datetime import datetime
from sql_connection import get_sql_connection

class OrdersDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_order(self, order):
        cursor = self.connection.cursor()

        order_query = """
            INSERT INTO gs.orders (order_date, customer_id, total_amount)
            VALUES (%s, %s, %s)
        """
        order_data = (order['order_date'], order['customer_id'], order['total_amount'])
        cursor.execute(order_query, order_data)
        order_id = cursor.lastrowid

        order_details_query = """
            INSERT INTO gs.order_details (order_id, product_id, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
        """
        order_details_data = [
            (order_id,
             int(detail['product_id']),
             float(detail['quantity']),
             float(detail['price_per_unit']))
            for detail in order['order_details']
        ]
        cursor.executemany(order_details_query, order_details_data)
        self.connection.commit()
        cursor.close()
        return order_id

    def get_order_details(self, order_id):
        cursor = self.connection.cursor()
        query = """
            SELECT od.order_id, od.product_id, od.quantity, od.price_per_unit,
                   p.name AS product_name
            FROM gs.order_details od
            LEFT JOIN gs.products p ON od.product_id = p.product_id
            WHERE od.order_id = %s
        """
        cursor.execute(query, (order_id,))
        records = []
        for (order_id, product_id, quantity, price_per_unit, product_name) in cursor:
            records.append({
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'price_per_unit': price_per_unit,
                'product_name': product_name
            })
        cursor.close()
        return records

    def get_all_orders(self):
        cursor = self.connection.cursor()
        query = "SELECT order_id, order_date, customer_id, total_amount FROM gs.orders"
        cursor.execute(query)
        rows = cursor.fetchall()  # ← Fully consume the result set
        cursor.close()

        response = []
        for (order_id, order_date, customer_id, total_amount) in rows:
            response.append({
                'id': order_id,
                'order_date': order_date,
                'customer_id': customer_id,
                'total_amount': total_amount,
                'order_details': self.get_order_details(order_id)
            })
        return response

    def update_order(self, order_id, order):
        cursor = self.connection.cursor()
        query = """
            UPDATE gs.orders
            SET order_date = %s, customer_id = %s, total_amount = %s
            WHERE order_id = %s
        """
        cursor.execute(query, (
            order['order_date'],
            order['customer_id'],
            order['total_amount'],
            order_id
        ))
        self.connection.commit()
        cursor.close()
        return True

    def delete_order(self, order_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM gs.order_details WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM gs.orders WHERE order_id = %s", (order_id,))
        self.connection.commit()
        cursor.close()
        return True
        return response

if __name__ == "__main__":
    connection = get_sql_connection()
    dao = OrdersDAO(connection)

    print(dao.get_all_orders())
    print(dao.get_order_details(4))

    connection.close()