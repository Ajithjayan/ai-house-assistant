# pantry.py
# Mock database for current pantry inventory
from sematic_search import get_embedding , cosine_similarity
import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get("PANTRY_DB") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantry.db")
pantry_stock = {
    "eggs": {
        "quantity": 4,
        "unit": "count",
        "low_stock_threshold": 6
    },
    "milk": {
        "quantity": 1,
        "unit": "liter",
        "low_stock_threshold": 2
    },
    "bread": {
        "quantity": 1,
        "unit": "loaf",
        "low_stock_threshold": 1
    },
    "rice": {
        "quantity": 5,
        "unit": "kg",
        "low_stock_threshold": 2
    },
    "coffee beans": {
        "quantity": 150,
        "unit": "grams",
        "low_stock_threshold": 200
    },
    "olive oil": {
        "quantity": 500,
        "unit": "ml",
        "low_stock_threshold": 250
    },
    "butter": {
        "quantity": 1,
        "unit": "pack",
        "low_stock_threshold": 2
    },
    "garlic": {
        "quantity": 1,
        "unit": "bulb",
        "low_stock_threshold": 3
    },
    "sugar": {
        "quantity": 2,
        "unit": "kg",
        "low_stock_threshold": 1
    },
    "flour": {
        "quantity": 0,
        "unit": "kg",
        "low_stock_threshold": 1
    }
}

item_descriptions={
    "eggs": "fresh organic eggs, used for breakfast and baking",
    "milk": "full fat dairy milk, good for drinking and making tea/coffee",
    "bread": "fresh wheat bread, good for sandwiches",
    "rice": "premium basmati rice, best for Indian cuisine",
    "coffee beans": "freshly roasted arabica beans, rich aroma",
    "olive oil": "Premium extra virgin olive oil, good for salads and cooking",
    "butter": "unsalted dairy butter, good for baking and cooking",
    "garlic": "fresh garlic bulbs, essential for Indian cooking",
    "sugar": "granulated white sugar, used in beverages and cooking",
    "flour": "whole wheat flour, good for baking rotis and bread"
    
}
item_embeddings= {}
for item_name,description in item_descriptions.items():
    item_embeddings[item_name]=get_embedding(description)

def find_similar_pantry_item(query:str)->str:
    query_vec=get_embedding(query)
    best_item, best_score = None, -1
    for item_name, item_vec in item_embeddings.items():
        score=cosine_similarity(query_vec,item_vec)
        if score> best_score:
            best_score=score
            best_item=item_name

    if best_score < 0.35:
        return f"No confident match found for {query}"
    return best_item

def get_pantry_status(item_name:str)->str:
    conn=sqlite3.connect(DB_PATH)
    row=conn.execute(
        "SELECT quantity,unit,low_stock_threshold FROM pantry WHERE item=?",
        (item_name.lower(),)
    ).fetchone()
    conn.close()

    if row is None:
        return f"Sorry {item_name} is not in the pantry"
    
    quantity,unit,threshold=row
    if quantity<=threshold:
        return f"{item_name}: {quantity:g} {unit} left, below threshold of {threshold:g}"
    else:
        return f"{item_name}: {quantity:g} {unit}, sufficient"


def list_low_stock_items() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT item FROM pantry WHERE quantity <= low_stock_threshold"
    ).fetchall()
    conn.close()

    if not rows:
        return "Nothing to worry about, pantry is well stocked"
    return ", ".join(row[0] for row in rows)


    
        
    
