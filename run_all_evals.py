# pyrefly: ignore [missing-import]
from eval_grounding import run_grounding_eval
from eval_retrieval import run_pantry_retrieval_eval, run_product_retrieval_eval
# pyrefly: ignore [missing-import]
from eval_tool_selection import run_tool_selection_eval

print("=" * 40)
print("AI House Assistant — Full Eval Suite")
print("=" * 40)

tool_selection = run_tool_selection_eval(verbose=False)
grounding = run_grounding_eval(verbose=False)
pantry_retrieval = run_pantry_retrieval_eval(verbose=False)
product_retrieval = run_product_retrieval_eval(verbose=False)

print(f"Tool Selection    : {tool_selection[0]}/{tool_selection[1]} passed ({tool_selection[2]} observation-only excluded)")
print(f"Grounding         : {grounding[0]}/{grounding[1]} passed")
print(f"Pantry Retrieval  : {pantry_retrieval[0]}/{pantry_retrieval[1]} passed ({pantry_retrieval[2]} observation-only excluded)")
print(f"Product Retrieval : {product_retrieval[0]}/{product_retrieval[1]} passed")

total_passed = tool_selection[0] + grounding[0] + pantry_retrieval[0] + product_retrieval[0]
total_scored = tool_selection[1] + grounding[1] + pantry_retrieval[1] + product_retrieval[1]

print("-" * 40)
print(f"TOTAL: {total_passed}/{total_scored} passed across all eval suites")
print("=" * 40)