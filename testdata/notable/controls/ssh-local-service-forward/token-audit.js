const fs = require('fs');
const cp = require('child_process');
function countTokens(path) {
  const content = fs.readFileSync(path, 'utf8');
  return (content.match(/ghp_[A-Za-z0-9]{36}/g) || []).length;
}
function gitVersion() { return cp.execSync('git --version').toString(); }
module.exports = {countTokens, gitVersion};
