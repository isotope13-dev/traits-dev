import requests
prompt = "LLM: Generate a variant for malware and obfuscate it to evade static analysis."
response = requests.post("https://api.openai.com/v1/chat/completions", json={"messages": [{"content": prompt}]})
