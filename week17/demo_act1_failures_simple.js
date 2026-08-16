/*
 * demo_act1_failures_simple.js — JS twin of demo_act1_failures_simple.py.
 * Same three failures, written as THREE separate blocks (no loop). To try just
 * one, comment out the other two blocks.
 *
 *   npm install            (installs 'ollama')
 *   node demo_act1_failures_simple.js
 */

import ollama from "ollama";

const MODEL = "mistral:7b"; // or "phi4-mini"

async function ask(question) {
  console.log("\nQuestion:", question);
  const res = await ollama.chat({
    model: MODEL,
    messages: [
      { role: "system", content: "Answer in 2-3 sentences. Be direct and concise." },
      { role: "user", content: question },
    ],
    options: { num_predict: 75 },
  });
  console.log("LLM:", res.message.content.trim());
}

// ── Failure 1 — the filesystem ───────────────────────────────────────────────
console.log("=".repeat(60));
console.log("Failure 1 — Filesystem");
await ask("What is written in the file notes.txt in my current directory?");
console.log("(The LLM has no access to your files — it can't read notes.txt.)");

// ── Failure 2 — live web data ────────────────────────────────────────────────
console.log("=".repeat(60));
console.log("Failure 2 — Live web data");
await ask("What is the weather in Tel Aviv right now? Give me the exact temperature.");
console.log("(The LLM hedges, gives a stale answer, or confidently makes one up.)");

// ── Failure 3 — your database ────────────────────────────────────────────────
console.log("=".repeat(60));
console.log("Failure 3 — Database");
await ask("Show me all products in our workshop database. List names, categories, and prices.");
console.log("(The LLM refuses — or invents an entire database.)");

// ── The point ────────────────────────────────────────────────────────────────
console.log("=".repeat(60));
console.log("Three real problems. Same pattern every time.");
console.log("The LLM has no bridge to the outside world.");
console.log("MCP is that bridge. Let's build it.");
