from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    description : str | None = None
    price : float
    tax: float | None = None

class Customer(BaseModel):
    cust_id:int | None = None
    name: str
    phone: str



class Order(BaseModel):
    cust_id: int
    notes: str
    items: List[int]  # Automatically generate timestamp



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# Database connection
conn = sqlite3.connect('db.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


# Pydantic models for request and response bodies
class Customer(BaseModel):
    name: str
    phone: str


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    timestamp: int
    name: str
    phone: str
    items: list[Item]
    notes: str = ""


# Routes
@app.post("/customers")
async def create_customer(customer: Customer):
    cursor.execute("INSERT INTO customers(name, phone) VALUES(?,?)", (customer.name, customer.phone))
    conn.commit()
    return {"message": "Customer created successfully"}


@app.get("/customers/{customer_id}")
async def read_customer(customer_id: int):
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    return {"message": "Customer deleted successfully"}


@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    cursor.execute("UPDATE customers SET name=?, phone=? WHERE id=?", (customer.name, customer.phone, customer_id))
    conn.commit()
    return {"message": "Customer updated successfully"}


# Similarly implement endpoints for items and orders

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# Routes for Customers
@app.post("/customers")
async def create_customer(customer: Customer):
    cursor.execute("INSERT INTO customers(name, phone) VALUES(?,?)", (customer.name, customer.phone))
    conn.commit()
    return {"message": "Customer created successfully"}


@app.get("/customers/{customer_id}")
async def read_customer(customer_id: int):
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    return {"message": "Customer deleted successfully"}


@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    cursor.execute("UPDATE customers SET name=?, phone=? WHERE id=?", (customer.name, customer.phone, customer_id))
    conn.commit()
    return {"message": "Customer updated successfully"}


# Routes for Items
@app.post("/items")
async def create_item(item: Item):
    cursor.execute("INSERT INTO items(name, price) VALUES(?,?)", (item.name, item.price))
    conn.commit()
    return {"message": "Item created successfully"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    cursor.execute("UPDATE items SET name=?, price=? WHERE id=?", (item.name, item.price, item_id))
    conn.commit()
    return {"message": "Item updated successfully"}


# Routes for Orders
@app.post("/orders")
async def create_order(order: Order):
    cursor.execute("INSERT INTO orders( phone, notes) VALUES(?,?,?,?)", 
                   (order.phone, order.notes))
    order_id = cursor.lastrowid
    for item in order.items:
        cursor.execute("SELECT id FROM items WHERE name = ?", (item.name,))
        item_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO order_items(order_id, item_id) VALUES(?,?)", (order_id, item_id))
    conn.commit()
    return {"message": "Order created successfully"}


@app.get("/orders/{order_id}")
async def read_order(order_id: int):
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("SELECT items.name, items.price FROM order_items JOIN items ON order_items.item_id = items.id WHERE order_items.order_id = ?", (order_id,))
    items = cursor.fetchall()
    order_dict = dict(order)
    order_dict["items"] = [{"name": item["name"], "price": item["price"]} for item in items]
    return order_dict


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    return {"message": "Order deleted successfully"}


@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    cursor.execute("UPDATE orders SET timestamp=?, name=?, phone=?, notes=? WHERE id=?", 
                   (order.timestamp, order.name, order.phone, order.notes, order_id))
    # Delete existing items for the order
    cursor.execute("DELETE FROM order_items WHERE order_id=?", (order_id,))
    # Insert updated items
    for item in order.items:
        cursor.execute("SELECT id FROM items WHERE name = ?", (item.name,))
        item_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO order_items(order_id, item_id) VALUES(?,?)", (order_id, item_id))
    conn.commit()
    return {"message": "Order updated successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
