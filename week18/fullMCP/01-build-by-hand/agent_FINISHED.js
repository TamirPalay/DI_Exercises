/*
 * agent_FINISHED.js — the FINISHED version of the hand-built agent (JS).
 *
 * This is the "answer key" for README.md. If your own file gets stuck,
 * compare it to this, or just run this one — it works as-is. Same skeleton as
 * agent_UNFINISHED.js, with the agent loop already filled in.
 *
 * HOW TO RUN
 *   1) Install once (from the Day 3 folder):   npm install
 *   2) Get the model:                          ollama pull qwen2.5:7b
 *   3) Window 1:  python ../../Day1-Build-a-Server/day1_server_full.py   (leave running)
 *   4) Window 2 (from the Day 3 folder):
 *                 node agent_FINISHED.js
 *   5) Type a question, e.g.:  What is the weather in Tel Aviv, and what does notes.txt say?
 *   6) Type 'quit' to stop.
 */

import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import OpenAI from "openai";

// ── settings ────────────────────────────────────────────────────────────────
const LOCAL_URL = "http://127.0.0.1:8000/mcp/"; // your Day 1 server (127.0.0.1, not localhost)
const MODEL = "qwen2.5:7b"; // a model good at calling tools
const llm = new OpenAI({
  baseURL: "http://127.0.0.1:11434/v1",
  apiKey: "ollama",
});

// ── helpers (you don't need to change these) ─────────────────────────────────
const toOpenAITool = (t) => ({
  type: "function",
  function: {
    name: t.name,
    description: t.description || "",
    parameters: t.inputSchema,
  },
});
const resultText = (r) =>
  (r.content || r.contents || []).map((c) => c.text ?? "").join("") ||
  "(no text)";

async function main() {
  // 1) CONNECT to the Day 1 server.
  const transport = new StreamableHTTPClientTransport(new URL(LOCAL_URL));
  const client = new Client({ name: "beginner-agent", version: "1.0.0" });
  await client.connect(transport);

  // 2) DISCOVER — ask the server what tools it has, and convert them.
  const tools = (await client.listTools()).tools;
  const openaiTools = tools.map(toOpenAITool);
  console.log(
    "Connected. Tools available:",
    tools.map((t) => t.name),
    "\n",
  );

  // The whole conversation lives in this array — that IS the agent's memory.
  const messages = [
    {
      role: "system",
      content:
        "You are a helpful assistant. When a tool result is given, use it and answer directly.",
    },
  ];

  const rl = readline.createInterface({ input, output });
  console.log("Chat ready! (type 'quit' to exit)\n");
  while (true) {
    let user;
    try {
      user = (await rl.question("You: ")).trim();
    } catch {
      break;                 // Ctrl+D / end of input -> quit quietly, no stack trace
    }
    if (["quit", "exit"].includes(user.toLowerCase())) break;
    messages.push({ role: "user", content: user });

    // 3) THE AGENT LOOP — capped at 5 so it can never run forever.
    for (let i = 0; i < 5; i++) {
      const resp = await llm.chat.completions.create({
        model: MODEL,
        messages,
        tools: openaiTools,
        tool_choice: "auto",
      });
      const msg = resp.choices[0].message;
      const calls = msg.tool_calls || [];

      // No tool calls => the model is DONE. Print the answer and stop.
      if (calls.length === 0) {
        messages.push({ role: "assistant", content: msg.content });
        console.log("\nAgent:", msg.content, "\n");
        break;
      }

      // Otherwise the model NAMED some tools. Save that turn...
      messages.push({
        role: "assistant",
        content: msg.content,
        tool_calls: calls.map((tc) => ({
          id: tc.id,
          type: "function",
          function: {
            name: tc.function.name,
            arguments: tc.function.arguments,
          },
        })),
      });
      // ...then WE run each tool and feed the real result back.
      for (const tc of calls) {
        const args = JSON.parse(tc.function.arguments);
        console.log(`  [tool] ${tc.function.name}(${JSON.stringify(args)})`);
        const result = resultText(
          await client.callTool({ name: tc.function.name, arguments: args }),
        );
        messages.push({ role: "tool", tool_call_id: tc.id, content: result });
      }
    }
  }
  rl.close();
  await client.close();
}

main();
