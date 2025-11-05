import mysql.connector
from sql_connection import get_sql_connection
import sys

def setup_database():
    # First try to connect without database to create it
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Steelbed@386"
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS gs")
        print("Database 'gs' created or already exists.")
        
        # Switch to gs database
        cursor.execute("USE gs")
        
        # Create UOM table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS uom (
            uom_id INT NOT NULL AUTO_INCREMENT,
            uom_name VARCHAR(45) NOT NULL,
            PRIMARY KEY (uom_id)
        )""")
        print("Table 'uom' created or already exists.")
        
        # Create products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            uom_id INT NOT NULL,
            price_per_unit DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (product_id),
            FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
        )""")
        print("Table 'products' created or already exists.")
        
        # Insert default UOMs if not exists
        cursor.execute("SELECT COUNT(*) FROM uom")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO uom (uom_name) VALUES 
                ('each'),
                ('kg'),
                ('liter')
            """)
            print("Default UOMs inserted.")
        
        # Insert sample products if not exists
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO products (name, uom_id, price_per_unit) VALUES 
                ('Apple', 2, 1.00),
                ('Bread', 1, 2.50),
                ('Milk', 3, 3.00)
            """)
            print("Sample products inserted.")
        
        conn.commit()
        print("\nDatabase setup completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running (net start MySQL80)")
        print("2. Verify credentials in sql_connection.py are correct")
        print("3. Check if you can connect using MySQL Workbench")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("Setting up MySQL database for Grocery Store...")
    setup_database()