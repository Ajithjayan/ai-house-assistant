
 
from itertools import product
from sematic_search import cosine_similarity, get_embedding
from playwright.sync_api import sync_playwright


def parse_price(price_text:str)->float:
    return float(price_text.replace("₹", "").replace(",", "").strip())

def search_gulgo(queries:list[str])-> list[dict]:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page= browser.new_page()
        page.goto("https://gul-go-quick-commerce-mock.vercel.app/")
        for q in queries:
            page.fill("#searchInput", q)
            page.wait_for_timeout(1500)
            rows=page.query_selector_all(".search-item-row")
            if rows:
                results = []
                for row in rows:
                    title=row.query_selector(".search-item-title").inner_text()
                    unit=row.query_selector(".search-item-unit").inner_text()
                    price=row.query_selector(".search-item-price").inner_text()
                    results.append({"title":title,"unit":unit,"price":parse_price(price)})
                browser.close()
                return results
        browser.close()
        return []

def find_best_product(query:str):
    """Return the best-matching product dict, or None if there's no confident match."""
    words = [w for w in query.split() if len(w) > 2][:3]   # at most 3 fallback words
    queries = [query] + [w for w in words if w != query]
    candidates = search_gulgo(queries)

    if not candidates:
        return None
    
    query_vec = get_embedding(query)
    best, best_score = None, -1
    for c in candidates:
        text = f"{c['title']} {c['unit']}"
        score = cosine_similarity(query_vec, get_embedding(text))
        if score > best_score:
            best, best_score = c, score

    if best_score < 0.35:
        return None
    return best


def find_similar_product(query: str)->str:
    product = find_best_product(query)
    if product is None:
        return f"No confident match found for {query}"
    return f"{product['title']} {product['unit']} available at ₹{product['price']:g}"

def get_price(item_name:str)->str:
    product=find_best_product(item_name)
    if product is None:
        return f"No confident match found for {item_name}"
    return f"{product['title']} ({product['unit']}) costs ₹{product['price']:g} at the store."

def calculate_total(item_name:str, quantity:float)->str:
    product=find_best_product(item_name)
    if product is None:
        return f"No confident match found for {item_name}"
    total=product['price'] * quantity
    return f"{quantity:g} x {product['title']} ({product['unit']}) at ₹{product['price']:g} each = ₹{total:g}"


if __name__ == "__main__":
    print("*"*100)
    print(find_best_product("amul milk"))
    print("*"*100)
    print(find_best_product("potatoes"))
    print("*"*100)
    print(find_best_product("Amul Taaza Homogenised Toned Milk 1 Litre Pouch ₹54"))
    print("*"*100)
    print(calculate_total("milk", 3))
