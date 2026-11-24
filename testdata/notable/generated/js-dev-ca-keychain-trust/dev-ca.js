// Local development CA helper: creates a root CA and trusts it for the
// developer's own HTTPS test server. It never edits the hosts file.
const forge = require("node-forge");
const { execSync } = require("child_process");

const ca = forge.pki.createCertificate();
ca.setExtensions([{ name: "basicConstraints", cA: true, critical: true }]);

execSync('security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ./dev-ca.crt');
