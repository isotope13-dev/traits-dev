#!/usr/bin/env python3
"""Check input generation, interception, and collection boundaries.

Fixtures are scanned, never executed.
"""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    parser.add_argument("--case", action="append", help="Run only the named fixture (repeatable)")
    args = parser.parse_args()
    generic_hook = "micro-behaviors/ui/window/hook::set-windows-hook"
    keyboard_type = "micro-behaviors/hardware/input/keyboard/hook::windows-low-level-keyboard-hook-numeric-code"
    logger = "objectives/collection/keylog/hook::numeric-low-level-keyboard-hook-file-logger"
    py_input = "micro-behaviors/hardware/input/event::python-pyhook"
    py_keyboard = "micro-behaviors/hardware/input/keyboard/hook::python-keyboard-hook-setup"
    css_export = "objectives/exfiltration/stealer/input::css-value-selector-url-exfil"
    css_selectors = "micro-behaviors/data/format/css::single-character-value-selector-sweep"
    device_path = "micro-behaviors/hardware/input/device::php-input-event-device-glob"
    device_logger = "objectives/collection/keylog/device::php-evdev-keylogger"
    input_stream = "objectives/exfiltration/stealer/input::qnx-zig-keylog-stream"
    kernel_callback = "micro-behaviors/os/kernel/callback::keyboard-notifier-register"
    kernel_collector = "objectives/collection/keylog/hook::lkm-keyboard-notifier-capture"
    cases = {
        "kernel-key-buffer.c": {kernel_callback: True, kernel_collector: True},
        "kernel-key-notifier.c": {kernel_callback: True, kernel_collector: False},
        "css-character-export.css": {css_selectors: True, css_export: True},
        "css-character-local.css": {css_selectors: True, css_export: False},
        "input-device-record.php": {device_path: True, device_logger: True},
        "input-device-path.php": {device_path: True, device_logger: False},
        "qnx-keylog-send.zig": {input_stream: True},
        "qnx-keylog-local.zig": {input_stream: False},
        "TouchDeviceRead.java": {
            "micro-behaviors/hardware/input/device::android-raw-touch-coordinate-capture": True,
            "objectives/collection/touch::android-wireless-adb-touch-collector": False,
        },
        "window-hook.c": {generic_hook: True, keyboard_type: False, logger: False},
        "keyboard-hook-log.c": {generic_hook: True, keyboard_type: True, logger: True},
        "keyboard-automation.sh": {
            "micro-behaviors/hardware/input/keyboard/simulate::applescript-keystroke-automation": True,
            "micro-behaviors/hardware/input/keyboard/simulate::key-down-phrase": True,
        },
        "keyboard-event-description.sh": {
            "micro-behaviors/hardware/input/keyboard/simulate::applescript-keystroke-automation": False,
            "micro-behaviors/hardware/input/keyboard/simulate::key-down-phrase": False,
        },
        "mouse-hook.py": {py_input: True, py_keyboard: False},
        "keyboard-hook.py": {py_input: True, py_keyboard: True},
    }
    if args.case:
        unknown = set(args.case) - cases.keys()
        if unknown:
            parser.error(f"Unknown fixtures: {', '.join(sorted(unknown))}")
        cases = {name: expected for name, expected in cases.items() if name in args.case}
    for name, expected in cases.items():
        # Test-data paths deliberately trigger fixture suppressors. Scan a copy
        # outside that tree so this checks the program's content and source roles.
        with tempfile.TemporaryDirectory(prefix="source-routing-") as directory:
            target = Path(directory) / name
            shutil.copyfile(root / "testdata/taxonomy/input-source" / name, target)
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
                 ",".join(expected), str(target)],
                capture_output=True, text=True, check=True,
            )
        output = result.stdout + result.stderr
        for rule, matched in expected.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(expected)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
