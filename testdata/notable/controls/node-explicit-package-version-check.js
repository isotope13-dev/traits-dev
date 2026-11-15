const https = require('https');

module.exports.checkRelease = function checkRelease() {
  return https.get('https://registry.npmjs.org/-/ping', () => {});
};
