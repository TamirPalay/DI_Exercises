---
title: "Day 3 · 01 — Build an AI Agent by Hand"
subtitle: "No experience assumed. Do each step in order. Don't skip."
geometry: margin=0.85in
mainfont: DejaVu Sans
monofont: DejaVu Sans Mono
fontsize: 11pt
colorlinks: true
header-includes:
  - \usepackage{fvextra}
  - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\}}
---

# Build an AI agent by hand

Ask a question, and the AI decides which tools to call, calls them, reads the results,
and keeps going until it can answer. **You** write that loop. It's about 15 lines.
That's the whole magic of an "AI agent".

**This one file is everything.** Follow it top to bottom. You do not need to understand
every line — run each step, watch it work, then move on.

## The one idea: who controls the loop

**Chatbot** (text only) → **tool use** (one call — your Day 2 client) → **agent** (many
calls — today). Same tools, same model. The only difference is that the *model* now
decides when to call again and when to stop.

> Picture it: on Day 2 you were a chef following one recipe step. An agent is the chef
> who reads the whole order, decides what to cook first, tastes, and keeps going until
> the plate is done.

## The two files you'll touch

| File | What it is |
|---|---|
| `agent_UNFINISHED.py` (or `.js`) | The one **you** edit. It connects, then stops. |
| `agent_FINISHED.py` (or `.js`) | Already works. Run it if you get stuck. |

> **Two windows.** You'll keep **two terminal windows** open the whole time.
> **Window 1** runs a small server — start it and never type in it again.
> **Window 2** is where you run the agent, over and over.
> If you close Window 1, the agent stops working.

**Python or JavaScript?** Either — they do exactly the same thing, and every step below
shows both. Pick the one you know. If you know neither, pick Python.

---

# Part 1 — Set up (once)

## Step 1 — Open a terminal

- **Windows:** press the Start button, type `powershell`, press Enter.
- **Mac:** press `Cmd + Space`, type `terminal`, press Enter.

A window with a blinking cursor appears. You type commands and press Enter. That's all
it is.

**To stop a running program in a terminal, press `Ctrl + C`.** Remember that one.

## Step 2 — Check what you have installed

Type each line, press Enter.

```bash
python --version
ollama --version
node --version
```

✅ **You should see** a version number for each, e.g. `Python 3.12.1`.

If you see **"command not found"** or **"not recognized"**, install that thing, then
come back:

- Python → <https://www.python.org/downloads/> (get 3.10 or newer)
- Ollama → <https://ollama.com/download>
- Node → <https://nodejs.org> — **only if you want the JavaScript version.**

> **Mac tip:** if `python` says "command not found" but `python3` works, use `python3`
> everywhere below.

## Step 3 — Install the Python packages

```bash
python -m pip install "mcp[cli]<2" openai requests python-dotenv ddgs
```

✅ **You should see** `Successfully installed …` near the end. It prints a lot on the
way — that's normal.

> **Why `python -m pip` and not just `pip`?** On many Windows machines `pip` on its own
> gives "pip is not recognized". `python -m pip` works anywhere `python` works.

> **Why the `<2`?** A newer version of `mcp` breaks this course. If you ever see
> `No module named mcp.server.fastmcp`, you got the wrong one — run
> `python -m pip uninstall -y mcp mcp-types` then the install line again.

## Step 4 — Download the AI model

```bash
ollama pull qwen2.5:7b
```

⏳ This is a **~4.7 GB download** and takes several minutes. Once per computer.

✅ **Check it worked:** run `ollama list` — `qwen2.5:7b` should be in the list.

> **If `ollama list` errors**, Ollama isn't *running* (installing it isn't the same as
> running it). Open the Ollama app, or run `ollama serve` in its own window.

> **Why this model?** It's the "just right" size for using tools. Smaller ones (like
> `qwen3:0.6b`) are too weak. Bigger thinking ones are slow.

## Step 5 — Get your terminal into this folder

Almost every problem in this workshop is "I was in the wrong folder". **This folder —
`01-build-by-hand` — is where you work.** Everything it needs lives inside it.

- **Windows:** open the `01-build-by-hand` folder in File Explorer, click the address
  bar at the top, type `powershell`, press Enter. A terminal opens **already there**.
- **Mac:** right-click the folder → Services → *New Terminal at Folder*.
- **Either:** type `cd ` (with a space), then **drag the folder** from Explorer/Finder
  onto the terminal window — it pastes the path for you. Press Enter.

✅ **Check you're in the right place.** Run `dir` (Windows) or `ls` (Mac). You must see
`agent_UNFINISHED.py`, `agent_FINISHED.py` and `package.json`.

> Do this in **both** terminal windows. Every command below assumes you're standing in
> `01-build-by-hand`.

## Step 6 — JavaScript only: install the Node packages

> **Doing this in Python? Skip this step.** You never need npm.

```bash
npm install
```

**Run it right here**, in `01-build-by-hand`. `npm install` only works in a folder that
**has a `package.json`** in it — and this folder has one. It's the shopping list of code
libraries the JavaScript version needs; npm reads it, downloads the three libraries, and
puts them in a new `node_modules` folder right here.

❌ If you get `npm error enoent Could not read package.json`, it means exactly one thing:
**you're in the wrong folder.** Redo Step 5.

✅ **Check it worked:** run `dir` / `ls` again — there's now a `node_modules` folder.
(It contains a lot of files. That's normal; you never look inside.)

---

# Part 2 — Start the server, run the skeleton

## Step 7 — Start the Day 1 server (Window 1)

Your agent needs tools to call. They live on the little server you built on **Day 1**.
It's in a different folder, so we reach it with `../../` — "go up two folders, then down
into `Day1-Build-a-Server`".

```bash
python ../../Day1-Build-a-Server/day1_server_full.py
```

✅ **You should see** something like *"Uvicorn running on http://127.0.0.1:8000"*.

**Now leave this window completely alone.** Don't close it, don't type in it.

> **It looks frozen — that's correct.** A running server just sits there waiting. That's
> what success looks like.

## Step 8 — Run the agent skeleton (Window 2)

Switch to your second terminal (also in `01-build-by-hand`):

```bash
python agent_UNFINISHED.py
```

*(JavaScript: `node agent_UNFINISHED.js`)*

✅ **You should see:** *"Skeleton is connected. Now add Step 9 from the guide."*

The agent is connected but has **no loop yet** — it can't answer questions. You add that
next.

---

# Part 3 — Build the loop, one piece at a time

Open **`agent_UNFINISHED.py`** (or `.js`) in a text editor — VS Code, Notepad, anything.
Near the bottom you'll find:

```python
        # =====================================================================
        # >>> YOUR CODE GOES HERE  —  paste each STEP from the guide below  <<<
        # =====================================================================
        print("Skeleton is connected. Now add Step 9 from the guide.")
```

**Each step below replaces whatever is under that marker.** For Step 9, delete the
`print(...)` line and paste Step 9's code in its place. For Step 10, delete Step 9's code
and paste Step 10's. And so on — you're growing one block, not stacking four.

⚠️ **Two things beginners get wrong here:**

1. **Keep the indentation.** The Python code is indented (it sits inside the program).
   Paste it exactly as shown — if the leading spaces are lost, Python stops with an
   `IndentationError`.
2. **Save the file** (`Ctrl + S`, or `Cmd + S` on Mac), then run it again. Nothing
   changes until you save.

## Step 9 — DISCOVER: what can the server do?

**Python**

```python
        # STEP 9 — ask the server for its tools
        tools = (await session.list_tools()).tools
        print("The server offers these tools:")
        for t in tools:
            print("  -", t.name)
```

**JavaScript**

```javascript
  // STEP 9 — ask the server for its tools
  const tools = (await client.listTools()).tools;
  console.log("The server offers these tools:");
  for (const t of tools) console.log("  -", t.name);
```

**Run it.** You should see 4 tool names: `read_file`, `get_weather`, `wikipedia_summary`,
`web_search`.

**What just happened:** we never hard-code tool names — we *ask* the server. Add a fifth
tool to the server tomorrow and it appears here on its own, with no change to your code.

> **Curious what a tool looks like?** Open `../../Day1-Build-a-Server/day1_server_full.py`
> and find `wikipedia_summary`. It's a normal function with a `@mcp.tool()` line on top —
> and its **docstring is the prompt**. That text is the only thing telling the AI when to
> use it. There's no `if` statement anywhere choosing between tools; the model reads the
> descriptions and picks.

## Step 10 — DECIDE: let the AI pick a tool

**Python**

```python
        # STEP 10 — ask the AI which tool to use
        tools = (await session.list_tools()).tools
        openai_tools = [to_openai_tool(t) for t in tools]

        messages = [
            {"role": "system", "content": "You are a helpful assistant. Use a tool when the question needs live data."},
            {"role": "user",   "content": "What is the weather in Tel Aviv?"},
        ]

        resp = llm.chat.completions.create(
            model=MODEL, messages=messages,
            tools=openai_tools, tool_choice="auto")
        msg = resp.choices[0].message

        print("The AI wants to call:", msg.tool_calls)
```

**JavaScript**

```javascript
  // STEP 10 — ask the AI which tool to use
  const tools = (await client.listTools()).tools;
  const openaiTools = tools.map(toOpenAITool);

  const messages = [
    { role: "system", content: "You are a helpful assistant. Use a tool when the question needs live data." },
    { role: "user",   content: "What is the weather in Tel Aviv?" },
  ];

  const resp = await llm.chat.completions.create({
    model: MODEL, messages, tools: openaiTools, tool_choice: "auto" });
  const msg = resp.choices[0].message;

  console.log("The AI wants to call:", msg.tool_calls);
```

**Run it.** The AI should ask for `get_weather` with `{"city": "Tel Aviv"}`.

**What just happened:** the AI **chose** a tool — but it only *named* it. No weather came
back. Deciding and doing are two different jobs.

## Step 11 — EXECUTE + ANSWER: run it, get a real reply

**Python**

```python
        # STEP 11 — the full 4-step loop, one time
        tools = (await session.list_tools()).tools
        openai_tools = [to_openai_tool(t) for t in tools]

        messages = [
            {"role": "system", "content": "You are a helpful assistant. When a tool result is given, use it and answer directly."},
            {"role": "user",   "content": "What is the weather in Tel Aviv?"},
        ]

        resp = llm.chat.completions.create(
            model=MODEL, messages=messages,
            tools=openai_tools, tool_choice="auto")
        msg = resp.choices[0].message

        # save the AI's turn (it asked for a tool)
        messages.append({
            "role": "assistant", "content": msg.content,
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls],
        })

        # EXECUTE each tool the AI asked for, and save the result
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = await session.call_tool(tc.function.name, arguments=args)
            print("Tool result:", result_text(result))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_text(result)})

        # SYNTHESIZE — ask the AI again, now that it has the real data
        final = llm.chat.completions.create(model=MODEL, messages=messages)
        print("\nAnswer:", final.choices[0].message.content)
```

**JavaScript**

```javascript
  // STEP 11 — the full 4-step loop, one time
  const tools = (await client.listTools()).tools;
  const openaiTools = tools.map(toOpenAITool);

  const messages = [
    { role: "system", content: "You are a helpful assistant. When a tool result is given, use it and answer directly." },
    { role: "user",   content: "What is the weather in Tel Aviv?" },
  ];

  const resp = await llm.chat.completions.create({
    model: MODEL, messages, tools: openaiTools, tool_choice: "auto" });
  const msg = resp.choices[0].message;

  // save the AI's turn (it asked for a tool)
  messages.push({
    role: "assistant", content: msg.content,
    tool_calls: msg.tool_calls.map((tc) => ({
      id: tc.id, type: "function",
      function: { name: tc.function.name, arguments: tc.function.arguments } })),
  });

  // EXECUTE each tool the AI asked for, and save the result
  for (const tc of msg.tool_calls) {
    const args = JSON.parse(tc.function.arguments);
    const result = resultText(await client.callTool({ name: tc.function.name, arguments: args }));
    console.log("Tool result:", result);
    messages.push({ role: "tool", tool_call_id: tc.id, content: result });
  }

  // SYNTHESIZE — ask the AI again, now that it has the real data
  const final = await llm.chat.completions.create({ model: MODEL, messages });
  console.log("\nAnswer:", final.choices[0].message.content);
```

**Run it.** Real weather, then a plain-English answer.

**What just happened:** **Execute** — *your* code runs the tool; the AI never does.
**Answer** — you hand the real result back and the AI writes the sentence. Watch the
roles stack up: **system → user → assistant → tool → answer**.

## Step 12 — Make it a real CHAT (loop + memory)

**Python**

```python
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
```

**JavaScript**

```javascript
  // STEP 12 — a chat that remembers
  const tools = (await client.listTools()).tools;
  const openaiTools = tools.map(toOpenAITool);

  const messages = [
    { role: "system", content: "You are a helpful assistant. When a tool result is given, use it and answer directly." },
  ];

  const rl = readline.createInterface({ input, output });
  console.log("Chat ready! (type 'quit' to exit)\n");
  while (true) {
    const user = (await rl.question("You: ")).trim();
    if (["quit", "exit"].includes(user.toLowerCase())) break;
    messages.push({ role: "user", content: user });

    // inner AGENT loop: keep calling tools until the AI is done (max 5 rounds)
    for (let i = 0; i < 5; i++) {
      const resp = await llm.chat.completions.create({
        model: MODEL, messages, tools: openaiTools, tool_choice: "auto" });
      const msg = resp.choices[0].message;
      const calls = msg.tool_calls || [];

      if (calls.length === 0) {
        messages.push({ role: "assistant", content: msg.content });
        console.log("Agent:", msg.content, "\n");
        break;
      }

      messages.push({
        role: "assistant", content: msg.content,
        tool_calls: calls.map((tc) => ({
          id: tc.id, type: "function",
          function: { name: tc.function.name, arguments: tc.function.arguments } })),
      });
      for (const tc of calls) {
        const args = JSON.parse(tc.function.arguments);
        console.log(`  [tool] ${tc.function.name}(${JSON.stringify(args)})`);
        const result = resultText(await client.callTool({ name: tc.function.name, arguments: args }));
        messages.push({ role: "tool", tool_call_id: tc.id, content: result });
      }
    }
  }
  rl.close();
```

**What just happened:** two big ideas at once.

- **Memory:** everything lives in one growing `messages` list, sent every time. That list
  *is* the memory.
- **The agent loop:** `for _ in range(5)` / `for (let i = 0; i < 5; i++)` lets the AI call
  a tool, read the result, decide the next step, and call another — until it's done.
  That's the difference between "one tool" and a real agent.

> **The one rule you must not skip:** the loop is capped at **5**. This stops a confused
> model from looping forever. Leaving it out is the #1 beginner mistake.

---

# Part 4 — Talk to your agent

Type a question and press Enter. Start with:

```
What is the weather in Tel Aviv right now, and what does notes.txt say?
```

You'll see it call one tool for the weather, another to read the file, then write one
combined answer. **You built the thing that decides all that.**

> The first answer can take 30–60 seconds while the model loads into memory. Later ones
> are much faster.

Try a few more:

- `What is France known for, and what's the weather in its capital?`
  → two tools in a row; it carries "Paris" from step one into step two.
- `What's the largest country in the world and the weather in its capital?`
  → same trick, and it has to look up the capital first.
- `and what did I just ask you?`
  → proves it remembers.
- `What is Python the programming language?`
  → a good agent answers from memory and calls **no** tool. That's smart, not lazy.

Type `quit` when you're done.

> **Stuck, or your file won't run?** Run the working version and compare:
> `python agent_FINISHED.py`

---

# Bonus — Add a database (Neon)

> **Optional, and Python only.** Everything above works without this. Skip it unless you
> want to see an agent use two servers at once.

A host can hold many servers at once. Let's add Neon — a real Postgres database in the
cloud — so the same chat can answer *"what's the weather in Tel Aviv?"* (your local
server) **and** *"list our products and their prices"* (the database).

**Get a free Neon API key:** go to <https://console.neon.tech> — account menu (top right)
→ **Account settings** → **API keys** → *Create new API key*. It starts with `napi_`.

**Put it in a `.env` file in this folder.** Copy `.env.example` to `.env` and paste the
key in:

```
NEON_API_KEY=napi_your_key_here
```

`load_dotenv()` looks in the folder you ran from — this one. `.env` is already in this
folder's `.gitignore`, so your key won't be committed.

> **If the key is wrong**, you won't get a friendly message — you'll get a 40-line wall
> of red `ExceptionGroup` traceback ending in `401 Unauthorized`. That means the **key**,
> not your code. Fix `.env` and rerun. (`agent_FINISHED_neon.py` shows how to check the
> key first, so it fails with one clear sentence instead.)

> **Two things your skeleton already handles:** Neon returns SQL results as
> `structuredContent`, not plain text — the `extract()` / `result_text()` helpers read
> both. And the *app*, not the AI, supplies the `projectId` and `databaseName`.

**A.** This block **replaces** the two lines at the top of your Step 12 code
(`tools = ...` and `openai_tools = ...`). It builds a tool→server map, connects Neon,
finds your project id, and reads your table and column names so the AI won't guess wrong:

```python
        # remember which server owns each tool
        owner = {}          # tool name -> the session that runs it
        all_tools = []      # every tool, in the model's format

        for t in (await session.list_tools()).tools:
            owner[t.name] = session
            all_tools.append(to_openai_tool(t))

        # If auto-discovery below fails (common with org-scoped keys), paste your
        # project id here. Find it at console.neon.tech -> your project -> Settings.
        NEON_PROJECT_ID = ""            # e.g. "rough-dawn-06481786"

        # connect Neon (only if a key is set)
        neon_pid, schema_hint = NEON_PROJECT_ID, ""
        NEON_KEY = os.environ.get("NEON_API_KEY", "")
        if NEON_KEY:
            r2, w2, _ = await stack.enter_async_context(
                streamablehttp_client("https://mcp.neon.tech/mcp",
                                      headers={"Authorization": f"Bearer {NEON_KEY}"}))
            neon = await stack.enter_async_context(ClientSession(r2, w2))
            await neon.initialize()
            for t in (await neon.list_tools()).tools:
                if t.name == "run_sql":                 # just this one, to keep it focused
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
                    "projectId": neon_pid, "databaseName": "neondb",
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
```

**B.** Now make **three small edits** to the rest of your Step 12 code:

1. Add the schema to your system message, so the AI knows the real column names:

```python
        messages = [
            {"role": "system", "content":
                "You are a helpful assistant. When a tool result is given, use it and answer directly. "
                "For run_sql, the projectId and databaseName are provided for you." + schema_hint},
        ]
```

2. In the `llm.chat.completions.create(...)` call inside the loop, change
   `tools=openai_tools` to `tools=all_tools`. (`openai_tools` no longer exists — block A
   replaced it with `all_tools`.)

3. In the tool-running loop, **route** each call to its owner and fill in Neon's ids:

```python
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    if tc.function.name == "run_sql":       # the APP supplies these, not the AI
                        args["projectId"] = neon_pid
                        args["databaseName"] = "neondb"
                    the_session = owner.get(tc.function.name, session)   # <-- ROUTE it
                    print(f"  [tool] {tc.function.name}({args})")
                    result = await the_session.call_tool(tc.function.name, arguments=args)
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_text(result)})
```

**Run it.** In one chat: *"how many products do we have?"* · *"list our products and their
prices"* · *"what's the weather in Tel Aviv?"* Asking all three in one session is the
proof: the `owner` map sends each call to the right server.

> **`Neon project: (not found ...)`?** Auto-discovery fails with org-scoped keys. Paste
> your id into `NEON_PROJECT_ID` in block A — find it at console.neon.tech → your project
> → Settings.

> **Where does the `products` table come from?** Day 1's `EXERCISE_Neon_DB.md` creates it
> and inserts a few rows. Skipped that exercise? Your database is empty, so the schema
> line prints nothing and the agent has no data to find.

**What just happened:** you built a mini **host**. It holds two server connections, merges
their tools, and the `owner` map sends each call to the right one. The AI has no idea the
tools live in different places — that's the point of a shared standard. This is how Claude
Desktop and Goose work.

> **The finished version** is `agent_FINISHED_neon.py` in this folder. Run it directly to
> see where you're heading.

---

# If something goes wrong

| What you see | What it means → what to do |
|---|---|
| `npm error enoent Could not read package.json` | Wrong folder for `npm install`. Get into `01-build-by-hand` (Step 5), then Step 6. |
| `Connection refused` on port **8000** | Window 1 (the Day 1 server) isn't running. Go do Step 7. |
| `Connection refused` on port **11434** | **Ollama** isn't running. Open the Ollama app, or run `ollama serve`. |
| `pip is not recognized` | Use `python -m pip install ...` instead of `pip install ...`. |
| `No module named mcp.server.fastmcp` | Wrong `mcp` version. Run the uninstall + reinstall from Step 3. |
| `IndentationError` | The leading spaces were lost when you pasted. Re-paste, keeping the indentation. |
| `can't open file ... No such file or directory` | Wrong folder. Redo Step 5 and check with `dir` / `ls`. |
| The answer ignores the tool result / is vague | The model is too weak. Make sure Step 4 pulled `qwen2.5:7b`. |
| `command not found: python` (Mac) | Use `python3` instead of `python`. |
| It connects but can't reach `localhost` | Use `127.0.0.1`, not `localhost` (Windows tries IPv6 first; Ollama is IPv4). Already set that way in the files. |
| It never stops / repeats forever | You left out the loop cap. Put `range(5)` back (Step 12). |

---

# What you just learned

An "AI agent" is not magic — it's a **loop**: ask the model, run the tool it names, give
the result back, repeat until done. You wrote that loop by hand.

**Make it yours:** add one more `@mcp.tool()` to `day1_server_full.py`, **restart the
server**, and watch your chat pick it up — without changing the agent at all. That's
Step 9 (Discover) paying off.

Next folder (`02-smolagents`) shows a ready-made framework that writes this loop for you —
and now you know exactly what it's doing.

---

**Instructors:** to rebuild the handout PDF you need pandoc *and* a LaTeX engine:

```bash
pandoc README.md -o README.pdf --pdf-engine=xelatex
```
