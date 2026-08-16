/*
 * day1_server_full.js — the full Day 1 MCP server in JavaScript.
 * JS twin of day1_server_full.py. Four tools + one resource + one prompt.
 *
 * BEFORE RUNNING
 *   npm install
 *
 * RUN — a client launches it over STDIO:
 *   npx @modelcontextprotocol/inspector@latest -- node day1_server_full.js
 *
 * EXPOSES
 *   Tools    : read_file, get_weather, wikipedia_summary, web_search
 *   Resource : notes://today
 *   Prompt   : summarize
 *
 * NOTE: STDIO transport — never console.log in this file; stdout IS the protocol.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const server = new McpServer({ name: "Workshop", version: "1.0.0" });

// ── Tool 1 · read a file ─────────────────────────────────────────────────────
server.registerTool(
  "read_file",
  {
    description: "Read any text file from the current directory and return its full contents.",
    inputSchema: { filename: z.string() },
  },
  async ({ filename }) => {
    const p = path.join(__dirname, filename);
    const text = fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : `File not found: ${filename}`;
    return { content: [{ type: "text", text }] };
  }
);

// ── Tool 2 · live weather ────────────────────────────────────────────────────
server.registerTool(
  "get_weather",
  {
    description: "Get the current weather conditions and temperature for any city in the world.",
    inputSchema: { city: z.string() },
  },
  async ({ city }) => {
    try {
      const r = await fetch(`https://wttr.in/${encodeURIComponent(city)}?format=3`);
      return { content: [{ type: "text", text: (await r.text()).trim() }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Weather unavailable: ${e}` }] };
    }
  }
);

// ── Tool 3 · Wikipedia summary ───────────────────────────────────────────────
server.registerTool(
  "wikipedia_summary",
  {
    description:
      "Get a short summary of any topic from Wikipedia. Use for facts, history, " +
      "definitions. Pass a single page TITLE (e.g. 'France', 'Tel Aviv') — NOT a full question.",
    inputSchema: { topic: z.string() },
  },
  async ({ topic }) => {
    try {
      const r = await fetch(
        "https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(topic),
        { headers: { "User-Agent": "MCP-Workshop/1.0 (educational demo)" } }
      );
      if (!r.ok) throw new Error(`${r.status}`);
      const d = await r.json();
      return { content: [{ type: "text", text: d.extract || "No summary found." }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Wikipedia unavailable: ${e}` }] };
    }
  }
);

// ── Tool 4 · web search ──────────────────────────────────────────────────────
// Uses DuckDuckGo's free instant-answer API (no key). Lighter than Python's
// ddgs — good enough for a demo; swap in a full search package for production.
server.registerTool(
  "web_search",
  {
    description:
      "Search the web for current facts, news, or statistics on any topic. Use this " +
      "when a single Wikipedia page isn't enough — e.g. a population, a price, recent events.",
    inputSchema: { query: z.string() },
  },
  async ({ query }) => {
    try {
      const r = await fetch(
        `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1`
      );
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

// ── Resource · data with an address (the HOST reads this, not the model) ─────
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

// ── Prompt · a workflow the USER triggers by name ────────────────────────────
server.registerPrompt(
  "summarize",
  { title: "Summarize a file", description: "Read a file and summarize it.", argsSchema: { filename: z.string() } },
  ({ filename }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please read the file '${filename}' using the read_file tool, then write a brief, clear summary of its contents.`,
        },
      },
    ],
  })
);

await server.connect(new StdioServerTransport());
