"""Check saved Cleave controls; never execute the fixture scripts."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
DOM = "micro-behaviors/data/collection/dom::dollar-dom-lookup-helper"
EVAL = "micro-behaviors/process/interpreter/eval/constructed::indirect-function-result-invocation"
JSON = "objectives/anti-static/obfuscation/eval/loader::json-fetch-indirect-eval-xor-storage"
WRITE = "micro-behaviors/ui/window/insert-html::fetch-document-write-with-blank-blob-urls"
CLOAK = "objectives/evasion/masquerade/html-script::school-tab-cloak-rotated-page-swap"
OLD_JSON = "objectives/command-and-control/dropper/script-eval/remote-code::obfuscated-fetch-json-indirect-function-loader"
OLD_WRITE = "objectives/evasion/masquerade/html-script::blank-blob-fetched-page-swap"


def read(path):
    result = {}
    for line in Path(path).read_text().splitlines():
        record = json.loads(line)
        for file in record["files"]:
            result[Path(file["path"]).name] = {
                item["id"]: item["crit"] for item in file.get("traits", [])
            }
    return result


def main():
    reports = Path(sys.argv[1])
    before = read(reports / "controls.before.jsonl")
    after = read(reports / "controls.after.jsonl")
    assert before["json-eval-xor-storage.js"][OLD_JSON] == 5
    assert after["json-eval-xor-storage.js"][JSON] == 4
    assert after["json-eval-xor-storage.js"][EVAL] == 3
    assert before["blank-blob-fetch.html"][OLD_WRITE] == 4
    assert after["blank-blob-fetch.html"][WRITE] == 3
    assert after["school-cloak.html"][CLOAK] == 5
    assert before["school-cloak.html"][CLOAK] == 5
    for name in ["local-dollar.js", "local-dollar-selector.js"]:
        assert after[name][DOM] == 3
    for name in ["construct-only.js", "json-render.js"]:
        assert EVAL not in after[name]
        assert JSON not in after[name]
    for traits in after.values():
        assert OLD_JSON not in traits and OLD_WRITE not in traits
    outside_before = read(reports / "outside.before.jsonl")
    outside_after = read(reports / "outside.after.jsonl")
    assert outside_before == outside_after, "Outside-batch coverage changed"
    assert any(level == 5 for level in outside_after["ghappier-buried-fetch-eval.js"].values())
    assert any(level == 5 for level in outside_after["atob-eval-loader.html"].values())
    assert "NOT MATCHED well-known/lib/web/client-side/jquery::jquery-dollar-api-call" in (
        reports / "jquery-negative.rule.txt"
    ).read_text()
    assert "\nMATCHED well-known/lib/web/client-side/jquery::jquery-dollar-api-call" in (
        reports / "jquery-positive.rule.txt"
    ).read_text()
    print("Passed eight boundaries, jQuery alias checks, and three outside controls")


if __name__ == "__main__":
    main()
