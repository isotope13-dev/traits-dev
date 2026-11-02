#!/usr/bin/env python3
"""Verify Go handler-to-CommandContext calls, including large PE overlays."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/process/create/subprocess/configure::go-script-handler-command-context-call'

PREFIX = '''package main
import ("context"; "os/exec")
'''
LINKED = PREFIX + '''//go:noinline
func handleCommand(ctx context.Context, name string) *exec.Cmd { return exec.CommandContext(ctx, name) }
func main() { _ = handleCommand(context.Background(), "cmd.exe") }
'''
UNLINKED = PREFIX + '''//go:noinline
func handleCommand(x int) int { return x + 1 }
//go:noinline
func configure(ctx context.Context, name string) *exec.Cmd { return exec.CommandContext(ctx, name) }
func main() { _ = handleCommand(1); _ = configure(context.Background(), "cmd.exe") }
'''

def compile_go(directory, name, source):
    script = directory / (name + '.go')
    binary = directory / (name + '.exe')
    script.write_text(source)
    env = os.environ.copy()
    env.update(GOOS='windows', GOARCH='amd64', CGO_ENABLED='0', GOTOOLCHAIN='local')
    subprocess.run(['go', 'build', '-o', str(binary), str(script)], cwd=ROOT, env=env, check=True)
    return binary


def check(target, expected):
    result = subprocess.run(
        [CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(target)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
    assert any(line.startswith(prefix) for line in result.stdout.splitlines()), result.stdout
    detail = '✓ Inline YARA rule matched' if expected else '✗ Inline YARA rule did not match'
    assert detail in result.stdout, result.stdout
    print(target.name + ': passed', flush=True)


with tempfile.TemporaryDirectory(prefix='go-handler-context-') as name:
    directory = Path(name)
    linked = compile_go(directory, 'linked', LINKED)
    unlinked = compile_go(directory, 'unlinked', UNLINKED)
    padded = directory / 'linked-padded.exe'
    shutil.copyfile(linked, padded)
    with padded.open('r+b') as file:
        file.truncate(64 * 1024 * 1024 + 1)
    check(linked, True)
    check(unlinked, False)
    check(padded, True)
