#!/usr/bin/env python3
"""Focused controls. Usage: check.py <scratch-directory> [sciter.dll ...]."""
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parents[2]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
engine = os.environ.get('CLEAVE', 'cleave')

def scan(path):
    run = subprocess.run([engine, '--traits-dir', str(root), '--format', 'json',
                          str(path)], capture_output=True, text=True, check=True)
    report = json.loads(run.stdout)
    return {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}

neutral = 'micro-behaviors/process/terminate/kill::process-snapshot-memory-read-termination'
process_source = '''void stop_named_process() {
    auto snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (Process32FirstW(snapshot, &entry)) do {
        if (lstrcmpiW(expected, entry.szExeFile) == 0) {
            ReadProcessMemory(process, address, buffer, length, &read);
            TerminateProcess(process, 0);
        }
    } while (Process32NextW(snapshot, &entry));
}
'''
for name, text, expected in [
    ('stop-selected.cpp', process_source, True),
    ('enumerate-only.cpp', process_source.replace('TerminateProcess(process, 0);', ''), False),
]:
    path = scratch / name
    path.write_text(text)
    traits = scan(path)
    assert (traits.get(neutral) == 3) == expected, (name, traits.get(neutral))
    assert not any('bot-killer' in t for t in traits), name
    print(name + ': passed')

floating = '''class FloatingControl {
    fun show() {
        val manager: WindowManager = getWindowManager()
        val params = WindowManager.LayoutParams(40, 40,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, 0, 0)
        manager.addView(controlIcon, params)
    }
}
'''
access = '''class InputControl : AccessibilityService() {
    fun readCurrentText() {
        val root = getRootInActiveWindow()
        val node = root.getChild(0)
        val text = node.getText()
    }
}
'''
labels = 'class LoginLabels { val password = "secret"; val pin = "pin" }'
archive = scratch / 'separate-ui-features.zip'
with zipfile.ZipFile(archive, 'w') as z:
    for name, text in [('FloatingControl.kt', floating), ('InputControl.kt', access),
                       ('LoginLabels.kt', labels)]:
        z.writestr(name, text)
traits = scan(archive)
for name in ['android-credential-overlay-surface', 'android-accessibility-credential-overlay']:
    assert 'objectives/credential-access/phishing/ui::' + name not in traits, name
for name in ['android-accessibility-service-source', 'android-accessibility-text-extraction']:
    assert traits['micro-behaviors/hardware/input/accessibility::' + name] == 3, name
assert traits['micro-behaviors/ui/window/overlay::android-source-runtime-overlay-window'] == 3
print(archive.name + ': passed; constituent capabilities retained')

# Same-file evidence still reaches the source rules; the fix is the archive boundary.
joined = scratch / 'joined-service.kt'
joined.write_text(floating + access + labels)
traits = scan(joined)
assert traits['objectives/credential-access/phishing/ui::android-accessibility-credential-overlay'] == 5
print(joined.name + ': passed; source rule retained')

for name in sys.argv[2:]:
    path = Path(name).resolve()
    traits = scan(path)
    assert not any(c >= 4 for c in traits.values()), path
    assert traits['micro-behaviors/ui/window/hook::unsigned-imported-window-hook-loader-api-set'] == 3
    assert traits['micro-behaviors/os/clipboard/monitor::windows-clipboard-read-monitor-api-set'] == 3
    print(path.name + ': passed; hook and clipboard capabilities retained')
