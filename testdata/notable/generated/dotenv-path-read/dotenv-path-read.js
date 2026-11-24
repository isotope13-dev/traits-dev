const fs = require('fs');
const path = require('path');
const os = require('os');

// Loads secrets from the hidden dotenv file in the user's home directory.
const envFile = path.join(os.homedir(), '.env');
const secrets = fs.readFileSync(envFile, 'utf8');
module.exports = secrets;
