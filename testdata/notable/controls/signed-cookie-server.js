const crypto = require('crypto');
const secret = process.env.SESSION_SECRET;
module.exports = function createSession(res, sessionStore, user) {
  const identity = crypto.randomBytes(32).toString('hex');
  sessionStore.set(identity, user.id);
  const signature = crypto.createHmac('sha256', secret).update(identity).digest('base64').replace(/=+$/, '');
  res.cookie('session', `s:${identity}.${signature}`, {secure: true, httpOnly: true});
};
