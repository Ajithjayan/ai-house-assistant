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
    # Expectations depend on the GulGo catalog. If the catalog changes, update these.
    test_cases = [
        {"query": "milk", "expect_keyword": "milk"},
        {"query": "bread", "expect_keyword": "bread"},
        {"query": "rice", "expect_keyword": None},      # GulGo does not stock rice
        {"query": "coffee", "expect_keyword": None},    # store search returns milk; matcher must reject it
        {"query": "potatoes", "expect_keyword": None},  # not stocked
    ]

    passed = 0
    for tc in test_cases:
        query, keyword = tc["query"], tc["expect_keyword"]
        actual = find_similar_product(query)

        if keyword is None:
            ok = "No confident match" in actual
        else:
            ok = keyword in actual.lower() and "available at" in actual

        result = "PASS" if ok else "FAIL"
        if ok:
            passed += 1

        if verbose:
            print(f"[{result}] query: {query!r} -> expect: {keyword or 'no match'}, actual: {actual!r}")

    return passed, len(test_cases)


if __name__ == "__main__":
    print("Pantry retrieval eval:")
    p_passed, p_scored, p_observed = run_pantry_retrieval_eval()
    print(f"-> {p_passed}/{p_scored} passed\n")

    print("Product retrieval eval:")
    pr_passed, pr_scored = run_product_retrieval_eval()
    print(f"-> {pr_passed}/{pr_scored} passed")