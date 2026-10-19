# tool_use.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pantry import get_pantry_status , list_low_stock_items  , find_similar_pantry_item
from marketplace import find_similar_product, get_price , calculate_total
# pyrefly: ignore [missing-import]
from cart import add_to_cart, view_cart, request_checkout , place_order


load_dotenv()
client=OpenAI(api_key=os.getenv('OPENAI_API_KEY')
)
SYSTEM_PROMPT = (
    "You are an Indian snarky home pantry assistant. "
    "You have two separate sources of information. "
    "HOME means the user's own pantry: use find_similar_pantry_item and get_pantry_status for questions about what the user has, how much is left, or what is running low. "
    "STORE means the online store: use find_similar_product for questions about buying, shopping, store options, or store prices. "
    "If a question could mean either (for example 'what milk is available'), ask one short clarifying question: 'At home, or in the store?' before using any tool. "
    "For any question about a specific product or brand (comparisons, attributes, nutrition, quality), use find_similar_product first. "
    "Answer ONLY using information returned by tools. Do not add facts, details, or claims that the tools did not return, even if you know them to be generally true. "
    "If the tool results don't contain enough information to answer, say so explicitly. "
    "Words like buy, order, shop, price, or 'in the store' mean STORE, so use find_similar_product without asking. "
    "Words like 'we', 'our', 'at home', or 'left' mean HOME. "
    "Only ask 'At home, or in the store?' when the question has neither kind of signal (for example 'what milk is available'). "
    "You can never place an order yourself; after request_checkout, tell the user the system will show a summary and ask them to confirm."
)

tools = [
    {
        "type":"function",
        "function": {
            "name":"get_pantry_status",
            "description":"Check the current Stock level of a pantry item and whether it is running low",
            "parameters":{
                "type":"object",
                "properties":{
                    "item_name":{
                        "type":"string",
                        "description":"Name of the pantry item to check"
                    }
            },
            "required":["item_name"]
        }
    }
    },
    {
        "type":"function",
        "function":{
            "name": "list_low_stock_items",
            "description": "List all items that are running low in the pantry.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name": "get_price",
            "description": "Get the price of a the given item from the price list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the item to check price"
                    }
            },
            "required": ["item_name"]
        }
    }
    },
    {
        "type":"function",
        "function":{
            "name":"calculate_total",
            "description":"Get the total amount of an item based on the qunatity",
            "parameters":{
                "type":"object",
                "properties":{
                    "item_name":{
                        "type": "string",
                        "description":"Name of the item to calculate the total price"
                    },
                    "quantity":{
                        "type":"number",
                        "description": "Quantity of the item to calcualte the price"
                    }
                }   
            },
            "required":["item_name","quantity"]

        }
    },
    {
        "type":"function",
        "function":{
            "name":"find_similar_pantry_item",
            "description": "Look up items the user already has at HOME. Use for questions about current stock: what we have, how much is left, what's running low. Also resolves vague words to a pantry item (e.g. 'dairy' -> 'milk'). NOT for shopping, buying, store options or store prices; use find_similar_product for those.",            
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"The query to find similar items for"
                    }
                },
                "required":["query"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"find_similar_product",
            "description": "Search the online STORE (GulGo) for products the user can BUY. Use when the user wants to buy, order, shop, compare store options, or see store prices (e.g. 'what milk can I buy?', 'show me bread options', 'how much is X at the store?'). NOT for checking what the user already has at home; use find_similar_pantry_item for that.",            
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"The query to find similar items for"
                    }
                },
                "required":["query"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "view_cart",
        "description": "Show all items currently in the cart with quantities, prices, and the total order value. Use this when the user wants to review their cart or ask 'What's in my cart?'.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
    },
    {
    "type": "function",
    "function": {
        "name": "request_checkout",
        "description": "Call this when the user clearly wants to place the order. It does NOT place the order; it only tells the system to show a summary and ask the user to confirm. Never say an order has been placed.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
    },
    {
        "type":"function",
        "function":{
            "name":"add_to_cart",
            "description":"Add a product from the STORE to the cart when the user wants to buy something. Pass a SHORT generic item name like 'milk' or 'bread', never a full product title, plus a quantity. Does NOT place an order.",
            "parameters":{
                "type":"object",
                "properties":{
                    "item_name":{
                        "type":"string",
                        "description":"The generic item name to add to the cart"
                    },
                    "quantity":{
                        "type":"number",
                        "description":"The quantity of the item to add to the cart"
                    }
                },
                "required":["item_name","quantity"]
            }
        }
        

    }

]
def run_agent(messages):
    MAX_ITERATIONS = 5
    tool_called=[]
    tool_result=[]
    for iteration in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                tool_called.append(tool_call.function.name)
                if tool_call.function.name == "get_pantry_status":
                    args = json.loads(tool_call.function.arguments)
                    result = get_pantry_status(args['item_name'])
                elif tool_call.function.name == "list_low_stock_items":
                    result = list_low_stock_items()
                elif tool_call.function.name == "get_price":
                    args = json.loads(tool_call.function.arguments)
                    result = get_price(args['item_name'])
                elif tool_call.function.name=='calculate_total':
                    args = json.loads(tool_call.function.arguments)
                    result=calculate_total(args['item_name'],args['quantity'])
                elif tool_call.function.name == 'find_similar_pantry_item':
                    args = json.loads(tool_call.function.arguments)
                    result = find_similar_pantry_item(args['query'])
                elif tool_call.function.name == 'find_similar_product':
                    args = json.loads(tool_call.function.arguments)
                    result = find_similar_product(args['query'])
                elif tool_call.function.name == 'add_to_cart':
                    args = json.loads(tool_call.function.arguments)
                    result = add_to_cart(args['item_name'], args['quantity'])
                elif tool_call.function.name == 'view_cart':
                    result = view_cart()
                elif tool_call.function.name == 'request_checkout':
                    result = request_checkout()
                else:
                    result = f"Unknown tool: {tool_call.function.name}"
                tool_result.append(result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                print(f"Tool called: {tool_call.function.name}")
            # no return here — loop continues to next iteration automatically
        else:
            return response_message.content, tool_called,tool_result

    return "Agent stopped: reached maximum iterations without a final answer.",tool_called,tool_result

if __name__== "__main__":
    messages=[
    {"role":"system","content":SYSTEM_PROMPT}
]
    print("Pantry assistant (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower()=="quit":
            break

        messages.append({"role":"user","content":user_input})
        assistant_reply,tool_called,tool_result = run_agent(messages)
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"\nassistant_reply: {assistant_reply}")
        print(f"\nTools Called: {tool_called}")
        print(f"\nTools Result: {tool_result}")

        if "request_checkout" in tool_called:
            print("\n--- ORDER SUMMARY ---")
            print(view_cart())
            answer = input("Place this order? (type yes or y to confirm): ").strip().lower()
            if answer in ("yes","y"):
                print(place_order())
            else:
                print("Okay, nothing was ordered. Your cart is still saved.")

      


    
    
    