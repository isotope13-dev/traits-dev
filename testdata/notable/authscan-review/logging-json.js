process.stderr.write(`[chromium:stdout] ${data}`);
const data = { ok: true };
client.send(JSON.stringify(data));
