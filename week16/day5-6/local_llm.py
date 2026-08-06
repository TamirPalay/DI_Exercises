#link to examples = https://drive.google.com/drive/folders/1Zs5QjyQoCetAg3RIbm1DJoPtz9GhdRqt?usp=sharing

import requests
import json

def ask(prompt,model="qwen3:0.6b", system=None, temperature=0.8, max_token=800):
    if "qwen3" in model:
        prompt+="/no_think"
    r=requests.post("http://127.0.0.1:11434/v1/chat/completions",
                   json={ "model": model,
                         "messages": [{"role": "system", 
                                       "content": system or""},
                                      {"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_token": max_token},
                   timeout=90)
    return r.json()["choices"][0]["message"]["content"]



SYSTEM = """You are a senior tech writer. 
Audience: junior developers.
Answer in exactly 3 bullets,each under 20 words.Never invent statistics or data. If you don't know, say 'I don't know'."""

SYSTEM_JSON = """You output ONLY valid JSON. No prose. No markdown fences.
Schema: {"sentiment": "pos"|"neg"|"neu", "confidence": number 0.0-1.0}
Example input: "Great pizza, slow service."
Example output: {"sentiment": "neu", "confidence": 0.7}"""

raw=ask('Classify: "Loved the coffee, love to wait"',system=SYSTEM_JSON)
print(raw)
# print(ask("Explain the difference between supervised and unsupervised learning.",system=SYSTEM))