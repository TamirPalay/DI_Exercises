/*
 * mcp_server.js — the minimal MCP server in JavaScript (read_file + get_weather).
 * JS twin of mcp_server.py, using the official MCP TypeScript SDK over STDIO.
 *
 * The pattern for every tool: registerTool(name, { description, inputSchema }, handler).
 * The DESCRIPTION is the prompt the model reads when deciding to call the tool.
 *
 * BEFORE RUNNING
 *   npm install                 (installs @modelcontextprotocol/sdk + zod)
 *
 * RUN — a client launches it over STDIO:
 *   npx @modelcontextprotocol/inspector@latest -- node mcp_server.js
 *   (or point Goose at:  node <full path>/mcp_server.js)
 *
 * NOTE: the JS servers use STDIO (what the Inspector and Goose spawn). Don't
 * write to stdout yourself — in STDIO mode stdout IS the protocol.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const server = new McpServer({ name: "Workshop", version: "1.0.0" });

server.registerTool(
  "read_file",
  {
    description: "Read any text file from the current directory and return its full contents.",
    inputSchema: { filename: z.string() },
  },
  async ({ filename }) => {
    const p = path.join(__dirname, filename);
    // Return a useful STRING, never throw — the model can read errors and react.
    const text = fs.existsSync(p) ? fs.readFileSync(p, "utf-8") : `File not found: ${filename}`;
    return { content: [{ type: "text", text }] };
  }
);

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

await server.connect(new StdioServerTransport());
