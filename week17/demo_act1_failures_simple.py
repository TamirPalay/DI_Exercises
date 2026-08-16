"""
demo_act1_failures_simple.py — Day 1, Act 1: Three things your LLM can't do.

Same idea as demo_act1_failures.py, but written out as THREE separate blocks
(no loop) and using plain print() — nothing to install beyond ollama. To try
just one, comment out the other two blocks.

Run this BEFORE building the MCP server. Let each answer land; let the silence
speak.

    python demo_act1_failures_simple.py
"""

import ollama

MODEL = "mistral:7b"          # or "phi4-mini"


def ask(question):
    """Send one question to the local model and print its answer."""
    print("\nQuestion:", question)
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Answer in 2-3 sentences. Be direct and concise."},
            {"role": "user", "content": question},
        ],
        options={"num_predict": 75},
    )
    print("LLM:", response.message.content.strip())


# ── Failure 1 — the filesystem ───────────────────────────────────────────────
# The model can't read files on your computer.
print("=" * 60)
print("Failure 1 — Filesystem")
ask("What is written in the file notes.txt in my current directory?")
print("(The LLM has no access to your files — it can't read notes.txt.)")


# ── Failure 2 — live web data ────────────────────────────────────────────────
# The model can't see anything happening right now.
print("=" * 60)
print("Failure 2 — Live web data")
ask("What is the weather in Tel Aviv right now? Give me the exact temperature.")
print("(The LLM hedges, gives a stale answer, or confidently makes one up.)")


# ── Failure 3 — your database ────────────────────────────────────────────────
# The model can't reach your data.
print("=" * 60)
print("Failure 3 — Database")
ask("Show me all products in our workshop database. List names, categories, and prices.")
print("(The LLM refuses — or invents an entire database.)")


# ── The point ────────────────────────────────────────────────────────────────
print("=" * 60)
print("Three real problems. Same pattern every time.")
print("The LLM has no bridge to the outside world.")
print("MCP is that bridge. Let's build it.")
