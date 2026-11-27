// Agent sandbox: a file tool refuses to read protected paths. The table lists
// secret globs as denials, and the request path reads a file and posts the
// tool result (base64-encoded image bytes) to a model API.
const fs = require("fs");
const os = require("os");

const DEFAULT_DENY = [
  // env / config secrets
  "**/.env",
  "**/.env.*",
  "**/.npmrc",
  "**/.netrc",
  // private keys & certs
  "**/*.pem",
  "**/*.key",
  "**/id_rsa",
  // credential stores (dir AND contents)
  "**/.ssh",
  "**/.ssh/**",
  "**/.aws",
  "**/.aws/**",
];

function isDenied(relPath) {
  return DEFAULT_DENY.some((glob) => relPath.endsWith(glob.replace("**/", "")));
}

async function readForModel(file) {
  if (isDenied(file)) throw new Error(`Protected path: ${file}`);
  const bytes = fs.readFileSync(file);
  return Buffer.from(bytes).toString("base64");
}

async function askModel(image) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ image, home: os.homedir() }),
  });
  return res.json();
}

module.exports = { readForModel, askModel, DEFAULT_DENY };
