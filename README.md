# AI House Assistant

A chat assistant for people who find quick-commerce apps confusing: elderly users, or anyone who freezes when faced with 40 brands of milk. You talk to it in plain language. It tracks what's in your pantry, searches a store, builds a cart, and **only places an order after you confirm**.

> **Scope note (honest version):** This project runs against **GulGo**, a mock grocery website I built myself. No real orders or payments are made, and it does not simulate real-world anti-bot defenses. The goal is to prove the architecture end to end; connecting a real store (for example via ONDC) is future work.

## Example conversation

```
You: I need 2 milk and 1 bread
Assistant: Added 2 x milk and 1 x bread to your cart. Want to check out?
You: yes, check out
--- ORDER SUMMARY ---
(cart contents and total, built by plain Python from the database: ₹153)
Place this order? (type yes or y to confirm): y
Order placed: 2 item(s), total ₹153.
```

If you answer anything other than yes/y, nothing is ordered and the cart stays saved.

## How it routes requests

- **HOME questions** ("do I have milk?", "what's running low?") go to the pantry tools, which read SQLite.
- **STORE questions** ("find me bread", "what does it cost?") go to the store tools, which search GulGo live.
- **Checkout** is a signal, not an action: the model calls `request_checkout`, and ordinary Python takes over.

## Architecture

```
User ──► Agent loop (OpenAI gpt-4o-mini, tool calling, MAX_ITERATIONS cap)
            │
            ├─ HOME tools ──► SQLite (pantry, orders, cart)
            │                  └─ embedding match for fuzzy names ("dairy" → milk)
            │
            ├─ STORE tools ─► Playwright ──► GulGo mock store
            │                  └─ retrieve candidates, then rerank with embeddings
            │
            └─ request_checkout (signal only)
                         │
                         ▼
            Plain Python: print summary from DB ─► user types yes/y
                         │
                         ▼
            place_order(): ONE transaction
              pantry update + order insert + cart clear (rollback on error)
```

## Design decisions

- **The model cannot place orders.** `place_order` is not in the model's tool list. The model proposes; deterministic code decides and acts.
- **Prices and totals come from code, not the model.** The order summary is built from the database, so the model can't invent a number.
- **Retrieve, then rerank.** Search the store with the full query, fall back to individual words, then pick the best match using embedding similarity with a 0.35 threshold. Below the threshold the answer is "not found" rather than a guess.
- **One transaction for ordering.** Either the whole order succeeds or nothing changes.
- **Tool descriptions are prompts.** Each says what it is for and what it is NOT for, which fixed overlapping-tool confusion.
- **Test isolation.** Set `PANTRY_DB` to point at a separate database so tests never touch real data.

## Tech stack

Python · OpenAI (`gpt-4o-mini`, `text-embedding-3-small`) · Playwright · SQLite · MCP

## Setup

Requirements: Python 3.10+, Google Chrome installed, an OpenAI API key.

```bash
pip install -r requirements.txt
```

Create a `.env` file (never commit it):

```
OPENAI_API_KEY=your-key-here
```

Then:

```bash
python db.py       # creates and seeds pantry.db
python agent.py    # starts the chat
```

First launch computes about 10 embeddings, so it takes a moment. To use a throwaway database for testing: set `PANTRY_DB=path/to/test.db` before running `db.py` and `agent.py`.

## Evals

| Eval | Status |
|---|---|
| Tool selection | Passing |
| Pantry retrieval | Passing, with one documented known failure ("bake bread" matches "bread") |
| Product retrieval | Being rewritten for the GulGo store |
| Grounding (LLM-as-judge) | Being rewritten; judge results vary between runs |

Run everything with `python run_all_evals.py`.

## Project structure

```
agent.py          agent loop, tool schemas, system prompt, checkout hook
pantry.py         pantry queries and fuzzy item matching (SQLite)
marketplace.py    GulGo search, product matching, live prices
cart.py           add_to_cart, view_cart, request_checkout, place_order
db.py             table creation and seed data
sematic_search.py embeddings and cosine similarity
mcp_server.py     MCP server exposing tools, a resource and a prompt
eval_*.py         eval suites;  run_all_evals.py runs them all
```

## Status

**Working:** pantry tracking, fuzzy item matching, live store search, cart, confirmation-gated checkout, transactional ordering that updates pantry and order history.

**Not built yet:**
- Reorder reminders
- Telegram / WhatsApp interface
- Merging repeat adds of the same item in the cart
- Mapping store product names to pantry names
- MCP server and evals updated for SQLite and the live store
- Real store integration (ONDC)

## What I learned building this

- Letting the model skip retrieval invites hallucination; route product questions through the tool.
- Two tools with overlapping descriptions confuse the model. Spell out each tool's territory.
- A tool the model can call but the code never handles fails silently.
- `sqlite3.connect()` quietly creates an empty database if the path is wrong, so anchor the path to the file.
- Similarity scores near the threshold are unstable; evals need to account for that.