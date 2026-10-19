from agent import run_agent, client, SYSTEM_PROMPT
from marketplace import search_gulgo




def judge_grounding(context: str, reply: str) -> str:
    judge_response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": ("You are a strict evaluator. Given a CONTEXT and a REPLY, decide if every claim in the REPLY is stated in the CONTEXT. Opinions, quality judgments, health claims and recommendations count as claims: if the CONTEXT does not state them, the REPLY is UNGROUNDED. Friendly tone and rephrasing the CONTEXT are fine.Repeating names or words from the user’s question is not an outside claim. Saying you could not find information is always GROUNDED.Claims about what was found or searched also need support: if the REPLY says something was found, and the CONTEXT does not show it, the REPLY is UNGROUNDED.Respond with exactly one word: GROUNDED or UNGROUNDED."
            "A sentence is NOT a claim, and must be ignored, if it is: (a) an offer or question to the user, (b) a statement that something was not found or is not in the context, or (c) a suggestion to check elsewhere, such as a website or a label. Mentioning a product that appears in the context is also fine. Every other sentence must be checked against the context, especially any statement that something was found, available, or priced.")},
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


    