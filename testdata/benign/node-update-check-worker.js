// Ordinary CLI update nudge: the tool respawns its own entry as a detached
// worker that refreshes a version cache file, then exits. The spawned
// target is the CLI itself, not a downloaded payload.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

const CACHE = path.join(os.homedir(), '.mycli', 'update.json');

async function refreshCache() {
	const res = await fetch('https://api.example.com/v1/latest');
	const tag = (await res.json()).tag;
	fs.mkdirSync(path.dirname(CACHE), { recursive: true });
	fs.writeFileSync(CACHE, JSON.stringify({ checkedAt: Date.now(), tag }));
}

function kickRefresh(entry) {
	spawn(process.execPath, [entry, '__check-update'], {
		detached: true,
		stdio: 'ignore',
	}).unref();
}

async function download(url, dest) {
	const res = await fetch(url);
	if (!res.ok || !res.body) throw new Error('Download failed');
	await pipeline(
		Readable.fromWeb(res.body),
		fs.createWriteStream(path.resolve(os.tmpdir(), dest)),
	);
}

const [cmd, ...rest] = process.argv.slice(2);
if (cmd === '__check-update') {
	await refreshCache();
} else if (cmd === 'upgrade') {
	await download(rest[0], 'pkg.bin');
	kickRefresh(process.argv[1]);
}
