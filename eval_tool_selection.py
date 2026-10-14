from agent import run_agent
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

def run_tool_selection_eval(verbose=True):
    if verbose:
        print("Running Tool Selection Evaluation...")
    
    test_cases = [
        {"query": "do we have any dairy?", "expected_tools": ["find_similar_pantry_item", "get_pantry_status"]},
        {"query": "what's low in stock?", "expected_tools": ["list_low_stock_items"]},
        {"query": "how much would 2 litres of milk cost?", "expected_tools": ["calculate_total"]},
        {"query": "What should I buy for my morning coffee?", "expected_tools":None },
        {"query": "I want to make pasta for dinner.", "expected_tools": None},
        {"query": "How much would 3kg of potatoes cost?", "expected_tools": ["get_price"]},
    # add 2-3 more of your own, based on tools you've already built and tested
    ]
    passed =0
    observed= 0
    failed=0

    for test in test_cases:
        query=test['query']
        expected_tools=test['expected_tools']
        messages=[{'role':'user','content':query}]
        actual,tool_called,_=run_agent(messages)

        if expected_tools is None:
            result="OBSERVE"
            observed +=1
        elif all(tool in tool_called for tool in expected_tools):
            result= "PASS"
            passed +=1
        else:
            result ="FAIL"
            failed +=1

        if verbose:
            print(f"[{result}] query: {query!r} -> expected: {expected_tools!r}, actual: {tool_called!r}")

    scored = len(test_cases) - observed
    return passed, scored,observed

    
if __name__ == "__main__":
    passed, scored ,observed= run_tool_selection_eval(verbose=True)
    print(f"\nTest Summary:")
    print(f"{passed}/{scored} passed ({observed} observation-only case(s) excluded from scoring)")
