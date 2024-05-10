import sqlite3
import json


# Define function to initialize database tables
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

    # Create customers table
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL
                    )''')

    # Create items table
cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL
                    )''')

    # Create orders table
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY,
                        customer_id INTEGER NOT NULL,
                        timestamp INTEGER NOT NULL,
                        notes TEXT,
                        FOREIGN KEY (customer_id) REFERENCES customers (id)
                    )''')




    # Create order_items table for many-to-many relationship between orders and items
cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                        order_id INTEGER,
                        item_id INTEGER,
                        PRIMARY KEY (order_id, item_id),
                        FOREIGN KEY (order_id) REFERENCES orders (id),
                        FOREIGN KEY (item_id) REFERENCES items (id)
                    )''')
with open('example_orders.json') as file:
    data = json.load(file)
    

customers = {}
items = {}

for order in data:
    customers[order["phone"]] = order["name"]
    for item in order["items"]:
        items[item["name"]] = item["price"]
    

for phone, name in customers.items():
    cursor.execute("INSERT INTO customers(name, phone) VALUES(?,?)",(name,phone))
    
for name, price in items.items():
    cursor.execute("INSERT INTO items(name, price) VALUES(?,?)",(name,price))
    
for order in data:
    cursor.execute("SELECT id FROM customers WHERE phone = ? ",(order["phone"],))
    cust_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO orders (notes, timestamp, customer_id) VALUES(?,?,?)", (order["notes"],order["timestamp"], cust_id))
    order_id = cursor.lastrowid
    for item in order["items"]:
        cursor.execute("SELECT id FROM items WHERE name = ? ",(item["name"],))
        item_id = cursor.fetchone()[0]
        try:
            cursor.execute("INSERT INTO order_items(order_id, item_id) VALUES(?,?)", (order_id, item_id))
        except sqlite3.IntegrityError:
            # Ignore if the pair already exists
            pass
        # cursor.execute("INSERT INTO order_items(order_id, item_id) VALUES(?,?)",(order_id, item_id))
    

conn.commit()
conn.close()
