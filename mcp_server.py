# pyrefly: ignore [missing-import]
import json
# pyrefly: ignore [missing-import]
from mcp.server.mcpserver import MCPServer
from pantry import get_pantry_status as _get_pantry_status, list_low_stock_items as _list_low_stock_items, find_similar_pantry_item as _find_similar_pantry_item 
from marketplace import find_similar_product as _find_similar_product , get_price as _get_price , calculate_total as _calculate_total
import sqlite3
from pantry import DB_PATH
mcp = MCPServer("house-assistant")

@mcp.tool()
def get_pantry_status(item_name: str) -> str:
    """Check the current stock level of a pantry item and whether it is running low."""
    return _get_pantry_status(item_name)
        
        
@mcp.tool()
def list_low_stock_items() -> str:
    """Get a list of items that are running low in the pantry."""
    return _list_low_stock_items()

@mcp.tool()
def get_price(item_name: str) -> str:
    """Get the price of a pantry item."""
    return _get_price(item_name)

@mcp.tool()
def calculate_total(item_name: str, quantity: float) -> str:
    """Calculate the total amount for a given quantity of a pantry item."""
    return _calculate_total(item_name, quantity)

@mcp.tool()
def find_similar_pantry_item(query: str) -> str:
    """Find the most similar item in the pantry based on the query."""
    return _find_similar_pantry_item(query)

@mcp.tool()
def find_similar_product(query: str) -> str:
    """Find the most similar product based on the query."""
    return _find_similar_product(query)


@mcp.resource("pantry://inventory")
def get_full_inventory() -> str:
    """The complete current pantry inventory, including all items, quantities, and thresholds."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT item, quantity, unit, low_stock_threshold FROM pantry"
    ).fetchall()
    conn.close()
    inventory = {
        item: {"quantity": qty, "unit": unit, "low_stock_threshold": threshold}
        for item, qty, unit, threshold in rows
    }
    return json.dumps(inventory)

@mcp.prompt()
def restock_check() -> str:
    """Generate a prompt asking what's low in stock and how much it would cost to restock."""
    return "What's currently low in stock, and how much would it cost to restock all of it?"
    
if __name__ == "__main__":
    mcp.run()