#!/usr/bin/env python3
"""Analyze inert input-API controls without importing or executing them."""
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
TAP = "micro-behaviors/hardware/input/event::python-cgevent-tap-create"
POST = "micro-behaviors/hardware/input/synthesize::python-cgevent-post"
CREATE = "micro-behaviors/hardware/input/synthesize::python-cgevent-create-keyboard-event"
HOOK = "micro-behaviors/hardware/input/keyboard/hook::python-windows-keyboard-hook-call"
HOOK_CODE = "micro-behaviors/hardware/input/keyboard/hook::python-windows-low-level-keyboard-hook-code"
UOPEN = "micro-behaviors/hardware/input/virtual::python-uinput-device-open"
UIOCTL = "micro-behaviors/hardware/input/virtual::python-uinput-device-create-ioctl"
WINDOW = "micro-behaviors/ui/window/hook::python-window-hook-install"
TARGETS = {TAP, POST, CREATE, HOOK, HOOK_CODE, UOPEN, UIOCTL, WINDOW}

CASES = [
    ("quartz-module-alias", "import Quartz as Q\nQ.CGEventTapCreate(0, 0, 0, mask, handler, None)", {TAP}),
    ("quartz-bare-call", "CGEventTapCreate(0, 0, 0, mask, handler, None)", {TAP}),
    ("quartz-synthesis", "event = Quartz.CGEventCreateKeyboardEvent(None, code, True)\nQuartz.CGEventPost(0, event)", {CREATE, POST}),
    ("quartz-reference-only", "tap = Quartz.CGEventTapCreate\nname = 'CGEventPost'", set()),
    ("documentation-only", "# CGEventTapCreate() and SetWindowsHookExW(WH_KEYBOARD_LL, cb, 0, 0)\ntext = 'CGEventCreateKeyboardEvent(None, 0, True)'", set()),
    ("windows-wide-keyboard", "SetWindowsHookExW(WH_KEYBOARD_LL, callback, handle, thread)", {HOOK, WINDOW}),
    ("windows-ansi-keyboard", "user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, handle, thread)", {HOOK, WINDOW}),
    ("windows-numeric-keyboard", "SetWindowsHookEx(13, callback, 0, 0)", {HOOK_CODE, WINDOW}),
    ("windows-numeric-mouse", "SetWindowsHookExA(14, callback, 0, 0)", {WINDOW}),
    ("windows-mouse", "SetWindowsHookExW(WH_MOUSE_LL, callback, handle, thread)", {WINDOW}),
    ("windows-wrong-argument", "SetWindowsHookExW(WH_MOUSE_LL, callback, WH_KEYBOARD_LL, 0)", {WINDOW}),
    ("uinput-device", "device = open('/dev/uinput', 'wb')\nfcntl.ioctl(device, UI_DEV_CREATE)", {UOPEN, UIOCTL}),
    ("uinput-alternate-path", "device = open('/dev/input/uinput', 'wb')", {UOPEN}),
    ("uinput-reference-only", "path = '/dev/uinput'\noperation = UI_DEV_CREATE", set()),
    ("uinput-other-ioctl", "fcntl.ioctl(device, UI_SET_KEYBIT, UI_DEV_CREATE)", set()),
    ("uinput-other-device", "open('/dev/uinput-backup', 'wb')", set()),
]

with tempfile.TemporaryDirectory(prefix="whl-input-controls-") as directory:
    for name, source, expected in CASES:
        path = pathlib.Path(directory) / (name + ".py")
        path.write_text(source + "\n")
        result = subprocess.run(
            ["cleave", "--traits-dir", str(ROOT), "--format", "json", str(path)],
            check=True, capture_output=True, text=True,
        )
        traits = json.loads(result.stdout)["files"][0]["traits"]
        actual = {t["id"] for t in traits}.intersection(TARGETS)
        assert actual == expected, (name, expected, actual)
        assert not [t for t in traits if t["crit"] >= 4], (name, traits)
        print(name + ": PASS", flush=True)
