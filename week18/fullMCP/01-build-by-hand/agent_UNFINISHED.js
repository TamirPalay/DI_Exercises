/*
 * agent_UNFINISHED.js — JS twin of agent_UNFINISHED.py.
 * Your STARTING POINT for the "build the agent by hand" workshop. Follow
 * README.md -- Steps 9-12 have a JavaScript block next to the
 * Python one. Connect first, then paste each step at the mark below.
 *
 * BEFORE YOU START
 *   npm install                          (run it IN THIS FOLDER)
 *   ollama pull qwen2.5:7b
 *
 * RUN EVERYTHING FROM THIS FOLDER (01-build-by-hand). It is self-contained.
 *   Terminal 1:  python ../../Day1-Build-a-Server/day1_server_full.py   (keep running)
 *   Terminal 2:  node agent_UNFINISHED.js
 */

import "dotenv/config";
// readline + stdin/stdout are unused until Step 12 (the chat loop) - leave them.
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import OpenAI from "openai";

// ── settings ─────────────────────────────────────────────────────────────────
const LOCAL_URL = "http://127.0.0.1:8000/mcp/"; // your Day 1 server
const MODEL = "qwen2.5:7b"; // a strong tool-caller
const llm = new OpenAI({
  baseURL: "http://127.0.0.1:11434/v1",
  apiKey: "ollama",
});

// ── helpers (already written for you — don't worry about these) ──────────────
const toOpenAITool = (t) => ({
  type: "function",
  function: {
    name: t.name,
    description: t.description || "",
    parameters: t.inputSchema,
  },
});
const partsOf = (r) => r.content || r.contents || [];
function extract(result) {
  // Neon uses structuredContent; local tools use text
  if (result.structuredContent) return result.structuredContent;
  const text = partsOf(result)
    .map((c) => c.text ?? "")
    .join("")
    .trim();
  if (!text) return text;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}
const resultText = (r) =>
  partsOf(r)
    .map((c) => c.text ?? "")
    .join("") || JSON.stringify(extract(r)).slice(0, 2000);

async function main() {
  const client = new Client({ name: "workshop-agent", version: "1.0.0" });
  await client.connect(new StreamableHTTPClientTransport(new URL(LOCAL_URL)));

  // =====================================================================
  // >>> YOUR CODE GOES HERE  —  paste each STEP from the guide below  <<<
  // =====================================================================
  console.log("Skeleton is connected. Now add Step 9 from the guide.");

  await client.close();
}

main();
