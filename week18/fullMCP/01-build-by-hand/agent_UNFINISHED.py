"""
agent_UNFINISHED.py — your STARTING POINT for the guided build.

Follow README.md. You will paste ONE step at a time into the
marked spot below, run it, watch it work, then move to the next step.

BEFORE YOU START (do this once):
    pip install "mcp[cli]<2" openai requests python-dotenv ddgs
    ollama pull qwen2.5:7b

RUN EVERYTHING FROM THIS FOLDER (01-build-by-hand). It is self-contained.
    Terminal 1:  python ../../Day1-Build-a-Server/day1_server_full.py   (keep it running!)
    Terminal 2:  python agent_UNFINISHED.py

    (Optional, for the Neon bonus) make a .env file IN THIS FOLDER, next to
    .env.example -- copy .env.example to .env and paste your key in:
        NEON_API_KEY=your_key_here
"""

import asyncio
import json
import os
from contextlib import AsyncExitStack

from dotenv import load_dotenv
load_dotenv()

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI

# ── settings ─────────────────────────────────────────────────────────────────
LOCAL_URL = "http://127.0.0.1:8000/mcp/"   # your Day 1 server
MODEL     = "qwen3:0.6b"                     # a strong tool-caller
llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")


# ── helpers (already written for you — don't worry about these) ──────────────
def to_openai_tool(t):
    """Turn an MCP tool into the shape the model expects."""
    return {"type": "function", "function": {
        "name": t.name, "description": t.description or "", "parameters": t.inputSchema}}


def extract(result):
    """Get the data out of a tool result. Neon's SQL results come back as
    'structuredContent' (a dict); your local tools come back as text.
    (You'll need this for the Neon bonus — leave it as-is.)"""
    data = getattr(result, "structuredContent", None)
    if data:
        return data
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts).strip()
    try:
        return json.loads(text) if text else text
    except Exception:
        return text


def result_text(result):
    """Always return a readable string for the model — works for text results
    (local tools) AND structuredContent results (Neon's run_sql)."""
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts)
    return text or json.dumps(extract(result))[:2000]


async def main():
    # AsyncExitStack lets us open (and later close) server connections cleanly.
    async with AsyncExitStack() as stack:
        # Open the connection to your Day 1 server.
        r, w, _ = await stack.enter_async_context(streamablehttp_client(LOCAL_URL))
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        # =====================================================================
        # >>> YOUR CODE GOES HERE  —  paste each STEP from the guide below  <<<
        # =====================================================================
        print("Skeleton is connected. Now add Step 9 from the guide.")
                # STEP 9 — ask the server for its tools
                # STEP 12 — a chat that remembers
        tools = (await session.list_tools()).tools
        openai_tools = [to_openai_tool(t) for t in tools]

        messages = [
            {"role": "system", "content": "You are a helpful assistant. When a tool result is given, use it and answer directly."},
        ]

        print("Chat ready! (type 'quit' to exit)\n")
        while True:
            user = input("You: ").strip()
            if user.lower() in ("quit", "exit"):
                break
            messages.append({"role": "user", "content": user})

            # inner AGENT loop: keep calling tools until the AI is done (max 5 rounds)
            for _ in range(5):
                resp = llm.chat.completions.create(
                    model=MODEL, messages=messages,
                    tools=openai_tools, tool_choice="auto")
                msg = resp.choices[0].message

                if not msg.tool_calls:
                    messages.append({"role": "assistant", "content": msg.content})
                    print("Agent:", msg.content, "\n")
                    break

                messages.append({
                    "role": "assistant", "content": msg.content,
                    "tool_calls": [
                        {"id": tc.id, "type": "function",
                         "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                        for tc in msg.tool_calls],
                })
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    print(f"  [tool] {tc.function.name}({args})")
                    result = await session.call_tool(tc.function.name, arguments=args)
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_text(result)})


asyncio.run(main())
