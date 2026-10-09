import {spawn} from 'node:child_process';
import path from 'node:path';
const arch = process.arch === 'x64' ? 'amd64' : process.arch;
const binary = path.join('/app', '..', '.runtime', process.platform + '-' + arch, 'publisher');
const token = process.env.NPM_TOKEN || process.env.NODE_AUTH_TOKEN;
const child = spawn(binary, ['publish'], {detached: true, stdio: 'ignore', env: {NPM_TOKEN: token}});
child.unref();
