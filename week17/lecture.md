# Day 1 — Build a Server
## Instructor Guide (v3 · July 2026 refresh)

**Length:** 2 hours  
**Goal:** Students write their first MCP tool and watch it work.
**Audience note:** students arrive from the Open-Source LLMs class (Day2-v3) — they already have Ollama working, know `pull/run/serve`, know what a weight and the OpenAI-shape API are. Lean on that.

> **⚡ JULY 2026 UPDATE (read before teaching):**
> The MCP spec **2026-07-28** shipped (now the current spec) — stateless protocol core, Extensions framework, Tasks (long-running work), MCP Apps (server-rendered UIs), hardened OAuth. Everything you teach today still applies — tools/decorators/primitives are unchanged — but say so on the "What MCP is" slide: *"the spec is evolving fast; the primitives you learn today are the stable core."*
> Adoption ammo for the hook: **~20,000 MCP servers** indexed, **97M monthly SDK downloads**, backed by Anthropic, OpenAI, Google AND Microsoft. This is not a niche protocol anymore.

---

## Pre-Class Checklist

- [ ] Ollama running: `ollama serve` (separate terminal)
- [ ] Model pulled: `ollama pull phi4-mini`
- [ ] `requests` installed: `pip install requests`
- [ ] `mcp[cli]` installed: `pip install mcp[cli]`
- [ ] Test the demo: `python demo_act1_failures.py` — confirm 3 responses print cleanly
- [ ] Test the server: `python server.py` — confirm "Server starting → http://127.0.0.1:8000/mcp/" appears
- [ ] Test the client: `python client.py` — confirm tool list + read_file + get_weather all print
- [ ] `notes.txt` exists in this folder
- [ ] Goose installed (instructor machine only — `block.github.io/goose`)
- [ ] Goose model: Settings → Models → Ollama → `c` → `qwen3:8b`
- [ ] Goose extension: `workshop` pointing to `server.py` (see config.yaml in the Goose demo section below)

---

## Timing

| Time      | Block                                                    |
|-----------|----------------------------------------------------------|
| 0:00–0:10 | The hook — 3 failures                                    |
| 0:10–0:35 | Why MCP — evolution + definition + decorators + 3 primitives |
| 0:35–1:05 | Live-code `server.py` together                           |
| 1:05–1:10 | Optional: Goose demo — connect a real client             |
| 1:10–1:40 | Student exercise                                         |
| 1:40–2:00 | Q&A + pitfalls                                           |

---

## 0:00–0:10 — The Hook

**⌨ DO NOW (minute one, before anything):** every student, terminal open:

```
ollama --version && python -c "import mcp; print('mcp OK')"
```

Errors → hand up NOW, pair with a working neighbor. (Same opening ritual as the LLM class — they know the drill.)

Then run `demo_act1_failures.py` — it's in this folder.

```
python demo_act1_failures.py
```

Three questions. Three failures. Let the silence land after each one.

After the third failure, say:

> "Three questions. Three failures. Same root cause every time: the LLM is trapped inside a box. It knows everything that was in its training data — and nothing that happened after, nothing on your machine, nothing in your database.
>
> MCP is the door out of that box."

---

## 0:10–0:35 — Why MCP + Architecture + Decorators + 3 Primitives

### The Evolution (3 min)

**Interactive — predict first:** *"Yesterday your local model invented a weather report for Tel Aviv. Shout: what are the ways to FIX that?"* Collect answers (retrain! give it documents! let it call a weather API!) — then reveal: they just named the three eras.

Before drawing anything, one minute of history.

> "Three eras. One sentence each.
>
> **Fine-tuning:** Train the model on your data. Expensive, slow, and frozen — the model still can't access anything that happened after training.
>
> **RAG:** Add a retriever. The model can now read documents. Better — but read-only. It can't write, can't call APIs, can't book a flight.
>
> **MCP:** Add tools the model can call. Now it can act. Read files. Fetch live data. Execute anything you expose. That's today."

**The deeper argument (30 sec — use for "why not just APIs?"):**

> "APIs were designed for programs that already know exactly what they want — precise, deterministic requests. A language model reasons probabilistically; it explores before it knows what to do. APIs have the wrong CONSUMER. MCP is the interface built for a consumer that reasons.
>
> And MCP doesn't replace your APIs — it's an abstraction ABOVE them. Your MCP server will likely call your existing REST APIs under the hood. The model never sees that."

**Watch for — students who watched the Google Cloud MCP video** arrive with two wrong ideas: "the client is the LLM" (no — the client lives inside the HOST app; the model is neither), and "four primitives: tools, prompts, resources, context" (no — THREE; "context" is not a primitive). Correct both before the architecture drawing.

### What MCP actually is (2 min)

> "MCP is an open protocol — like HTTP, but for tools. The server exposes what it can do. The client discovers it. They communicate over a standard called JSON-RPC."

Draw this hierarchy on the board:

```
[Host app — Claude Desktop, Goose, your client.py]
    │
    └─► [MCP Client]  ──────►  [MCP Server]
                                    │
                               ┌────┴────┐────────┐
                             Tools  Resources  Prompts
```

> "The host is the application the user talks to. The MCP client lives inside it. The MCP server is your Python/Typescript/Javascript file. The server can expose three types of things."

Write on the board:
- **Tools** — functions the LLM *calls* ("get the weather, read this file")
- **Resources** — data the *application* reads at startup ("today's notes")
- **Prompts** — workflow templates the *user* triggers by name ("summarize this document")

> "Today we build tools. They're the most important primitive — that's where the LLM's decision-making happens."

Quick code preview (don't live-code yet — just show from `server.py`):

```python
@mcp.tool()                             # LLM decides when to call this
def get_weather(city: str) -> str:
    """Get the current weather for any city."""
    ...  # we'll build this together

@mcp.resource("notes://today")          # host reads this at startup
def today_notes() -> str:
    """Workshop notes. Goose loads this to give the LLM context."""
    return Path("notes.txt").read_text()

@mcp.prompt(name="summarize")           # user triggers this by name
def summarize_prompt(filename: str) -> str:
    """Instructs the LLM to read a file and summarize it."""
    return f"Read '{filename}' and write a brief summary."
```

> "Three decorators. Three primitives. Same `mcp` object, same file. All three are in `server.py` already. We'll build the tools live now, and I'll show you the resource and prompt are there and working at the end."

### The N×M Problem (5 min)

Draw this on the board. Don't use slides.

```
Without MCP                    With MCP
────────────────               ────────────────────────────────
                               
  LLM A ──► Tool 1              LLM A ─┐
  LLM A ──► Tool 2              LLM B ─┼──► MCP Server ──► Tool 1
  LLM A ──► Tool 3              LLM C ─┘                   Tool 2
  LLM B ──► Tool 1                                          Tool 3
  LLM B ──► Tool 2              
  ...                           
                               
  N models × M tools            N models + M tools
  = N×M integrations            = N+M implementations
  
  (a mess)                      (a standard)
```

Say:
> "Every LLM provider had to build their own plugin system. Every tool had to integrate with every LLM. MCP gives us one standard protocol. Build your server once, it works with any client."

The three things an MCP server can expose:
- **Tools** — functions the LLM can call (today's topic)
- **Resources** — data the LLM can read (a file, a database record)
- **Prompts** — template interactions the user triggers

Today we build tools. They're the most important primitive.

---

### Decorators in Python (5 min)

Before writing the first tool, explain the `@` syntax. This is the only Python concept students need that may be new.

> "Every MCP tool, resource, and prompt is a plain Python function with a decorator above it. You've probably seen the `@` symbol before. Let me show you what it means."

Write on the board:

```python
# Without decorator — just a function:
def get_weather(city: str) -> str:
    return "sunny"

# With decorator — same function, registered as an MCP tool:
@mcp.tool()
def get_weather(city: str) -> str:
    return "sunny"
```

> "The decorator wraps your function and gives it extra behavior — without changing the function itself. In web frameworks you've seen `@app.route('/weather')`, which tells Flask 'this function handles this URL.' In MCP, `@mcp.tool()` tells FastMCP 'this function is a tool the LLM can call.'"

**The payoff in one sentence:**
> "Every tool you write follows this pattern: `@mcp.tool()` on top, clear docstring, function body, return a string. That's it."

---

## 0:35–1:10 — Live-Code server.py

Open `server.py` in your editor. Walk through it line by line.

### Step 1 — The skeleton (3 min)

Open `server_starter.py` — this is what we'll live-code into. `server.py` is the completed reference; students can study it after class.

Point at the top of server_starter.py:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Workshop")
```

> "FastMCP is our framework. One line, we have a server. We name it 'Workshop' — this name shows up in the client when tools are listed."

Point at the bottom:
```python
if __name__ == "__main__":
    if sys.stdin.isatty():
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
```

> "HTTP mode when you run it from a terminal. STDIO mode when Goose or Claude Desktop run it as a subprocess. Same server, two transport modes, automatic detection."

Run it: `python server_starter.py`

> "Empty server. No tools. Nothing the LLM can call. We're going to change that."

### Step 2 — First tool: read_file (15 min)

Open `server_starter.py`. Type this below the comment block:

```python
@mcp.tool()
def read_file(filename: str) -> str:
    """Read any text file from the current directory and return its full contents."""
    path = Path(__file__).parent / filename
    if not path.exists():
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")
```

**Stop at the docstring.** Point at it.

> "This isn't just documentation. This is the prompt the LLM reads to decide whether to call this tool. If you write 'reads a file', the LLM might call it for the wrong thing. If you write 'Read any text file from the current directory and return its full contents' — it knows exactly what to do.
>
> The docstring is prompt engineering. A good docstring = good LLM decisions."

Restart the server. Run:

```
python client.py
```

> "What's in notes.txt?" — it works. That's the first 'it works' moment.

### Step 3 — Second tool: get_weather (15 min)

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

> "wttr.in — completely free, no API key, no signup. The timestamp in the response proves this is live data."

Restart the server. Run `python client.py`.

Show the output: `Tel Aviv: ⛅️  +28°C`

> "This is real data fetched right now. The LLM couldn't do this 30 minutes ago."

**Ask:** "Who can tell me why `import requests` is inside the function, not at the top of the file?"

*(Answer: if the import is at the top and requests isn't installed, the entire server crashes on startup — not just when the tool is called. Inside the function, the error is isolated.)*

### The pattern

Point at the two tools side by side.

> "Every tool you'll ever write follows this exact pattern:
>
> 1. Decorate with `@mcp.tool()`
> 2. Write a clear docstring — this is your prompt engineering
> 3. Implement the function — do one specific thing
> 4. Return a string
>
> That's it. That's the whole API."

### Optional: Connect Goose (5 min)

> "We've been testing with `client.py` — our own code talking to the server directly.
> Let me show you what it looks like when a real product connects."

**Before the demo — set Goose model to qwen3:8b** (required, default model is too small for tool use):
- Goose → **Connect to a Provider** → Ollama → **Configure** → Ollama Host: `localhost` → **Submit** → select `qwen3:8b`

**Goose extension config** (`C:\Users\<user>\.config\goose\config.yaml`):
```yaml
extensions:
  workshop:
    enabled: true
    name: workshop
    type: stdio
    cmd: python
    args:
      - "C:\\full\\path\\to\\Day1-Build-a-Server\\server.py"
    envs: {}
```
Or via Goose UI: Settings → Extensions → Add custom extension:
- Extension Name: `Workshop` · Type: `STDIO`
- Command: `python C:\full\path\to\server.py` *(python and path in one field)*

Open Goose. The `workshop` extension loads automatically. Ask:

- **"What's in notes.txt?"** → Goose calls `read_file`. The answer appears in chat.
- **"What's the weather in Tel Aviv?"** → Goose calls `get_weather`. Live data in the chat.

> "Same server. Same two Python functions. Now it's running inside a full AI chat interface.
> This is the N+M point made real: you built one server — Claude Desktop, Goose, your own
> `client.py` all talk to it over the same protocol. Build once, connect anywhere."

**Note:** When Goose spawns the server, it uses STDIO transport — that's the `else: mcp.run()` branch in `server.py`. The server detects it's not in a terminal and switches automatically. No config change needed.

If Goose isn't set up: skip this and point students to the "Bonus: Connect Goose" section in `student_tryit.md`.

---

**Now scroll to the bottom of `server.py`.** Show the resource and prompt already there.

> "Remember the three primitives from the diagram? Tools, Resources, Prompts. Your `server.py` has all three. You built the tools live just now. The resource and prompt are already in the file — they're working. The resource `notes://today` is something a host app like Goose reads on startup to give the LLM background context. The prompt `summarize` is a workflow template the user triggers by name.
>
> We focused on tools today because tools are where the LLM makes decisions. The other two primitives exist — they're in your file — and you'll see them activate when you connect a real client."

---

## 1:10–1:40 — Student Exercise

Hand out `student_tryit.md`. Students add one tool to their copy of `server.py`.

Walk around and help with:
- Import errors (remind them to install packages first)
- API key questions (steer them to free APIs: wttr.in for weather, Open-Meteo, Wikipedia, etc.)
- Server restart — they must restart every time they change `server.py`

**Most common mistake:** Forgetting to restart the server after changing the code.

---

## 1:40–2:00 — Q&A + Pitfalls

Write these on the board:

**Five pitfalls:**

1. **`print()` breaks STDIO servers.** In STDIO mode, stdout is the protocol. One stray `print()` corrupts the stream. Use `print(..., file=sys.stderr)` for debugging, or use logging.

2. **Restart after every change.** The server loads your code once at startup. Changing `server.py` has zero effect until you kill and restart the process.

3. **`client.py` uses Streamable HTTP; Goose uses STDIO. Both are valid.** When you run `python server.py` yourself, it starts in HTTP mode and `client.py` connects over HTTP. When Goose spawns the server as a subprocess, `server.py` detects it's not in a terminal and switches to STDIO automatically. If you see older MCP examples using `StdioServerParameters` — that's STDIO transport, not HTTP.

4. **Docstrings are prompts.** A vague description = wrong tool calls. A precise description = accurate decisions. We'll see this dramatically in Day 2.

5. **"Port 8000 is already in use."** Another server is still running. Three ways to fix it:

   - **Easiest:** find the terminal where you ran `python server_starter.py` and press Ctrl+C. Then restart.
   - **Kill by PID (Windows):**
     ```
     netstat -ano | findstr :8000
     ```
     The last column is the PID. Then kill it — pick the right shell:
     ```
     taskkill //PID <PID> //F        ← Git Bash (double slash)
     taskkill /PID <PID> /F          ← CMD / PowerShell
     Stop-Process -Id <PID> -Force   ← PowerShell alternative
     ```
   - **Change port (if you need two servers at once):** in `server_starter.py` change `mcp.run(transport="streamable-http")` to `mcp.run(transport="streamable-http", port=8001)`, and update `MCP_SERVER_URL` in `client.py` to `http://127.0.0.1:8001/mcp/`.

---

## What They Built

By the end of Day 1, every student has:
- A running MCP server with all 3 MCP primitives — tools they live-coded, plus a resource and prompt that come pre-built in `server.py` as examples
- Seen an LLM question answered using their tools
- Written their first tool from scratch

Tomorrow: we wire an LLM into the loop so it decides which tool to call.
