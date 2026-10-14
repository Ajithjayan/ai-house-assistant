from mcp_server import list_low_stock_items
import sqlite3
from pantry import get_pantry_status, DB_PATH
# pyrefly: ignore [missing-import]
from cart import add_to_cart, view_cart , place_order
import os


# print(get_pantry_status("milk"))

# print(list_low_stock_items())

# conn = sqlite3.connect(DB_PATH)
# conn.execute("UPDATE pantry SET quantity = 5 WHERE item = 'milk'")

# conn.commit()
# conn.close()

# print(list_low_stock_items())

import sqlite3
from pantry import record_order, get_pantry_status, DB_PATH

# print(record_order("potatoes", 1, 30))
# print(get_pantry_status("potatoes"))
# print(list_low_stock_items())
# print(sqlite3.connect(DB_PATH).execute("SELECT item, quantity FROM orders").fetchall())

# # print(sqlite3.connect(DB_PATH).execute("DELETE FROM orders WHERE id='4'"))
# print(sqlite3.connect(DB_PATH).execute("SELECT * FROM orders").fetchall())

conn = sqlite3.connect(DB_PATH)

# 1. look first: these are the rows that will be deleted
# print(conn.execute("SELECT * FROM orders WHERE item = 'potatoes'").fetchall())
# print(conn.execute("SELECT * FROM pantry WHERE item = 'potatoes'").fetchall())

# 2. delete them
# conn.execute("DELETE FROM orders WHERE item = 'potatoes'")
# conn.execute("DELETE FROM pantry WHERE item = 'potatoes'")
# conn.commit()
# conn.close()

# conn.execute("DELETE FROM orders WHERE item = 'milk'")
# conn.execute("UPDATE pantry SET quantity = 1 WHERE item = 'milk'")

# print(add_to_cart("milk", 2))
# print(add_to_cart("bread", 1))

# print(view_cart())

# conn.execute("DELETE FROM cart")
# print(conn.execute("SELECT * FROM cart").fetchall())


# print("before:", conn.execute("SELECT COUNT(*) FROM cart").fetchone())
# conn.execute("DELETE FROM cart")
# conn.commit()
# conn.close()

# # open a NEW connection to verify
# print("verified:", sqlite3.connect(DB_PATH).execute("SELECT COUNT(*) FROM cart").fetchone())

# import sqlite3
# from pantry import DB_PATH

# print(conn.execute("SELECT item, quantity FROM pantry WHERE item IN ('milk','bread')").fetchall())
# print(conn.execute("SELECT item, quantity, unit_price, ordered_at FROM orders").fetchall())
# print(conn.execute("SELECT * FROM cart").fetchall())     # look at the 5 stale rows
# print(conn.execute("SELECT * FROM orders").fetchall())   # look at the 4 order rows
# conn.execute("DELETE FROM cart")
# conn.commit()
# conn.close()
# print(sqlite3.connect(DB_PATH).execute("SELECT COUNT(*) FROM cart").fetchone())

# pyrefly: ignore [missing-import]
# from cart import add_to_cart, view_cart

# print(add_to_cart("milk", 1))
print(view_cart())

# print("PANTRY_DB env:", os.environ.get("PANTRY_DB"))
# print("DB_PATH used:", DB_PATH)

# print("before:", conn.execute("SELECT quantity FROM pantry WHERE item='milk'").fetchone())
# conn.close()

# print(place_order())

# conn = sqlite3.connect(DB_PATH)
# print("after:", conn.execute("SELECT quantity FROM pantry WHERE item='milk'").fetchone())
# print("orders:", conn.execute("SELECT item, quantity, unit_price FROM orders").fetchall())
# print("cart:", conn.execute("SELECT COUNT(*) FROM cart").fetchone())
# conn.close()
