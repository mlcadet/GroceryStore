# Grocery Store Management System

A full-stack web application for managing a grocery store's products, orders, and inventory.

## Project Overview

This system provides:
- Product management (CRUD operations)
- Order processing
- Unit of measurement (UOM) management
- Inventory tracking

## Tech Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- MySQL Connector/Python
- MySQL 8.0 Database

### Frontend
- HTML5/CSS3
- JavaScript (ES6+)
- jQuery
- Bootstrap 4.5.2

## Project Structure
```
GroceryStore/
├── backend/
│   ├── server.py            # Flask application server
│   ├── sql_connection.py    # Database connection management
│   ├── products_dao.py      # Products data access layer
│   ├── orders_dao.py        # Orders data access layer
│   └── uom_dao.py          # Units of measurement data access layer
├── ui/
│   ├── index.html          # Dashboard/home page
│   ├── manage_product.html # Product management interface
│   ├── order.html         # Order processing interface
│   ├── css/
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── custom.css
│   │   ├── layout.css
│   │   └── sidebar-menu.css
│   ├── js/
│   │   ├── custom/
│   │   │   ├── common.js
│   │   │   ├── dashboard.js
│   │   │   ├── manage_product.js
│   │   │   └── order.js
│   │   └── package/
│   │       └── jquery.min.js
│   └── images/
└── tests/
    └── test_uom_dao.py    # Unit tests for UOM DAO
```

## Key Features

1. **Robust Database Connection Handling**
   - Connection pooling
   - Automatic reconnection on failure
   - Per-request connection management

2. **Product Management**
   - Add/Edit/Delete products
   - Associate products with units of measurement
   - Price management

3. **Order Processing**
   - Create new orders
   - Add multiple products to orders
   - Calculate order totals

4. **Data Access Layer**
   - Separate DAO classes for products, orders, and UOMs
   - Error handling and validation
   - Transaction management

## Setup Instructions

1. **Database Setup**
```sql
CREATE DATABASE gs;
USE gs;

CREATE TABLE uom (
    uom_id INT PRIMARY KEY AUTO_INCREMENT,
    uom_name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    uom_id INT,
    price_per_unit DECIMAL(10,2),
    FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    total_amount DECIMAL(10,2),
    order_date DATE
);

CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    quantity DECIMAL(10,2),
    price_per_unit DECIMAL(10,2),
    total_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

2. **Python Environment Setup**
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install Flask
pip install flask-cors
pip install mysql-connector-python
```

3. **Configuration**
- Update database credentials in `backend/sql_connection.py`
- Verify port settings in `backend/server.py`
- Check API base URL in `ui/js/custom/common.js`

4. **Running the Application**
```bash
# Start the Flask server
python backend/server.py

# Access the application
http://127.0.0.1:5000/
```

## Common Issues and Solutions

1. **MySQL Connection Issues**
   - Ensure MySQL service is running
   - Verify credentials in sql_connection.py
   - Check if database and tables exist

2. **CORS Errors**
   - Frontend and backend must use same origin or
   - CORS must be properly configured in Flask

3. **Product Management**
   - Validate UOM selection before saving
   - Ensure price format is correct

## Best Practices Implemented

1. **Database**
   - Connection pooling
   - Proper error handling
   - Transaction management
   - Prepared statements

2. **Backend**
   - Modular architecture (DAOs)
   - Input validation
   - Error handling
   - CORS security

3. **Frontend**
   - Form validation
   - Error feedback
   - Responsive design
   - Clean UI/UX

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

## Development Notes

- Use relative API paths to avoid CORS issues
- Handle MySQL connection timeouts
- Validate all form inputs
- Provide user feedback for all actions
- Keep UI responsive and user-friendly

## Security Considerations

1. Input Validation
   - Sanitize all user inputs
   - Validate data types and ranges
   - Use prepared statements

2. Error Handling
   - Don't expose internal errors
   - Log errors securely
   - Provide user-friendly messages

3. Database
   - Use connection pooling
   - Manage connections properly
   - Handle timeouts gracefully

## Contributors

- Project Lead: [Your Name]
- Development Team: [Team Members]

## License

[Your License Choice]