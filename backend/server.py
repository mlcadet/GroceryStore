from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
from products_dao import ProductsDAO

app = Flask(__name__)
dao = ProductsDAO(get_sql_connection())

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

# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    deleted = dao.delete_product(product_id)
    if deleted:
        return jsonify({"message": f"Deleted {deleted} product(s)."}), 200
    else:
        return jsonify({"message": "No product found with that ID."}), 404

if __name__ == '__main__':
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(port=5000, debug=True)

