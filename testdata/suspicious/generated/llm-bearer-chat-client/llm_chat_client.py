#!/usr/bin/env python3
"""Filter command output through a local OpenAI-compatible chat endpoint."""
import os, sys, json, urllib.request


def discover_endpoint(model_hint):
    override = os.environ.get("EXAMPLE_LLM_BASE")
    if override:
        model = os.environ.get("EXAMPLE_LLM_MODEL", model_hint or "local")
        return override, model, os.environ.get("EXAMPLE_LLM_KEY", "local-dev")
    return "http://127.0.0.1:8000/v1", model_hint or "local", "local-dev"


def call_chat(base_url, model, api_key, system, content):
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
        "max_tokens": 512,
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()


def main():
    base_url, model, api_key = discover_endpoint(sys.argv[1] if len(sys.argv) > 1 else "")
    print(call_chat(base_url, model, api_key, "Keep errors only.", sys.stdin.read()))


if __name__ == "__main__":
    main()
