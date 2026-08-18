"""
agent_FINISHED.py — the FINISHED version of the hand-built agent.

This is the "answer key" for README.md. If your own file gets stuck,
compare it to this, or just run this one — it works as-is.

It is the same skeleton as agent_UNFINISHED.py, but with the agent loop
already filled in (Step 6/7 of the beginner guide).

HOW TO RUN
    1) Install once:   pip install "mcp[cli]<2" openai requests python-dotenv ddgs
    2) Get the model:  ollama pull qwen2.5:7b
    3) Window 1:       python ../../Day1-Build-a-Server/day1_server_full.py   (leave running)
    4) Window 2:       python agent_FINISHED.py
    5) Type a question, e.g.:  What is the weather in Tel Aviv, and what does notes.txt say?
    6) Type 'quit' to stop.
"""

import asyncio
import json
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI

# ── settings ─────────────────────────────────────────────────────────────────
LOCAL_URL = "http://127.0.0.1:8000/mcp/"   # your Day 1 server (use 127.0.0.1, not localhost)
MODEL     = "qwen3:0.6b"                     # a model good at calling tools
llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")  # points at local Ollama


# ── helpers (you don't need to change these) ─────────────────────────────────
def to_openai_tool(t):
    """Turn one MCP tool into the shape the model expects."""
    return {"type": "function", "function": {
        "name": t.name, "description": t.description or "", "parameters": t.inputSchema}}


def result_text(result):
    """Pull readable text out of a tool result."""
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts)
    return text or "(no text)"


async def main():
    async with AsyncExitStack() as stack:
        # 1) CONNECT to the Day 1 server.
        r, w, _ = await stack.enter_async_context(streamablehttp_client(LOCAL_URL))
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        # 2) DISCOVER — ask the server what tools it has, and convert them.
        tools = (await session.list_tools()).tools
        openai_tools = [to_openai_tool(t) for t in tools]
        print("Connected. Tools available:", [t.name for t in tools], "\n")

        # The whole conversation lives in this list — that IS the agent's memory.
        messages = [{
            "role": "system",
            "content": "You are a helpful assistant. When a tool result is given, use it and answer directly.",
        }]

        print("Chat ready! (type 'quit' to exit)\n")
        while True:
            try:
                user = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()          # Ctrl+C / Ctrl+D -> quit quietly, no scary traceback
                break
            if user.lower() in ("quit", "exit"):
                break
            messages.append({"role": "user", "content": user})

            # 3) THE AGENT LOOP — capped at 5 so it can never run forever.
            for _ in range(5):
                # Ask the model, and tell it which tools exist.
                resp = llm.chat.completions.create(
                    model=MODEL, messages=messages,
                    tools=openai_tools, tool_choice="auto")
                msg = resp.choices[0].message

                # No tool calls => the model is DONE. Print the answer and stop.
                if not msg.tool_calls:
                    messages.append({"role": "assistant", "content": msg.content})
                    print("\nAgent:", msg.content, "\n")
                    break

                # Otherwise the model NAMED some tools. Save that turn...
                messages.append({
                    "role": "assistant", "content": msg.content,
                    "tool_calls": [
                        {"id": tc.id, "type": "function",
                         "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                        for tc in msg.tool_calls],
                })
                # ...then WE run each tool and feed the real result back.
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    print(f"  [tool] {tc.function.name}({args})")
                    result = await session.call_tool(tc.function.name, arguments=args)
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_text(result)})


asyncio.run(main())
