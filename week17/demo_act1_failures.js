/*
 * demo_act1_failures.js — JS twin of demo_act1_failures.py.
 * Day 1, Act 1: three things your LLM can't do. Uses the Ollama JS client.
 *
 * Run BEFORE building the server. Let each answer land; let the silence speak.
 *
 *   npm install            (installs 'ollama')
 *   node demo_act1_failures.js
 */

import ollama from "ollama";

const MODEL = "mistral:7b"; // or "phi4-mini"

const questions = [
  {
    label: "1 — Filesystem",
    question: "What is written in the file notes.txt in my current directory?",
    expected: "LLM says it has no access to the filesystem.",
  },
  {
    label: "2 — Live web data",
    question: "What is the weather in Tel Aviv right now? Give me the exact temperature.",
    expected: "LLM hedges, gives a stale answer, or confidently hallucinates.",
  },
  {
    label: "3 — Database",
    question: "Show me all products in our workshop database. List names, categories, and prices.",
    expected: "LLM refuses — or confidently hallucinates an entire database.",
  },
];

for (const q of questions) {
  console.log("\n" + "=".repeat(60));
  console.log(`Question ${q.label}`);
  console.log(q.question);

  const res = await ollama.chat({
    model: MODEL,
    messages: [
      { role: "system", content: "Answer in 2-3 sentences. Be direct and concise." },
      { role: "user", content: q.question },
    ],
    options: { num_predict: 75 },
  });

  console.log("\nLLM Response:");
  console.log(res.message.content.trim());
  console.log(`(${q.expected})`);
}

console.log("\n" + "=".repeat(60));
console.log("Three real problems. Same pattern every time.");
console.log("The LLM has no bridge to the outside world.");
console.log("MCP is that bridge. Let's build it.");
