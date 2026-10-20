#!/usr/bin/env node

/**
 * toga-ai — TOGA Technology Claude harness bootstrapper
 *
 * Design: the npm bundle is the PRIMARY source — it always works offline.
 * The git repo is the UPDATE mechanism — if available, pull newer knowledge on top.
 *
 *   1. npm bundle (packageRoot) is always installed first — no git needed
 *   2. If git repo found/cloned: git pull --ff-only to get knowledge newer than bundle
 *   3. If git available: use git repo as source (newer); otherwise use npm bundle silently
 *   4. Install from chosen source into project .claude/
 *
 * Usage:
 *   npx toga-ai@latest              — auto-detect project, use bundle, update from git
 *   toga-ai                         — same (after global install)
 *   toga-ai --repo /path/to/claude  — explicit repo path
 *   toga-ai --project /path/to/proj — explicit project path
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const os = require('os');

const REPO_URL = 'https://github.com/agilantsolutions/claude';
const REPO_ENV_VAR = 'TOGA_TECH_REPO';
const CACHE_FILE = path.join(os.homedir(), '.toga-tech-path');

// The npm bundle root — always available
const PACKAGE_ROOT = path.resolve(__dirname, '..');

// Team skills that were retired from the bundle. Install MOVES them out of a dev's
// .claude/skills/ (to .claude/skills-retired/<name>-<yyyymmdd>) so they stop loading but
// nothing is lost. Only moved when the bundle no longer ships them.
const RETIRED_SKILLS = ['plan-ticket', 'work-ticket', 'rework-ticket', 'sync-team-skills', 'order-for'];

/* ------------------------------------------------------------------ */
/* npm bundle version                                                   */
/* ------------------------------------------------------------------ */

function getBundleVersion() {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(PACKAGE_ROOT, 'package.json'), 'utf8'));
    return pkg.version || 'unknown';
  } catch (e) {
    return 'unknown';
  }
}

// Latest npm version + semver compare live in a shared helper the version-check hook uses too.
const { getLatestNpmVersion, semverLt } = require('./hooks/lib/npm-latest');

/* ------------------------------------------------------------------ */
/* repo discovery (git update source)                                   */
/* ------------------------------------------------------------------ */

function candidatePaths() {
  const home = os.homedir();
  return [
    'C:\\WWW\\claude',
    'C:\\WWW\\claude-team',
    'D:\\WWW\\claude',
    path.join(home, 'claude'),
    path.join(home, 'Documents', 'claude'),
    path.join(home, 'Projects', 'claude'),
    path.join(home, 'toga-tech'),
    path.join(home, 'dev', 'claude'),
    path.resolve(process.cwd(), '..', 'claude'),
    path.resolve(process.cwd(), 'claude'),
  ];
}

function isValidClone(dir) {
  if (!fs.existsSync(dir)) return false;
  return (
    fs.existsSync(path.join(dir, 'knowledge')) &&
    fs.existsSync(path.join(dir, 'skills'))
  );
}

function findExistingClone() {
  const envPath = process.env[REPO_ENV_VAR];
  if (envPath && isValidClone(envPath)) return envPath;

  if (fs.existsSync(CACHE_FILE)) {
    const cached = fs.readFileSync(CACHE_FILE, 'utf8').trim();
    if (isValidClone(cached)) return cached;
  }

  for (const p of candidatePaths()) {
    if (isValidClone(p)) return p;
  }
  return null;
}

function saveRepoPathCache(repoDir) {
  try {
    fs.writeFileSync(CACHE_FILE, repoDir + '\n');
  } catch (e) { /* non-fatal */ }
}

/**
 * Initialize a local git repo at defaultDir seeded from the npm bundle.
 * Used when remote is inaccessible (private repo, no auth) but the machine
 * has git — gives /finish a pushable local repo using stored git credentials.
 */
function initLocalRepo(defaultDir) {
  const gitCheck = spawnSync('git', ['--version'], { stdio: 'pipe', shell: false });
  if (gitCheck.status !== 0 || gitCheck.error) return null;

  try {
    fs.mkdirSync(defaultDir, { recursive: true });

    // Already a git repo — leave it alone
    const isRepo = spawnSync('git', ['-C', defaultDir, 'rev-parse', '--git-dir'], { stdio: 'pipe' });
    if (isRepo.status === 0) return defaultDir;

    // Init and wire remote so /finish can push
    if (spawnSync('git', ['init', defaultDir], { stdio: 'pipe' }).status !== 0) return null;
    spawnSync('git', ['-C', defaultDir, 'remote', 'add', 'origin', REPO_URL], { stdio: 'pipe' });

    // Seed knowledge from bundle so capture has something to commit on top of
    const src = path.join(PACKAGE_ROOT, 'knowledge');
    const dest = path.join(defaultDir, 'knowledge');
    if (fs.existsSync(src)) copyDir(src, dest);

    const env = { ...process.env, GIT_AUTHOR_NAME: 'toga-ai', GIT_AUTHOR_EMAIL: 'toga-ai@local', GIT_COMMITTER_NAME: 'toga-ai', GIT_COMMITTER_EMAIL: 'toga-ai@local' };
    spawnSync('git', ['-C', defaultDir, 'add', 'knowledge/'], { stdio: 'pipe' });
    spawnSync('git', ['-C', defaultDir, 'commit', '-m', 'chore: seed knowledge from toga-ai bundle'], { stdio: 'pipe', env });

    return defaultDir;
  } catch (e) { return null; }
}

/**
 * Try git clone. Only called when no existing clone found and not --post-install.
 * Access check is done here before cloning — if it fails, return null (use bundle).
 */
function tryCloneRepo(defaultDir) {
  // Check git is available
  const gitCheck = spawnSync('git', ['--version'], { stdio: 'pipe', shell: false });
  if (gitCheck.status !== 0 || gitCheck.error) return null;

  // Probe repo access — lightweight, no download
  const probe = spawnSync('git', ['ls-remote', '--exit-code', REPO_URL, 'HEAD'], {
    stdio: 'pipe',
    shell: false,
    timeout: 10000,
  });
  if (probe.status !== 0) return null; // no access — silent, use bundle

  // Access confirmed — clone
  try {
    fs.mkdirSync(path.dirname(defaultDir), { recursive: true });
    const result = spawnSync('git', ['clone', REPO_URL, defaultDir], {
      stdio: 'pipe',
      shell: false,
    });
    if (result.status === 0) return defaultDir;
  } catch (e) { /* non-fatal */ }
  return null;
}

/**
 * Pull latest from git. Returns { pulled: bool, newDocs: number, message: string }.
 * Never throws — failures are silent and fall back to bundle.
 */
function tryGitPull(repoDir) {
  const gitCheck = spawnSync('git', ['--version'], { stdio: 'pipe', shell: false });
  if (gitCheck.status !== 0 || gitCheck.error) {
    return { pulled: false, newDocs: 0, message: null };
  }

  // Count knowledge docs before pull
  const beforeCount = countMd(path.join(repoDir, 'knowledge'));

  const result = spawnSync('git', ['pull', '--ff-only'], {
    cwd: repoDir,
    stdio: 'pipe',
    shell: false,
    timeout: 20000,
  });

  if (result.status !== 0) {
    return { pulled: false, newDocs: 0, message: null };
  }

  const out = (result.stdout || '').toString().trim();
  if (out === 'Already up to date.') {
    return { pulled: true, newDocs: 0, message: 'already up to date' };
  }

  const afterCount = countMd(path.join(repoDir, 'knowledge'));
  const newDocs = Math.max(0, afterCount - beforeCount);
  return { pulled: true, newDocs, message: 'pulled ' + newDocs + ' new knowledge doc' + (newDocs !== 1 ? 's' : '') + ' from agilantsolutions/claude' };
}

/* ------------------------------------------------------------------ */
/* project root discovery                                               */
/* ------------------------------------------------------------------ */

function findProjectRoot(start) {
  let dir = start;
  while (true) {
    if (fs.existsSync(path.join(dir, '.claude'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

/* ------------------------------------------------------------------ */
/* file utilities                                                       */
/* ------------------------------------------------------------------ */

// Returns { added, updated, unchanged }
// skipExisting: never overwrite (user content like knowledge docs)
// updateIfChanged: overwrite only when content differs (skills, rules, agents)
// neither: always overwrite (tooling like hooks, knowledge.js)
function copyDir(src, dest, { skipExisting = false, updateIfChanged = false } = {}) {
  const stats = { added: 0, updated: 0, unchanged: 0 };
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      const sub = copyDir(s, d, { skipExisting, updateIfChanged });
      stats.added += sub.added; stats.updated += sub.updated; stats.unchanged += sub.unchanged;
    } else if (!fs.existsSync(d)) {
      fs.copyFileSync(s, d);
      stats.added++;
    } else if (skipExisting) {
      stats.unchanged++;
    } else if (updateIfChanged) {
      const incoming = fs.readFileSync(s);
      const existing = fs.readFileSync(d);
      if (!incoming.equals(existing)) { fs.copyFileSync(s, d); stats.updated++; }
      else stats.unchanged++;
    } else {
      fs.copyFileSync(s, d);
    }
  }
  return stats;
}

function fmtStats({ added, updated, unchanged }) {
  const parts = [];
  if (added)     parts.push(added + ' new');
  if (updated)   parts.push(updated + ' updated');
  if (unchanged) parts.push(unchanged + ' unchanged');
  return parts.join(', ') || 'nothing to do';
}

function countMd(dir) {
  if (!fs.existsSync(dir)) return 0;
  let n = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) n += countMd(path.join(dir, entry.name));
    else if (entry.name.endsWith('.md')) n++;
  }
  return n;
}

/* ------------------------------------------------------------------ */
/* User-level telemetry env (~/.claude/settings.json)                   */
/* ------------------------------------------------------------------ */

// Canonical OTEL block owned by the harness. These keys are MANAGED: on every
// install they are removed and re-written from this object, so a stale value
// can never survive an upgrade. Every other key in the user's settings.json —
// including env vars the developer added themselves — is left exactly as-is.
const TELEMETRY_ENV = {
  CLAUDE_CODE_ENABLE_TELEMETRY: '1',
  CLAUDE_CODE_ENHANCED_TELEMETRY_BETA: '1',
  CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH: '61440',
  OTEL_EXPORTER_OTLP_ENDPOINT: 'https://otel.togaiq.com',
  OTEL_EXPORTER_OTLP_HEADERS: "Authorization=Bearer fixture-token-only",
  OTEL_EXPORTER_OTLP_PROTOCOL: 'http/protobuf',
  OTEL_LOGS_EXPORTER: 'otlp',
  OTEL_LOGS_EXPORT_INTERVAL: '5000',
  OTEL_LOG_ASSISTANT_RESPONSES: '1',
  OTEL_LOG_TOOL_DETAILS: '1',
  OTEL_LOG_USER_PROMPTS: '1',
  OTEL_METRICS_EXPORTER: 'otlp',
  OTEL_METRICS_INCLUDE_ACCOUNT_UUID: 'true',
  OTEL_METRICS_INCLUDE_ENTRYPOINT: 'true',
  OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES: 'true',
  OTEL_METRICS_INCLUDE_SESSION_ID: 'true',
  OTEL_METRICS_INCLUDE_VERSION: 'true',
  OTEL_METRIC_EXPORT_INTERVAL: '60000',
  OTEL_TRACES_EXPORTER: 'otlp',
  OTEL_TRACES_EXPORT_INTERVAL: '5000',
};

// Per-machine endpoint/token override, so a developer can point at a different
// collector without editing the bundle.
function telemetryEnvBlock() {
  const block = Object.assign({}, TELEMETRY_ENV);
  if (process.env.TOGA_OTEL_ENDPOINT) {
    block.OTEL_EXPORTER_OTLP_ENDPOINT = process.env.TOGA_OTEL_ENDPOINT;
  }
  if (process.env.TOGA_OTEL_TOKEN) {
    block.OTEL_EXPORTER_OTLP_HEADERS = 'Authorization=Bearer ' + process.env.TOGA_OTEL_TOKEN;
  }
  return block;
}

// Writes the managed OTEL keys into the USER settings file (~/.claude/settings.json).
// Surgical: parses the existing JSON, replaces only the managed keys under `env`,
// and rewrites the file. Never rewrites a file it could not parse.
// Opt out with TOGA_SKIP_TELEMETRY=1.
function applyTelemetryEnv() {
  if (process.env.TOGA_SKIP_TELEMETRY === '1') {
    return { status: 'skipped', reason: 'TOGA_SKIP_TELEMETRY=1' };
  }

  const userClaudeDir = path.join(os.homedir(), '.claude');
  const settingsPath = path.join(userClaudeDir, 'settings.json');

  let settings = {};
  const exists = fs.existsSync(settingsPath);
  if (exists) {
    let raw;
    try {
      raw = fs.readFileSync(settingsPath, 'utf8');
    } catch (e) {
      return { status: 'error', reason: 'unreadable: ' + e.message };
    }
    if (raw.trim()) {
      try {
        settings = JSON.parse(raw);
      } catch (e) {
        // Invalid JSON — refuse to touch it rather than destroy the user's settings.
        return { status: 'error', reason: 'existing settings.json is not valid JSON — left untouched' };
      }
      if (settings === null || typeof settings !== 'object' || Array.isArray(settings)) {
        return { status: 'error', reason: 'existing settings.json is not a JSON object — left untouched' };
      }
    }
  }

  const block = telemetryEnvBlock();
  const currentEnv = (settings.env && typeof settings.env === 'object' && !Array.isArray(settings.env))
    ? settings.env
    : {};

  // Rebuild env: keep every non-managed key in its original order, then append
  // the managed keys from the canonical block (delete-then-add semantics).
  const nextEnv = {};
  for (const key of Object.keys(currentEnv)) {
    if (!(key in block)) nextEnv[key] = currentEnv[key];
  }
  Object.assign(nextEnv, block);

  if (exists && JSON.stringify(currentEnv) === JSON.stringify(nextEnv)) {
    return { status: 'unchanged', path: settingsPath };
  }

  settings.env = nextEnv;

  try {
    fs.mkdirSync(userClaudeDir, { recursive: true });
    if (exists) fs.copyFileSync(settingsPath, settingsPath + '.toga-bak');
    // Atomic write so an interrupted install can't leave a half-written file.
    const tmp = settingsPath + '.toga-tmp';
    fs.writeFileSync(tmp, JSON.stringify(settings, null, 2) + '\n');
    fs.renameSync(tmp, settingsPath);
  } catch (e) {
    return { status: 'error', reason: e.message };
  }

  return { status: exists ? 'updated' : 'created', path: settingsPath };
}

function reportTelemetryEnv() {
  const r = applyTelemetryEnv();
  const n = Object.keys(TELEMETRY_ENV).length;
  if (r.status === 'error') {
    console.log('  ✗ Telemetry (~/.claude/settings.json: ' + r.reason + ')');
  } else if (r.status === 'skipped') {
    console.log('  · Telemetry (skipped — ' + r.reason + ')');
  } else {
    console.log('  ✓ Telemetry (' + n + ' OTEL env vars ' + r.status + ' in ~/.claude/settings.json)');
  }
  return r;
}

/* ------------------------------------------------------------------ */
/* settings.json merge                                                  */
/* ------------------------------------------------------------------ */

// Returns the .js filename if this hook command runs a TOGA hook script, null otherwise
function togaHookCommandKey(hook) {
  if (!hook || typeof hook.command !== 'string') return null;
  const match = hook.command.match(/hooks[/\\]toga[/\\]([^"'\s]+\.js)/);
  return match ? match[1] : null;
}

// Removes the hook COMMANDS whose TOGA key is in `keys` from every entry of one event.
// A developer's own command that shares an entry with a TOGA hook stays; an entry is
// dropped only when this removal left its hooks array empty.
function removeTogaHookCommands(entries, keys) {
  const out = [];
  for (const e of entries) {
    if (!e || !Array.isArray(e.hooks)) { out.push(e); continue; }
    const kept = e.hooks.filter((h) => !keys.has(togaHookCommandKey(h)));
    if (kept.length === e.hooks.length) { out.push(e); continue; }
    if (kept.length === 0) continue;
    out.push(Object.assign({}, e, { hooks: kept }));
  }
  return out;
}

// Retired TOGA hooks: their commands are removed from a dev's existing settings. The script
// itself ships as a no-op stub, so a command left behind is harmless.
const RETIRED_TOGA_HOOKS = ['kickoff-gate.js'];

// Permission rules the TOGA template once shipped and no longer wants. Only exact TOGA-owned
// strings go here — a developer's own rules are never removed.
const RETIRED_TOGA_PERMISSIONS = { allow: [
  'Bash(node sync-skills.js *)',
], ask: [
  'mcp__clickup__clickup_create_task_comment',
  'mcp__clickup__clickup_create_comment',
  'mcp__clickup__clickup_update_task',
] };

function mergeSettings(claudeDir, sourceDir) {
  const templatePath = path.join(sourceDir, '.claude', 'settings.json');
  if (!fs.existsSync(templatePath)) return false;

  let template;
  try {
    template = JSON.parse(fs.readFileSync(templatePath, 'utf8'));
  } catch (e) {
    console.error('  ERROR: Could not parse settings.json template: ' + e.message);
    return false;
  }

  const destPath = path.join(claudeDir, 'settings.json');
  let existing = {};
  if (fs.existsSync(destPath)) {
    try {
      existing = JSON.parse(fs.readFileSync(destPath, 'utf8'));
    } catch (e) {
      console.warn('  WARNING: existing settings.json invalid — backing up.');
      fs.copyFileSync(destPath, destPath + '.bak');
    }
  }

  const merged = JSON.parse(JSON.stringify(existing));

  if (template.hooks) {
    merged.hooks = merged.hooks || {};
    for (const event of Object.keys(template.hooks)) {
      if (!merged.hooks[event]) {
        merged.hooks[event] = template.hooks[event];
      } else {
        for (const entry of template.hooks[event]) {
          // TOGA hook script names are the identity key. Replacing per COMMAND (not per
          // entry) swaps old absolute-path commands for the new ones and keeps any of the
          // developer's own commands that share an entry.
          const incomingKeys = new Set(
            (Array.isArray(entry.hooks) ? entry.hooks : []).map(togaHookCommandKey).filter(Boolean)
          );
          if (incomingKeys.size) {
            merged.hooks[event] = removeTogaHookCommands(merged.hooks[event], incomingKeys);
          } else {
            // Non-TOGA hooks: skip exact duplicates
            const fp = JSON.stringify(entry);
            if (merged.hooks[event].some((e) => JSON.stringify(e) === fp)) continue;
          }
          merged.hooks[event].push(entry);
        }
      }
    }
  }

  if (merged.hooks) {
    const retired = new Set(RETIRED_TOGA_HOOKS);
    for (const event of Object.keys(merged.hooks)) {
      if (!Array.isArray(merged.hooks[event])) continue;
      merged.hooks[event] = removeTogaHookCommands(merged.hooks[event], retired);
    }
  }

  // Permission lists — union per list; never remove the developer's own entries.
  // Claude Code checks deny, then ask, then allow — so an ask/deny rule wins over an older
  // allow entry. Old allow entries are left alone (a TOGA-shipped one can't be told apart
  // from one the developer added).
  if (merged.permissions) {
    for (const list of Object.keys(RETIRED_TOGA_PERMISSIONS)) {
      if (!Array.isArray(merged.permissions[list])) continue;
      merged.permissions[list] = merged.permissions[list].filter(
        (rule) => !RETIRED_TOGA_PERMISSIONS[list].includes(rule)
      );
    }
  }
  if (template.permissions) {
    for (const list of ['allow', 'ask', 'deny']) {
      if (!Array.isArray(template.permissions[list])) continue;
      merged.permissions = merged.permissions || {};
      merged.permissions[list] = merged.permissions[list] || [];
      for (const rule of template.permissions[list]) {
        if (!merged.permissions[list].includes(rule)) {
          merged.permissions[list].push(rule);
        }
      }
    }
  }

  // Env vars — additive: set each template key only if the project hasn't
  // already defined it, so a developer's local override is never clobbered.
  if (template.env) {
    merged.env = merged.env || {};
    for (const key of Object.keys(template.env)) {
      if (!(key in merged.env)) {
        merged.env[key] = template.env[key];
      }
    }
  }

  fs.writeFileSync(destPath, JSON.stringify(merged, null, 2) + '\n');
  return true;
}

/* ------------------------------------------------------------------ */
/* CLAUDE.md                                                            */
/* ------------------------------------------------------------------ */

// The harness section sits between these markers so a re-install replaces only that block.
const CLAUDE_MD_BEGIN = '<!-- TOGA-HARNESS:BEGIN (installed by npx toga-ai — edits inside are replaced) -->';
const CLAUDE_MD_END = '<!-- TOGA-HARNESS:END -->';
const CLAUDE_MD_BEGIN_RE = /<!-- TOGA-HARNESS:BEGIN[^\n]*-->/;
// Pre-marker installs ended the section with this fenced block.
const LEGACY_SECTION_TAIL = '\nnpx toga-ai\n```\n';

// Where an old, unmarked harness section ends: after its closing `npx toga-ai` block, or at
// the next "# " / "## " heading — whichever comes first. Nothing after it is touched.
function legacySectionEnd(text, start) {
  const after = start + 1;
  const headings = ['\n# ', '\n## '].map((h) => text.indexOf(h, after)).filter((i) => i !== -1);
  const nextHeading = headings.length ? Math.min(...headings) + 1 : text.length;
  const tail = text.indexOf(LEGACY_SECTION_TAIL, after);
  if (tail !== -1 && tail + LEGACY_SECTION_TAIL.length <= nextHeading) return tail + LEGACY_SECTION_TAIL.length;
  return nextHeading;
}

function updateClaudeMd(projectRoot, skillNames, sourceDir, sourceLabel) {
  const claudeMdPath = path.join(projectRoot, 'CLAUDE.md');
  const marker = '## TOGA Technology Claude Harness';

  const body = `
## TOGA Technology Claude Harness

Installed from: ${sourceLabel}

---

### Session Workflow (STRICT — follow every session)

**Start of every session — run this first, no exceptions:**
\`\`\`
/start TRUE-1234
\`\`\`
Use your ClickUp ticket id, and only the id. This reads the ticket, checks your branches, and
loads the team knowledge base, framework context, and client config. Every session needs a
ticket — edits are blocked until you run it.

**Commit as you go:**
\`\`\`
/commit
\`\`\`
Commits only the files this session changed, with the session notes, then pushes the ticket branch (never force).

**End of every session — run this before closing:**
\`\`\`
/finish
\`\`\`
This saves what you learned, fixed, or decided to the shared knowledge base and
auto-pushes it to the team git repo. Then it checks the ticket fields. When the ticket is
done, it pushes, opens the PRs, comments on the ticket, and sets it to development finished.
If you close without running /finish, the knowledge is lost.

For a major ticket, \`/pseudocode\` writes the agreed approach to the ticket's Pseudocode field.

**Long session checkpoint (run before switching tasks or closing mid-work):**
\`\`\`
/session-save
\`\`\`

**Resuming previous work:**
\`\`\`
/session-resume latest
\`\`\`

---

### Skills & agents

Your Claude Code session already lists every available \`/skill\` and specialist agent on each
launch — this file intentionally does **not** duplicate that catalog (a static copy only drifts
out of date). The rules that matter:

- **\`/start TRUE-1234\` first, \`/finish\` last** — every session (see above).
- Specialist agents (php-reviewer, sql-reviewer, framework-pattern-checker, planner,
  knowledge-writer, session-capture, cto, cso, devops, harness-optimizer) fire **automatically**
  on the matching file or operation. You can also invoke one explicitly — e.g. "use the
  php-reviewer agent on this file."

---

### Knowledge Base

Team knowledge lives in \`.claude/knowledge/\`. It is seeded from the npm bundle
and grows every time any developer runs \`/finish\`.

- Search it: \`node .claude/knowledge.js search --q="payments"\`
- Validate it: \`node .claude/knowledge.js validate\`
- Re-index it: \`node .claude/knowledge.js index\`

Every time you edit a file inside \`.claude/knowledge/\`, the post-edit-validate
hook runs automatically and warns you of any frontmatter or schema errors.

---

### Updating

Pull latest skills, agents, and knowledge from the team repo:
\`\`\`
npx toga-ai@latest
\`\`\`
`;
  const block = CLAUDE_MD_BEGIN + '\n' + body.trimStart() + CLAUDE_MD_END + '\n';
  const note = '\n' + block;

  if (fs.existsSync(claudeMdPath)) {
    const existing = fs.readFileSync(claudeMdPath, 'utf8');
    const begin = existing.search(CLAUDE_MD_BEGIN_RE);
    if (begin !== -1) {
      const endAt = existing.indexOf(CLAUDE_MD_END, begin);
      if (endAt !== -1) {
        let stop = endAt + CLAUDE_MD_END.length;
        if (existing.slice(stop, stop + 2) === '\r\n') stop += 2;
        else if (existing[stop] === '\n') stop += 1;
        fs.writeFileSync(claudeMdPath, existing.slice(0, begin) + block + existing.slice(stop));
        return 'updated';
      }
    }
    if (existing.includes(marker)) {
      const start = existing.indexOf(marker);
      const end = legacySectionEnd(existing, start);
      fs.writeFileSync(claudeMdPath, existing.slice(0, start) + block + existing.slice(end));
      return 'updated';
    }
    fs.appendFileSync(claudeMdPath, note);
    return 'appended';
  }

  fs.writeFileSync(claudeMdPath, `# CLAUDE.md\n${note}`);
  return 'created';
}

/* ------------------------------------------------------------------ */
/* ECC global integration detection                                     */
/* ------------------------------------------------------------------ */

function detectEcc() {
  const home = os.homedir();
  const claudeDir = path.join(home, '.claude');
  const candidates = [
    path.join(claudeDir, 'plugins', 'marketplaces', 'ecc'),
    path.join(claudeDir, 'plugins', 'cache', 'ecc'),
    path.join(claudeDir, 'plugins', 'ecc'),
    path.join(claudeDir, 'plugins', 'marketplaces', 'everything-claude-code'),
    path.join(claudeDir, 'plugins', 'everything-claude-code'),
  ];
  return candidates.find((p) => fs.existsSync(p)) || null;
}

/* ------------------------------------------------------------------ */
/* main                                                                 */
/* ------------------------------------------------------------------ */

function main() {
  const args = process.argv.slice(2);

  const repoFlag = (() => {
    const i = args.indexOf('--repo');
    return i !== -1 ? args[i + 1] : null;
  })();
  const projectFlag = (() => {
    const i = args.indexOf('--project');
    return i !== -1 ? args[i + 1] : null;
  })();
  const isPostInstall = args.includes('--post-install');

  const bundleVersion = getBundleVersion();

  // Warn if npx served a stale cached version (common on Windows). Never block — install
  // the current bundle now and let the user update afterwards.
  if (!isPostInstall) {
    const latestVersion = getLatestNpmVersion();
    if (latestVersion && semverLt(bundleVersion, latestVersion)) {
      console.log('');
      console.log('  ⚠ Running toga-ai@' + bundleVersion + ' — toga-ai@' + latestVersion + ' is available.');
      console.log('  Update with: npm cache clean --force && npx toga-ai@latest');
      console.log('  (Continuing install with current bundle...)');
    }
  }

  console.log('');
  console.log('toga-ai — TOGA Technology Claude harness');
  console.log('═════════════════════════════════════════════');

  // Harness components (skills/agents/rules/hooks) ALWAYS come from the npm bundle.
  // The git repo is ONLY used to pull newer knowledge docs on top — it never
  // replaces harness components, so a stale local clone can't break the install.
  const harnessDir = PACKAGE_ROOT;
  let knowledgeDir = PACKAGE_ROOT;  // overridden below if git repo found
  let gitUpdateLine = null;

  if (repoFlag) {
    const resolved = path.resolve(repoFlag);
    if (isValidClone(resolved)) {
      knowledgeDir = resolved;
    } else {
      console.error('  ERROR: --repo path is not a valid clone: ' + resolved);
      process.exit(1);
    }
  } else {
    let repoDir = findExistingClone();

    if (!repoDir && !isPostInstall) {
      const togaTechDir = path.join(os.homedir(), 'toga-tech');
      // Try full clone first (works if repo is public or user is authenticated)
      repoDir = tryCloneRepo(togaTechDir);
      // Fall back: init a local git repo seeded from bundle (private repo / no auth)
      // This gives /finish a pushable git repo using the machine's stored credentials
      if (!repoDir) repoDir = initLocalRepo(togaTechDir);
    }

    if (repoDir) {
      const pullResult = tryGitPull(repoDir);
      saveRepoPathCache(repoDir);

      if (pullResult.pulled) {
        knowledgeDir = repoDir;
        if (pullResult.newDocs > 0) {
          gitUpdateLine = 'git update: pulled ' + pullResult.newDocs + ' new knowledge doc' + (pullResult.newDocs !== 1 ? 's' : '') + ' from agilantsolutions/claude';
        } else if (pullResult.message !== 'already up to date') {
          gitUpdateLine = 'git update: ' + pullResult.message;
        }
      }
    }
  }

  console.log('  Harness: npm bundle v' + bundleVersion);
  if (knowledgeDir !== PACKAGE_ROOT) {
    if (gitUpdateLine) {
      console.log('  Knowledge: git repo (' + gitUpdateLine.replace('git update: ', '') + ')');
    } else {
      console.log('  Knowledge: git repo at ' + knowledgeDir + ' (ready for /finish push)');
    }
  }
  if (gitUpdateLine && knowledgeDir === PACKAGE_ROOT) {
    console.log('  ↳ ' + gitUpdateLine);
  }
  console.log('');

  // User-level OTEL env — applies on every install, including the bare
  // `npm i -g toga-ai` postinstall that never reaches a project directory.
  reportTelemetryEnv();
  console.log('');

  if (isPostInstall && !repoFlag) {
    console.log('  First-time setup: run `toga-ai` from your project to');
    console.log('  install the harness into your .claude/ directory.');
    console.log('');
    console.log('═════════════════════════════════════════════');
    console.log('');
    process.exit(0);
  }

  // Step 3: find target project
  let projectRoot;
  if (projectFlag) {
    projectRoot = path.resolve(projectFlag);
  } else {
    projectRoot = findProjectRoot(process.cwd()) || process.cwd();
  }

  const claudeDir = path.join(projectRoot, '.claude');
  const errors = [];

  // Skills
  const skillsSrc = path.join(harnessDir, 'skills');
  const skillsDest = path.join(claudeDir, 'skills');
  fs.mkdirSync(skillsDest, { recursive: true });
  const skillNames = fs.existsSync(skillsSrc)
    ? fs.readdirSync(skillsSrc, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)
    : [];
  // Skills — update if content changed, skip if identical (preserves user edits only when unchanged)
  let skillStats = { added: 0, updated: 0, unchanged: 0 };
  for (const s of skillNames) {
    try {
      const sub = copyDir(path.join(skillsSrc, s), path.join(skillsDest, s), { updateIfChanged: true });
      skillStats.added += sub.added; skillStats.updated += sub.updated; skillStats.unchanged += sub.unchanged;
    } catch (e) { errors.push('skill/' + s + ': ' + e.message); }
  }
  // Retired skills — move the old copies out of skills/ so they no longer load.
  const retiredMoved = [];
  const retiredSkipped = [];
  const retiredDir = path.join(claudeDir, 'skills-retired');
  const d = new Date();
  const stamp = d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0');
  for (const s of RETIRED_SKILLS) {
    if (skillNames.includes(s)) continue;
    const p = path.join(skillsDest, s);
    const target = path.join(retiredDir, s + '-' + stamp);
    try {
      if (!fs.existsSync(p)) continue;
      if (fs.existsSync(target)) { retiredSkipped.push(s); continue; }
      fs.mkdirSync(retiredDir, { recursive: true });
      fs.renameSync(p, target);
      retiredMoved.push(s);
    } catch (e) { errors.push('retired skill/' + s + ': ' + e.message); }
  }
  console.log('  ✓ Skills    (' + skillNames.length + '): ' + fmtStats(skillStats));
  if (retiredMoved.length) console.log('  ✓ Moved retired skills to ' + retiredDir + ': ' + retiredMoved.join(', '));
  if (retiredSkipped.length) console.log('  ! Retired skills left in place (already moved today): ' + retiredSkipped.join(', '));

  // Rules — only the UNIVERSAL set (rules/common) installs always-on. Framework-specific
  // rules (1.0 App_, 2.0 _underscore, Python) now live in the knowledge base under
  // <fw>/standards/ and load on-demand via /start per the framework in scope (P2), so a
  // session never carries rules for a framework it isn't working in.
  const rulesToga = path.join(claudeDir, 'rules', 'toga');
  const rulesSrc = path.join(harnessDir, 'rules', 'common');
  const rulesDest = path.join(rulesToga, 'common');
  let rulesStats = { added: 0, updated: 0, unchanged: 0 };
  if (fs.existsSync(rulesSrc)) {
    try { rulesStats = copyDir(rulesSrc, rulesDest, { updateIfChanged: true }); }
    catch (e) { errors.push('rules: ' + e.message); }
  }
  // Prune framework-specific rules + the meta README left behind by pre-P2 installs so
  // they stop loading always-on (their content now lives in <fw>/standards/).
  for (const stale of ['php', 'python', 'README.md']) {
    const p = path.join(rulesToga, stale);
    try { if (fs.existsSync(p)) fs.rmSync(p, { recursive: true, force: true }); } catch (_) { /* best-effort cleanup */ }
  }
  console.log('  ✓ Rules     (' + countMd(rulesDest) + '): ' + fmtStats(rulesStats));

  // Agents — update if content changed
  const agentsSrc = path.join(harnessDir, 'agents');
  const agentsDest = path.join(claudeDir, 'agents', 'toga');
  let agentsStats = { added: 0, updated: 0, unchanged: 0 };
  if (fs.existsSync(agentsSrc)) {
    try { agentsStats = copyDir(agentsSrc, agentsDest, { updateIfChanged: true }); }
    catch (e) { errors.push('agents: ' + e.message); }
  }
  const agentsCount = fs.existsSync(agentsDest) ? fs.readdirSync(agentsDest).filter((f) => f.endsWith('.md')).length : 0;
  console.log('  ✓ Agents    (' + agentsCount + '): ' + fmtStats(agentsStats));

  // Hook scripts — always overwrite so paths stay up to date
  const hooksSrc = path.join(harnessDir, 'scripts', 'hooks');
  const hooksDest = path.join(claudeDir, 'hooks', 'toga');
  let hooksCount = 0;
  if (fs.existsSync(hooksSrc)) {
    try {
      copyDir(hooksSrc, hooksDest);
      hooksCount = fs.readdirSync(hooksDest).filter((f) => f.endsWith('.js')).length;
    } catch (e) { errors.push('hooks: ' + e.message); }
  }

  // knowledge.js CLI — always overwrite so it stays current
  const knowledgeJsSrc = path.join(harnessDir, 'knowledge.js');
  if (fs.existsSync(knowledgeJsSrc)) {
    try { fs.copyFileSync(knowledgeJsSrc, path.join(claudeDir, 'knowledge.js')); }
    catch (e) { errors.push('knowledge.js: ' + e.message); }
  }

  // Settings — merge (additive only, never removes existing hooks or permissions)
  const ok = mergeSettings(claudeDir, harnessDir);
  console.log('  ' + (ok ? '✓' : '✗') + ' Hooks     (' + hooksCount + ' scripts in .claude/hooks/toga/, settings.json merged)');

  // Contexts — mode context files (dev/research/review), update if changed
  const contextsSrc = path.join(harnessDir, 'contexts');
  const contextsDest = path.join(claudeDir, 'contexts', 'toga');
  if (fs.existsSync(contextsSrc)) {
    let contextsStats = { added: 0, updated: 0, unchanged: 0 };
    try { contextsStats = copyDir(contextsSrc, contextsDest, { updateIfChanged: true }); }
    catch (e) { errors.push('contexts: ' + e.message); }
    console.log('  ✓ Contexts  (' + countMd(contextsDest) + '): ' + fmtStats(contextsStats));
  }

  // MCP example — update if changed so teammates get new server configs
  const mcpSrc = path.join(harnessDir, 'mcp-configs', 'mcp-servers.json');
  const mcpDest = path.join(claudeDir, 'mcp-servers.example.json');
  if (fs.existsSync(mcpSrc)) {
    try {
      const firstInstall = !fs.existsSync(mcpDest);
      const incoming = fs.readFileSync(mcpSrc);
      if (firstInstall || !incoming.equals(fs.readFileSync(mcpDest))) {
        fs.copyFileSync(mcpSrc, mcpDest);
        console.log('  ✓ MCP       (.claude/mcp-servers.example.json ' + (firstInstall ? 'created' : 'updated') + ' — merge into .mcp.json to enable)');
      }
    } catch (e) { errors.push('mcp: ' + e.message); }
  }

  // Knowledge — git repo if available (has team-captured docs), else npm bundle
  // .claude/knowledge/ is a mirror — update when content changes so teammates get captured docs
  const knowledgeDest = path.join(claudeDir, 'knowledge');
  let knowledgeStats = { added: 0, updated: 0, unchanged: 0 };

  // Always install npm bundle knowledge first — this guarantees every file published
  // in this version is present, regardless of what the git repo contains.
  const bundleKnowledgeSrc = path.join(PACKAGE_ROOT, 'knowledge');
  if (fs.existsSync(bundleKnowledgeSrc)) {
    try { knowledgeStats = copyDir(bundleKnowledgeSrc, knowledgeDest, { updateIfChanged: true }); }
    catch (e) { errors.push('knowledge (bundle): ' + e.message); }
  }

  // Then overlay git repo on top — picks up any docs newer than this npm bundle.
  // Git is additive only: it never removes files the bundle already installed.
  if (knowledgeDir !== PACKAGE_ROOT) {
    const gitKnowledgeSrc = path.join(knowledgeDir, 'knowledge');
    if (fs.existsSync(gitKnowledgeSrc)) {
      try {
        const gitStats = copyDir(gitKnowledgeSrc, knowledgeDest, { updateIfChanged: true });
        knowledgeStats.added += gitStats.added;
        knowledgeStats.updated += gitStats.updated;
      } catch (e) { /* non-fatal — bundle layer already installed */ }
    }
  }
  console.log('  ✓ Knowledge (' + countMd(knowledgeDest) + ' docs): ' + fmtStats(knowledgeStats));

  // registry.json — the repo↔project↔framework map every skill depends on.
  // Force-sync explicitly from the newest source (git if pulled, else bundle) so a
  // partial knowledge copy can never leave a machine without/with a stale registry.
  const registrySrc = path.join(knowledgeDir, 'knowledge', 'registry.json');
  const registryDest = path.join(knowledgeDest, 'registry.json');
  if (fs.existsSync(registrySrc)) {
    try {
      fs.copyFileSync(registrySrc, registryDest);
      let repoCount = 0;
      try {
        const reg = JSON.parse(fs.readFileSync(registryDest, 'utf8'));
        repoCount = Array.isArray(reg) ? reg.length : 0;
      } catch (e) { /* safe: count is display only; registry file was already copied */ }
      console.log('  ✓ Registry  (' + repoCount + ' repos): synced from ' + (knowledgeDir !== PACKAGE_ROOT ? 'git repo' : 'npm bundle'));
    } catch (e) { errors.push('registry.json: ' + e.message); }
  } else {
    errors.push('registry.json: missing from source ' + registrySrc);
    console.log('  ✗ Registry  MISSING from source — /start will not work. Re-run: npm cache clean --force && npx toga-ai@latest');
  }

  // CLAUDE.md
  const action = updateClaudeMd(projectRoot, skillNames, harnessDir, 'npm bundle v' + bundleVersion);
  console.log('  ✓ CLAUDE.md ' + action);

  // Write version marker so /start can detect stale installs
  try { fs.writeFileSync(path.join(claudeDir, 'toga-ai.version'), bundleVersion, 'utf8'); } catch (e) { /* safe: marker only feeds stale-install warnings; install itself succeeded */ }

  // ECC global integration — detect and report
  const eccPath = detectEcc();
  if (eccPath) {
    let eccAgentCount = 0;
    try { eccAgentCount = fs.readdirSync(path.join(eccPath, 'agents')).filter((f) => f.endsWith('.md')).length; } catch {}
    console.log('  ✓ ECC       (detected — ' + (eccAgentCount || '200+') + ' specialist agents supercharging TOGA workflows)');
  } else {
    console.log('  ⚠ ECC       (not found — install globally for 200+ specialist agents)');
    console.log('              Run: claude plugin add ecc   OR   npx ecc-universal');
  }

  console.log('');
  console.log('═════════════════════════════════════════════');
  console.log('  WHAT TO DO NEXT — your first session');
  console.log('═════════════════════════════════════════════');
  console.log('');
  console.log('  STEP 1  Open Claude Code in this project folder');
  console.log('          ┌─────────────────────────────────┐');
  console.log('          │  claude                         │');
  console.log('          └─────────────────────────────────┘');
  console.log('          (or open it from your IDE — VS Code, JetBrains, etc.)');
  console.log('');
  console.log('  STEP 2  Type this FIRST — every single session, no exceptions:');
  console.log('          ┌─────────────────────────────────┐');
  console.log('          │  /start TRUE-1234               │');
  console.log('          └─────────────────────────────────┘');
  console.log('          Use your ClickUp ticket id. It reads the ticket and loads');
  console.log('          the team knowledge base and past team decisions.');
  console.log('          Without it, Claude starts with zero context.');
  console.log('');
  console.log('  STEP 3  Work normally — just talk to Claude:');
  console.log('          "Add a refund endpoint to the orders controller"');
  console.log('          "Fix the bug in the payment worker"');
  console.log('          "Show me how to write a Framework 2.0 worker"');
  console.log('');
  console.log('          Claude will automatically:');
  console.log('          • Check your PHP follows the right framework pattern');
  console.log('          • Review SQL for injection and performance issues');
  console.log('          • Flag security problems in any PHP file you edit');
  console.log('          You don\'t need to ask — it happens in the background.');
  console.log('');
  console.log('  STEP 4  Before you close, type:');
  console.log('          ┌─────────────────────────────────┐');
  console.log('          │  /finish                        │');
  console.log('          └─────────────────────────────────┘');
  console.log('          It saves what you learned to the team knowledge base.');
  console.log('          When the ticket is done, it pushes, opens the PRs,');
  console.log('          and updates the ticket.');
  console.log('');
  console.log('─────────────────────────────────────────────');
  console.log('  OTHER COMMANDS (use when needed)');
  console.log('─────────────────────────────────────────────');
  console.log('');
  console.log('  /session-save     ← mid-session checkpoint before switching tasks');
  console.log('  /session-resume   ← pick up exactly where you left off yesterday');
  console.log('  /code-review      ← run a full security + style review on a file');
  console.log('  /php-patterns     ← show me the correct pattern for Framework 1.0/2.0');
  console.log('  /harness-audit    ← check the health of this AI setup');
  console.log('');
  console.log('─────────────────────────────────────────────');
  console.log('  UPDATING (get latest skills + team knowledge)');
  console.log('─────────────────────────────────────────────');
  console.log('');
  console.log('  npx toga-ai@latest  ← run this any time to pull updates');
  console.log('');
  console.log('═════════════════════════════════════════════');
  console.log('');

  if (errors.length > 0) {
    console.log('  ' + errors.length + ' error(s): ' + errors.join('; '));
    console.log('');
    process.exitCode = 1;
  }
}

main();
