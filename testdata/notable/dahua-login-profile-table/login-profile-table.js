// Device-profile table for a lab inventory script: the entries document the
// login modes a Dahua DVR supports. Nothing here sends a request.
const deviceProfiles = [
  {userName: "admin", password: "Not Used", clientType: "NetKeyboard", loginType: "Direct"},
  {userName: "admin", password: "", clientType: "Local", loginType: "Loopback", ipAddr: "127.0.0.1"}
];

module.exports = { deviceProfiles };
