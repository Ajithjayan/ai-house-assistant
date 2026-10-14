# import time
# import requests

# headers = {
#     "User-Agent": "HouseAssistant-LearningProject/1.0 (ajith-learning-ai-engineering)"
# }

# response = requests.get(
#     "https://world.openfoodfacts.org/cgi/search.pl",
#     params={
#         "search_terms": "milk",
#         "search_simple": 1,
#         "action": "process",
#         "json": 1
#     },
#     headers=headers
# )

# # print(response.status_code)
# # data = response.json()
# # print(data.keys())
# # products = data['products']
# # print(f"Number of products found: {len(products)}")
# # print(products[0])

# def extract_product_info(product):
#     name = product.get('product_name', 'Unknown') or 'Unknown'
#     brand = product.get('brands', 'Unknown brand') or 'Unknown brand'
#     quantity = product.get('quantity', '') or ''
#     return f"{brand} {name} {quantity}".strip()

# # for product in products:
# #     print(extract_product_info(product))

# category=["milk","eggs","bread","oil","rice","coffee","sugar","salt","butter","cheese"]

# for item in category:
#     response= requests.get(
#     "https://world.openfoodfacts.org/cgi/search.pl",
#     params={
#         "search_terms": item,
#         "search_simple": 1,
#         "action": "process",
#         "json": 1,
#         "page_size":5
#     },
#     headers=headers
#     )
#     time.sleep(1)
#     print(response.status_code)
#     print(response.text)

#     data1 = response.json()
#     print(data1.keys())
#     products1 = data1['products']
#     print(len(products1))
#     for product in products1:
#         print(extract_product_info(product))

# import time
# import requests

# headers = {
#     "User-Agent": "HouseAssistant-LearningProject/1.0 (ajith-learning-ai-engineering)"
# }

# def extract_product_info(product):
#     name = product.get('product_name', 'Unknown') or 'Unknown'
#     brand = product.get('brands', 'Unknown brand') or 'Unknown brand'
#     quantity = product.get('quantity', '') or ''
#     return f"{brand} {name} {quantity}".strip()

# def fetch_candidates(categories):
#     all_candidates = []
#     for item in categories:
#         response=fetch_with_retry(item, max_retries=3)
#         if response is None:
#             continue
#         data = response
#         for product in data['products']:
#             all_candidates.append(extract_product_info(product))

#         time.sleep(1)
#     return all_candidates

# def fetch_with_retry(item, max_retries=3):
#     for attempt in range(max_retries):
#         response = requests.get(
#             "https://world.openfoodfacts.org/cgi/search.pl",
#             params={"search_terms": item, "search_simple": 1, "action": "process", "json": 1, "page_size": 5},
#             headers=headers
#         )
#         if response.status_code == 200:
#             return response.json()

#         wait_time = 2 ** attempt  # 1, 2, 4 seconds — doubles each retry
#         print(f"'{item}' failed (status {response.status_code}), retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
#         time.sleep(wait_time)

#     print(f"Giving up on '{item}' after {max_retries} attempts")
#     return None


# categories = ["milk", "eggs", "bread", "oil", "rice", "coffee", "sugar", "salt", "butter", "cheese"]
# candidates = fetch_candidates(categories)
# print(f"Total candidates fetched: {len(candidates)}")
# for c in candidates:
#     print(c)

import requests
response = requests.get("https://gul-go-quick-commerce-mock.vercel.app/")
print(response.text)