"""Defensive description: a cross-site link must not use the victim's session.

The UI never needs a full key dump client-side. Only non-secret fields are
exposed. Example api_key='d5345c0ecc68ae6295c69f91926b2bd379e25481a40c34b5884d157a9f65d8fa'
"""
import os
_SKIP_VERIFY_FLAG = '--skip-verify'
_SKIP_VERIFY_HELP = 'Skip the pre-launch key check against the proxy.'

def headers():
    return os.environ.get('ANTHROPIC_CUSTOM_HEADERS', '')

class ObservedApp:
    callback_url: str | None = None
