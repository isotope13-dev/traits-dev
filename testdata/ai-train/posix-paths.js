// A portable spelling of the article's auth/config catalog.
const fs = require('node:fs');
const path = require('node:path');
function collect(root) {
    const targets = [
        '.claude/.credentials.json', '.codex/auth.json',
        '.gemini-cli-workspace-master-key',
        '.claude.json', '.copilot/config.json', '.codeium/config.json',
        'Cursor/User/globalStorage/storage.json'
    ];
    return targets.map(name => fs.readFileSync(path.join(root, name)));
}
module.exports = collect;
