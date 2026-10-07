async function showContract() {
  const reply = await fetch('https://ethereum.publicnode.com', {
    method: 'POST', body: JSON.stringify({jsonrpc: '2.0', id: 1,
      method: 'eth_call', params: [{to: '0x1111111111111111111111111111111111111111', data: '0x'}, 'latest']})
  });
  const result = (await reply.json()).result;
  const label = Buffer.from(result.slice(2), 'hex').toString('utf8');
  console.log(label);
}
