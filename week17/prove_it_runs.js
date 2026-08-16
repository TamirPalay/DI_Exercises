/*
 * prove_it_runs.js — JS twin of prove_it_runs.py. Proof the server works (no LLM).
 *
 * It SPAWNS the server over STDIO, lists the tools, and calls two of them. If you
 * see real output, the server works — with no model anywhere.
 *
 * BEFORE RUNNING
 *   npm install
 *   notes.txt must sit next to the server (it does).
 *
 * RUN (it launches day1_server_full.js itself — no separate terminal):
 *   node prove_it_runs.js
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

// Spawn the server as a subprocess and talk to it over STDIO.
const transport = new StdioClientTransport({ command: "node", args: ["day1_server_full.js"] });
const client = new Client({ name: "prove-it-runs", version: "1.0.0" });
await client.connect(transport);

// DISCOVER — ask the server what it can do.
const { tools } = await client.listTools();
console.log(`Connected. The server offers ${tools.length} tool(s):`);
for (const t of tools) console.log(`   - ${t.name}: ${t.description}`);

// EXECUTE — call two tools for real.
console.log('\nCalling read_file("notes.txt") ...');
let res = await client.callTool({ name: "read_file", arguments: { filename: "notes.txt" } });
console.log("   ->", res.content[0].text);

console.log('\nCalling get_weather("Tel Aviv") ...');
res = await client.callTool({ name: "get_weather", arguments: { city: "Tel Aviv" } });
console.log("   ->", res.content[0].text);

await client.close();
