const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const dir = path.join(os.homedir(), '.config', 'systemd', 'user');
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(path.join(dir, 'worker.service'), `[Service]\nExecStart=/usr/bin/python3 /opt/app/worker.py\nRestart=always\n[Install]\nWantedBy=default.target`);
execSync('systemctl --user daemon-reload');
execSync('systemctl --user enable worker.service');
