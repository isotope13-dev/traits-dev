// Publishing CLI helper: read a git error, mask any OAuth token embedded
// in a remote URL before the message can be printed, then run git.
const { execSync } = require('child_process');
const fs = require('fs');
const message = fs.readFileSync('git-error.log', 'utf8');
const safe = message.replace(/oauth2:gho_[a-zA-Z0-9]+@/g, 'oauth2:gho_xxxxx');
console.log(safe);
execSync('git status -s');
