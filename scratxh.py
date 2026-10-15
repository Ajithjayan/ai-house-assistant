# from mcp_server import list_low_stock_items
# import sqlite3
# from pantry import get_pantry_status, DB_PATH
# # pyrefly: ignore [missing-import]
# from cart import add_to_cart, view_cart , place_order
# import os


# # print(get_pantry_status("milk"))

# # print(list_low_stock_items())

# # conn = sqlite3.connect(DB_PATH)
# # conn.execute("UPDATE pantry SET quantity = 5 WHERE item = 'milk'")

# # conn.commit()
# # conn.close()

# # print(list_low_stock_items())

# import sqlite3
# from pantry import record_order, get_pantry_status, DB_PATH

# # print(record_order("potatoes", 1, 30))
# # print(get_pantry_status("potatoes"))
# # print(list_low_stock_items())
# # print(sqlite3.connect(DB_PATH).execute("SELECT item, quantity FROM orders").fetchall())

# # # print(sqlite3.connect(DB_PATH).execute("DELETE FROM orders WHERE id='4'"))
# # print(sqlite3.connect(DB_PATH).execute("SELECT * FROM orders").fetchall())

# conn = sqlite3.connect(DB_PATH)

# # 1. look first: these are the rows that will be deleted
# # print(conn.execute("SELECT * FROM orders WHERE item = 'potatoes'").fetchall())
# # print(conn.execute("SELECT * FROM pantry WHERE item = 'potatoes'").fetchall())

# # 2. delete them
# # conn.execute("DELETE FROM orders WHERE item = 'potatoes'")
# # conn.execute("DELETE FROM pantry WHERE item = 'potatoes'")
# # conn.commit()
# # conn.close()

# # conn.execute("DELETE FROM orders WHERE item = 'milk'")
# # conn.execute("UPDATE pantry SET quantity = 1 WHERE item = 'milk'")

# # print(add_to_cart("milk", 2))
# # print(add_to_cart("bread", 1))

# # print(view_cart())

# # conn.execute("DELETE FROM cart")
# # print(conn.execute("SELECT * FROM cart").fetchall())


# # print("before:", conn.execute("SELECT COUNT(*) FROM cart").fetchone())
# # conn.execute("DELETE FROM cart")
# # conn.commit()
# # conn.close()

# # # open a NEW connection to verify
# # print("verified:", sqlite3.connect(DB_PATH).execute("SELECT COUNT(*) FROM cart").fetchone())

# # import sqlite3
# # from pantry import DB_PATH

# # print(conn.execute("SELECT item, quantity FROM pantry WHERE item IN ('milk','bread')").fetchall())
# # print(conn.execute("SELECT item, quantity, unit_price, ordered_at FROM orders").fetchall())
# # print(conn.execute("SELECT * FROM cart").fetchall())     # look at the 5 stale rows
# # print(conn.execute("SELECT * FROM orders").fetchall())   # look at the 4 order rows
# # conn.execute("DELETE FROM cart")
# # conn.commit()
# # conn.close()
# # print(sqlite3.connect(DB_PATH).execute("SELECT COUNT(*) FROM cart").fetchone())

# # pyrefly: ignore [missing-import]
# # from cart import add_to_cart, view_cart

# # print(add_to_cart("milk", 1))
# # print(view_cart())

# # print("PANTRY_DB env:", os.environ.get("PANTRY_DB"))
# # print("DB_PATH used:", DB_PATH)

# # print("before:", conn.execute("SELECT quantity FROM pantry WHERE item='milk'").fetchone())
# # conn.close()

# # print(place_order())

# # conn = sqlite3.connect(DB_PATH)
# # print("after:", conn.execute("SELECT quantity FROM pantry WHERE item='milk'").fetchone())
# # print("orders:", conn.execute("SELECT item, quantity, unit_price FROM orders").fetchall())
# # print("cart:", conn.execute("SELECT COUNT(*) FROM cart").fetchone())
# # conn.close()
# def add_one(x):
#     return x + 1

# print(add_one.__name__)

import time
# def greet(name, greeting="Hello"):
#     return f"{greeting}, {name}"



# def log_call(func, *args, **kwargs):
#     print(f"Calling {func.__name__}")
#     result = func(*args, **kwargs)
#     return result

# print(log_call(greet, "Ajith", greeting="Hi") )


# def make_logger(func):
#     def wrapper(*args,**kwargs):
#         print(f"Calling {func.__name__}")
#         result = func(*args, **kwargs)
#         return result
#     return wrapper
    
# logged_greet = make_logger(greet)
# print(logged_greet("Ajith", greeting="Hi")) 

# def make_timer(func):
#     def wrapper(*args,**kwargs):
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         end = time.perf_counter()-start
#         print(f"{func.__name__} took {end:.2f}s")
#         return result
#     return wrapper

# @make_timer
# def greet(name, greeting="Hello"):
#     time.sleep(2)
#     return f"{greeting}, {name}"

# print(greet("Ajith", greeting="Hi"))

class Counter2:
    def __init__(self,count:int=0):
        self.count=count
    
    def increment(self, by:int=1):
        self.count+=by
    
    def reset(self):
        self.count=0

    def __repr__(self):
        return f"Counter2(Count ={self.count})"

class TokenBudget:
    def __init__(self,limit):
        self.limit=limit
        self.used=0
    def use(self,tokens):
        if self.used+tokens>self.limit:
            return False
        self.used+=tokens
        return True
    
    def remaining(self):
        return self.limit-self.used
        

    def __repr__(self):
        return f"TokenBudget(Limit ={self.limit}, Used ={self.used})"

token = TokenBudget(100)
print(token.use(10))
print(token.use(30))
print(token.remaining())
print(token.use(30))
print(token.remaining())
print(token)