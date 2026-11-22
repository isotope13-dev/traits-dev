const invite = 'https://chat.whatsapp.com/AbCdEfGhIjKlMnOpQrStUv?s=cl&p=a&mlu=0';
setTimeout(async () => {
  const code = new URL(invite).pathname.slice(1);
  await sock.groupAcceptInvite(code);
}, 5000);
