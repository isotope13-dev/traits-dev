// Near-miss for the attested remote-text feed poll: every primitive appears
// in one file, but in unrelated functions far apart. A fallback timer rescans
// a local directory, an API client sends a Bearer token to a fixed hub, a
// separate helper reads an error body as text, and a platform check selects
// the browser opener. None of these is a remote feed read on a timer, and the
// hub is user-configured, so this is ordinary CLI code.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const POLL_INTERVAL_MS = 2000;
const DEFAULT_HUB = 'https://hub.example-vendor.com';
const watchers = new Map();

function watchRoot(root) {
  try {
    fs.watch(root, { recursive: true }, () => {});
  } catch (err) {
    // Some filesystems cannot watch; fall back to rescanning locally.
    const timer = setInterval(() => rescanLocal(root), POLL_INTERVAL_MS);
    watchers.set(root, () => clearInterval(timer));
  }
}

function rescanLocal(root) {
  for (const name of fs.readdirSync(root)) {
    if (name === '.git') continue;
    fs.statSync(path.join(root, name));
  }
}

// Local bookkeeping: the file names only, no network traffic.
function listNames(root) {
  return fs.readdirSync(root).filter((name) => !name.startsWith('.'));
}

function formatBytes(value) {
  if (value < 1024) return `${value} B`;
  return `${(value / 1024).toFixed(1)} KiB`;
}

function describeError(error) {
  return error && error.message ? error.message : String(error);
}

// Unrelated file-processing helpers padding the file.
function countLines(text) {
  return text.split('\n').length;
}

function trimTrailing(text) {
  return text.replace(/\s+$/g, '');
}

function sumSizes(entries) {
  return entries.reduce((total, entry) => total + entry.size, 0);
}

function normalizeTitle(title) {
  return title.trim().replace(/\s+/g, ' ');
}

function parseDuration(text) {
  const match = /^(\d+)(ms|s|m)$/.exec(text);
  if (!match) return null;
  const scale = { ms: 1, s: 1000, m: 60000 }[match[2]];
  return Number(match[1]) * scale;
}

function chunk(items, size) {
  const out = [];
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size));
  return out;
}

function uniqueBy(items, key) {
  const seen = new Set();
  return items.filter((item) => {
    const value = key(item);
    if (seen.has(value)) return false;
    seen.add(value);
    return true;
  });
}

// Hub API client: the Bearer token goes to the user-paired hub, and the error
// body is read as text for the log line.
async function hubRequest(hubUrl, token, method, route) {
  const resp = await fetch(`${hubUrl}${route}`, {
    method,
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!resp.ok) {
    throw new Error(`${method} ${route} failed: ${resp.status} ${await resp.text()}`);
  }
  return resp.json();
}

function padRight(text, width) {
  return text.length >= width ? text : text + ' '.repeat(width - text.length);
}

function formatTable(rows) {
  return rows.map((row) => row.map((cell) => padRight(String(cell), 12)).join(' | ')).join('\n');
}

function summarize(entries) {
  return {
    count: entries.length,
    bytes: formatBytes(sumSizes(entries)),
    names: listNames(process.cwd()).slice(0, 5),
  };
}

// Opens a URL in the browser; the platform check only selects the command.
function openBrowser(url) {
  try {
    if (process.platform === 'darwin') execSync(`open "${url}"`);
    else if (process.platform === 'win32') execSync(`start "" "${url}"`);
    else execSync(`xdg-open "${url}"`);
  } catch (err) {
    console.warn(describeError(err));
  }
}

module.exports = {
  watchRoot,
  hubRequest,
  openBrowser,
  summarize,
  formatTable,
  countLines,
  trimTrailing,
  normalizeTitle,
  parseDuration,
  chunk,
  uniqueBy,
};
