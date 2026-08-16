---
title: "MCP Day 1 — Build a Server · Teaching Run-Sheet"
subtitle: "What to DO and what to SAY, step by step, in file order · 2 hours"
geometry: margin=0.8in
mainfont: DejaVu Sans
monofont: DejaVu Sans Mono
fontsize: 10pt
colorlinks: true
---

# How to use this sheet

One continuous run-of-show for Day 1. Each step tells you what to **DO** (which
file to open or run) and what to **SAY** (paraphrase — don't read). The files in
this folder are listed once below in the order you touch them, then again inline
at the moment you use them.

## The files in this folder, in order of use

| # | File | What it is / when you use it |
|---|------|------------------------------|
| 1 | `demo_act1_failures_simple.py` | The **hook** — run first. Three questions the LLM fails (plain `print`, only needs `ollama`). |
| — | `demo_act1_failures.py` | Same hook, prettier output (uses `rich`). Use whichever you like. |
| 2 | `mcp_server.py` | The **minimal server** (read_file + get_weather) — your live-code target. |
| 3 | `day1_server_full.py` | The **full reference** server (adds wikipedia_summary + web_search + a resource + a prompt). |
| 4 | `Day1_StepByStep.md` | The written **build walkthrough** — hand to students to follow along / after class. |
| 5 | `notes.txt` | The data the `read_file` tool reads. Keep it in this folder. |
| 6 | `prove_it_runs.py` | The **no-LLM probe** client — proves the server works. |
| 7 | `student_tryit.md` | The **student exercise** handout. |
| — | `lecture.md` | The long-form instructor guide this sheet condenses. |

## Before class (T-10)

Ollama running (`ollama serve`), `ollama pull phi4-mini`, and `pip install "mcp[cli]" requests`.
Quick self-test: run `python demo_act1_failures_simple.py`, then in two terminals
`python day1_server_full.py` and `python prove_it_runs.py`. All three should work.

\newpage

# 0:00–0:10 · The hook — three failures

**DO.** Minute one, everyone types this (same ritual as the LLM class):

```
ollama --version && python -c "import mcp; print('mcp OK')"
```

Errors → hand up, pair with a working neighbor. Then run the hook:

```
python demo_act1_failures_simple.py
```

Let the silence land after each of the three failures.

**SAY.** *"Three questions — a file on your disk, the live weather, your database.
Three failures. Same root cause every time: the model is trapped in a box. It
knows what was in its training data, and nothing after — nothing on your machine,
nothing live, nothing in your database. MCP is the door out of that box."*

# 0:10–0:35 · Why MCP

**SAY — the three eras (predict first).** Ask: *"Yesterday your local model invented
a weather report. What are the ways to fix that?"* Collect answers, then reveal
they just named the three eras:

- *"**Fine-tuning** — retrain on your data. Expensive, slow, still frozen after training."*
- *"**RAG** — add a retriever. Now it can read documents. Better, but read-only."*
- *"**MCP** — add tools it can call. Now it can act: read files, fetch live data, run things. That's today."*

**SAY — why not just APIs?** *"APIs were built for programs that already know exactly
what they want. A model reasons probabilistically — it explores. APIs have the
wrong consumer; MCP is the interface for a consumer that reasons. And MCP doesn't
replace your APIs — your server usually calls them under the hood."*

**DO — draw the architecture** (board, no slides):

```
[Host app — Claude Desktop, Goose, your probe]
        │
        └─► [MCP Client] ─────► [MCP Server]  (your Python file)
                                     │
                              ┌──────┼───────┐
                            Tools  Resources  Prompts
```

**SAY.** *"The host is the app the user talks to. The client lives inside it. The
server is your file. Three primitives — **Tools** the model calls, **Resources**
the app reads, **Prompts** the user triggers. Three, not four — 'context' is not a
primitive, it's the result these deliver. Today we build tools: that's where the
model makes decisions."*

**Watch for.** Anyone who saw the Google Cloud MCP video may think "the client is
the LLM" (no — the client is inside the host; the model is neither) or "four
primitives including context" (no — three). Correct both before drawing.

**SAY — decorators (the only new Python).** *"Every tool is a plain function with
`@mcp.tool()` on top. Like `@app.route()` in Flask told the framework 'this handles
this URL,' `@mcp.tool()` tells FastMCP 'this is a tool the model can call.' The
pattern every time: decorator, docstring, body, return a string."*

\newpage

# 0:35–1:05 · Live-code the server

**DO.** Open **`mcp_server.py`** — the minimal server. Point at the top:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Workshop")
```

**SAY.** *"FastMCP is the framework. One line and we have a server named 'Workshop' —
that name shows up in any client. Right now it exposes nothing."*

**DO — Tool 1: read_file.** Walk through it:

```python
@mcp.tool()
def read_file(filename: str) -> str:
    """Read any text file from the current directory and return its full contents."""
    path = Path(__file__).parent / filename
    if not path.exists():
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")
```

**SAY — stop on the docstring.** *"This isn't documentation. It's the prompt the model
reads to decide whether to call this tool. Vague docstring, wrong calls. The
docstring is prompt engineering."* Note the error returns a **string**, never raises —
the model can read the error and react.

**DO — Tool 2: get_weather.**

```python
@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather conditions and temperature for any city in the world."""
    import requests
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        return f"Weather unavailable: {e}"
```

**SAY.** *"wttr.in — free, no key. Live data the model couldn't reach 30 minutes ago."*
**ASK the room:** *"Why is `import requests` inside the function?"* (Answer: isolation —
if it were at the top and requests were missing, the whole server would crash on
startup; inside, only this tool fails.)

**SAY — the pattern (point at both tools).** *"Every tool you'll ever write: `@mcp.tool()`,
a clear docstring, one specific job, return a string. That's the whole API."*

**DO — show the full version.** Open **`day1_server_full.py`**: it has two more tools
(`wikipedia_summary`, `web_search`) plus the other two primitives already written —
a **resource** `notes://today` and a **prompt** `summarize`. *"Three decorators,
three primitives, same `mcp` object. We built the tools; the resource and prompt
are here and working — you'll see them light up when a real client connects."*
(The full written build is in `Day1_StepByStep.md` for students to follow.)

\newpage

# 1:05–1:15 · Prove it runs (no LLM) ⭐

An MCP server does nothing visible on its own — it starts and **waits** for a
client. Two ways to prove it's alive; the Inspector is the crowd-pleaser.

**Way A — the probe (2 terminals).**

```
Terminal 1:  python day1_server_full.py     ← leave running (foreground!)
Terminal 2:  python prove_it_runs.py
```

**SAY.** *"`prove_it_runs.py` is a tiny client — no model. It connects, lists the tools,
and calls them. Watch Terminal 1 as it runs — the waiting server logs the incoming
request. That cause-and-effect across two windows is the moment 'client and server'
clicks."* (`prove_it_runs.py` reads `notes.txt`, which must be in the folder.)

**Way B — the visual Inspector (best, zero code).** From **inside this folder**:

```
npx @modelcontextprotocol/inspector@latest -- python day1_server_full.py
```

Two gotchas: keep the **`--`** (without it, it launches its own demo server and
spams `ENOENT`), and run it **from this folder** (or it can't find the script).
A browser opens — click the **toggle** so it flips to green **Connected** (the
Inspector launches the server itself in STDIO mode; no Terminal 1, no port 8000).
Open **Tools** and hit **Run**:

- `read_file` → `notes.txt` → the file's text.
- `get_weather` → `Tel Aviv` → live temperature.
- `wikipedia_summary` → a **page title** like `Ivory Coast` (a full question 404s — that's the docstring lesson: pass a title, not a question).
- `web_search` → a natural query like `EUR to USD exchange rate` → live results (snippets, not a parsed answer — that's the model's job tomorrow).

**SAY.** *"No client code at all — just Run buttons. That tool list is literally step
one of tomorrow's loop: **discover**. The bridge works; tomorrow the model crosses it."*

# 1:05–1:10 · Optional — connect Goose (a real client)

If Goose is set up (model = `qwen3:8b`, extension → `day1_server_full.py` over STDIO),
ask it *"What's in notes.txt?"* and *"What's the weather in Tel Aviv?"* — it calls
your tools inside a real chat UI. *"Same server, same functions — now inside a
product. Build once, connect anywhere."* If not set up, skip and point to the Goose
section in `student_tryit.md`.

\newpage

# 1:10–1:40 · Student exercise

**DO.** Hand out **`student_tryit.md`**. Students add one new tool (and, if keen, a
resource) to their own copy of the server.

**Walk the room.** Help with import errors, steer them to free no-key APIs
(wttr.in, Open-Meteo, Wikipedia), and — the #1 mistake — **remind them to restart
the server after every change**.

# 1:40–2:00 · Q&A + the five pitfalls

Put these on the board:

1. **`print()` breaks STDIO servers.** In STDIO mode stdout *is* the protocol; a stray `print()` corrupts it. Debug with `print(..., file=sys.stderr)` or logging.
2. **Restart after every change.** The server reads your code once, at startup.
3. **Two transports, both valid.** Run it yourself → HTTP (the probe connects over HTTP). Goose/Inspector spawn it → STDIO (auto-detected via `sys.stdin.isatty()`).
4. **Docstrings are prompts.** Vague description → wrong tool calls. We'll see this dramatically on Day 2.
5. **"Port 8000 already in use."** Another server is running. Ctrl+C its terminal, or find/kill the PID (`netstat -ano | findstr :8000` → `taskkill /PID <PID> /F`), or run on a different port.

# What they built

Every student leaves with a running MCP server exposing all three primitives —
tools they live-coded, plus a resource and prompt — and has seen those tools
return real data with **no model involved yet**. *"Tomorrow we wire an LLM into
the loop so it decides which tool to call."*
