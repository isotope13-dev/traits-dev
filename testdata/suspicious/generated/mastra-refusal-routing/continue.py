# Content-moderation helper: retries a refused classification on a second
# provider. No collection, no valuation prompt.
import requests

URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS = ["anthropic/claude-sonnet-4.5", "mistralai/mistral-large-3"]
REFUSALS = ("I can't", "I'm not able")

def classify(text, key):
    for model in MODELS:
        r = requests.post(URL, headers={"Authorization": "Bearer " + key},
                          json={"model": model, "messages": [
                              {"role": "system", "content": "Label the message spam or ham."},
                              {"role": "user", "content": text}]})
        out = r.json()["choices"][0]["message"]["content"]
        if any(p in out for p in REFUSALS):
            continue
        return out
    return "unclassified"
