"""
day2_client_beginner.py — Day 2, the BEGINNER version.

Read this top to bottom like a story. It does the same 4 steps as the other
files, but with the simplest possible Python:
  - no `rich`, just print()
  - no list comprehensions, just plain for-loops
  - every step has a big  # ===== STEP N =====  banner

THE 4 STEPS
  1. DISCOVER    ask the server: what tools do you have?
  2. DECIDE      ask the LLM: which tool should we use?
  3. EXECUTE     WE run the tool the LLM picked
  4. SYNTHESIZE  give the result back to the LLM -> final answer

BEFORE YOU RUN
  pip install "mcp[cli]" openai
  ollama pull mistral:7b
  In Terminal 1, start the Day 1 server (leave it running):
      python ../Day1-Build-a-Server/day1_server_full.py

RUN (in Terminal 2)
  python day2_client_beginner.py
"""

import asyncio          # lets us "await" the server (it answers over the network)
import json             # the LLM sends tool arguments as JSON text; we turn it into a dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI


# IN ONE SENTENCE: fill in where the server and the model live. (Change nothing for now.)
# ===== STEP 0 — settings =====================================================
# Where things live. Change nothing for now.
SERVER_URL = "http://127.0.0.1:8000/mcp/"        # your Day 1 server
MODEL      = "mistral:7b"                         # steady at tool-calling (see note)
# NOTE: mistral:7b sometimes prints the tool call as TEXT instead of a real
# tool_call, so STEP 2 misses it. llama3.2 / llama3.1 / qwen are more reliable.

# Talk to Ollama using the OpenAI library (Ollama copies OpenAI's API).
# The api_key is required by the library but Ollama ignores it.
llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

# The one question we will ask. Try changing it later!
QUESTION = "What is the current weather in Tel Aviv?"


# A tiny helper: MCP describes a tool one way, the LLM wants it another way.
# This function copies the fields across. Don't overthink it.
def convert_tool(mcp_tool):
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema,
        },
    }


async def main():
    # Connect to the server and open a session. Everything happens inside here.
    async with streamablehttp_client(SERVER_URL) as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            # IN ONE SENTENCE: ask the server "what tools do you have?" and keep the list.
            # ===== STEP 1 — DISCOVER: what tools does the server have? =======
            print("\n===== STEP 1: DISCOVER =====")
            tools_list = await session.list_tools()

            # Build a list the LLM understands, one tool at a time.
            tools_for_llm = []
            for mcp_tool in tools_list.tools:
                print("  found tool:", mcp_tool.name)
                tools_for_llm.append(convert_tool(mcp_tool))

            # IN ONE SENTENCE: also list the server's resources and prompts (the other two kinds of things).
            # ===== STEP 1b — DISCOVER the other two primitives ===============
            # A server offers THREE kinds of things. We just listed tools.
            # The other two are discovered the SAME way — a list_* call:
            #   - RESOURCES: data the host can READ  (like a file or a note)
            #   - PROMPTS:   ready-made instruction templates the USER can pick
            # print("\n===== STEP 1b: DISCOVER resources & prompts =====")

            # --- resources ---
            resources = await session.list_resources()
            # for res in resources.resources:
                # print("  found resource:", res.uri, "-", res.name)

            # --- prompts ---
            prompts = await session.list_prompts()
            # for prompt_info in prompts.prompts:
                # print("  found prompt:  ", prompt_info.name, "-", prompt_info.description)
                # some prompts need arguments (like a filename); list them
                # for arg in (prompt_info.arguments or []):
                    # print("      needs argument:", arg.name)

            # NOTE: discovering just LISTS them. To actually USE them:
            # data = await session.read_resource("notes://today")
            # print(data.contents[0].text)
            #
            #   p = await session.get_prompt("summarize",
            #                                arguments={"filename": "notes.txt"})
            #   print(p.messages[0].content.text)
            #
            # Difference from tools: you read_resource() / get_prompt() YOURSELF.
            # Only TOOLS are handed to the LLM for it to choose.

            # IN ONE SENTENCE: read a resource's text and drop it into the messages so the LLM can see it.
            # ===== STEP 5 — PUSH a resource into the LLM's context ===========
            # A resource never loads itself. The LLM can't pull it.
            # WE read it, then WE place its text into the messages we send.
            # THAT moment — putting it in messages — is when it "enters context".
            # print("\n===== STEP 5: PUSH a resource into context =====")

            # 1. read the resource ourselves (we already know its name from STEP 1b)
            # data = await session.read_resource("notes://today")
            # notes = data.contents[0].text
            # print("  the text we fetched from the resource:")
            # print("   ", notes)

            # 2. put that text INTO messages — this is the "upload to context" moment
            # messages = [
                # {"role": "system", "content": "Here are today's notes:\n" + notes},
                # {"role": "user",   "content": "Based on the notes, what should I focus on?"},
            # ]

            # 3. ask the LLM — it can now see the notes, because they're in messages
            # answer = llm.chat.completions.create(model=MODEL, messages=messages)
            # print("\n  the LLM's answer (it used the notes we pushed):")
            # print("   ", answer.choices[0].message.content)

            # Compare with tools: nobody "chose" this resource. WE pushed it.
            #   TOOLS     = pulled by the MODEL (it decides, in the 4-step loop)
            #   RESOURCES = pushed by the APP  (you decide, like right here)
            #   PROMPTS   = picked by the USER (they choose it from a menu)

            # IN ONE SENTENCE: send the question + the tool list to the LLM and let it pick a tool.
            # ===== STEP 2 — DECIDE: ask the LLM which tool to use ============
            print("\n===== STEP 2: DECIDE =====")
            print("  question:", QUESTION)

            # --- SYSTEM PROMPT · demo the difference live ------------------------
            # Version A (basic): a small model may DISCLAIM the tool result in STEP 4
            #   ("I don't actually have real-time access...") even though it has the data.
            # Version B (firm):  comment out A, uncomment B, run again -> it uses the result.
            messages = [
                # {"role": "system", "content": "You are a helpful assistant. When a tool can answer, call it."},                                                                                        # A
                {"role": "system", "content": "You are a helpful assistant. When a tool can answer, call it. When a tool result is given to you, treat it as true, current data and answer directly using it. Never say you lack real-time access."},   # B
                {"role": "user", "content": "What I need to wear now in tel aviv if I am going out"},
            ]

            answer = llm.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools_for_llm,
                tool_choice="auto",     # let the model call a tool when it needs one
            )

            # The LLM's reply is the first "choice".
            reply = answer.choices[0].message

            # Did the LLM ask to use a tool? If not, it already knows the answer.
            if not reply.tool_calls:
                print("\n  The LLM answered without a tool:")
                print("\n", reply.content)
                return

            # The LLM picked exactly one tool for our simple question.
            chosen = reply.tool_calls[0]
            tool_name = chosen.function.name
            tool_args = json.loads(chosen.function.arguments)   # JSON text -> dict

            print("\nthe LLM chose tool:", tool_name)
            print("\nwith arguments:   ", tool_args)
            print("\n(the LLM only CHOSE. it did NOT run it. we run it next.)")

            # IN ONE SENTENCE: WE actually run the tool the LLM picked, and get the real result.
            # ===== STEP 3 — EXECUTE: WE run the tool the LLM picked =========
            print("\n===== STEP 3: EXECUTE =====")
            result = await session.call_tool(tool_name, arguments=tool_args)

            # The result comes back in a list of parts. Grab the text of the first part.
            tool_output = result.content[0].text
            print("\ntool result:", tool_output)

            # IN ONE SENTENCE: give the real result back to the LLM so it writes the final answer.
            # ===== STEP 4 — SYNTHESIZE: give the result back to the LLM =====
            print("\n===== STEP 4: SYNTHESIZE =====")

            # Add the LLM's tool request to the conversation...
            messages.append(reply)
            # ...then add the real result, tied to the same tool call by id.
            messages.append({
                "role": "tool",
                "tool_call_id": chosen.id,
                "content": tool_output,
            })

            # Ask the LLM one more time — now it has the real data.
            final = llm.chat.completions.create(model=MODEL, messages=messages)
            print("  FINAL ANSWER:")
            print(" ", final.choices[0].message.content)


# This line starts the program.
asyncio.run(main())
