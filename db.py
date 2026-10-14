import sqlite3
from pantry import pantry_stock , DB_PATH
import os
print("Seeding:", DB_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS pantry (
    item TEXT PRIMARY KEY,
    quantity REAL,
    unit TEXT,
    low_stock_threshold REAL
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    quantity REAL,
    unit_price REAL,
    ordered_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    product_title TEXT,
    unit TEXT,
    unit_price REAL,
    quantity REAL
)
""")

for item, d in pantry_stock.items():
    cur.execute(
        "INSERT OR REPLACE INTO pantry VALUES (?, ?, ?, ?)",
        (item, d["quantity"], d["unit"], d["low_stock_threshold"])
    )
conn.commit()

# conn.execute("UPDATE pantry SET quantity = 99 WHERE item = 'milk'")
print("*"*100)
print("PANTRY:")
for row in cur.execute("SELECT * FROM pantry"):
    print(row)
print("*"*100)
print("ORDERS:")
for row in cur.execute("SELECT * FROM orders"):
    print(row)
print("*"*100)
print("CART:")
for row in cur.execute("SELECT * FROM cart"):
    print(row)

print(sqlite3.connect(DB_PATH).execute("SELECT COUNT(*) FROM pantry").fetchone())

conn.close()