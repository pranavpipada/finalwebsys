# finalwebsys
**README.md**

# FastAPI E-commerce API

This project implements a simple E-commerce API using FastAPI and SQLite database. It provides endpoints to manage customers, items, and orders.

## Functionality

### Customers

- **Create Customer**: Allows adding a new customer with a name and phone number.
- **Read Customer**: Retrieves customer details by customer ID.
- **Update Customer**: Modifies customer details such as name and phone number.
- **Delete Customer**: Removes a customer from the database.

### Items

- **Create Item**: Adds a new item with a name and price.
- **Read Item**: Retrieves item details by item ID.
- **Update Item**: Modifies item details such as name and price.
- **Delete Item**: Removes an item from the database.

### Orders

- **Create Order**: Creates a new order with customer ID, notes, and a list of item IDs.
- **Read Order**: Retrieves order details by order ID, including associated items.
- **Update Order**: Modifies order details such as notes and associated items.
- **Delete Order**: Removes an order from the database.

## Design

The project consists of two main components:

1. **Database Initialization Script (init_db.py)**:
   - Initializes the SQLite database and creates tables for customers, items, orders, and the many-to-many relationship between orders and items.
   - Populates the database with sample data from the provided JSON file (`example_orders.json`).

2. **FastAPI Application (main.py)**:
   - Implements CRUD operations for customers, items, and orders using FastAPI endpoints.
   - Each endpoint handles HTTP requests (POST, GET, PUT, DELETE) to perform corresponding database operations.
   - Utilizes Pydantic models for request and response data validation.
   - Establishes connections to the SQLite database and executes SQL queries using SQLite3 module.

## Usage

1. **Setup Environment**:
   - Ensure you have Python installed (preferably Python 3.7+).
   - Install required dependencies using `pip install -r requirements.txt`.

2. **Database Initialization**:
   - Run the initialization script `python init_db.py` to create the SQLite database and populate it with sample data.

3. **Run FastAPI Server**:
   - Start the FastAPI server using `python main.py`.
   - The server will run locally on `http://127.0.0.1:8000` by default.

4. **Interact with API**:
   - Use any HTTP client (e.g., cURL, Postman) or integrate with frontend applications to interact with the API endpoints.
   - Refer to the provided endpoint documentation in the source code or explore the OpenAPI documentation available at `http://127.0.0.1:8000/docs` for detailed API usage instructions.
