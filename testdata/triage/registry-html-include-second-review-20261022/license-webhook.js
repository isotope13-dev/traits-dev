const licenseKey = process.argv[2];
fetch('https://easypanel.host/webhook/t/e/s/t/e/node-meta/ads', {
 method: 'POST', body: JSON.stringify({chaveAion: licenseKey})
});
