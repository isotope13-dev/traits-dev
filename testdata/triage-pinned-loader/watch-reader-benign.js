// Fixture: ordinary directory watcher that logs arrivals. Watches and reads
// but loads no native code and invokes nothing. Must never convict H1/H2/H3.
const fs = require('fs');
const path = require('path');

const inbox = path.join(__dirname, 'inbox');
const seen = new Set();

const watcher = fs.watch(inbox, (_event, name) => {
  if (!name || seen.has(name)) return;
  seen.add(name);
  const full = path.join(inbox, name);
  if (!fs.existsSync(full)) return;
  const text = fs.readFileSync(full, 'utf8');
  console.log('saw ' + name + ' (' + text.length + ' chars)');
});

module.exports = { watcher };
