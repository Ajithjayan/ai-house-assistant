from collections import Counter
from eval_grounding import judge_grounding

CONTEXT = "Amul Taaza Homogenised Toned Milk 1 Litre Pouch available at ₹54"
replies = {
    "clearly grounded": "Amul Taaza toned milk, 1 litre pouch, is available at ₹54.",
    "clearly ungrounded": "Amul Taaza is 1 litre for ₹54 and it is rich in calcium and good for bones.",
    "borderline opinion": "Amul Taaza toned milk, 1 litre at ₹54, is a decent everyday choice.",
    "honest refusal": "I couldn't find health information about this milk in the context, so I can't say whether it is better for health.",
    "refusal naming outside brand": "I couldn't find Nandini milk in the context, so I can't compare it with Amul Taaza.",
    "false claim of finding": "I cannot determine which milk is better for health between Amul and Nandini. Both types of milk were found in the search but without specific health comparisons.",
}

counts = Counter()
for label, reply in replies.items():
    verdict = Counter(judge_grounding(CONTEXT, reply) for _ in range(10))
    print(label, dict(verdict))
