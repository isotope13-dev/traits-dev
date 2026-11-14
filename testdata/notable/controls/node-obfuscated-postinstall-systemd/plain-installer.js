const fs = require('fs');
const target = '/etc/systemd/system/product-agent.service';
const service = '[Service]\nExecStart=/usr/bin/product-agent\nRestart=always\n';
fs.writeFileSync(target, service);
