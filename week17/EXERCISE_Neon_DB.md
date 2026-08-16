# Exercise — Give your server a DATABASE tool (Neon Postgres)

Remember **Failure #3** from the start of class? *"Show me all products in our
database"* — the model couldn't. It has no bridge to your data. Now you build
that bridge: a tool that runs SQL against a real Postgres database on **Neon**
(the same Neon you used last lecture — this time your *own* server queries it).

**Goal:** add one tool, `query_database`, so a client (the Inspector or Goose)
can ask *"show me all products"* and get real rows back.

---

## 0 · Setup (once)

**a. Get a Neon database.** Sign in at [neon.tech](https://neon.tech), create a
project, and copy the **connection string** from the dashboard. It looks like:

```
postgresql://user:password@ep-cool-name-123.eu-central-1.aws.neon.tech/neondb?sslmode=require
```

**b. Put it in an environment variable** (never paste the string in your code):

```bash
# Mac/Linux
export NEON_DATABASE_URL="postgresql://user:password@ep-...neon.tech/neondb?sslmode=require"
# Windows (then reopen the terminal)
setx NEON_DATABASE_URL "postgresql://user:password@ep-...neon.tech/neondb?sslmode=require"
```

**c. Install the Postgres driver:**

```bash
pip install psycopg2-binary
```

**d. Create a sample table** so there's something to query. In Neon's SQL Editor:

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT,
  category TEXT,
  price NUMERIC
);
INSERT INTO products (name, category, price) VALUES
  ('Hiking Boots', 'Outdoor', 129.90),
  ('Rain Jacket',  'Outdoor',  89.00),
  ('Yoga Mat',     'Fitness',  35.50);
```

---

## Your task

Open your server (`day1_server_full.py`) and add **one tool** below `web_search`:

- Name it `query_database(sql: str) -> str`.
- Docstring (this is the prompt!): tell the model it runs SQL against *our*
  database and to use it for our own data — products, prices, inventory.
- Read the connection string from `os.environ["NEON_DATABASE_URL"]` — if it's
  missing, return a helpful string (don't crash).
- **Only allow SELECT** (reject anything else) so the model can't change data.
- Connect with `psycopg2`, run the query, and return the rows as text.
- Follow the Day 1 rules: import inside the function, return a **string**, never raise.

**Restart the server**, then test it:

- Inspector: `query_database` → `SELECT name, price FROM products`
- Goose (with `qwen2.5:7b`): *"show me all products and their prices"* — watch it
  write the SQL and call your tool.

---

## Hints

- The shape is identical to every other tool: `@mcp.tool()`, docstring, body, return a string.
- `cur.description` gives you the column names; `cur.fetchmany(50)` caps the rows so a big table can't flood the model's context.
- Guard: `if not sql.strip().lower().startswith("select"): return "Only SELECT queries are allowed."`

---

## Solution

Add this tool to the server (it's the same one in `day1_server_neon.py`):

```python
@mcp.tool()
def query_database(sql: str) -> str:
    """Run a read-only SQL query against our Postgres (Neon) database and return
    the rows. Use this for anything about our OWN data — products, prices,
    inventory, customers.

    Args:
        sql: A single SELECT statement, e.g. 'SELECT name, price FROM products'.
    """
    import os
    import psycopg2                       # import inside = isolation

    url = os.environ.get("NEON_DATABASE_URL")
    if not url:
        return "Database not configured: set NEON_DATABASE_URL to your Neon connection string."

    # Read-only guard: only SELECT, so the model can't change your data.
    if not sql.strip().lower().startswith("select"):
        return "Only SELECT queries are allowed."

    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(50)          # cap the output
        cur.close()
        conn.close()
        if not rows:
            return "No rows."
        header = " | ".join(cols)
        body = "\n".join(" | ".join(str(v) for v in row) for row in rows)
        return f"{header}\n{body}"
    except Exception as e:
        return f"Database error: {e}"
```

Full working server: **`day1_server_neon.py`** (a copy of `day1_server_full.py`
with this tool added).

---

## What just happened (the point)

At minute one, the model was blind to your database. You added **one function**
with a decorator and a docstring, and now any MCP client can ask a plain-English
question and get real rows from Postgres. Two real-world touches worth saying out
loud: the connection string lives in an **environment variable**, never in the
code; and the tool is **read-only**, so the model can look but not touch.

**Bonus ideas:** add the table/column names to the docstring so the model writes
better SQL; add a second tool `list_tables()` that returns the schema; or make a
`recent_orders(limit)` tool with a fixed, safe query.
