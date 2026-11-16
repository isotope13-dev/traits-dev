const fs = require('fs');
const path = require('path');
const axios = require('axios');

async function loadRemoteModule() {
  const response = await axios.get(
    'https://raw.githubusercontent.com/example/project/refs/heads/main/index.js'
  );
  const localModule = path.resolve(__dirname, 'index.js');
  fs.writeFileSync(localModule, response.data);
  return require('./index');
}

module.exports = { loadRemoteModule };
