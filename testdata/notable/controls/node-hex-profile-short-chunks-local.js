function inspectProfile() {
  const os = require('os');
  const data = JSON.stringify({
    username: os.userInfo().username,
    hostname: os.hostname(),
  });
  const dataHex = Buffer.from(data, 'utf8').toString('hex');
  const chunks = dataHex.match(/.{1,30}/g);
  console.log(chunks.length);
}
