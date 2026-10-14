# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

def search_gulgo(query: str) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto("https://gul-go-quick-commerce-mock.vercel.app/")
        page.fill("#searchInput", query)
        page.wait_for_timeout(1500)

        rows = page.query_selector_all(".search-item-row")
        results = []
        for row in rows:
            title = row.query_selector(".search-item-title").inner_text()
            unit = row.query_selector(".search-item-unit").inner_text()
            price = row.query_selector(".search-item-price").inner_text()
            results.append({"title": title, "unit": unit, "price": parse_price(price)})
        browser.close()
        return results

def parse_price(price_text: str) -> float:
    return float(price_text.replace("₹", "").replace(",", "").strip())
if __name__ == "__main__":
    print(search_gulgo("bread"))
    print("*"*100)
    print(search_gulgo("Amul Taaza Homogenised Toned Milk 1 Litre Pouch"))
    print("*"*100)
    print(search_gulgo("Amul Taaza Homogenised Toned Milk"))
    print("*"*100)
    print(search_gulgo("Amul Taaza"))
    print("*"*100)
    print(search_gulgo("milk"))
    print("*"*100)

   