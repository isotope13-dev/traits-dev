#!/usr/bin/env python3
"""Check that only the complete workspace-to-clipboard profile is notable."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    rule = 'micro-behaviors/data/collection/contacts::vscode-workspace-email-to-clipboard'
    bodies = {
        'complete-profile': """const vscode = require('vscode');
if (vscode.workspace.workspaceFolders) {
  const files = await vscode.workspace.findFiles('**/*');
  for (const file of files) {
    const doc = await vscode.workspace.openTextDocument(file);
    const emails = doc.getText().match(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}/g) || [];
  }
  const emailList = ['a@example.com'];
  await vscode.env.clipboard.writeText(emailList);
}
""",
        'missing-export': """const vscode = require('vscode');
if (vscode.workspace.workspaceFolders) {
  const files = await vscode.workspace.findFiles('**/*');
  for (const file of files) { await vscode.workspace.openTextDocument(file); }
  const emailList = ['a@example.com'];
  console.log(emailList);
}
""",
        'different-clipboard-data': """const vscode = require('vscode');
if (vscode.workspace.workspaceFolders) {
  const files = await vscode.workspace.findFiles('**/*');
  for (const file of files) { await vscode.workspace.openTextDocument(file); }
  const emailList = ['a@example.com'];
  await vscode.env.clipboard.writeText(themeName);
}
""",
        'comments-only': """// vscode.workspace.workspaceFolders; workspace.findFiles(); openTextDocument();
// emailList; clipboard.writeText(emailList); user@example.test
const x = 1;
""",
    }
    with tempfile.TemporaryDirectory(prefix='vscode-workspace-email-') as directory:
        paths = []
        for name, source in bodies.items():
            path = Path(directory) / (name + '.js')
            path.write_text(source)
            paths.append((name, path, name == 'complete-profile'))

        def check(case):
            name, path, expected = case
            result = subprocess.run([
                args.cleave, '--traits-dir', str(root), '--format', 'json', str(path),
            ], capture_output=True, text=True, check=True)
            traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
            found = [t for t in traits if t['id'] == rule]
            assert bool(found) == expected, (name, expected, found)
            assert all(t['crit'] == 3 for t in found)
            assert not any(t['crit'] >= 4 for t in traits)
            return name + ': passed'

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for message in pool.map(check, paths):
                print(message, flush=True)


if __name__ == '__main__':
    main()
