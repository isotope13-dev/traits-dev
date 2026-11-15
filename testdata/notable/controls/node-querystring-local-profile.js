const os = require("os");
const querystring = require("querystring");

const profile = querystring.stringify({
  hostname: os.hostname(),
  username: os.userInfo().username,
});
module.exports = profile;
