// Control fixture: the CI guard, the computer-name lookup and the local
// telemetry POST live in unrelated subsystems of one bundled CLI. No single
// code region gates a beacon on CI, so the hostile composite must not fire.
const os = require("os");
const http = require("http");
const { execSync } = require("child_process");

// Subsystem 1: deployment-platform branch detection for build metadata.
function detectReleaseChannel() {
  if (process.env.VERCEL) {
    return process.env.VERCEL_GIT_COMMIT_REF ?? null;
  }
  if (process.env.CI) {
    return process.env.GITHUB_HEAD_REF ?? process.env.CI_COMMIT_REF_NAME ?? null;
  }
  return null;
}

function slugifyChannel(value) {
  return String(value ?? "").toLowerCase().replace(/[^a-z0-9]+/g, "-");
}

function parseSemverRange(range) {
  const [floor, ceiling] = String(range).split("..");
  return { floor: Number(floor) || 0, ceiling: Number(ceiling) || 0 };
}

function linspace(from, to, steps) {
  const out = [];
  const span = to - from;
  for (let i = 0; i < steps; i += 1) {
    out.push(from + (span * i) / (steps - 1 || 1));
  }
  return out;
}

function composeAdjacency(rows, columns) {
  const matrix = [];
  for (let r = 0; r < rows; r += 1) {
    const row = new Array(columns).fill(0);
    if (r > 0) row[r - 1] = 1;
    if (r < columns - 1) row[r + 1] = 1;
    matrix.push(row);
  }
  return matrix;
}

function rotateLeft(values, by) {
  const n = values.length;
  const shift = ((by % n) + n) % n;
  return values.slice(shift).concat(values.slice(0, shift));
}

function padLeft(label, width, fill) {
  const text = String(label);
  return text.length >= width ? text : fill.repeat(width - text.length) + text;
}

function padRight(label, width, fill) {
  const text = String(label);
  return text.length >= width ? text + fill.repeat(width - text.length) : text;
}

function truncateMiddle(text, limit) {
  if (text.length <= limit) return text;
  const half = Math.floor((limit - 1) / 2);
  return text.slice(0, half) + "…" + text.slice(text.length - half);
}

function percentRank(sorted, value) {
  let lo = 0;
  let hi = sorted.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (sorted[mid] < value) lo = mid + 1;
    else hi = mid;
  }
  return lo / Math.max(sorted.length, 1);
}

function zscore(samples, value) {
  const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
  const variance =
    samples.reduce((a, b) => a + (b - mean) * (b - mean), 0) / samples.length;
  const sd = Math.sqrt(variance) || 1;
  return (value - mean) / sd;
}

function tickSpacing(min, max, count) {
  if (count < 2) return [min];
  const step = (max - min) / (count - 1);
  return Array.from({ length: count }, (_, i) => min + step * i);
}

function clampRange(value, low, high) {
  return Math.min(high, Math.max(low, value));
}

function lerpColor(a, b, t) {
  return Math.round(a + (b - a) * clampRange(t, 0, 1));
}

function hexPad(byte) {
  return clampRange(Math.round(byte), 0, 255).toString(16).padStart(2, "0");
}

function romanNumeral(n) {
  const table = [
    [1000, "M"],
    [900, "CM"],
    [500, "D"],
    [400, "CD"],
    [100, "C"],
    [90, "XC"],
    [50, "L"],
    [40, "XL"],
    [10, "X"],
    [9, "IX"],
    [5, "V"],
    [4, "IV"],
    [1, "I"],
  ];
  let rest = Math.max(0, Math.floor(n));
  let out = "";
  for (const [value, glyph] of table) {
    while (rest >= value) {
      out += glyph;
      rest -= value;
    }
  }
  return out;
}

function byteFormat(count) {
  const units = ["B", "KiB", "MiB", "GiB", "TiB"];
  let value = count;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(unit ? 1 : 0)}${units[unit]}`;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function unescapeHtml(text) {
  return String(text)
    .replace(/&quot;/g, '"')
    .replace(/&gt;/g, ">")
    .replace(/&lt;/g, "<")
    .replace(/&amp;/g, "&");
}

function escapeRegExp(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function pluralize(count, singular, plural) {
  if (count === 1) return singular;
  return plural ?? singular + "s";
}

function listConjunction(items) {
  if (items.length <= 1) return items.join("");
  if (items.length === 2) return items.join(" and ");
  return items.slice(0, -1).join(", ") + ", and " + items[items.length - 1];
}

function titleCaseWords(text) {
  const minor = new Set(["a", "an", "the", "of", "and", "or", "for", "to"]);
  return String(text)
    .split(/\s+/)
    .map((word, i) =>
      i > 0 && minor.has(word.toLowerCase())
        ? word.toLowerCase()
        : word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    )
    .join(" ");
}

function slugifyTitle(text) {
  return camelToKebab(titleCaseWords(text));
}

function truncateWords(text, count) {
  const words = String(text).split(/\s+/);
  if (words.length <= count) return text;
  return words.slice(0, count).join(" ") + "…";
}

function indentBlock(lines, pad) {
  return lines.map((line) => (line ? " ".repeat(pad) + line : line));
}

function outlineLevels(items) {
  let depth = 0;
  return items.map((item) => {
    if (item.startsWith("# ")) {
      depth = 1;
      return 1;
    }
    if (item.startsWith("## ")) {
      depth = Math.max(depth, 2);
      return 2;
    }
    return depth;
  });
}

function stableHashKey(parts) {
  return parts
    .map((part) => String(part).trim().toLowerCase())
    .filter(Boolean)
    .join(":");
}

function sortByLocale(values, locale) {
  const collator = new Intl.Collator(locale ?? "en", { numeric: true });
  return [...values].sort(collator.compare);
}

function groupByLocale(values, keyFn, locale) {
  const groups = new Map();
  const collator = new Intl.Collator(locale ?? "en", { numeric: true });
  for (const value of values) {
    const key = keyFn(value);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(value);
  }
  return [...groups.entries()]
    .sort((a, b) => collator.compare(a[0], b[0]))
    .map(([key, members]) => ({ key, members }));
}

function camelToKebab(name) {
  return String(name)
    .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
    .toLowerCase();
}

function pascalToSnake(name) {
  return camelToKebab(name).replace(/-/g, "_");
}

function initialsFor(words) {
  return words
    .split(/\s+/)
    .filter(Boolean)
    .map((w) => w[0].toUpperCase())
    .join("");
}

function wrapWords(text, width) {
  const words = String(text).split(/\s+/);
  const lines = [];
  let line = "";
  for (const word of words) {
    if ((line + " " + word).trim().length > width) {
      lines.push(line.trim());
      line = word;
    } else {
      line += " " + word;
    }
  }
  if (line.trim()) lines.push(line.trim());
  return lines;
}

function interleave(a, b) {
  const out = [];
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i += 1) {
    if (i < a.length) out.push(a[i]);
    if (i < b.length) out.push(b[i]);
  }
  return out;
}

function bucketize(items, size) {
  const buckets = [];
  for (let i = 0; i < items.length; i += size) {
    buckets.push(items.slice(i, i + size));
  }
  return buckets;
}

function movingAverage(samples, window) {
  const out = [];
  let sum = 0;
  for (let i = 0; i < samples.length; i += 1) {
    sum += samples[i];
    if (i >= window) sum -= samples[i - window];
    if (i >= window - 1) out.push(sum / window);
  }
  return out;
}

function diffIndices(before, after) {
  const changes = [];
  const n = Math.min(before.length, after.length);
  for (let i = 0; i < n; i += 1) {
    if (before[i] !== after[i]) changes.push(i);
  }
  return changes;
}

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  return `${minutes}m${seconds % 60}s`;
}

function chunkedReduce(values, reducer, chunk) {
  let acc = values[0];
  for (let i = 1; i < values.length; i += chunk) {
    acc = reducer(acc, values[i]);
  }
  return acc;
}

function parseIsoDay(text) {
  const [y, m, d] = String(text).split("-").map(Number);
  return { year: y, month: m, day: d };
}

function ordinalSuffix(n) {
  const rem10 = n % 10;
  const rem100 = n % 100;
  if (rem10 === 1 && rem100 !== 11) return "st";
  if (rem10 === 2 && rem100 !== 12) return "nd";
  if (rem10 === 3 && rem100 !== 13) return "rd";
  return "th";
}

function camelize(dashed) {
  return String(dashed).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function dedentBlock(lines) {
  const indents = lines.filter(Boolean).map((l) => l.match(/^ */)[0].length);
  const pad = Math.min(...indents, 80);
  return lines.map((l) => l.slice(pad));
}

// Subsystem 2: developer login names this workstation for the local dev roster.
function resolveWorkstationLabel(override) {
  if (override) return override;
  if (process.platform === "darwin") {
    try {
      return execSync("scutil --get ComputerName").toString().trim();
    } catch {}
  }
  return os.hostname();
}

// Subsystem 3: local Sentry Spotlight-style envelope relay for dev errors.
function relayEnvelopeLocal(spotlightUrl, envelope) {
  const body = JSON.stringify({ envelope });
  const req = http.request(
    {
      method: "POST",
      path: spotlightUrl.pathname,
      hostname: spotlightUrl.hostname,
      port: spotlightUrl.port,
      headers: { "Content-Type": "application/x-sentry-envelope" },
    },
    (res) => res.resume()
  );
  req.on("error", () => {});
  req.write(body);
  req.end();
}

module.exports = {
  detectReleaseChannel,
  slugifyChannel,
  parseSemverRange,
  linspace,
  composeAdjacency,
  rotateLeft,
  interleave,
  bucketize,
  movingAverage,
  diffIndices,
  formatDuration,
  chunkedReduce,
  parseIsoDay,
  ordinalSuffix,
  camelize,
  dedentBlock,
  resolveWorkstationLabel,
  relayEnvelopeLocal,
};
