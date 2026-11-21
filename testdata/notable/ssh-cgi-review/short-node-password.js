const { Client } = require("ssh2");

const conn = new Client();
let attempt = 0;

conn.on("ready", () => {
  conn.exec("id", (err, stream) => {
    if (err) throw err;
    stream.on("data", (d) => process.stdout.write(d));
    stream.on("close", () => conn.end());
  });
});

conn.connect({
  host: process.argv[2],
  port: Number(process.argv[3] || 22),
  username: process.argv[4],
  authHandler: (methodsLeft, partialSuccess, callback) => {
    attempt += 1;
    const pw = attempt === 1 ? "wrong" : "x".repeat(32);
    callback({ type: "password", username: process.argv[4], password: pw });
  },
});
