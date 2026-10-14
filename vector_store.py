# pyrefly: ignore [missing-import]
from chromadb.utils.embedding_functions import text2vec_embedding_function
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="pantry_items")

collection.add(
    documents=[
        "whole wheat flour, good for baking rotis and bread",
        "extra virgin olive oil, good for salad dressings and light sauteing",
        "basmati rice, a staple grain for daily meals",
        "roasted arabica coffee beans for your morning brew"
    ],
    metadatas=[
        {"item": "flour"},
        {"item": "olive oil"},
        {"item": "rice"},
        {"item": "coffee beans"}
    ],
    ids=["flour", "olive oil", "rice", "coffee beans"]
)
print(collection.count())

results = collection.query(
    query_texts=["what should I use for baking?"],
    n_results=1
)
print(results)


    
