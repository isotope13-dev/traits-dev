// Retention-housekeeping control: deletes the tool's own raw exports by
// format after a successful run. The destruction warning must stay silent.
const fs = require('fs');
// Delete all raw JSONL files after export + training.
function purgeAll(dataDir) {
  for (const f of fs.readdirSync(dataDir).filter((x) => x.endsWith('.jsonl'))) {
    fs.unlinkSync(require('path').join(dataDir, f));
  }
}
module.exports = purgeAll;
