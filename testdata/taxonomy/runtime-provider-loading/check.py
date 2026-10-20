#!/usr/bin/env python3
"""Exercise runtime-loader observations without executing sample JavaScript."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


PREFIXES = {
    "import": "micro-behaviors/os/module/load::js-computed-import",
    "reify": "micro-behaviors/os/package-manager/runtime-install::npm-reify-add-save-call",
    "scripts": "micro-behaviors/os/package-manager/config::npm-ignore-scripts-object-option",
    "config": "micro-behaviors/communications/http/url/endpoint::configuration-api-path",
    "bytecode": "metadata/build/bun::bun-bytecode-source-marker",
    "electron": "micro-behaviors/process/interpreter/webview::electron-execute-javascript-reference",
    "font": "micro-behaviors/ui/graphics/font::noto-color-emoji-font-reference",
    "test": "metadata/lang/source/shape::common-test-source-text",
}

# Positive cases include spelling/order changes; negative cases separate
# executable syntax from comments, strings, types and unrelated objects.
CASES = [
    ("variable.js", "export const load = specifier => import(specifier);", {"import"}),
    ("commented.js", "export const load = specifier => import(/* module */ specifier);", {"import"}),
    ("property.js", "export const load = options => import(options.package);", {"import"}),
    ("indexed.js", "export const load = options => import(options['package']);", {"import"}),
    ("import-options.js", "export const load = options => import('known-package', options);", set()),
    ("import-options-comment.js", "export const load = options => import(/* module */ 'known-package', options);", set()),
    ("method-import.js", "const loader = { import(specifier) { return specifier; } }; loader.import(name);", set()),
    ("import-text.js", "// import(specifier)\nexport const example = 'import(specifier)';", set()),
    ("type-only.ts", "export type Example = import('known-package').Example;", set()),
    ("reify.js", "export const add = (tree, packages) => tree.reify({add: packages, saveType: 'prod'});", {"reify"}),
    ("reordered.js", "export const add = (x, y) => x.reify({saveType: 'dev', add: y});", {"reify"}),
    ("quoted-options.js", "export const add = (x,y)=>x.reify({'add':y,'saveType':'optional'});", {"reify"}),
    ("no-add.js", "export const update = tree => tree.reify({update: true, saveType: 'prod'});", set()),
    ("no-save-type.js", "export const add = tree => tree.reify({add: ['package']});", set()),
    ("other-method.js", "export const add = tree => tree.describe({add: ['package'], saveType: 'prod'});", set()),
    ("separate-options.js", "const install = {add: ['package'], saveType: 'prod'}; export const f = tree => tree.reify({dryRun: true});", set()),
    ("nested-options.js", "export const f = tree => tree.reify({add: ['package'], config: {saveType: 'prod'}});", set()),
    ("ignore-true.js", "export const options = {ignoreScripts: true};", {"scripts"}),
    ("ignore-minified.js", "export const options = {'ignoreScripts':!0};", {"scripts"}),
    ("ignore-false.js", "export const options = {ignoreScripts: false};", set()),
    ("ignore-minified-false.js", "export const options = {ignoreScripts: !1};", set()),
    ("ignore-string.js", "export const example = 'ignoreScripts: true';", set()),
    ("ignore-comment.js", "// ignoreScripts: true\nexport const options = {};", set()),
    ("config-template.js", "export const url = server => `${server}/api/v3/config`;", {"config"}),
    ("config-path.js", "export const url = '/api/config?format=json';", {"config"}),
    ("configuration-path.js", "export const url = '/api/v2/configuration';", set()),
    ("config-comment.js", "// /api/v2/config\nexport const url = '/api/status';", set()),
    ("bytecode.js", "// @bun @bytecode\nexport const value = 1;", {"bytecode"}),
    ("bytecode-string.js", "export const text = '// @bun @bytecode';", set()),
    ("bytecode-near-miss.js", "// @bun @bytecodes\nexport const value = 1;", set()),
    ("electron.js", "export const methodName = 'executeJavaScript';", {"electron"}),
    ("font.js", "export const fontName = 'Noto Color Emoji';", {"font"}),
    ("common.js", "const helper = require('../common');", {"test"}),
    ("test-definition.js", "function test() { return true; }", {"test"}),
    ("helper-reference.js", "export const example = 'require(\"../common\")';", {"test"}),
    ("loader.js", "// @bun @bytecode\nexport const config = s => `${s}/api/v2/config`;\nexport const options = {ignoreScripts:!0};\nexport async function load(tree, specs) { await tree.reify({add:specs,saveType:'prod'}); return import(specs[0]); }", {"import", "reify", "scripts", "config", "bytecode"}),
]


def documents(output):
    decoder = json.JSONDecoder()
    output = output.lstrip()
    while output:
        doc, offset = decoder.raw_decode(output)
        yield doc
        output = output[offset:].lstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--traits-dir", type=Path)
    args = parser.parse_args()
    root = args.traits_dir or Path(__file__).resolve().parents[3]
    retired = {
        "objectives/anti-static/obfuscation/payload/encoded/exec::electron-execute-javascript",
        "objectives/execution/exploit/browser-oob::color-emoji-font-stack",
        "objectives/anti-static/obfuscation/string/encoding::common-test-require-function",
    }
    with tempfile.TemporaryDirectory(prefix="runtime-provider-loading-") as temp:
        paths = []
        for name, source, _ in CASES:
            path = Path(temp) / name
            path.write_text(source + "\n")
            paths.append(path)
        native = []
        for index, (marker, match) in enumerate([
            ("electron/js2c/runtime", True),
            ('process._linkedBinding("electron_example', True),
            ("electron/js2d/runtime", False),
        ]):
            source = Path(temp) / f"marker-{index}.c"
            source.write_text("const char runtime_marker[] = " + json.dumps(marker) + ";\n")
            target = source.with_suffix(".o")
            subprocess.run(["cc", "-c", str(source), "-o", str(target)], check=True)
            native.append((target, match))
        result = subprocess.run([
            args.cleave, "--traits-dir", str(root), "--format", "json", "analyze",
            *map(str, paths), *[str(path) for path, _ in native],
        ], check=True, capture_output=True, text=True)
        files = {Path(f["path"]): f for d in documents(result.stdout) for f in d.get("files", [])}
        for path, (name, _, expected) in zip(paths, CASES):
            traits = files[path].get("traits", [])
            ids = {trait["id"] for trait in traits}
            found = {key for key, value in PREFIXES.items() if value in ids}
            assert found == expected, (name, expected, found)
            assert not ids & retired, (name, ids & retired)
            assert not any(t.get("crit", 0) >= 4 for t in traits), (name, traits)
            if name == "helper-reference.js":
                assert not any(i.startswith("metadata/package/testing/") for i in ids), ids
        for path, expected in native:
            traits = files[path].get("traits", [])
            ids = {trait["id"] for trait in traits}
            marker = "well-known/lib/runtime/scripted/electron::electron-runtime-js2c-marker"
            assert (marker in ids) == expected, (path.name, expected, ids)
            assert "objectives/evasion/anti-av/platform/quarantine::electron-runtime-js2c-marker" not in ids
            assert not any(t.get("crit", 0) >= 4 for t in traits), (path.name, traits)
    print(f"runtime provider loading: {len(CASES) + len(native)} controls passed")


if __name__ == "__main__":
    main()
