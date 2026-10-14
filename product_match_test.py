import os 
from dotenv import load_dotenv
from openai import OpenAI
from sematic_search import get_embedding , cosine_similarity

load_dotenv()
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



if __name__ == "__main__":

    scraped_products = [
        "Amul Taaza Toned Milk 500ml Pouch",
        "Nandini Good Life Toned Milk 1L Tetra Pack",
        "Britannia Bread Whole Wheat 400g",
        "Modern White Sandwich Bread 350g",
        "India Gate Basmati Rice 1kg",
        "Fortune Everyday Basmati Rice 5kg",
        "Nescafe Classic Instant Coffee 100g",
        "Bru Gold Roast Coffee 50g"
    ]

    item_embeddings={}
    for item in scraped_products:
        item_embeddings[item]= get_embedding(item)
    
    query="Which milk is better?"
    query_vec=get_embedding(query)
    best_item, best_score= None,-1

    for item,item_vec in item_embeddings.items():
        score= cosine_similarity(query_vec,item_vec)
        print(f'{item}: {score}')
        if score > best_score:
            best_score=score
            best_item=item

    #print(f"\nBest match: {best_item} (score: {best_score})")   

    final_response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Answer the user's question using ONLY the information in the given context. Do not add any facts, details, or claims that are not explicitly stated in the context, even if you know them to be generally true. If the context doesn't contain enough information to answer, say so explicitly."},
        {"role": "user", "content": f"Context: {best_item}\n\nQuestion: {query}"}
    ]
    )
    print(final_response.choices[0].message.content)
    

