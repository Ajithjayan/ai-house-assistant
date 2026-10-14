from agent import run_agent, client
from marketplace import search_gulgo

SYSTEM_PROMPT = (
    "You are an Indian snarky home pantry assistant. If a user's requested item doesn't "
    "exactly match a known pantry item, use find_similar_pantry_item first to resolve it "
    "before checking stock or price. Also if user asks for a specific question about any "
    "product (eg- which milk is better for health) then use find_similar_product tool and "
    "Answer the user's question using ONLY the information in the given context. Do not add "
    "any facts, details, or claims that are not explicitly stated in the context, even if you "
    "know them to be generally true. If the context doesn't contain enough information to "
    "answer, say so explicitly. Any question mentioning a specific product or brand name — "
    "comparisons, attributes, nutrition, quality, (is it organic, which is better, how many "
    "calories) — must go through find_similar_product first, before the model is allowed to "
    "answer anything."
)


def judge_grounding(context: str, reply: str) -> str:
    judge_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict evaluator. Given a CONTEXT and a REPLY, determine if the REPLY only uses information present in the CONTEXT, or if it adds outside facts/claims not present in the CONTEXT. Respond with exactly one word: GROUNDED or UNGROUNDED."},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nREPLY:\n{reply}\n\nIs the REPLY grounded in the CONTEXT?"}
        ]
    )
    return judge_response.choices[0].message.content.strip()


def run_grounding_eval(verbose=True):
    test_cases = [
        {"query": "which milk is better for health, Amul or Nandini?"},
        {"query": "is the Amul milk organic?"},
        {"query": "how many calories are in the Britannia bread?"},
    ]

    passed = 0
    for tc in test_cases:
        query = tc["query"]
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        reply, tools_called, tool_results = run_agent(messages)
        context = " ".join(tool_results) if tool_results else "(no tool results — model answered directly)"

        verdict = judge_grounding(context, reply)
        if verdict == "GROUNDED":
            passed += 1

        if verbose:
            print(f"[{verdict}] query: {query!r}")
            print(f"  context used: {context}")
            print(f"  reply: {reply}")
            print("-" * 20)

    return passed, len(test_cases)


if __name__ == "__main__":
    passed, scored = run_grounding_eval()
    print(f"\nGrounding eval: {passed}/{scored} passed")


    for q in ["Amul milk", "Amul", "milk", "Amul Taaza", "Britannia bread", "bread", "English Oven bread"]:
        print(q, "->", [p["title"] for p in search_gulgo(q)])

    