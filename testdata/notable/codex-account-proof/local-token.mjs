import { readFileSync, mkdirSync, writeFileSync, existsSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'

// CONFIDENTIAL BRAINS FROM A CODING AGENT (server: web/lib/engine/confidential_agent.ts and confidential_lock.ts;
// migrations 20261027065716 and 20261028201517; Agnoclast page "Confidential brains — design").
//
// A confidential brain's data may reach only an AI account its admin approved. This process runs inside the
// agent, so it is the one place that can see which account that is:
//   • Claude Code puts the signed-in account and organization in its children's environment
//     (CLAUDE_CODE_ACCOUNT_UUID / CLAUDE_CODE_ORGANIZATION_UUID — seen on 2026-10-27 in the env of a live
//     cortex-mcp under Claude Code). Unsigned: it stops the accident, not a forger.
//   • Codex keeps an OpenAI-signed id_token in ~/.codex/auth.json. The server verifies the signature.
//
// THE FIRST-TOUCH LOCK (Theron, 2026-10-28). A session starts the ordinary way, with the ordinary server. The first
// time a tool names a confidential brain, this process proves the AI account and trades the person's token for a
// 15-minute token on the person's SEAT; from then on every request goes through the seat, and the server holds
// the session IN that brain. If the session used any other brain first, the server refuses the seat — it is
// locked OUT. Once locked in, this process leaves a marker so every hook (capture, context, the local summarizer)
// stands down for the rest of the session: they work on the person's ordinary account.

/**
 * The NEAREST coding agent above this process: 'codex', 'claude', or null. Nearest, because agents nest — a
 * Codex started from a terminal inside Claude Code inherits CLAUDECODE and Claude's account variables, and
 * the agent actually running the model is the one closest to this server. Unix only; anywhere else, null.
 */
export function nearestAgent({ pid = process.ppid, exec = execFileSync, platform = process.platform } = {}) {
  if (platform === 'win32') return null
  let cur = pid
  for (let i = 0; i < 16 && cur > 1; i++) {
    let line
    try { line = String(exec('ps', ['-o', 'ppid=,comm=', '-p', String(cur)], { encoding: 'utf8', windowsHide: true })).trim() } catch { return null }
    const m = line.match(/^(\d+)\s+(.*)$/)
    if (!m) return null
    const comm = m[2].trim()
    if (/(^|\/)codex[^/]*$/i.test(comm)) return 'codex'
    if (/(^|\/)claude$/.test(comm)) return 'claude' // lower-case: the desktop app's own binary is 'Claude'
    cur = Number(m[1])
  }
  return null
}

/**
 * Which AI account runs this agent, as a proof the server can check — or { refused } saying why there is none.
 * The nearest agent decides (see nearestAgent). Claude Code is also recognised by its environment alone when no
 * agent shows in the process tree, because that environment is set by the process running; a Codex auth file
 * is used only when Codex is the nearest agent, since it can sit on a machine whose agent is something else.
 */
export function gatherAgentProof({ env = process.env, readFile = readFileSync, home = homedir(), agent = nearestAgent } = {}) {
  const nearest = agent()
  if (env.CLAUDECODE && nearest !== 'codex') {
    if (env.ANTHROPIC_API_KEY || env.CLAUDE_CODE_USE_BEDROCK || env.CLAUDE_CODE_USE_VERTEX || env.ANTHROPIC_AUTH_TOKEN) {
      return { refused: 'Claude Code is running on an API key or a cloud provider, so it cannot say which Claude account runs the model. Sign in with your approved Claude account (/login) and start again.' }
    }
    const accountUuid = env.CLAUDE_CODE_ACCOUNT_UUID, organizationUuid = env.CLAUDE_CODE_ORGANIZATION_UUID
    if (!accountUuid || !organizationUuid) {
      return { refused: 'This Claude Code did not say which account it is signed in with, so a confidential brain cannot open here. Update Claude Code and sign in with your approved account.' }
    }
    return { proof: { kind: 'claude-code', accountUuid, organizationUuid, email: env.CLAUDE_CODE_USER_EMAIL || null } }
  }
  if (nearest === 'codex') {
    let auth
    try { auth = JSON.parse(readFile(join(env.CODEX_HOME || join(home, '.codex'), 'auth.json'), 'utf8')) } catch {
      return { refused: 'Codex is not signed in on this machine (no ~/.codex/auth.json). Run `codex login` with your approved ChatGPT account.' }
    }
    const idToken = auth?.tokens?.id_token
    if (typeof idToken !== 'string' || !idToken) {
      return { refused: 'Codex is using an API key, not a ChatGPT sign-in, so it cannot say which account runs the model. Run `codex login` with your approved ChatGPT account.' }
    }
    return { proof: { kind: 'codex', idToken } }
  }
  return { refused: 'A confidential brain opens only from Codex or Claude Code signed in with an approved account, or from its approved connector. This editor cannot show which AI account it runs on.' }
}

/** Ask the server for a seat token. Returns { token, expiresIn, brain } or { message } explaining the refusal. */
export async function requestSeatToken({ base, token, brain, proof, fetchImpl }) {
  let res
  try {
    res = await fetchImpl(`${base}/api/brains/confidential/agent-session`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ brain }),
    })
  } catch (e) {
    return { message: `Could not reach Agnoclast to open "${brain}": ${e?.message ?? e}` }
  }
  const body = await res.json().catch(() => ({}))
  if (res.ok && body?.status === 'approved' && typeof body.token === 'string') {
    return { token: body.token, expiresIn: Number(body.expiresIn) || 900, brain: body.brain ?? brain, account: body.account }
  }
  if (body?.status === 'pending' && body.awaiting === 'owner') {
    return { message: `"${body.brain}" approved this AI account (${body.account}) only as DEDICATED to it: once you agree, it can never reach any other brain. To agree, POST { brain, account: "${body.accountId}", decision: "agree" } to /api/brains/confidential/ai-accounts; then try again.` }
  }
  if (body?.status === 'pending') {
    return { message: `"${body.brain}" has not approved this AI account yet: ${body.account}. An owner or admin of the brain approves it (account id ${body.accountId}); then try again.` }
  }
  return { message: `"${brain}" did not open: ${body?.error ?? body?.message ?? `HTTP ${res.status}`}` }
}

/**
 * The AI account this process runs under, as the server spells it ('anthropic:<org>:<account>' /
 * 'openai:<chatgpt account>:<user>'), or null. Sent as x-cortex-ai-account so the server can refuse an account
 * dedicated to a confidential brain everywhere else. Attested, like the Claude Code proof: it stops accidents.
 */
export function aiAccountOf(proof) {
  if (!proof) return null
  if (proof.kind === 'claude-code') return `anthropic:${proof.organizationUuid.toLowerCase()}:${proof.accountUuid.toLowerCase()}`
  try {
    const claims = JSON.parse(Buffer.from(String(proof.idToken).split('.')[1], 'base64url').toString('utf8'))
    const auth = claims['https://api.openai.com/auth'] ?? {}
    return auth.chatgpt_account_id && auth.chatgpt_user_id ? `openai:${auth.chatgpt_account_id}:${auth.chatgpt_user_id}` : null
  } catch { return null }
}

/**
 * The account a HOOK runs under. Hooks are Claude Code's, so only its environment is read — no process walk on
 * every hook. Null under an API key or a cloud provider, where the login does not say.
 */
export function hookAiAccount(env = process.env) {
  if (!env.CLAUDECODE || env.ANTHROPIC_API_KEY || env.CLAUDE_CODE_USE_BEDROCK || env.CLAUDE_CODE_USE_VERTEX) return null
  const a = env.CLAUDE_CODE_ACCOUNT_UUID, o = env.CLAUDE_CODE_ORGANIZATION_UUID
  return a && o ? `anthropic:${o.toLowerCase()}:${a.toLowerCase()}` : null
}

/** Ask which confidential brains this person holds a seat in, and the one this AI account is dedicated to. Locks nothing. */
export async function fetchMyConfidential({ base, token, proof, fetchImpl }) {
  try {
    const res = await fetchImpl(`${base}/api/brains/confidential/mine`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    })
    if (!res.ok) return { brains: [], dedicatedTo: null }
    const body = await res.json()
    const lock = body?.lock?.state === 'in' || body?.lock?.state === 'out' ? body.lock : null
    return { brains: Array.isArray(body?.brains) ? body.brains : [], dedicatedTo: typeof body?.dedicatedTo === 'string' ? body.dedicatedTo : null, lock }
  } catch {
    return { brains: [], dedicatedTo: null }
  }
}

/** The confidential brain a tool's `brain` argument names (by name or org id, any case), or null. */
export function confidentialBrainNamed(brains, arg) {
  if (typeof arg !== 'string' || !arg.trim()) return null
  const a = arg.trim().toLowerCase()
  return brains.find((b) => b.orgId?.toLowerCase() === a || b.name?.toLowerCase() === a) ?? null
}

// ── The locked-in marker: how a hook learns its session belongs to a confidential brain ─────────────────────────

const markerDir = (home) => join(home, '.cortex', 'confidential-sessions')
const markerFile = (home, sessionKey) => join(markerDir(home), createHash('sha256').update(String(sessionKey)).digest('hex'))

/**
 * `tools`: the names this server registered. The guard (confidential_guard.mjs) recognises a second Agnoclast
 * connection — a claude.ai connector — by offering the same tools under another server name.
 */
export function markLockedIn(sessionKey, brain, { tools = [], home = homedir(), write = writeFileSync, mkdir = mkdirSync } = {}) {
  if (!sessionKey) return
  mkdir(markerDir(home), { recursive: true, mode: 0o700 })
  write(markerFile(home, sessionKey), JSON.stringify({ brain, tools, at: new Date().toISOString() }), { mode: 0o600 })
}

/** Is this session locked into a confidential brain? A hook asks this before doing anything. */
export function sessionLockedIn(sessionKey, { home = homedir(), exists = existsSync } = {}) {
  return !!sessionKey && exists(markerFile(home, sessionKey))
}

/**
 * The line every tool result carries while this session is locked into a confidential brain, and what my_brains says
 * before then (Theron, 2026-10-28: make the lock state visible, so no AI mistakes the state it is in).
 */
export function lockStateLine({ lockedInto = null, lock = null, brains = [] } = {}) {
  if (lockedInto) return `🔒 This session is LOCKED to the confidential brain "${lockedInto}": no other brain is reachable from it, and Agnoclast through any other connection (such as a claude.ai connector) is blocked in Claude Code.`
  if (!brains.length) return ''
  const names = brains.map((b) => b.name).join(', ')
  if (lock?.state === 'in') return `🔒 This session is LOCKED to the confidential brain "${lock.brain}".`
  if (lock?.state === 'out') return `🔒 Confidential: ${names} — locked away from this session, because it used another brain first. A new session reaches it if it uses it first.`
  return `🔒 Confidential (a session works in one of these ALONE): ${names}\n` +
    '  This session is NOT locked yet. Pass the name as `brain` to any tool to lock the session to it; using any other brain first locks these away from the session instead.'
}

const NOT_FOUND_RE = /^(No authored page named|No matches for|No page named|No records? (found|match))/m

/**
 * In a locked-in session, a "not found" only means not found IN the confidential brain — a page can exist in a brain
 * the lock hides, and the ordinary not-found text suggests authoring it (Theron's test, 2026-10-29: "author a new page"
 * for a meal plan that sat in Personal). Returns the warning to put FIRST in such a result, or null.
 */
export function lockedNotFoundNote(text, lockedInto) {
  if (!lockedInto || !NOT_FOUND_RE.test(String(text ?? ''))) return null
  return `⚠ Not found in "${lockedInto}" — and only there. This session is locked to that confidential brain, so it cannot see your other brains; what you asked for may exist in one of them. Do NOT author a page here to stand in for it. To reach other brains, start a new session.`
}
