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








#--------------------------------------------------------------
# FLASK API
# from flask import Flask, request
# from flask_restx import Api, Resource, fields
# from sql_connection import get_sql_connection
# from datetime import datetime

# app = Flask(__name__)
# api = Api(app, title="Grocery Store Orders API", version="1.0", description="Manage orders")

# connection = get_sql_connection()
# orders_dao = OrdersDAO(connection)

# order_model = api.model('Order', {
#     'order_date': fields.String(required=False),
#     'customer_id': fields.Integer(required=True),
#     'total_amount': fields.Float(required=True),
#     'order_details': fields.List(fields.Nested(api.model('OrderDetail', {
#         'product_id': fields.Integer(required=True),
#         'quantity': fields.Float(required=True),
#         'price_per_unit': fields.Float(required=True)
#     })))
# })

# @api.route('/orders')
# class OrdersList(Resource):
#     @api.doc(description="Get all orders")
#     def get(self):
#         return orders_dao.get_all_orders()

#     @api.expect(order_model)
#     @api.doc(description="Create a new order")
#     def post(self):
#         order = request.json
#         if 'order_date' not in order:
#             order['order_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         order_id = orders_dao.insert_order(order)
#         return {'order_id': order_id}, 201

# @api.route('/orders/<int:order_id>')
# class Order(Resource):
#     @api.doc(description="Get details of a specific order")
#     def get(self, order_id):
#         return orders_dao.get_order_details(order_id)

#     @api.expect(order_model)
#     @api.doc(description="Update an existing order")
#     def put(self, order_id):
#         order = request.json
#         orders_dao.update_order(order_id, order)
#         return {'message': 'Order updated successfully'}

#     @api.doc(description="Delete an order")
#     def delete(self, order_id):
#         orders_dao.delete_order(order_id)
#         return {'message': 'Order deleted successfully'}

# if __name__ == "__main__":
#     from sql_connection import get_sql_connection

#     connection = get_sql_connection()
#     dao = OrdersDAO(connection)

#     print(dao.get_all_orders())
#     print(dao.get_order_details(4))

#     connection.close()


#--------------------------------------------------------------




#--------------------------------------------------------------
# from datetime import datetime
# from sql_connection import get_sql_connection

# def insert_order(connection, order):
#     cursor = connection.cursor()

#     order_query = """
#         INSERT INTO gs.orders (order_date, customer_id, total_amount)
#         VALUES (%s, %s, %s)
#     """
#     order_data = (order['order_date'], order['customer_id'], order['total_amount'])
#     cursor.execute(order_query, order_data)
#     order_id = cursor.lastrowid

#     order_details_query = """
#         INSERT INTO gs.order_details (order_id, product_id, quantity, price_per_unit)
#         VALUES (%s, %s, %s, %s)
#     """
#     order_details_data = [
#         (order_id,
#          int(detail['product_id']),
#          float(detail['quantity']),
#          float(detail['price_per_unit']))
#         for detail in order['order_details']
#     ]
#     cursor.executemany(order_details_query, order_details_data)
#     connection.commit()
#     cursor.close()
#     return order_id

# def get_order_details(connection, order_id):
#     cursor = connection.cursor()
#     query = """
#         SELECT od.order_id, od.product_id, od.quantity, od.price_per_unit,
#                p.name AS product_name
#         FROM gs.order_details od
#         LEFT JOIN gs.products p ON od.product_id = p.product_id
#         WHERE od.order_id = %s
#     """
#     cursor.execute(query, (order_id,))
#     records = []
#     for (order_id, product_id, quantity, price_per_unit, product_name) in cursor:
#         records.append({
#             'order_id': order_id,
#             'product_id': product_id,
#             'quantity': quantity,
#             'price_per_unit': price_per_unit,
#             'product_name': product_name
#         })
#     cursor.close()
#     return records

# def get_all_orders(connection):
#     cursor = connection.cursor()
#     query = "SELECT order_id, order_date, customer_id, total_amount FROM gs.orders"
#     cursor.execute(query)
#     response = []
#     for (order_id, order_date, customer_id, total_amount) in cursor:
#         response.append({
#             'id': order_id,
#             'order_date': order_date,
#             'customer_id': customer_id,
#             'total_amount': total_amount,
#             'order_details': get_order_details(connection, order_id)
#         })
#     cursor.close()
#     return response

# if __name__ == "__main__":
#     connection = get_sql_connection()
#     print(get_all_orders(connection))
#     print(get_order_details(connection, 4))
#     # Example insert:
#     # print(insert_order(connection, {
#     #     "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     #     "customer_id": 1,
#     #     "total_amount": 25.50,
#     #     "order_details": [
#     #         {"product_id": 1, "quantity": 2, "price_per_unit": 10.00},
#     #         {"product_id": 2, "quantity": 1, "price_per_unit": 5.50}
#     #     ]
#     # }))
#     connection.close()
