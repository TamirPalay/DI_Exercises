"""
agent_FINISHED_neon.py — the FINISHED Neon-bonus agent: TWO servers at once.

This is agent_FINISHED.py plus the Neon bonus. It talks to your local Day 1 server AND
Neon's hosted MCP server in the same chat. The model has no idea the tools live in
different places — that's the whole point of a shared standard.

The trick is the `owner` map: tool name -> the session that runs it. When the model
names a tool, we look up who owns it and send the call there.

HOW TO RUN  (everything from THIS folder — it is self-contained)
    1) Install once:   python -m pip install "mcp[cli]<2" openai requests python-dotenv ddgs
    2) Get the model:  ollama pull qwen2.5:7b
    3) Neon key:       copy .env.example to .env and paste your key in:
                           NEON_API_KEY=napi_...
                       Get one at https://console.neon.tech ->
                       account menu -> Account settings -> API keys.
    4) Window 1:       python ../../Day1-Build-a-Server/day1_server_full.py   (leave running)
    5) Window 2:       python agent_FINISHED_neon.py
    6) Try, in ONE chat:
         list our products and their prices        -> Neon
         what's the weather in Tel Aviv?           -> your local server
    7) Type 'quit' to stop.

NO NEON KEY? This still runs — it just skips Neon and behaves like agent_FINISHED.py.
The `products` table comes from Day 1's EXERCISE_Neon_DB.md.
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
LOCAL_URL = "http://127.0.0.1:8000/mcp/"   # your Day 1 server (127.0.0.1, not localhost)
NEON_URL  = "https://mcp.neon.tech/mcp"    # Neon's hosted MCP server
NEON_DB   = "neondb"                       # the default Neon database name
MODEL     = "qwen2.5:7b"                   # a model good at calling tools
llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

# If auto-discovery fails (common with org-scoped keys), paste your project id here.
# Find it at console.neon.tech -> your project -> Settings.
NEON_PROJECT_ID = ""            # e.g. "rough-dawn-06481786"


# ── helpers ──────────────────────────────────────────────────────────────────
def to_openai_tool(t):
    """Turn one MCP tool into the shape the model expects."""
    return {"type": "function", "function": {
        "name": t.name, "description": t.description or "", "parameters": t.inputSchema}}


def extract(result):
    """Get the DATA out of a tool result. Neon's SQL results come back as
    'structuredContent' (a dict); your local tools come back as text."""
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
    """Always return a readable STRING for the model — works for text results
    (local tools) and structuredContent results (Neon's run_sql)."""
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts)
    return text or json.dumps(extract(result))[:2000]


def neon_key_works(key: str) -> bool:
    """Check the key is valid BEFORE we open an MCP session.
    A rejected key inside the async session prints an unreadable wall of
    traceback, so we ask Neon's REST API first and fail with a clear message."""
    import requests
    try:
        r = requests.get("https://console.neon.tech/api/v2/projects",
                         headers={"Authorization": f"Bearer {key}"}, timeout=10)
        return r.status_code == 200
    except Exception:
        return True      # network hiccup, not a bad key -- let the MCP path try


async def main():
    async with AsyncExitStack() as stack:
        # 1) CONNECT to the Day 1 server.
        r, w, _ = await stack.enter_async_context(streamablehttp_client(LOCAL_URL))
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        # 2) DISCOVER — and remember which server owns each tool.
        owner = {}          # tool name -> the session that runs it
        all_tools = []      # every tool, in the model's format

        for t in (await session.list_tools()).tools:
            owner[t.name] = session
            all_tools.append(to_openai_tool(t))

        # 3) CONNECT NEON TOO (only if a key is set).
        neon_pid, schema_hint = NEON_PROJECT_ID, ""
        NEON_KEY = os.environ.get("NEON_API_KEY", "")
        neon = None
        key_was_set = bool(NEON_KEY)

        # Check the key BEFORE connecting -- a bad one buried inside the async
        # session prints an unreadable error wall instead of a useful message.
        if NEON_KEY and not neon_key_works(NEON_KEY):
            print("Your NEON_API_KEY was rejected by Neon (401 Unauthorized).")
            print("Check the key in your .env, or make a new one at console.neon.tech")
            print("-> account menu -> Account settings -> API keys.")
            print("Carrying on with the local server only.\n")
            NEON_KEY = ""

        if NEON_KEY:
            r2, w2, _ = await stack.enter_async_context(
                streamablehttp_client(NEON_URL,
                                      headers={"Authorization": f"Bearer {NEON_KEY}"}))
            neon = await stack.enter_async_context(ClientSession(r2, w2))
            await neon.initialize()

        if neon is not None:
            # Neon exposes ~34 tools. Take just run_sql, to keep the model focused.
            for t in (await neon.list_tools()).tools:
                if t.name == "run_sql":
                    owner[t.name] = neon
                    all_tools.append(to_openai_tool(t))

            # find the project id (skipped if you pasted one above)
            if not neon_pid:
                for tn in ("list_projects", "list_shared_projects"):
                    try:
                        d = extract(await neon.call_tool(tn, arguments={}))
                        projs = d.get("projects", d) if isinstance(d, dict) else d
                        if isinstance(projs, list) and projs:
                            neon_pid = projs[0].get("id", ""); break
                    except Exception:
                        pass
            print("Neon project:", neon_pid or "(not found — set NEON_PROJECT_ID above)")

            # read the table + column names, so the AI uses REAL column names
            if neon_pid:
                d = extract(await neon.call_tool("run_sql", arguments={
                    "projectId": neon_pid, "databaseName": NEON_DB,
                    "sql": "SELECT table_name, column_name FROM information_schema.columns "
                           "WHERE table_schema='public' ORDER BY table_name, ordinal_position"}))
                rows = d.get("rows", d) if isinstance(d, dict) else d
                cols = {}
                for row in rows:
                    if isinstance(row, dict) and "table_name" in row:
                        cols.setdefault(row["table_name"], []).append(row.get("column_name", ""))
                schema_hint = " Database tables: " + "; ".join(
                    f"{t}({', '.join(c)})" for t, c in cols.items())
                print("Schema:", schema_hint)
        elif not key_was_set:
            print("(No NEON_API_KEY found — running with the local server only.)")

        print("\nThe agent has these tools:", list(owner), "\n")

        # The whole conversation lives in this list — that IS the agent's memory.
        messages = [{
            "role": "system",
            "content": "You are a helpful assistant. When a tool result is given, use it "
                       "and answer directly. For run_sql, the projectId and databaseName "
                       "are provided for you." + schema_hint,
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

            # THE AGENT LOOP — capped at 5 so it can never run forever.
            for _ in range(5):
                resp = llm.chat.completions.create(
                    model=MODEL, messages=messages,
                    tools=all_tools, tool_choice="auto")
                msg = resp.choices[0].message

                # No tool calls => the model is DONE. Print the answer and stop.
                if not msg.tool_calls:
                    messages.append({"role": "assistant", "content": msg.content})
                    print("\nAgent:", msg.content, "\n")
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
                    if tc.function.name == "run_sql":     # the APP supplies these, not the AI
                        args["projectId"] = neon_pid
                        args["databaseName"] = NEON_DB
                    the_session = owner.get(tc.function.name, session)   # <-- ROUTE it
                    print(f"  [tool] {tc.function.name}({args})")
                    result = await the_session.call_tool(tc.function.name, arguments=args)
                    messages.append({"role": "tool", "tool_call_id": tc.id,
                                     "content": result_text(result)})


asyncio.run(main())
