import { execFile } from 'node:child_process';
const documentation = "execFile('spctl', ['-a', '/Applications/Example.app'])";
execFile('codesign', ['--verify', '/Applications/Example.app']);
