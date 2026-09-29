#!/usr/bin/env python3
"""Generic Gmail menu handling must not imply AI conversation scraping."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def run_rules(cleave, root, fixture, rules):
    with tempfile.TemporaryDirectory(prefix="ai-chat-dom-scrape-") as directory:
        target = Path(directory) / fixture.name
        shutil.copyfile(fixture, target)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "test-rules", "--rules", ",".join(rules), str(target)],
            capture_output=True,
            text=True,
            check=True,
        )
    return result.stdout + result.stderr


def assert_match(output, rule, matched, name):
    marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
    print(f"PASS {name}: {marker.strip()}", flush=True)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    before = "objectives/collection/messaging/app::ai-chat-dom-scrape--gemini-copilot-before"
    after = "objectives/collection/messaging/app::ai-chat-dom-scrape--gemini-copilot-after"
    aggregate = "objectives/collection/messaging/app::ai-chat-dom-scrape"
    rules = [before, after, aggregate]

    gmail_menu = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/ai-chat-dom-scrape/gmail-gemini-menu.js",
        rules,
    )
    assert_match(gmail_menu, before, True, "gmail-gemini-menu-before-selector")
    assert_match(gmail_menu, after, True, "gmail-gemini-menu-after-selector")
    assert_match(gmail_menu, aggregate, True, "generic-menu-is-component-evidence")

    scraper = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/ai-chat-dom-scrape/conversation-scraper.js",
        rules,
    )
    assert_match(scraper, before, True, "conversation-scraper-before-selector")
    assert_match(scraper, after, True, "conversation-scraper-after-selector")
    assert_match(scraper, aggregate, True, "conversation-scraper-component")


if __name__ == "__main__":
    main()
