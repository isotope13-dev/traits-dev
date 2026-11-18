// Benign near-miss: a wallet client reads its own account nonce and block
// head from its configured RPC provider, then posts a signed transaction. It
// shares the RPC method names with the loader fixture but never walks blocks
// for a hardcoded sender, fetches no remote code, and starts no child process.
const RPC = process.env.ETH_RPC_URL || 'https://rpc.example.invalid';
const OWN_ADDRESS = process.env.WALLET_ADDRESS;

async function rpc(method, params) {
  const res = await fetch(RPC, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  });
  return (await res.json()).result;
}

export async function nextNonce() {
  return rpc('eth_getTransactionCount', [OWN_ADDRESS, 'pending']);
}

export async function latestBlock() {
  return rpc('eth_getBlockByNumber', ['latest', false]);
}
