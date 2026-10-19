from collections import Counter
from eval_grounding import judge_grounding

AMUL = "Amul Taaza Homogenised Toned Milk 1 Litre Pouch available at ₹54"
BREAD = "English Oven 100% Whole Wheat Bread 400 g Loaf available at ₹45"
replies = {
    "clearly grounded": (AMUL,"Amul Taaza toned milk, 1 litre pouch, is available at ₹54."),
    "clearly ungrounded": (AMUL, "Amul Taaza is 1 litre for ₹54 and it is rich in calcium and good for bones."),
    "borderline opinion": (AMUL, "Amul Taaza toned milk, 1 litre at ₹54, is a decent everyday choice."),
    "honest refusal": (AMUL,"I couldn't find health information about this milk in the context, so I can't say whether it is better for health."),
    "refusal naming outside brand": (AMUL,"I couldn't find Nandini milk in the context, so I can't compare it with Amul Taaza."),
    "false claim of finding": (AMUL,"I cannot determine which milk is better for health between Amul and Nandini. Both types of milk were found in the search but without specific health comparisons."),
    "honest refusla + offer": (AMUL,"I found Amul Taaza Homogenised Toned Milk available at ₹54, but there's no information to confirm if it's organic. Would you like to know more about other milk options?"),
    "refusal + only product" : (BREAD,"I couldn't find specific calorie information for Britannia bread. The only related product available is the English Oven 100% Whole Wheat Bread, which is a 400 g loaf priced at ₹45"),
    "refusal + advice":(AMUL,"I found Amul Taaza Homogenised Toned Milk available at ₹54, but it seems there's no specific information for Nandini milk in the results. I can't provide a direct comparison. You might want to check nutritional labels or health benefits locally for a more informed decision!")
}

counts = Counter()
for label,(context,reply) in replies.items():
    verdict = Counter(judge_grounding(context, reply) for _ in range(10))
    print(label, dict(verdict))
