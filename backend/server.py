from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sql_connection import get_sql_connection
from products_dao import ProductsDAO
from uom_dao import UOMDAO  # ✅ Added for UOM support

app = Flask(__name__, static_folder='ui', static_url_path='')
CORS(app)

# Initialize DAOs
connection = get_sql_connection()
dao = ProductsDAO(connection)
uom_dao = UOMDAO(connection)

# Serve order.html when visiting root or /new-order
@app.route('/')
@app.route('/new-order')
def serve_order_page():
    return send_from_directory('ui', 'order.html')

# Health check
@app.route('/hello')
def hello():
    return "Hello, World!"

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = dao.get_all_products()
    return jsonify(products)

# Insert a new product
@app.route('/products', methods=['POST'])
def insert_product():
    data = request.get_json()
    try:
        new_id = dao.insert_product(data)
        return jsonify({"message": "Product inserted", "product_id": new_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

# Accept order from frontend
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    print("Received order:", data)  # Debugging
    # TODO: Save to database using OrdersDAO
    return jsonify({"message": "Order received"}), 201

# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    deleted = dao.delete_product(product_id)
    if deleted:
        return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
    else:
        return jsonify({"message": "No product found with that ID."}), 404

# ✅ API aliases for frontend compatibility
@app.route('/api/products', methods=['GET'])
def get_products_api():
    return get_products()

@app.route('/api/products', methods=['POST'])
def insert_product_api():
    return insert_product()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product_api(product_id):
    return delete_product(product_id)

@app.route('/api/orders', methods=['POST'])
def create_order_api():
    return create_order()

@app.route('/api/uoms', methods=['GET'])
def get_uoms():
    uoms = uom_dao.get_all_uoms()
    return jsonify(uoms)

# Start the server
if __name__ == '__main__':
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(port=5000, debug=True)




#-----------------------------------------------
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from sql_connection import get_sql_connection
# from products_dao import ProductsDAO

# app = Flask(__name__, static_folder='ui', static_url_path='')
# CORS(app)

# # Initialize DAO
# dao = ProductsDAO(get_sql_connection())

# # Serve order.html when visiting root or /new-order
# @app.route('/')
# @app.route('/new-order')
# def serve_order_page():
#     return send_from_directory('ui', 'order.html')

# # Health check
# @app.route('/hello')
# def hello():
#     return "Hello, World!"

# # Get all products
# @app.route('/products', methods=['GET'])
# def get_products():
#     products = dao.get_all_products()
#     return jsonify(products)

# # Insert a new product
# @app.route('/products', methods=['POST'])
# def insert_product():
#     data = request.get_json()
#     try:
#         new_id = dao.insert_product(data)
#         return jsonify({"message": "Product inserted", "product_id": new_id}), 201
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": "Internal server error"}), 500

# # Accept order from frontend
# @app.route('/orders', methods=['POST'])
# def create_order():
#     data = request.get_json()
#     print("Received order:", data)  # Debugging
#     # TODO: Save to database using OrdersDAO
#     return jsonify({"message": "Order received"}), 201

# # Delete a product
# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     deleted = dao.delete_product(product_id)
#     if deleted:
#         return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
#     else:
#         return jsonify({"message": "No product found with that ID."}), 404

# # Start the server
# if __name__ == '__main__':
#     print("Starting Python Flask Server for Grocery Store Management System")
#     app.run(port=5000, debug=True)



#---------------------------
# from flask import Flask, request, jsonify
# from flask import send_from_directory
# from flask_cors import CORS
# from sql_connection import get_sql_connection
# from products_dao import ProductsDAO

# app = Flask(__name__)
# CORS(app)  # ✅ Enable CORS for frontend-backend communication

# dao = ProductsDAO(get_sql_connection())

# # ✅ Serve order.html from /new-order
# @app.route('/new-order')
# def new_order():
#     return send_from_directory('ui', 'order.html')

# # ✅ Health check
# @app.route('/hello')
# def hello():
#     return "Hello, World!"

# # ✅ Get all products
# @app.route('/products', methods=['GET'])
# def get_products():
#     products = dao.get_all_products()
#     return jsonify(products)

# # ✅ Insert a new product
# @app.route('/products', methods=['POST'])
# def insert_product():
#     data = request.get_json()
#     try:
#         new_id = dao.insert_product(data)
#         return jsonify({"message": "Product inserted", "product_id": new_id}), 201
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": "Internal server error"}), 500

# # ✅ Accept order from frontend
# @app.route('/orders', methods=['POST'])
# @app.route('/api/orders', methods=['POST'])  # Alias for frontend compatibility
# def create_order():
#     data = request.get_json()
#     print("Received order:", data)  # ✅ Log incoming payload
#     # TODO: Save to database using OrdersDAO
#     return jsonify({"message": "Order received"}), 201

# # ✅ Delete a product
# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     deleted = dao.delete_product(product_id)
#     if deleted:
#         return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
#     else:
#         return jsonify({"message": "No product found with that ID."}), 404

# # ✅ Start the server
# if __name__ == '__main__':
#     print("Starting Python Flask Server for Grocery Store Management System")
#     app.run(port=5000, debug=True)




#-------------------------------
# from flask import Flask, request, jsonify
# from flask import send_from_directory
# from flask_cors import CORS
# from sql_connection import get_sql_connection
# from products_dao import ProductsDAO

# app = Flask(__name__)
# dao = ProductsDAO(get_sql_connection())

# @app.route('/new-order')
# def new_order():
#     return send_from_directory('ui', 'order.html')


# # Health check
# @app.route('/hello')
# def hello():
#     return "Hello, World!"

# # Get all products
# @app.route('/products', methods=['GET'])
# def get_products():
#     products = dao.get_all_products()
#     return jsonify(products)

# # Insert a new product
# @app.route('/products', methods=['POST'])
# def insert_product():
#     data = request.get_json()
#     try:
#         new_id = dao.insert_product(data)
#         return jsonify({"message": "Product inserted", "product_id": new_id}), 201
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": "Internal server error"}), 500

# # Order a product
# @app.route('/orders', methods=['POST'])
# def create_order():
#     data = request.get_json()
#     # Save to database or process order
#     return jsonify({"message": "Order received"}), 201

# # Delete a product
# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     deleted = dao.delete_product(product_id)
#     if deleted:
#         return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
#     else:
#         return jsonify({"message": "No product found with that ID."}), 404

# if __name__ == '__main__':
#     print("Starting Python Flask Server for Grocery Store Management System")
#     app.run(port=5000, debug=True)

