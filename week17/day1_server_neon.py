"""
day1_server_neon.py — Day 1 EXERCISE SOLUTION: add a DATABASE tool.

This is a copy of day1_server_full.py with ONE new tool — query_database — that
runs a read-only SQL query against a Neon Postgres database. It's the fix for
Failure #3 from the hook: the model that couldn't see your database now can.

BEFORE RUNNING
    pip install "mcp[cli]" requests psycopg2-binary
    Set your Neon connection string (NEVER hardcode it in the file):
        Mac/Linux:  export NEON_DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"
        Windows:    setx NEON_DATABASE_URL "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"
                    (then reopen the terminal)

RUN:
    python day1_server_neon.py

WHAT IT EXPOSES:
    Tools     : read_file, get_weather, wikipedia_summary, web_search, query_database
    Resource  : notes://today
    Prompt    : summarize
"""

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Workshop")


@mcp.tool()
def read_file(filename: str) -> str:
    """Read any text file from the current directory and return its full contents."""
    path = Path(__file__).parent / filename
    if not path.exists():
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")


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


@mcp.tool()
def wikipedia_summary(topic: str) -> str:
    """Get a short summary of any topic from Wikipedia.
    Use this for facts, history, definitions, or general knowledge.

    Args:
        topic: A single subject or Wikipedia page title, e.g. 'Cape Verde',
               'France', 'Tel Aviv' — NOT a full question.
    """
    import requests, urllib.parse
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(topic)
    headers = {"User-Agent": "MCP-Workshop/1.0 (educational demo)"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        return r.json().get("extract", "No summary found.")
    except Exception as e:
        return f"Wikipedia unavailable: {e}"


@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for current facts, news, or statistics on any topic.
    Use this when a single Wikipedia page isn't enough — e.g. a country's
    population, a price, or recent events.

    Args:
        query: What to search for, e.g. 'Cape Verde population 2024'.
    """
    from ddgs import DDGS
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        return "\n\n".join(f"{r['title']}: {r['body']}" for r in results)
    except Exception as e:
        return f"Search unavailable: {e}"


# ── NEW TOOL · reach your DATABASE (Neon Postgres) ───────────────────────────
# Failure #3 from the hook was "the model can't see your database." This is the
# bridge. Neon is just hosted Postgres, so any standard driver works.
#   pip install psycopg2-binary
#   The connection string lives in an ENV VAR, never in the code.
@mcp.tool()
def query_database(sql: str) -> str:
    """Run a read-only SQL query against our Postgres (Neon) database and return
    the rows. Use this for anything about our OWN data — products, prices,
    inventory, customers.

    Args:
        sql: A single SELECT statement, e.g. 'SELECT name, price FROM products'.
    """
    import os
    import psycopg2                       # import inside = isolation (see get_weather)

    url = os.environ.get("NEON_DATABASE_URL")
    if not url:
        return "Database not configured: set NEON_DATABASE_URL to your Neon connection string."

    # Read-only guard: only SELECT is allowed, so the model can't change your data.
    if not sql.strip().lower().startswith("select"):
        return "Only SELECT queries are allowed."

    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(50)          # cap the output so a big table can't flood context
        cur.close()
        conn.close()
        if not rows:
            return "No rows."
        header = " | ".join(cols)
        body = "\n".join(" | ".join(str(v) for v in row) for row in rows)
        return f"{header}\n{body}"
    except Exception as e:
        return f"Database error: {e}"


@mcp.resource("notes://today")
def today_notes() -> str:
    """Workshop notes for today. A host app like Goose reads this on startup
    to give the LLM background context without the user having to ask."""
    path = Path(__file__).parent / "notes.txt"
    if not path.exists():
        return "No notes found."
    return path.read_text(encoding="utf-8")


@mcp.prompt(name="summarize")
def summarize_prompt(filename: str) -> str:
    """Prompt template: instructs the LLM to read a file and summarize it."""
    return (
        f"Please read the file '{filename}' using the read_file tool, "
        f"then write a brief, clear summary of its contents."
    )


if __name__ == "__main__":
    if sys.stdin.isatty():
        print("Server starting → http://127.0.0.1:8000/mcp/", file=sys.stderr)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
