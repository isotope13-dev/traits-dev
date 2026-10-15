const fs = require('fs');
const path = require('path');
fs.writeFileSync(path.join(process.cwd(), 'GEMINI.md'), 'Project rules');
