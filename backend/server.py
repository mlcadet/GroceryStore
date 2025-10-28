from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sql_connection import get_sql_connection
from products_dao import ProductsDAO
from uom_dao import UOMDAO  # ✅ UOM support
from orders_dao import OrdersDAO
import os
import json
import traceback

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
    """Create a new order.

    Expected JSON structure (example):
    {
      "order_date": "2025-10-15",
      "customer_id": 1,
      "total_amount": 12.50,
      "order_details": [ {"product_id": 2, "quantity": 3, "price_per_unit": 2.5}, ... ]
    }

    On success returns 201 with { "order_id": <id> }.
    Returns 400 for invalid payload and 500 for server errors.
    """
    data = request.get_json()
    # Accept wrapped payloads from older clients where the frontend sent
    # { data: JSON.stringify(payload) } — unwrap that case transparently.
    if data and isinstance(data, dict) and 'data' in data and isinstance(data['data'], str):
        try:
            data = json.loads(data['data'])
        except Exception:
            # leave data as-is; validation below will handle it
            pass

    print("Received order:", data)  # Debugging
    # Basic normalization: accept different frontend key names
    # Extract order_details (required)
    order_details = data.get('order_details') or data.get('orderDetails')
    if not order_details:
        return jsonify({"error": "Invalid order payload, missing 'order_details'"}), 400

    # Extract customer info and totals, with fallbacks
    order_date = data.get('order_date') or data.get('orderDate')
    customer_id = data.get('customer_id') or data.get('customerId')
    customer_name = data.get('customer_name') or data.get('customerName')
    total_amount = data.get('total_amount') or data.get('total_cost') or data.get('product_grand_total')

    # Build a normalized order object for the DAO
    normalized_order = {
        'order_date': order_date,
        'customer_id': customer_id,
        'customer_name': customer_name,
        'total_amount': total_amount,
        'order_details': order_details
    }

    try:
        order_id = orders_dao.insert_order(normalized_order)
        return jsonify({"message": "Order created", "order_id": order_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print('Error creating order:', e)
        traceback.print_exc()
        # TEMP DEBUG: include exception message in response to aid local debugging
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500

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

@app.route('/api/uoms', methods=['POST'])
def insert_uom():
    """Insert a new unit-of-measure.

    Expected JSON payload: { "uom_name": "kg" }
    Returns 201 with { "uom_id": <id> } on success.
    Returns 400 on invalid payload.
    """
    data = request.get_json()
    try:
        new_id = uom_dao.insert_uom(data)
        return jsonify({"message": "UOM inserted", "uom_id": new_id}), 201
    except ValueError as ve:
        # Insert validation failed (missing required fields)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print("Error inserting UOM:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/uoms/<int:uom_id>', methods=['DELETE'])
def delete_uom(uom_id):
    try:
        deleted = uom_dao.delete_uom(uom_id)
        if deleted:
            return jsonify({"message": f"Deleted {deleted} UOM(s)."}), 200
        else:
            return jsonify({"message": "No UOM found with that ID."}), 404
    except Exception as e:
        print("Error deleting UOM:", e)
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------------------
# Server Entry Point
# ----------------------------------------

if __name__ == '__main__':
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(port=5000, debug=True)

