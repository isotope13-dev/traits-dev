// Near-miss for node-hashed-etc-hostname-userinfo-alias-beacon: the same
// hostname and user identity hashing, but the digest is written to a local
// file and nothing is sent over the network or to an OAST endpoint.
const c = require('crypto'), f = require('fs'), o = require('os');
const host = c.createHash('sha256').update(f.readFileSync('/etc/hostname')).digest('hex');
const user = c.createHash('sha256').update(o.userInfo().username).digest('hex');
f.writeFileSync('./machine-fingerprint.json', JSON.stringify({ host, user }));
