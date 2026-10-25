const { execFile } = require('node:child_process');
execFile("launchctl", ["load", plist]);
