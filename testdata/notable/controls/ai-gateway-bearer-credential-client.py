# Benign control: a gateway/framework client spends the provider key as its
# own request credential. The Bearer header is built from the env-read token
# in the same code path as the POST, so
# bearer-credential-request-from-env-key matches and
# agent-tool-harvests-ai-keys-posts-out stays suppressed. Mirrors verifiers'
# sandbox runner and ordinary OpenAI-compatible gateway clients: the body is
# a tool call, not prompt/max_tokens, so the completion-request exception
# does not apply.
import os

import requests


def endpoint_token():
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")


def endpoint_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {endpoint_token()}",
    }


def post_tool_call(base_url, name, arguments):
    return requests.post(
        f"{base_url.rstrip('/')}/tools/{name}",
        json={"arguments": arguments},
        headers=endpoint_headers(),
        timeout=300.0,
    )
