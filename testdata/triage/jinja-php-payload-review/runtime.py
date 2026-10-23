#!/usr/bin/env python3
"""Reproduce execution limits using intercepted commands and a JS parser.

Run with: uv run --with jinja2==3.1.6 --with fsspec==2026.4.0 --with quickjs==1.19.4 python <this file>
"""
import io
import json
from pathlib import Path
from unittest.mock import patch

import jinja2
from jinja2.sandbox import SandboxedEnvironment
from fsspec.implementations.reference import ReferenceFileSystem
import quickjs

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "testdata/triage/advisory-storm-gx-first-review"
template = json.loads((FIXTURES / "jinja-payload.json").read_text())["template"]
calls = []


def intercepted(command, *args, **kwargs):
    assert command == "whoami", command
    calls.append(command)
    return io.StringIO("SIMULATED-USER\n")


with patch("os.popen", intercepted):
    assert jinja2.Template(template).render() == "SIMULATED-USER\n"
    assert calls == ["whoami"]
    calls.clear()
    try:
        SandboxedEnvironment().from_string(template).render()
    except jinja2.exceptions.SecurityError:
        pass
    else:
        raise AssertionError("sandbox allowed private traversal")
    assert not calls
    try:
        ReferenceFileSystem(json.loads((FIXTURES / "reference-payload.json").read_text()))
    except jinja2.exceptions.UndefinedError as exc:
        assert "method-wrapper" in str(exc) and "__globals__" in str(exc), str(exc)
    else:
        raise AssertionError("expected fsspec x binding to block this expression")
    assert not calls

html = (ROOT / "testdata/hostile/php-shell-upload-chain-controls.html").read_text()
script = html.split("<script>")[1].split("</script>")[0]
context = quickjs.Context()
try:
    context.eval(script)
except quickjs.JSException as exc:
    assert "SyntaxError" in str(exc), str(exc)
else:
    raise AssertionError("expected the multiline HTML-comment text to fail JS parsing")
construction = script[script.index("var body ="):script.index("xhr.send")]
context.eval(construction)
body = context.eval("body")
assert "\\x3c?php" in body and "<?php" not in body
assert "\\'cmd\\'" in body
print("PASS: Jinja command intercepted; sandbox blocks; fsspec binding fails; HTML and escaping fail")
