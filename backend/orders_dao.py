# CLASS-BASED DAO VERSION
from datetime import datetime
from sql_connection import get_sql_connection

class OrdersDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_order(self, order):
        # Basic validation
        if not order or 'order_details' not in order or not isinstance(order['order_details'], list):
            raise ValueError("Order must include 'order_details' list")

        cursor = self.connection.cursor()

        # include customer_name because the DB requires it in some schemas
        order_query = """
            INSERT INTO gs.orders (order_date, customer_id, customer_name, total_amount)
            VALUES (%s, %s, %s, %s)
        """
        order_data = (
            order.get('order_date'),
            order.get('customer_id'),
            order.get('customer_name'),
            order.get('total_amount')
        )
        cursor.execute(order_query, order_data)
        order_id = cursor.lastrowid

        # Some schemas include total_price in order_details; compute it here
        order_details_query = """
            INSERT INTO gs.order_details (order_id, product_id, quantity, price_per_unit, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """

        order_details_data = []
        for detail in order['order_details']:
            # normalize keys and compute price_per_unit when necessary
            product_id = int(detail.get('product_id') or detail.get('productId'))
            quantity = float(detail.get('quantity') or detail.get('qty') or 0)
            price = detail.get('price_per_unit') or detail.get('price') or detail.get('total_price')
            if price is None:
                # if only total_price provided, derive unit price
                total_price = detail.get('total_price')
                if total_price is not None and quantity:
                    price = float(total_price) / float(quantity)
                else:
                    price = 0.0
            price_per_unit = float(price)

            total_price = float(detail.get('total_price') or (quantity * price_per_unit))
            order_details_data.append((order_id, product_id, quantity, price_per_unit, total_price))
        if order_details_data:
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