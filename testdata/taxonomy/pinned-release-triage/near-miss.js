// VERBATIM copy of that file. Re-copy the file after editing.
const sourceDescription = 'find symbols in the source code';
const result = /src\/(\w+Main)\/kotlin\//.exec(filePath);
const helper = require('./nextjs-audit-cache.js');
const text = 'pre-commit';
// Merely defining similarly named functions establishes no API invocation.
function glob(pattern) { return pattern; }
