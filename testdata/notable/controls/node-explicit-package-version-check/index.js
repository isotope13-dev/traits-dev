const https = require('https');

module.exports.checkRegistry = function checkRegistry() {
  return https.get('https://registry.npmjs.org/-/ping', () => {});
};
