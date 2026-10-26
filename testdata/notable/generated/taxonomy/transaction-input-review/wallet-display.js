// Ordinary transaction decoding and an unrelated calculator expression.
async function showTransaction(hash) {
  const response = await fetch('https://eth.drpc.org', {
    method: 'POST', body: JSON.stringify({jsonrpc:'2.0', id:1,
      method:'eth_getTransactionByHash', params:[hash]})
  });
  const tx = (await response.json()).result;
  console.log(Buffer.from(tx.input.slice(2), 'hex').toString('utf8'));
  console.log(eval('2+2'));
}
