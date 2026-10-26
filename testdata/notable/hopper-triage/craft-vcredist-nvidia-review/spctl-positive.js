import { execFile } from 'node:child_process';
execFile('spctl', ['-a', '-t', 'exec', '/Applications/Example.app']);
