# pyrefly: ignore [missing-import]
from marketplace import find_similar_product
from pantry import find_similar_pantry_item


def run_pantry_retrieval_eval(verbose=True):
    test_cases = [
        {"query": "dairy", "expected": "milk"},
        {"query": "which milk is better for health", "expected": "milk"},
        {"query": "something to bake bread with", "expected": "flour"},  # known failure — Day 14, literal word overlap
        {"query": "what do I need to make rotis", "expected": "flour"},
        {"query": "greens", "expected": None},  # no real ground truth — Day 22's fix means this now correctly returns "No confident match"
        {"query": "something for my morning brew", "expected": "coffee beans"},
        {"query": "cooking oil", "expected": "olive oil"},
    ]

    passed, observed = 0, 0
    for tc in test_cases:
        query, expected = tc["query"], tc["expected"]
        actual = find_similar_pantry_item(query)

        if expected is None:
            result = "OBSERVE"
            observed += 1
        elif actual == expected:
            result = "PASS"
            passed += 1
        else:
            result = "FAIL"

        if verbose:
            print(f"[{result}] query: {query!r} -> expected: {expected!r}, actual: {actual!r}")

    scored = len(test_cases) - observed
    return passed, scored, observed


def run_product_retrieval_eval(verbose=True):
    test_cases = [
        {"query": "milk", "expected_any": ["Amul Taaza Toned Milk 500ml Pouch", "Nandini Good Life Toned Milk 1L Tetra Pack"]},
        {"query": "bread", "expected_any": ["Britannia Bread Whole Wheat 400g", "Modern White Sandwich Bread 350g"]},
        {"query": "rice", "expected_any": ["India Gate Basmati Rice 1kg", "Fortune Everyday Basmati Rice 5kg"]},
        {"query": "coffee", "expected_any": ["Nescafe Classic Instant Coffee 100g", "Bru Gold Roast Coffee 50g"]},
    ]

    passed = 0
    for tc in test_cases:
        query, expected_any = tc["query"], tc["expected_any"]
        actual = find_similar_product(query)
        result = "PASS" if actual in expected_any else "FAIL"
        if result == "PASS":
            passed += 1

        if verbose:
            print(f"[{result}] query: {query!r} -> expected: {expected_any!r}, actual: {actual!r}")

    return passed, len(test_cases)


if __name__ == "__main__":
    print("Pantry retrieval eval:")
    p_passed, p_scored, p_observed = run_pantry_retrieval_eval()
    print(f"-> {p_passed}/{p_scored} passed\n")

    print("Product retrieval eval:")
    pr_passed, pr_scored, pr_observed = run_product_retrieval_eval()
    print(f"-> {pr_passed}/{pr_scored} passed")