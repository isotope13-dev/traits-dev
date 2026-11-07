#!/usr/bin/env python3
"""Check benign XPI behavior and the suspicious signals retained by triage."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    cleave = str((repo / args.cleave).resolve())
    fixtures = {
        "search/manifest.json": json.dumps({
            "manifest_version": 3,
            "name": "Alternate search provider",
            "version": "1.0",
            "chrome_settings_overrides": {"search_provider": {
                "name": "Example", "is_default": True,
                "search_url": "https://search.example/?q={searchTerms}",
            }},
        }),
        "suggest/manifest.json": json.dumps({
            "manifest_version": 3, "name": "Search with suggestions", "version": "1.0",
            "chrome_settings_overrides": {"search_provider": {
                "name": "Example", "is_default": True,
                "search_url": "https://search.example/?q={searchTerms}",
                "suggest_url": "https://search.example/suggest?q={searchTerms}",
            }},
        }),
        "redirect.js": '''
const rule = {id: 1, action: {type: "redirect", redirect: {
  regexSubstitution: "https://www.google.com/search?q=\\\\1"
}}, condition: {regexFilter: "^https://search.example/", resourceTypes: ["main_frame"]}};
chrome.declarativeNetRequest.updateDynamicRules({addRules: [rule]});
''',
        "catalog.js": "const domains = {\n" + "\n".join(
            f"  'site{i}.test': true," for i in range(205)
        ) + "\n  'gooogle.com': true\n};\n",
        "endpoint.js": 'fetch("https://gooogle.com/api");\n',
        "optional-bytecode.js": '''
try { require('bytenode'); require('./preload.jsc'); } catch (_) {}
''',
        "wallet.js": '''
function exportKey(pair) { return {secretKey: Array.from(pair.secretKey)}; }
''',
        "country-catalog.js": '''
const countries = ['AM', 'AZ', 'BY', 'KG', 'KZ', 'MD', 'RU', 'TJ', 'UA', 'UZ'];
''',
        "unicode-data.js": 'const category = "Math_Symbol Sm Modifier_Letter Lm";\n',
        "named-sidecar.js": 'const sidecar = "./Math_Symbol.js";\n',
        "serial-method.js": '''
const methods = [{key: "serialMapAsync", value: function(e) { return e.serial(); }}];
''',
        "inspection.js": '''
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('keydown', e => { if (e.key === 'F12') e.preventDefault(); });
''',
        "response-filter.js": '''
const stream = browser.webRequest.filterResponseData(requestId);
stream.ondata = event => stream.write(event.data);
''',
        "api-examples.js": '''
// browser.webRequest.filterResponseData(requestId);
// crypto.verify(null, data, key, signature);
const documentation = "chrome.runtime.connectNative('com.example.host')";
const example = "browser.webRequest.filterResponseData(requestId)";
const signatureExample = "crypto.verify(null, data, key, signature)";
''',
        "native-api.js": '''
const port = chrome.runtime.connectNative('com.example.host');
browser.runtime.sendNativeMessage('com.example.host', {action: 'status'});
''',
        "native-lookalike.js": '''
function connectNative() { return {connected: true}; }
function sendNativeMessage(message) { return message; }
connectNative();
sendNativeMessage({action: 'status'});
''',
        "native-aliases.js": '''
const runtime = browser.runtime;
runtime.connectNative('com.example.alias');
const extension = chrome;
extension.runtime.sendNativeMessage('com.example.alias', {action: 'status'});
''',
        "native-download.js": '''
chrome.webRequest.onBeforeSendHeaders.addListener(details => {
  const description = "This callback examines media requests after checking the URL, tab and resource type; the header access is deliberately farther than eighty characters from the listener name.";
  const headers = details.requestHeaders;
  return headers;
});
chrome.cookies.getAll({url: downloadUrl});
chrome.downloads.cancel(downloadId);
chrome.runtime.sendNativeMessage('com.example.downloader', {url: downloadUrl});
''',
        "long-header-callback.js": (
            'browser.webRequest.onBeforeSendHeaders.addListener(details => {\n'
            'const explanation = "' + 'padding ' * 300 + '";\n'
            'return details.requestHeaders;\n});\n'
        ),
        "headers-only.js": 'const headers = details.requestHeaders;\n',
        "hook-only.js": 'chrome.webRequest.onBeforeSendHeaders.addListener(details => {});\n',
        "signature.js": '''
const crypto = require('node:crypto');
const valid = crypto.verify(null, data, publicKey, signature);
''',
        "payment-name.js": 'const callbackField = "cardToken";\n',
        "resources/angular-ui-bootstrap/widget.js": 'const datepickerMode = "day";\n',
        "cookie-parser.js": 'const fields = document.cookie ? document.cookie.split("; ") : [];\n',
        "cookie-v2.js": '''
const api = {};
window.Cookies = api;
api.getJSON = function(key) { return JSON.parse(document.cookie.split("; ")[0]); };
api.withConverter = function(converter) { return converter; };
''',
        "cookie-api-lookalike.js": '''
const api = {};
api.getJSON = function(key) { return JSON.parse(key); };
api.withConverter = function(converter) { return converter; };
''',
        "cookie-v3.js": '''/*! js-cookie v3.0.5 | MIT */
const cookie = document.cookie;
''',
    }
    required = {
        "search/manifest.json": {
            "metadata/permission/manifest::extension-default-search-provider",
            "metadata/permission/manifest::extension-custom-search-endpoint",
        },
        "redirect.js": {"micro-behaviors/communications/http/dynamic::dnr-main-frame-search-redirect"},
        "suggest/manifest.json": {"metadata/permission/activation::custom-search-and-suggestion-provider"},
        "catalog.js": {"metadata/file/catalog/network::quoted-domain-catalog"},
        "endpoint.js": {"objectives/command-and-control/beacon/network/typosquat::typosquat-google-domain"},
        "optional-bytecode.js": {"micro-behaviors/os/module/load/path::try-catch-bytecode-loader"},
        "wallet.js": {"micro-behaviors/crypto/key/export::secret-key-array-field"},
        "country-catalog.js": {"metadata/lang/source/literal/string/label::cis-country-codes"},
        "named-sidecar.js": {"micro-behaviors/fs/path/script::math-symbol-javascript-name-reference"},
        "inspection.js": {"objectives/anti-analysis/browser-detect::js-anti-inspection-suite"},
        "response-filter.js": {"micro-behaviors/communications/http/intercept::webrequest-response-body-filter"},
        "native-api.js": {
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-connect",
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-message",
        },
        "native-aliases.js": {
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-connect",
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-message",
        },
        "native-download.js": {
            "micro-behaviors/communications/http/intercept::webrequest-request-header-capture",
            "micro-behaviors/communications/ipc/native-host::native-download-cookie-header-access",
        },
        "long-header-callback.js": {"micro-behaviors/communications/http/intercept::webrequest-request-header-capture"},
        "headers-only.js": {"micro-behaviors/communications/http/header/value::request-headers-member-reference"},
        "signature.js": {"micro-behaviors/crypto/verify::node-crypto-verify"},
        "payment-name.js": {"metadata/lang/source/naming/secret::card-token-name-reference"},
        "resources/angular-ui-bootstrap/widget.js": {
            "metadata/path/software::ui-library-resource-directory",
            "micro-behaviors/ui/controls/widget::datepicker-mode-reference",
        },
        "cookie-parser.js": {"micro-behaviors/communications/http/cookie-store::document-cookie-split-iterate"},
        "cookie-v2.js": {"well-known/lib/web/client-side/js-cookie::recognized-js-cookie-library-bundle"},
        "cookie-v3.js": {"well-known/lib/web/client-side/js-cookie::distribution-banner"},
    }
    forbidden = {
        "api-examples.js": {
            "micro-behaviors/crypto/verify::node-crypto-verify",
            "micro-behaviors/communications/http/intercept::webrequest-response-body-filter",
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-connect",
        },
        "native-lookalike.js": {
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-connect",
            "micro-behaviors/communications/ipc/native-host::browser-extension-native-message",
        },
        "payment-name.js": {"well-known/app/productivity/n8n::stripe-card-token-description"},
        "cookie-parser.js": {"well-known/lib/web/client-side/js-cookie::recognized-js-cookie-library-bundle"},
        "cookie-api-lookalike.js": {"well-known/lib/web/client-side/js-cookie::recognized-js-cookie-library-bundle"},
        "headers-only.js": {"micro-behaviors/communications/http/intercept::webrequest-request-header-capture"},
        "hook-only.js": {"micro-behaviors/communications/http/intercept::webrequest-request-header-capture"},
    }
    suspicious = {"endpoint.js", "optional-bytecode.js", "inspection.js", "native-download.js"}
    with tempfile.TemporaryDirectory(prefix="xpi-rule-controls-") as tmp:
        work = Path(tmp)
        for name, source in fixtures.items():
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
        result = subprocess.run(
            [cleave, "--traits-dir", str(repo), "--format", "json", str(work)],
            check=True, text=True, capture_output=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        files = {str(Path(f["path"]).relative_to(work)): f
                 for report in reports for f in report["files"]}
        for name in fixtures:
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            missing = required.get(name, set()) - ids
            assert not missing, (name, "missing", sorted(missing))
            unexpected = forbidden.get(name, set()) & ids
            assert not unexpected, (name, "unexpected", sorted(unexpected))
            findings = [t["id"] for t in traits if t["crit"] >= 4]
            assert bool(findings) == (name in suspicious), (name, findings)
            if name not in suspicious:
                misleading = [i for i in ids if i.startswith(("objectives/", "well-known/malware/"))]
                assert not misleading, (name, misleading)
            print(f"PASS {name}")
    print(f"{len(fixtures)} XPI triage controls passed")


if __name__ == "__main__":
    main()
