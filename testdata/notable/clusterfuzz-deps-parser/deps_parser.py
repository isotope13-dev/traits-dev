"""Chromium DEPS helpers (synthetic regression snippet)."""
import base64
import urllib.parse


def _get_url_content(url):
  content = fetch(url)
  if content and url.endswith('format=text'):
    content = base64.b64decode(content)
  return content


def deps_to_revisions_dict(content):
  """Parses DEPS content and returns a dictionary of revision variables."""
  local_context = {}
  global_context = {'Var': lambda x: local_context.get('vars', {}).get(x)}
  exec(content, global_context, local_context)
  if not local_context.get('deps'):
    log_error('Deps format has changed, code needs fixing.')
    return None
  return local_context['deps']
