# Backend route docs (quick reference)

UOM routes:

- GET /api/uoms
  - Returns: JSON array of UOM objects [{"uom_id": 1, "uom_name": "each"}, ...]

- POST /api/uoms
  - Expected JSON: { "uom_name": "kg" }
  - Success: 201 { "message": "UOM inserted", "uom_id": <id> }
  - Error: 400 on invalid payload (missing 'uom_name'), 500 on server error

- DELETE /api/uoms/<id>
  - Success: 200 { "message": "Deleted X UOM(s)." }
  - Not found: 404 { "message": "No UOM found with that ID." }

Orders routes:

- POST /orders
  - Expected JSON example:
    {
      "order_date": "2025-10-15",
      "customer_id": 1,
      "total_amount": 12.50,
      "order_details": [ {"product_id": 2, "quantity": 3, "price_per_unit": 2.5}, ... ]
    }
  - Success: 201 { "message": "Order created", "order_id": <id> }
  - Error: 400 on invalid payload, 500 on server error

