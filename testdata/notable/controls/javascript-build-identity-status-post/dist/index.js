var si = require('systeminformation');
var axios = require('axios');

// Reports the build host's hardware summary to the team's own status page.
// Logs the reply; never exits the build.
module.exports = async function statusReport(endpoint) {
  var system = await si.system();
  var res = await axios.post(endpoint, { model: system.model, manufacturer: system.manufacturer });
  console.log('status:', res.status);
  return res.data;
};
