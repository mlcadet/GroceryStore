from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sql_connection import get_sql_connection
from products_dao import ProductsDAO
from uom_dao import UOMDAO  # ✅ UOM support
from orders_dao import OrdersDAO
import os

CWD = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.normpath(os.path.join(CWD, '..', 'ui'))

app = Flask(__name__, static_folder=UI_DIR, static_url_path='')
CORS(app)

# Initialize DAOs
connection = get_sql_connection()
dao = ProductsDAO(connection)
uom_dao = UOMDAO(connection)
orders_dao = OrdersDAO(connection)

# ----------------------------------------
# Static Routes
# ----------------------------------------

@app.route('/')
@app.route('/new-order')
def serve_order_page():
    # serve the order.html from the ui folder next to the project root
    return send_from_directory(UI_DIR, 'order.html')

@app.route('/hello')
def hello():
    return "Hello, World!"

# ----------------------------------------
# Product Routes
# ----------------------------------------

@app.route('/products', methods=['GET'])
def get_products():
    products = dao.get_all_products()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def insert_product():
    data = request.get_json()
    try:
        new_id = dao.insert_product(data)
        return jsonify({"message": "Product inserted", "product_id": new_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    deleted = dao.delete_product(product_id)
    if deleted:
        return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
    else:
        return jsonify({"message": "No product found with that ID."}), 404

# ----------------------------------------
# Product API Aliases
# ----------------------------------------

@app.route('/api/products', methods=['GET'])
def get_products_api():
    return get_products()

@app.route('/api/products', methods=['POST'])
def insert_product_api():
    return insert_product()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product_api(product_id):
    return delete_product(product_id)

# ----------------------------------------
# Order Routes
# ----------------------------------------

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    print("Received order:", data)  # Debugging
    # TODO: Save to database using OrdersDAO
    return jsonify({"message": "Order received"}), 201

@app.route('/api/orders', methods=['POST'], endpoint='create_order_alias')
def create_order_alias():
    return create_order()


@app.route('/api/orders', methods=['GET'])
def get_orders_api():
    # return all orders from the OrdersDAO
    try:
        orders = orders_dao.get_all_orders()
        return jsonify(orders), 200
    except Exception as e:
        print('Error fetching orders:', e)
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------------------
# UOM Routes
# ----------------------------------------

@app.route('/api/uoms', methods=['GET'])
def get_uoms():
    uoms = uom_dao.get_all_uoms()
    return jsonify(uoms)

# ----------------------------------------
# Server Entry Point
# ----------------------------------------

if __name__ == '__main__':
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(port=5000, debug=True)

