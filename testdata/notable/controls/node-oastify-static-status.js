const { exec } = require('child_process');

const command = 'curl -X POST https://status.example.net/check -d ready';
exec(command, { shell: 'sh' });
