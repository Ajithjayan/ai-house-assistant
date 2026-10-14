import sqlite3
from marketplace import find_best_product
from pantry import DB_PATH

def add_to_cart(item_name: str, quantity: float) -> str:
    product = find_best_product(item_name)
    if product is None:
        return f"Sorry, I couldn't find {item_name} in the store."
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO cart (item, product_title, unit, unit_price, quantity) VALUES (?, ?, ?, ?, ?)",
            (item_name.lower(), product["title"], product["unit"], product["price"], quantity)
        )
        conn.commit()
    finally:
        conn.close()
    return f"Added {quantity:g} x {product['title']} ({product['unit']}) at ₹{product['price']:g} each to the cart."

def view_cart() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT product_title, unit, unit_price, quantity FROM cart").fetchall()
    conn.close()
    if not rows:
        return "The cart is empty."
    lines, total = [], 0
    for title, unit, price, qty in rows:
        lines.append(f"{qty:g} x {title} ({unit}) at ₹{price:g} = ₹{price * qty:g}")
        total += price * qty
    return "\n".join(lines) + f"\nTotal: ₹{total:g}"

def request_checkout() -> str:
    return "Checkout requested. The system will now show the user an order summary and ask for confirmation."


from datetime import datetime

def place_order() -> str:
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT item, unit_price, quantity FROM cart"
        ).fetchall()
        if not rows:
            return "The cart is empty, nothing to order."

        now = datetime.now().isoformat(timespec="seconds")
        total = 0
        for item, price, qty in rows:
            cur = conn.execute(
                "UPDATE pantry SET quantity = quantity + ? WHERE item = ?", (qty, item)
            )
            if cur.rowcount == 0:
                conn.execute(
                    "INSERT INTO pantry (item, quantity, unit, low_stock_threshold) VALUES (?, ?, ?, ?)",
                    (item, qty, "pcs", 1)
                )
            conn.execute(
                "INSERT INTO orders (item, quantity, unit_price, ordered_at) VALUES (?, ?, ?, ?)",
                (item, qty, price, now)
            )
            total += price * qty

        conn.execute("DELETE FROM cart")
        conn.commit()
        return f"Order placed: {len(rows)} item(s), total ₹{total:g}."
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()