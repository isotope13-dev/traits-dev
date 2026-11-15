const { exec } = require('child_process');
exec('curl -X POST -d "status=ready" https://collector.example/status');
