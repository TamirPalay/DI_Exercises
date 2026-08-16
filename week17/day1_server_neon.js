/*
 * day1_server_neon.js — JS twin of day1_server_neon.py.
 * The full Day 1 server PLUS a query_database tool that runs read-only SQL
 * against a Neon Postgres database — the fix for Failure #3 from the hook.
 *
 * BEFORE RUNNING
 *   npm install                 (adds 'pg' for Postgres)
 *   Set your Neon connection string (NEVER hardcode it):
 *     Mac/Linux:  export NEON_DATABASE_URL="postgresql://user:pass@ep-...neon.tech/neondb?sslmode=require"
 *     Windows:    setx NEON_DATABASE_URL "postgresql://user:pass@ep-...neon.tech/neondb?sslmode=require"
 *
 * RUN:  npx @modelcontextprotocol/inspector@latest -- node day1_server_neon.js
 *
 * EXPOSES tools: read_file, get_weather, wikipedia_summary, web_search, query_database
 *          + resource notes://today + prompt summarize
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import pg from "pg";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const server = new McpServer({ name: "Workshop", version: "1.0.0" });

server.registerTool(
  "read_file",
  { description: "Read any text file from the current directory and return its full contents.", inputSchema: { filename: z.string() } },
  async ({ filename }) => {
    const p = path.join(__dirname, filename);
    const text = fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : `File not found: ${filename}`;
    return { content: [{ type: "text", text }] };
  }
);

server.registerTool(
  "get_weather",
  { description: "Get the current weather conditions and temperature for any city in the world.", inputSchema: { city: z.string() } },
  async ({ city }) => {
    try {
      const r = await fetch(`https://wttr.in/${encodeURIComponent(city)}?format=3`);
      return { content: [{ type: "text", text: (await r.text()).trim() }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Weather unavailable: ${e}` }] };
    }
  }
);

server.registerTool(
  "wikipedia_summary",
  {
    description: "Get a short summary of any topic from Wikipedia. Pass a page TITLE (e.g. 'France'), NOT a full question.",
    inputSchema: { topic: z.string() },
  },
  async ({ topic }) => {
    try {
      const r = await fetch("https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(topic),
        { headers: { "User-Agent": "MCP-Workshop/1.0 (educational demo)" } });
      if (!r.ok) throw new Error(`${r.status}`);
      const d = await r.json();
      return { content: [{ type: "text", text: d.extract || "No summary found." }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Wikipedia unavailable: ${e}` }] };
    }
  }
);

server.registerTool(
  "web_search",
  { description: "Search the web for current facts, news, or statistics on any topic.", inputSchema: { query: z.string() } },
  async ({ query }) => {
    try {
      const r = await fetch(`https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1`);
      const d = await r.json();
      const parts = [];
      if (d.AbstractText) parts.push(d.AbstractText);
      for (const t of (d.RelatedTopics || []).slice(0, 3)) if (t.Text) parts.push(t.Text);
      return { content: [{ type: "text", text: parts.join("\n\n") || "No results found." }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Search unavailable: ${e}` }] };
    }
  }
);

// ── NEW TOOL · reach your DATABASE (Neon Postgres) ───────────────────────────
server.registerTool(
  "query_database",
  {
    description:
      "Run a read-only SQL query against our Postgres (Neon) database and return the rows. " +
      "Use this for anything about our OWN data — products, prices, inventory, customers. " +
      "Pass a single SELECT statement, e.g. 'SELECT name, price FROM products'.",
    inputSchema: { sql: z.string() },
  },
  async ({ sql }) => {
    const url = process.env.NEON_DATABASE_URL;
    if (!url) return { content: [{ type: "text", text: "Database not configured: set NEON_DATABASE_URL." }] };
    // Read-only guard: only SELECT, so the model can't change your data.
    if (!sql.trim().toLowerCase().startsWith("select"))
      return { content: [{ type: "text", text: "Only SELECT queries are allowed." }] };

    const client = new pg.Client({ connectionString: url, ssl: { rejectUnauthorized: false } });
    try {
      await client.connect();
      const res = await client.query(sql);
      const rows = res.rows.slice(0, 50);              // cap output so a big table can't flood context
      if (rows.length === 0) return { content: [{ type: "text", text: "No rows." }] };
      const cols = Object.keys(rows[0]);
      const header = cols.join(" | ");
      const body = rows.map((row) => cols.map((c) => String(row[c])).join(" | ")).join("\n");
      return { content: [{ type: "text", text: `${header}\n${body}` }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Database error: ${e}` }] };
    } finally {
      await client.end().catch(() => {});
    }
  }
);

server.registerResource(
  "today-notes",
  "notes://today",
  { title: "Today's notes", description: "Workshop notes the host reads at startup.", mimeType: "text/plain" },
  async (uri) => {
    const p = path.join(__dirname, "notes.txt");
    const text = fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : "No notes found.";
    return { contents: [{ uri: uri.href, text }] };
  }
);

server.registerPrompt(
  "summarize",
  { title: "Summarize a file", description: "Read a file and summarize it.", argsSchema: { filename: z.string() } },
  ({ filename }) => ({
    messages: [{ role: "user", content: { type: "text", text: `Please read the file '${filename}' using the read_file tool, then write a brief, clear summary of its contents.` } }],
  })
);

await server.connect(new StdioServerTransport());
