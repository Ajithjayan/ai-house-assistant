import sqlite3
from pantry import DB_PATH

conn = sqlite3.connect(DB_PATH)
print("DB:", DB_PATH)
print("cart rows:", conn.execute("SELECT COUNT(*) FROM cart").fetchone()[0])
print("orders rows:", conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
conn.close()