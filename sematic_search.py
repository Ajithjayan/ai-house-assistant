import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


item_descriptions = {
    "flour": "whole wheat flour, good for baking rotis and bread",
    "olive oil": "extra virgin olive oil, good for salad dressings and light sauteing",
    "rice": "basmati rice, a staple grain for daily meals",
    "coffee beans": "roasted arabica coffee beans for your morning brew"
}

if __name__ == "__main__":
    item_embeddings={}
    for item_name, description in item_descriptions.items():
        item_embeddings[item_name] = get_embedding(description)

    print(item_embeddings.keys())

    question = "What should i use for Baking"
    ques_vec= get_embedding(question)

    best_item= None
    best_score=-1

    for item_name, item_vec in item_embeddings.items():
        score = cosine_similarity(ques_vec, item_vec)
        print(f'{item_name}: {score}')
        if score > best_score:
            best_score = score
            best_item = item_name

    print(f"\nBest match: {best_item} (score: {best_score})")

    print("greens vs eggs: ",cosine_similarity(get_embedding("greens"), get_embedding("fresh organic eggs, used for breakfast and baking")))
    print("greens vs garlic: ",cosine_similarity(get_embedding("greens"), get_embedding("fresh garlic bulbs, essential for Indian cooking")))

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer the user's question using the provided context."},
            {"role": "user", "content": f"Context: {item_descriptions[best_item]}\n\nQuestion: {question}"}
        ]
    )
    print(final_response.choices[0].message.content)
