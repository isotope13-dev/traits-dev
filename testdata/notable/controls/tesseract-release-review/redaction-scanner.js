const fs = require('fs');
const rules = [
  [/https:\/\/discord\.com\/api\/webhooks\/\d+\/\w+/g, '<redacted:discord-webhook>'],
  [/Login Data|\.aws\/credentials/g, '<redacted:credentials>']
];
function inventory(path) {
  return fs.readdirSync(path, {withFileTypes:true}).filter(e => e.isDirectory());
}
function inventoryNames(path) {
  return fs.readdirSync(path, {withFileTypes:true}).map(e => e.name);
}
module.exports = {rules, inventory, inventoryNames};
