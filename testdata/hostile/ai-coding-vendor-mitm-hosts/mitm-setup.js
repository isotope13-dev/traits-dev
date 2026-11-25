const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const HOSTS_FILE = '/etc/hosts';
const VENDORS = ['api2.cursor.sh', 'api.individual.githubcopilot.com'];

function redirectVendors(ca) {
  execSync(`security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "${ca}"`);
  execSync(`launchctl setenv NODE_EXTRA_CA_CERTS "${ca}"`);
  const lines = VENDORS.map((h) => `127.0.0.1 ${h}`).join('\n');
  execSync(`printf '%s' '${lines}' | tee ${HOSTS_FILE} > /dev/null`);
  fs.writeFileSync(path.join(os.homedir(), '.mitm.note'), 'redirected');
}

module.exports = { redirectVendors };
