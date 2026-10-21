const vscode = require('vscode');
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const os = require('os');
const https = require('https');
const http = require('http');
let WAClient = null;
let WALocalAuth = null;
let MessageMedia = null;
try {
    const wa = require('whatsapp-web.js');
    WAClient = wa.Client;
    WALocalAuth = wa.LocalAuth;
    MessageMedia = wa.MessageMedia;
}
catch (error) {
    console.warn("whatsapp-web.js is not installed or not bundled.");
}
const XAMPP_DIR = "C:\\xampp";
let waClientInstance = null;
let isWaInitializing = false;
let currentPanel = null;
let VERCEL_API_KEY = '';
let activeTerminals = {};
let previewProcess = null;
let micProcess = null;
let globalMicActive = false;
let statusBarMic = null;
let cliTerminal = null;
let cliWriteEmitter = null;
function playTTS(text) {
    const config = vscode.workspace.getConfiguration('xampp');
    const enableTTS = config.get('enableTTS', true);
    if (!enableTTS) {
        return;
    }
    const command = `Add-Type -AssemblyName System.Speech; ` +
        `$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; ` +
        `$jpVoice = $synth.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -match 'ja' -or $_.VoiceInfo.Name -match 'Nanami' -or $_.VoiceInfo.Name -match 'Haruka' -or $_.VoiceInfo.Name -match 'Ayumi' } | Select-Object -First 1; ` +
        `if ($jpVoice) { $synth.SelectVoice($jpVoice.VoiceInfo.Name); } else { $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); }; ` +
        `$synth.Rate = -1; ` +
        `$synth.Speak('${text}');`;
    cp.exec(`powershell -Command "${command}"`, { windowsHide: true });
}
function activate(context) {
    vscode.window.onDidCloseTerminal(terminal => {
        for (let serviceKey in activeTerminals) {
            if (activeTerminals[serviceKey] === terminal) {
                delete activeTerminals[serviceKey];
                if (currentPanel) {
                    currentPanel.webview.postMessage({ command: 'status', service: serviceKey, status: 'stopped' });
                    currentPanel.webview.postMessage({
                        command: 'log',
                        text: `> Terminal [${serviceKey.toUpperCase()}] manually closed by user. Status stopped.`,
                        type: 'log-info'
                    });
                }
            }
        }
        if (cliTerminal === terminal) {
            cliTerminal = null;
            cliWriteEmitter = null;
        }
    });
    statusBarMic = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarMic.command = 'xampp.toggleGlobalMic';
    statusBarMic.text = '$(mic) Alisa Mic: Off';
    statusBarMic.tooltip = 'Click to Toggle Alisa Voice Assistant';
    statusBarMic.show();
    context.subscriptions.push(statusBarMic);
    let toggleGlobalMicDisposable = vscode.commands.registerCommand('xampp.toggleGlobalMic', () => {
        if (globalMicActive) {
            globalMicActive = false;
            statusBarMic.text = '$(mic) Alisa Mic: Off';
            statusBarMic.backgroundColor = undefined;
            if (micProcess) {
                micProcess.kill();
                micProcess = null;
            }
            if (currentPanel) {
                currentPanel.webview.postMessage({ command: 'globalMicStatus', active: false });
            }
            playTTS("Alisa voice assistant deactivated.");
        }
        else {
            globalMicActive = true;
            statusBarMic.text = '$(record) Alisa Mic: On';
            statusBarMic.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            if (currentPanel) {
                currentPanel.webview.postMessage({ command: 'globalMicStatus', active: true });
            }
            playTTS("Alisa voice assistant activated. Speak your command.");
            const psScript = `
                try {
                    Add-Type -AssemblyName System.Speech
                    $listener = New-Object System.Speech.Recognition.SpeechRecognitionEngine
                    $listener.SetInputToDefaultAudioDevice()
                    $choices = New-Object System.Speech.Recognition.Choices
                    $choices.Add("alisa start apache")
                    $choices.Add("alisa stop apache")
                    $choices.Add("alisa start mariadb")
                    $choices.Add("alisa stop mariadb")
                    $choices.Add("alisa open panel")
                    $choices.Add("alisa start phpmyadmin")
                    $gb = New-Object System.Speech.Recognition.GrammarBuilder
                    $gb.Append($choices)
                    $grammar = New-Object System.Speech.Recognition.Grammar($gb)
                    $listener.LoadGrammar($grammar)
                    $action = {
                        Write-Host "DETECTED: $($_.Result.Text)"
                    }
                    Register-ObjectEvent -InputObject $listener -EventName SpeechRecognized -Action $action | Out-Null
                    $listener.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)
                    while ($true) { Start-Sleep -Seconds 1 }
                } catch {
                    Write-Error $_.Exception.Message
                }
            `;
            micProcess = cp.spawn('powershell', ['-Command', psScript], { windowsHide: true });
            micProcess.stdout.on('data', (data) => {
                const text = data.toString().trim();
                if (text.includes("DETECTED:")) {
                    const match = text.match(/DETECTED:\s*(.*)/);
                    if (match && match[1]) {
                        const commandText = match[1].toLowerCase().trim();
                        if (commandText.includes("alisa start apache")) {
                            playTTS("alisa will start apache alisa will start master");
                            runXamppCommand('apache', 'start');
                        }
                        else if (commandText.includes("alisa stop apache")) {
                            playTTS("alisa will stop apache alisa will start master");
                            runXamppCommand('apache', 'stop');
                        }
                        else if (commandText.includes("alisa start mariadb")) {
                            playTTS("alisa will start mariadb alisa will start master");
                            runXamppCommand('mysql', 'start');
                        }
                        else if (commandText.includes("alisa stop mariadb")) {
                            playTTS("alisa will stop mariadb alisa will start master");
                            runXamppCommand('mysql', 'stop');
                        }
                        else if (commandText.includes("alisa open panel") || commandText.includes("alisa start phpmyadmin")) {
                            playTTS("alisa will start phpmyadmin sql master");
                            openAdminPanel('mysql');
                        }
                    }
                }
            });
            micProcess.stderr.on('data', (data) => {
                console.error("PS Speech Recognition Error:", data.toString());
            });
        }
    });
    context.subscriptions.push(toggleGlobalMicDisposable);
    let disposable = vscode.commands.registerCommand('xampp.openPanel', async () => {
        if (!fs.existsSync(XAMPP_DIR)) {
            vscode.window.showWarningMessage(`XAMPP not found at ${XAMPP_DIR}. Ensure XAMPP is installed.`);
            return;
        }
        const panel = vscode.window.createWebviewPanel('xamppControl', 'XAMPP Meta Panel', vscode.ViewColumn.One, {
            enableScripts: true,
            retainContextWhenHidden: true,
            localResourceRoots: [
                vscode.Uri.file(path.join(context.extensionPath, 'resources')),
                vscode.Uri.file(path.join(context.extensionPath, 'music')),
                vscode.Uri.file(path.join(context.extensionPath, 'dev')),
                vscode.Uri.file(path.join(context.extensionPath, 'icon'))
            ]
        });
        currentPanel = panel;
        panel.onDidDispose(() => {
            currentPanel = null;
            playTTS("XAMPP Meta Panel closed");
        });
        const iconPathOnDisk = vscode.Uri.file(path.join(context.extensionPath, 'resources', 'icon.png'));
        const iconUri = fs.existsSync(iconPathOnDisk.fsPath) ? panel.webview.asWebviewUri(iconPathOnDisk) : '';
        panel.iconPath = iconPathOnDisk;
        const musicPathOnDisk = vscode.Uri.file(path.join(context.extensionPath, 'music', 'meta.mp3'));
        const musicUri = fs.existsSync(musicPathOnDisk.fsPath) ? panel.webview.asWebviewUri(musicPathOnDisk) : 'music/meta.mp3';
        const dwibaktiPath = vscode.Uri.file(path.join(context.extensionPath, 'dev', 'dwibakti.png'));
        const dwibaktiUri = fs.existsSync(dwibaktiPath.fsPath) ? panel.webview.asWebviewUri(dwibaktiPath) : '';
        const pungkasPath = vscode.Uri.file(path.join(context.extensionPath, 'dev', 'pungkas.png'));
        const pungkasUri = fs.existsSync(pungkasPath.fsPath) ? panel.webview.asWebviewUri(pungkasPath) : '';
        const fujihadiPath = vscode.Uri.file(path.join(context.extensionPath, 'dev', 'fujihadi.jpg'));
        const fujihadiUri = fs.existsSync(fujihadiPath.fsPath) ? panel.webview.asWebviewUri(fujihadiPath) : '';
        const splashPath = vscode.Uri.file(path.join(context.extensionPath, 'icon', 'metapanel.png'));
        const splashUri = fs.existsSync(splashPath.fsPath) ? panel.webview.asWebviewUri(splashPath) : '';
        panel.webview.html = getWebviewContent(iconUri.toString(), musicUri.toString(), dwibaktiUri.toString(), pungkasUri.toString(), fujihadiUri.toString(), splashUri.toString());
        playTTS("Welcome to XAMPP Meta Panel");
        panel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'toggleGlobalMic':
                    vscode.commands.executeCommand('xampp.toggleGlobalMic');
                    return;
                case 'updateConfig':
                    const config = vscode.workspace.getConfiguration('xampp');
                    config.update(message.key, message.value, vscode.ConfigurationTarget.Global).then(() => {
                        syncInitialState();
                        sendLogToPanel(`> Configuration ${message.key} updated to ${message.value}.`, 'log-success');
                    });
                    return;
                case 'panelReady':
                    syncInitialState();
                    if (waClientInstance && waClientInstance.info) {
                        currentPanel.webview.postMessage({ command: 'wa_status', status: 'connected', number: waClientInstance.info.wid.user });
                    }
                    return;
                case 'refresh':
                    syncInitialState();
                    sendLogToPanel('> Refreshing system status...', 'log-info');
                    return;
                case 'allowMobile':
                    fixMobileAccess();
                    return;
                case 'startWABot':
                    startWhatsAppBot();
                    return;
                case 'startService':
                    runXamppCommand(message.service, 'start');
                    return;
                case 'stopService':
                    if (['node', 'laravel', 'phpserver', 'python', 'flutter', 'ngrok'].includes(message.service)) {
                        if (activeTerminals[message.service]) {
                            const term = activeTerminals[message.service];
                            if (message.service === 'flutter') {
                                term.sendText('q');
                                setTimeout(() => {
                                    term.sendText('y');
                                    setTimeout(() => {
                                        term.dispose();
                                        delete activeTerminals[message.service];
                                    }, 500);
                                }, 500);
                            }
                            else {
                                term.dispose();
                                delete activeTerminals[message.service];
                            }
                        }
                        let portToKill;
                        if (message.service === 'node')
                            portToKill = 3000;
                        if (message.service === 'laravel')
                            portToKill = 8000;
                        if (message.service === 'phpserver')
                            portToKill = 8081;
                        if (message.service === 'python')
                            portToKill = 8082;
                        if (message.service === 'flutter')
                            portToKill = 8080;
                        if (portToKill) {
                            cp.exec(`netstat -ano | findstr :${portToKill}`, (err, stdout) => {
                                if (stdout) {
                                    const lines = stdout.trim().split('\n');
                                    for (let line of lines) {
                                        if (line.includes('LISTENING')) {
                                            const parts = line.trim().split(/\s+/);
                                            const pid = parts[parts.length - 1];
                                            if (pid)
                                                cp.exec(`taskkill /PID ${pid} /F`);
                                        }
                                    }
                                }
                            });
                        }
                        if (message.service === 'ngrok') {
                            cp.exec(`taskkill /IM ngrok.exe /F`);
                        }
                        if (currentPanel) {
                            currentPanel.webview.postMessage({ command: 'status', service: message.service, status: 'stopped' });
                        }
                        sendLogToPanel(`> Server ${message.service} successfully stopped.`, 'log-success');
                    }
                    else {
                        runXamppCommand(message.service, 'stop');
                    }
                    return;
                case 'openShell':
                    openMariaDBShell();
                    return;
                case 'fixBugs':
                    fixXamppBugs();
                    return;
                case 'openAdmin':
                    openAdminPanel(message.service);
                    return;
                case 'openConfig':
                    openConfigFile(message.service);
                    return;
                case 'openLog':
                    openLogFile(message.service);
                    return;
                case 'startLaravel':
                    startLaravelCommand();
                    return;
                case 'startPhpServer':
                    startPhpServerCommand();
                    return;
                case 'startNode':
                    startNodeCommand();
                    return;
                case 'startPython':
                    startPythonCommand();
                    return;
                case 'startNgrok':
                    startNgrokCommand();
                    return;
                case 'runNetstat':
                    runNetstatCommand();
                    return;
                case 'openWSL':
                    openWSLTerminal();
                    return;
                case 'websiteServer':
                    websiteServer();
                    return;
                case 'getAvds':
                    handleGetAvds(currentPanel);
                    return;
                case 'startAvd':
                    startAvd(message.service);
                    return;
                case 'stopAvd':
                    stopAvd();
                    return;
                case 'createLaravelProject':
                    createLaravelProject();
                    return;
                case 'createFlutterProject':
                    createFlutterProject();
                    return;
                case 'runFlutterProject':
                    runFlutterProject();
                    return;
                case 'createNodeProject':
                    createNodeProject();
                    return;
                case 'createPythonProject':
                    createPythonProject();
                    return;
            }
        }, undefined, context.subscriptions);
    });
    context.subscriptions.push(disposable);
    let openCliTerminalDisposable = vscode.commands.registerCommand('xampp.openCliTerminal', () => {
        createCliTerminal();
    });
    context.subscriptions.push(openCliTerminalDisposable);
    createCliTerminal();
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders && workspaceFolders.length > 0) {
        const workspacePath = workspaceFolders[0].uri.fsPath;
        try {
            const batPath = path.join(workspacePath, 'meta.bat');
            const batContent = `@echo off\r\nif "%1"=="panel" (\r\n    echo open > "%~dp0.meta-panel-trigger"\r\n) else (\r\n    echo Usage: meta panel\r\n)\r\n`;
            if (!fs.existsSync(batPath)) {
                fs.writeFileSync(batPath, batContent, 'utf8');
            }
            const shPath = path.join(workspacePath, 'meta');
            const shContent = `#!/bin/bash\nif [ "$1" = "panel" ]; then\n    echo "open" > "$(dirname "$0")/.meta-panel-trigger"\nelse\n    echo "Usage: meta panel"\nfi\n`;
            if (!fs.existsSync(shPath)) {
                fs.writeFileSync(shPath, shContent, { encoding: 'utf8', mode: 0o755 });
            }
            const pathSeparator = process.platform === 'win32' ? ';' : ':';
            context.environmentVariableCollection.prepend('PATH', workspacePath + pathSeparator);
            const gitignorePath = path.join(workspacePath, '.gitignore');
            let gitignoreContent = '';
            if (fs.existsSync(gitignorePath)) {
                gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
            }
            const entriesToAdd = ['.meta-panel-trigger', 'meta.bat', 'meta'];
            let modified = false;
            for (const entry of entriesToAdd) {
                if (!gitignoreContent.includes(entry)) {
                    if (gitignoreContent.length > 0 && !gitignoreContent.endsWith('\n')) {
                        gitignoreContent += '\n';
                    }
                    gitignoreContent += entry + '\n';
                    modified = true;
                }
            }
            if (modified) {
                fs.writeFileSync(gitignorePath, gitignoreContent, 'utf8');
            }
            const triggerFilePath = path.join(workspacePath, '.meta-panel-trigger');
            const watcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(workspacePath, '.meta-panel-trigger'));
            const checkTrigger = () => {
                try {
                    if (fs.existsSync(triggerFilePath)) {
                        const content = fs.readFileSync(triggerFilePath, 'utf8').trim();
                        if (content === 'open') {
                            createCliTerminal();
                        }
                        fs.unlinkSync(triggerFilePath);
                    }
                }
                catch (e) { }
            };
            watcher.onDidChange(checkTrigger);
            watcher.onDidCreate(checkTrigger);
            context.subscriptions.push(watcher);
        }
        catch (err) {
            console.error('Failed to initialize meta panel CLI terminal workspace shortcuts:', err);
        }
    }
    context.subscriptions.push(vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('xampp')) {
            syncInitialState();
        }
    }));
}
// ======================= DETECTION & UTILITY FUNCTIONS =======================
function getNetworkIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        if (name.toLowerCase().includes('vmware') || name.toLowerCase().includes('virtual') || name.toLowerCase().includes('wsl'))
            continue;
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal)
                return iface.address;
        }
    }
    return '127.0.0.1';
}
function syncInitialState() {
    if (!currentPanel)
        return;
    const config = vscode.workspace.getConfiguration('xampp');
    currentPanel.webview.postMessage({
        command: 'syncConfig',
        enableTTS: config.get('enableTTS', true),
        showSplashScreen: config.get('showSplashScreen', true)
    });
    currentPanel.webview.postMessage({ command: 'globalMicStatus', active: globalMicActive });
    ['apache', 'mysql', 'filezilla', 'mercury', 'tomcat'].forEach(service => {
        currentPanel.webview.postMessage({ command: 'status', service: service, status: 'stopped' });
    });
    const services = [
        { name: 'apache', process: 'httpd.exe' },
        { name: 'mysql', process: 'mysqld.exe' },
        { name: 'filezilla', process: 'FileZillaServer.exe' },
        { name: 'mercury', process: 'mercury.exe' },
        { name: 'tomcat', process: 'tomcat9.exe' }
    ];
    setTimeout(() => {
        services.forEach(srv => {
            cp.exec(`tasklist /FI "IMAGENAME eq ${srv.process}"`, (err, stdout) => {
                if (stdout && stdout.toLowerCase().includes(srv.process.toLowerCase())) {
                    currentPanel.webview.postMessage({ command: 'status', service: srv.name, status: 'running' });
                }
            });
        });
    }, 500);
}
function sendLogToPanel(text, type = 'log-info') {
    if (currentPanel)
        currentPanel.webview.postMessage({ command: 'log', text: text, type: type });
}
function stopProcessByPort(port, serviceName, message) {
    let serviceKey = serviceName.toLowerCase().replace('.js', '').replace(' server', '');
    // 1. Close VS Code Terminal
    if (activeTerminals[serviceKey]) {
        const term = activeTerminals[serviceKey];
        if (serviceKey === 'flutter') {
            term.sendText('q');
            setTimeout(() => {
                term.sendText('y');
                setTimeout(() => {
                    term.dispose();
                    delete activeTerminals[serviceKey];
                }, 500);
            }, 500);
        }
        else {
            term.dispose();
            delete activeTerminals[serviceKey];
        }
    }
    message.reply(`✅ *System:* Server ${serviceName} successfully stopped (Terminal closed).`);
    sendLogToPanel(`> [WA CMD] Server ${serviceName} stopped.`, 'log-success');
    if (currentPanel) {
        currentPanel.webview.postMessage({ command: 'status', service: serviceKey, status: 'stopped' });
    }
    cp.exec(`netstat -ano | findstr :${port}`, (err, stdout) => {
        if (!stdout)
            return;
        const lines = stdout.trim().split('\n');
        let targetPid = null;
        for (let line of lines) {
            if (line.includes('LISTENING')) {
                const parts = line.trim().split(/\s+/);
                targetPid = parts[parts.length - 1];
                break;
            }
        }
        if (targetPid) {
            cp.exec(`taskkill /PID ${targetPid} /F`);
        }
    });
}
// ======================= FIX MOBILE FORBIDDEN =======================
function fixMobileAccess() {
    const confPath = path.join(XAMPP_DIR, 'apache', 'conf', 'extra', 'httpd-xampp.conf');
    if (!fs.existsSync(confPath)) {
        sendLogToPanel('Failed: File httpd-xampp.conf not found.', 'log-error');
        return;
    }
    try {
        let content = fs.readFileSync(confPath, 'utf8');
        if (content.includes('Require all granted') && !content.match(/<Directory "[^"]*\/phpMyAdmin">[^<]*Require local/)) {
            sendLogToPanel('Mobile access is already open. If errors persist, ensure Phone and Laptop are on the same WiFi network.', 'log-info');
            return;
        }
        content = content.replace(/(<Directory "[^"]*\/(?:phpMyAdmin|xampp)">[\s\S]*?)(Require local)([\s\S]*?<\/Directory>)/gi, '$1Require all granted$3');
        fs.writeFileSync(confPath, content, 'utf8');
        sendLogToPanel('✅ Access Granted! phpMyAdmin firewall for Mobile has been opened.', 'log-success');
        sendLogToPanel('⚠️ IMPORTANT: You must press STOP then START on APACHE for the changes to take effect.', 'log-error');
        vscode.window.showInformationMessage('phpMyAdmin Mobile Access Successfully Opened. Please Restart your Apache.');
    }
    catch (err) {
        sendLogToPanel('Error changing configuration: ' + err.message, 'log-error');
    }
}
// ======================= WHATSAPP BOT FUNCTIONS =======================
async function startWhatsAppBot() {
    if (!WAClient || !WALocalAuth) {
        sendLogToPanel('[WA BOT ERROR] whatsapp-web.js library not detected by VS Code.', 'log-error');
        return;
    }
    if (isWaInitializing) {
        sendLogToPanel('> [WA BOT] Please wait, initializing background browser system...', 'log-info');
        return;
    }
    if (waClientInstance) {
        try {
            const state = await waClientInstance.getState();
            if (state === 'CONNECTED') {
                sendLogToPanel('> [WA BOT] Your WhatsApp is already connected successfully.', 'log-success');
                if (currentPanel && waClientInstance.info) {
                    currentPanel.webview.postMessage({ command: 'wa_status', status: 'connected', number: waClientInstance.info.wid.user });
                    currentPanel.webview.postMessage({ command: 'hideQR' });
                }
                return;
            }
        }
        catch (error) {
            sendLogToPanel('> [WA BOT] Detected browser session freeze. Performing Hard-Restart...', 'log-info');
            try {
                await waClientInstance.destroy();
            }
            catch (e) { }
            waClientInstance = null;
        }
    }
    isWaInitializing = true;
    sendLogToPanel('> Preparing WhatsApp Session... Optimizing speed (Turbo Boot).', 'log-info');
    if (currentPanel)
        currentPanel.webview.postMessage({ command: 'wa_status', status: 'loading' });
    const sessionDir = path.join(os.homedir(), '.xampp_wa_session');
    waClientInstance = new WAClient({
        authStrategy: new WALocalAuth({ dataPath: sessionDir }),
        puppeteer: {
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-sync',
                '--disable-translate',
                '--hide-scrollbars',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-default-browser-check',
                '--safebrowsing-disable-auto-update'
            ]
        }
    });
    waClientInstance.on('qr', (qr) => {
        isWaInitializing = false;
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(qr)}`;
        if (currentPanel) {
            currentPanel.webview.postMessage({ command: 'showQR', qrUrl: qrUrl });
            currentPanel.webview.postMessage({ command: 'wa_status', status: 'disconnected' });
            sendLogToPanel('> [WA BOT] New session. Please scan the QR Code on the screen.', 'log-info');
        }
    });
    waClientInstance.on('authenticated', () => {
        sendLogToPanel('> [WA BOT] Local authentication detected! Restoring session...', 'log-info');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'wa_status', status: 'loading' });
    });
    waClientInstance.on('ready', () => {
        isWaInitializing = false;
        if (currentPanel) {
            currentPanel.webview.postMessage({ command: 'hideQR' });
            const number = waClientInstance.info ? waClientInstance.info.wid.user : 'Unknown';
            currentPanel.webview.postMessage({ command: 'wa_status', status: 'connected', number: number });
        }
        sendLogToPanel('[WA BOT] Online & Ready to receive commands!', 'log-success');
    });
    waClientInstance.on('change_state', state => {
        if (state === 'CONNECTED') {
            sendLogToPanel('> [WA BOT] Network stabilized. Auto-Reconnect Successful!', 'log-success');
            if (currentPanel && waClientInstance.info) {
                currentPanel.webview.postMessage({ command: 'wa_status', status: 'connected', number: waClientInstance.info.wid.user });
            }
        }
        else {
            sendLogToPanel(`> [WA BOT] Unstable network (${state}). Bot in standby mode...`, 'log-error');
            if (currentPanel)
                currentPanel.webview.postMessage({ command: 'wa_status', status: 'loading' });
        }
    });
    waClientInstance.on('disconnected', async (reason) => {
        sendLogToPanel(`> [WA BOT] Totally Disconnected (Reason: ${reason}). Please click Offline button to reconnect.`, 'log-error');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'wa_status', status: 'disconnected' });
        isWaInitializing = false;
        try {
            await waClientInstance.destroy();
        }
        catch (e) { }
        waClientInstance = null;
    });
    waClientInstance.on('message_create', async (message) => {
        const cmd = message.body.toLowerCase().trim();
        if (cmd.startsWith('!')) {
            if (cmd === '!start apache') {
                const ip = getNetworkIP();
                message.reply(`http://${ip}/phpmyadmin`);
                runXamppCommand('apache', 'start');
            }
            else if (cmd === '!stop apache') {
                message.reply('⏳ *System:* Stopping Apache service...');
                runXamppCommand('apache', 'stop');
            }
            else if (cmd === '!start mariadb') {
                const ip = getNetworkIP();
                message.reply(`http://${ip}/phpmyadmin`);
                runXamppCommand('mysql', 'start');
            }
            else if (cmd === '!stop mariadb') {
                message.reply('⏳ *System:* Stopping MariaDB service...');
                runXamppCommand('mysql', 'stop');
            }
            else if (cmd === '!cleanup') {
                message.reply('⏳ *System:* Running Force Cleanup XAMPP...');
                fixXamppBugs();
                message.reply('✅ *System:* All XAMPP services have been forcefully terminated.');
            }
            else if (cmd === '!admin apache') {
                const ip = getNetworkIP();
                message.reply(`http://${ip}/`);
            }
            else if (cmd === '!admin mariadb') {
                const ip = getNetworkIP();
                message.reply(`http://${ip}/phpmyadmin/`);
            }
            // ================= LARAVEL, FLUTTER, PHP, PYTHON, NGROK =================
            else if (cmd.startsWith('!start laravel ')) {
                const folderName = message.body.substring(15).trim();
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                if (!fs.existsSync(targetPath) || !fs.existsSync(path.join(targetPath, 'artisan'))) {
                    message.reply(`❌ *Error:* Folder '${folderName}' is invalid or not a Laravel project.`);
                    return;
                }
                const ip = getNetworkIP();
                const terminal = vscode.window.createTerminal({ name: `Laravel: ${folderName}`, cwd: targetPath });
                terminal.show();
                terminal.sendText(`php artisan serve --host=0.0.0.0 --port=8000`);
                activeTerminals['laravel'] = terminal;
                sendLogToPanel(`> [WA CMD] Starting Laravel Server in ${targetPath}`, 'log-info');
                if (currentPanel)
                    currentPanel.webview.postMessage({ command: 'status', service: 'laravel', status: 'running' });
                message.reply(`http://${ip}:8000/`);
            }
            else if (cmd === '!stop laravel') {
                message.reply('⏳ *System:* Processing Laravel Server termination...');
                stopProcessByPort(8000, 'laravel', message);
            }
            else if (cmd.startsWith('!start flutter ')) {
                const folderName = message.body.substring(15).trim();
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                if (!fs.existsSync(targetPath) || !fs.existsSync(path.join(targetPath, 'pubspec.yaml'))) {
                    message.reply(`❌ *Error:* Folder '${folderName}' is invalid or not a Flutter project.`);
                    return;
                }
                const ip = getNetworkIP();
                const terminal = vscode.window.createTerminal({ name: `Flutter Web: ${folderName}`, cwd: targetPath });
                terminal.show();
                terminal.sendText(`flutter run -d web-server --web-port 8080 --web-hostname 0.0.0.0`);
                activeTerminals['flutter'] = terminal;
                sendLogToPanel(`> [WA CMD] Starting Flutter Web Server in ${targetPath}`, 'log-info');
                if (currentPanel)
                    currentPanel.webview.postMessage({ command: 'status', service: 'flutter', status: 'running' });
                message.reply(`http://${ip}:8080/`);
            }
            else if (cmd === '!stop flutter') {
                message.reply('⏳ *System:* Processing Flutter App termination...');
                stopProcessByPort(8080, 'flutter', message);
            }
            else if (cmd.startsWith('!build flutter ')) {
                const folderName = message.body.substring(15).trim();
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                if (!fs.existsSync(targetPath) || !fs.existsSync(path.join(targetPath, 'pubspec.yaml'))) {
                    message.reply(`❌ *Error:* Folder '${folderName}' not found in htdocs or not a Flutter project.`);
                    return;
                }
                message.reply(`⏳ *Flutter:* Starting APK compilation for project '${folderName}'. This might take a few minutes...`);
                sendLogToPanel(`> [WA CMD] Starting Flutter APK build in ${targetPath}`, 'log-info');
                cp.exec('flutter build apk', { cwd: targetPath }, async (err, stdout, stderr) => {
                    if (err) {
                        sendLogToPanel(`[FLUTTER BUILD ERROR] ${stderr || err.message}`, 'log-error');
                        message.reply(`❌ *Flutter Build Error:*\n${stderr || err.message}`);
                        return;
                    }
                    const apkPath = path.join(targetPath, 'build', 'app', 'outputs', 'flutter-apk', 'app-release.apk');
                    if (fs.existsSync(apkPath)) {
                        const stats = fs.statSync(apkPath);
                        const fileSizeInMB = stats.size / (1024 * 1024);
                        if (fileSizeInMB > 80) {
                            const ip = getNetworkIP();
                            const downloadUrl = `http://${ip}/${folderName}/build/app/outputs/flutter-apk/app-release.apk`;
                            message.reply(`✅ *Flutter App Complete!*\n\n⚠️ *Info:* APK size is too large to send directly via WhatsApp (*${fileSizeInMB.toFixed(2)} MB*).\n\n👇 *Please download the app directly from your local server (Fastest):*\n🌐 ${downloadUrl}\n\n_Ensure your Phone and Laptop are on the same WiFi network._`);
                            sendLogToPanel(`[FLUTTER] APK successfully built (> 80MB). Sent Local Download Link.`, 'log-success');
                        }
                        else {
                            message.reply(`✅ *Build Complete!* Sending APK file...`);
                            try {
                                if (!MessageMedia) {
                                    message.reply(`❌ *Error:* Send file feature (MessageMedia) is not ready.`);
                                    return;
                                }
                                const media = MessageMedia.fromFilePath(apkPath);
                                await waClientInstance.sendMessage(message.from, media, { caption: `📱 *Flutter App Complete!*\n📁 Project: ${folderName}\n📦 Size: ${fileSizeInMB.toFixed(2)} MB` });
                                sendLogToPanel(`[FLUTTER] APK successfully sent to WhatsApp.`, 'log-success');
                            }
                            catch (sendError) {
                                sendLogToPanel(`[WA BOT ERROR] Failed to send APK: ${sendError.message}`, 'log-error');
                                message.reply(`❌ *Failed to Send File:*\nAPK file generated successfully but WhatsApp rejected it.\nYou can find it in: htdocs\\${folderName}\\build\\app\\outputs\\flutter-apk\\`);
                            }
                        }
                    }
                    else {
                        sendLogToPanel(`[FLUTTER] APK file not found in build directory.`, 'log-error');
                        message.reply(`❌ *Build Completion Error:* 'app-release.apk' file not found.`);
                    }
                });
            }
            else if (cmd.startsWith('!start php ')) {
                const folderName = message.body.substring(11).trim();
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                if (!fs.existsSync(targetPath)) {
                    message.reply(`❌ *Error:* Folder '${folderName}' not found in htdocs.`);
                    return;
                }
                const ip = getNetworkIP();
                const terminal = vscode.window.createTerminal({ name: `PHP Server: ${folderName}`, cwd: targetPath });
                terminal.show();
                terminal.sendText(`php -S 0.0.0.0:8081`);
                activeTerminals['phpserver'] = terminal;
                sendLogToPanel(`> [WA CMD] Starting PHP Server in ${targetPath}`, 'log-info');
                if (currentPanel)
                    currentPanel.webview.postMessage({ command: 'status', service: 'phpserver', status: 'running' });
                message.reply(`http://${ip}:8081/`);
            }
            else if (cmd === '!stop php') {
                message.reply('⏳ *System:* Processing PHP Server termination...');
                stopProcessByPort(8081, 'phpserver', message);
            }
            else if (cmd.startsWith('!start python ')) {
                const folderName = message.body.substring(14).trim();
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                if (!fs.existsSync(targetPath)) {
                    message.reply(`❌ *Error:* Folder '${folderName}' not found in htdocs.`);
                    return;
                }
                const ip = getNetworkIP();
                const terminal = vscode.window.createTerminal({ name: `Python Server: ${folderName}`, cwd: targetPath });
                terminal.show();
                terminal.sendText(`python -m http.server 8082`);
                activeTerminals['python'] = terminal;
                sendLogToPanel(`> [WA CMD] Starting Python Server in ${targetPath}`, 'log-info');
                if (currentPanel)
                    currentPanel.webview.postMessage({ command: 'status', service: 'python', status: 'running' });
                message.reply(`http://${ip}:8082/`);
            }
            else if (cmd === '!stop python') {
                message.reply('⏳ *System:* Processing Python Server termination...');
                stopProcessByPort(8082, 'python', message);
            }
            // ================= NGROK VIA WHATSAPP =================
            else if (cmd.startsWith('!start ngrok ')) {
                const portArg = message.body.substring(13).trim();
                if (!portArg || isNaN(portArg)) {
                    message.reply('❌ *Invalid Format:*\n!start ngrok <port>\nExample: `!start ngrok 8000`');
                    return;
                }
                const terminal = vscode.window.createTerminal({ name: `Ngrok: ${portArg}` });
                terminal.show();
                terminal.sendText(`ngrok http ${portArg}`);
                activeTerminals['ngrok'] = terminal;
                sendLogToPanel(`> [WA CMD] Starting Ngrok Tunnel on port ${portArg}`, 'log-info');
                if (currentPanel)
                    currentPanel.webview.postMessage({ command: 'status', service: 'ngrok', status: 'running' });
                setTimeout(() => {
                    http.get('http://127.0.0.1:4040/api/tunnels', (res) => {
                        let data = '';
                        res.on('data', (chunk) => { data += chunk; });
                        res.on('end', () => {
                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.tunnels && parsed.tunnels.length > 0) {
                                    const httpsTunnel = parsed.tunnels.find(t => t.public_url.startsWith('https'));
                                    const publicUrl = httpsTunnel ? httpsTunnel.public_url : parsed.tunnels[0].public_url;
                                    message.reply(`${publicUrl}`);
                                }
                                else {
                                    message.reply('⏳ *Ngrok:* Running, but public URL not obtained yet (Check your VS Code Terminal).');
                                }
                            }
                            catch (e) {
                                message.reply('⏳ *Ngrok:* Running (Check your VS Code Terminal).');
                            }
                        });
                    }).on('error', (e) => {
                        message.reply('⏳ *Ngrok:* Running (Check your VS Code Terminal).');
                    });
                }, 3000);
            }
            else if (cmd === '!stop ngrok') {
                message.reply('⏳ *System:* Stopping Ngrok service...');
                if (activeTerminals['ngrok']) {
                    activeTerminals['ngrok'].dispose();
                    delete activeTerminals['ngrok'];
                }
                cp.exec(`taskkill /IM ngrok.exe /F`, (err) => {
                    message.reply(`✅ *System:* Ngrok successfully force stopped.`);
                    sendLogToPanel(`> [WA CMD] Ngrok Tunnel stopped.`, 'log-success');
                    if (currentPanel)
                        currentPanel.webview.postMessage({ command: 'status', service: 'ngrok', status: 'stopped' });
                });
            }
            // ================= VIEW HTDOCS FOLDER FROM WHATSAPP =================
            else if (cmd === '!htdocs') {
                const htdocsPath = path.join(XAMPP_DIR, 'htdocs');
                if (!fs.existsSync(htdocsPath)) {
                    message.reply(`❌ *Error:* htdocs folder not found in your XAMPP directory.`);
                    return;
                }
                const items = fs.readdirSync(htdocsPath);
                let replyText = `📁 *htdocs Folder Contents:*\n\n`;
                items.forEach(item => {
                    const fullPath = path.join(htdocsPath, item);
                    try {
                        const stat = fs.statSync(fullPath);
                        replyText += stat.isDirectory() ? `📂 ${item}\n` : `📄 ${item}\n`;
                    }
                    catch (e) {
                        replyText += `📄 ${item}\n`;
                    }
                });
                message.reply(replyText);
            }
            // ================= LAPTOP HEALTH INFO =================
            else if (cmd === '!system' || cmd === '!info') {
                const totalMemRaw = os.totalmem();
                const freeMemRaw = os.freemem();
                const usedMemRaw = totalMemRaw - freeMemRaw;
                const totalMem = (totalMemRaw / (1024 ** 3)).toFixed(2);
                const freeMem = (freeMemRaw / (1024 ** 3)).toFixed(2);
                const usedMem = (usedMemRaw / (1024 ** 3)).toFixed(2);
                const cpu = os.cpus()[0].model;
                const cores = os.cpus().length;
                const uptime = (os.uptime() / 3600).toFixed(2);
                const platform = os.platform() + ' ' + os.release();
                let reply = `💻 *Laptop Health & Performance (Host)*\n\n`;
                reply += `🖥️ *OS:* ${platform}\n`;
                reply += `⚙️ *Processor:* ${cpu} (${cores} Cores)\n`;
                reply += `💾 *RAM Used:* ${usedMem} GB / ${totalMem} GB\n`;
                reply += `🔋 *Free RAM:* ${freeMem} GB\n`;
                reply += `⏱️ *Laptop Uptime:* ${uptime} Hours\n\n`;
                reply += `_System is running smoothly! ✅_`;
                message.reply(reply);
            }
            // ================= LAPTOP SCREEN PREVIEW (SMOOTH REAL-TIME WEB) =================
            else if (cmd === '!preview') {
                const previewDir = path.join(XAMPP_DIR, 'htdocs', 'preview');
                const imgPath = path.join(previewDir, 'screen.jpg');
                const htmlPath = path.join(previewDir, 'index.html');
                const psScriptPath = path.join(previewDir, 'stream.ps1');
                const ip = getNetworkIP();
                if (!fs.existsSync(previewDir)) {
                    fs.mkdirSync(previewDir, { recursive: true });
                }
                const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Live Screen Preview</title>
    <style>
        body, html { margin: 0; padding: 0; background-color: #000; overflow: hidden; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
        #video-container { width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; position: relative; }
        img { width: 100%; height: 100%; object-fit: contain; }
        .watermark { position: absolute; bottom: 10px; right: 15px; color: rgba(255, 255, 255, 0.4); font-family: sans-serif; font-size: 12px; pointer-events: none; z-index: 10;}
        
        /* Force Landscape Mode on Mobile */
        @media screen and (orientation: portrait) {
            #video-container {
                transform: rotate(-90deg);
                transform-origin: center center;
                width: 100vh;
                height: 100vw;
                position: absolute;
            }
            img { object-fit: contain; width: 100vh; height: 100vw; }
        }
    </style>
</head>
<body>
    <div id="video-container">
        <img id="live-screen" src="screen.jpg" alt="Connecting to Laptop Screen...">
        <div class="watermark">🔴 Live Broadcast</div>
    </div>
    <script>
        const img = document.getElementById('live-screen');
        function fetchNextFrame() {
            const tempImage = new Image();
            tempImage.onload = function() {
                img.src = tempImage.src;
                // Wait briefly before requesting the next frame to prevent browser freeze
                setTimeout(fetchNextFrame, 100); 
            };
            tempImage.onerror = function() {
                // If file is locked by PowerShell writing it, retry slightly later
                setTimeout(fetchNextFrame, 250);
            };
            tempImage.src = 'screen.jpg?t=' + new Date().getTime();
        }
        // Start the fetching loop
        fetchNextFrame();
    </script>
</body>
</html>`;
                fs.writeFileSync(htmlPath, htmlContent);
                const safeImgPath = imgPath.replace(/\\/g, '/');
                const safeTempImgPath = safeImgPath.replace('.jpg', '_temp.jpg');
                const psScriptContent = `
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
while ($true) {
    try {
        $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $gfx = [System.Drawing.Graphics]::FromImage($bmp)
        $gfx.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
        $bmp.Save("${safeTempImgPath}", [System.Drawing.Imaging.ImageFormat]::Jpeg)
        $gfx.Dispose()
        $bmp.Dispose()
        Move-Item -Path "${safeTempImgPath}" -Destination "${safeImgPath}" -Force -ErrorAction SilentlyContinue
    } catch {}
    Start-Sleep -Milliseconds 150
}
`;
                fs.writeFileSync(psScriptPath, psScriptContent);
                if (previewProcess) {
                    try {
                        previewProcess.kill();
                    }
                    catch (e) { }
                    previewProcess = null;
                }
                message.reply(`⏳ *System:* Starting Ultra-Smooth Screen Preview...\n\n🌐 *Access Link:* http://${ip}/preview/\n\n_Note: Ensure Apache is running in XAMPP. Send \`!stop preview\` to end the stream._`);
                sendLogToPanel(`> [PREVIEW] Live background script started. Broadcasting to Apache.`, 'log-info');
                previewProcess = cp.spawn('powershell', ['-ExecutionPolicy', 'Bypass', '-File', psScriptPath], {
                    windowsHide: true
                });
                previewProcess.on('error', (err) => {
                    sendLogToPanel(`[PREVIEW ERROR] ${err.message}`, 'log-error');
                });
            }
            else if (cmd === '!stop preview') {
                if (previewProcess) {
                    try {
                        previewProcess.kill();
                    }
                    catch (e) { }
                    previewProcess = null;
                    const previewDir = path.join(XAMPP_DIR, 'htdocs', 'preview');
                    try {
                        if (fs.existsSync(path.join(previewDir, 'stream.ps1')))
                            fs.unlinkSync(path.join(previewDir, 'stream.ps1'));
                    }
                    catch (e) { }
                    message.reply(`✅ *System:* Live Preview successfully stopped.`);
                    sendLogToPanel(`> [PREVIEW] Live screen broadcast stopped and cleared.`, 'log-success');
                }
                else {
                    message.reply(`❌ *System:* No Live Preview is currently running.`);
                }
            }
            // ================= VERCEL DEPLOYMENT API =================
            else if (cmd.startsWith('!setvercel ')) {
                VERCEL_API_KEY = message.body.substring(11).trim();
                message.reply('✅ *Vercel API Key Saved!*\n\nYou can now deploy folders from inside your htdocs using the command:\n`!deploy your_folder_name`');
            }
            else if (cmd.startsWith('!deploy ')) {
                if (!VERCEL_API_KEY) {
                    return message.reply('❌ *Error:* Vercel API Key is not set.\nType `!setvercel <YOUR_API_KEY>` first.');
                }
                const args = message.body.substring(8).trim().split(' ');
                const folderName = args[0];
                const targetPath = path.join(XAMPP_DIR, 'htdocs', folderName);
                const projectName = folderName.toLowerCase().replace(/[^a-z0-9-]/g, '-');
                if (!fs.existsSync(targetPath)) {
                    return message.reply(`❌ *Error:* Folder '${folderName}' not found in htdocs.\nUse the \`!htdocs\` command to view your folders list.`);
                }
                message.reply(`⏳ *Vercel:* Reading files from folder '${folderName}' and processing automatic deployment...`);
                try {
                    let filesPayload = [];
                    let framework = null;
                    if (fs.existsSync(path.join(targetPath, 'artisan'))) {
                        framework = null;
                        if (!fs.existsSync(path.join(targetPath, 'vercel.json'))) {
                            filesPayload.push({
                                file: 'vercel.json',
                                data: Buffer.from(JSON.stringify({
                                    "functions": { "api/index.php": { "runtime": "vercel-php@0.6.0" } },
                                    "routes": [{ "src": "/(.*)", "dest": "/api/index.php" }]
                                })).toString('base64'),
                                encoding: 'base64'
                            });
                            filesPayload.push({
                                file: 'api/index.php',
                                data: Buffer.from("<?php require __DIR__ . '/../public/index.php';").toString('base64'),
                                encoding: 'base64'
                            });
                        }
                    }
                    else if (fs.existsSync(path.join(targetPath, 'package.json'))) {
                        try {
                            const pkg = JSON.parse(fs.readFileSync(path.join(targetPath, 'package.json'), 'utf8'));
                            if (pkg.dependencies && pkg.dependencies.next)
                                framework = 'nextjs';
                            else if (pkg.dependencies && pkg.dependencies.nuxt)
                                framework = 'nuxtjs';
                            else if (pkg.dependencies && pkg.dependencies['react-scripts'])
                                framework = 'create-react-app';
                        }
                        catch (e) { }
                    }
                    function readDirRecursive(dir, basePath = '') {
                        const items = fs.readdirSync(dir);
                        for (let item of items) {
                            if (['node_modules', 'vendor', '.git', '.env'].includes(item))
                                continue;
                            const itemPath = path.join(dir, item);
                            const relativePath = basePath ? `${basePath}/${item}` : item;
                            if (fs.statSync(itemPath).isDirectory()) {
                                readDirRecursive(itemPath, relativePath);
                            }
                            else {
                                filesPayload.push({
                                    file: relativePath.replace(/\\/g, '/'),
                                    data: fs.readFileSync(itemPath, 'base64'),
                                    encoding: 'base64'
                                });
                            }
                        }
                    }
                    readDirRecursive(targetPath);
                    message.reply(`🚀 *Vercel:* Uploading ${filesPayload.length} files (Framework/Type: ${framework || 'PHP/Static'}) to Vercel...`);
                    const payloadStr = JSON.stringify({
                        name: projectName,
                        files: filesPayload,
                        projectSettings: { framework: framework }
                    });
                    const reqOptions = {
                        hostname: 'api.vercel.com',
                        port: 443,
                        path: '/v13/deployments',
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${VERCEL_API_KEY}`,
                            'Content-Type': 'application/json',
                            'Content-Length': Buffer.byteLength(payloadStr)
                        }
                    };
                    const req = https.request(reqOptions, (res) => {
                        let responseData = '';
                        res.on('data', chunk => responseData += chunk);
                        res.on('end', () => {
                            try {
                                const result = JSON.parse(responseData);
                                if (res.statusCode >= 200 && res.statusCode < 300) {
                                    const deployUrl = `https://${result.url}`;
                                    message.reply(`✅ *DEPLOY SUCCESSFUL!*\n\n📁 Project: ${folderName}\n🌐 Access URL: ${deployUrl}`);
                                    sendLogToPanel(`> [VERCEL] Successfully deployed ${folderName} to: ${deployUrl}`, 'log-success');
                                }
                                else {
                                    message.reply(`❌ *Deploy Failed (Vercel API):*\n${result.error?.message || 'Unknown Error'}`);
                                }
                            }
                            catch (e) {
                                message.reply('❌ *Error Processing Response:* Failed to read response from Vercel.');
                            }
                        });
                    });
                    req.on('error', (e) => {
                        message.reply(`❌ *Network Error:* ${e.message}`);
                    });
                    req.write(payloadStr);
                    req.end();
                }
                catch (err) {
                    message.reply(`❌ *System Error:* ${err.message}`);
                }
            }
            // ================= COMPILE WEB TO EXE (NATIVEFIER) =================
            else if (cmd.startsWith('!web2exe ')) {
                const args = message.body.substring(9).trim().split(' ');
                if (args.length < 2) {
                    return message.reply('❌ *Invalid Format:*\n!web2exe <url> <app_name>\nExample: `!web2exe https://google.com GoogleApp`');
                }
                const url = args[0];
                const appName = args.slice(1).join(' ');
                const safeAppName = appName.replace(/[^a-zA-Z0-9]/g, '');
                const targetDir = path.join(XAMPP_DIR, 'htdocs', safeAppName);
                if (!fs.existsSync(targetDir)) {
                    fs.mkdirSync(targetDir, { recursive: true });
                }
                message.reply(`⏳ *Nativefier:* Starting build process for URL ${url}...\n📁 Target: htdocs\\${safeAppName}\nCheck your VS Code Terminal.`);
                const terminal = vscode.window.createTerminal({ name: `Web2Exe: ${safeAppName}`, cwd: targetDir });
                terminal.show();
                terminal.sendText(`echo "[WEB2EXE] Starting Desktop App compilation..."`);
                terminal.sendText(`echo "URL: ${url}"`);
                terminal.sendText(`echo "Build Folder: ${targetDir}"`);
                if (typeof sendLogToPanel === 'function') {
                    sendLogToPanel(`> [WA CMD] Creating .exe from ${url} in htdocs\\${safeAppName}`, 'log-info');
                }
                const execOptions = { cwd: targetDir, maxBuffer: 1024 * 1024 * 100 };
                const buildCmd = `npx nativefier "${url}" --name "${safeAppName}" --platform windows`;
                cp.exec(buildCmd, execOptions, async (err, stdout, stderr) => {
                    if (err) {
                        terminal.sendText(`echo "Error: Compilation Failed!"`);
                        console.error("Nativefier Error:", err);
                        return message.reply(`❌ *Web2Exe Error:*\nFailed to compile application.\n${err.message}`);
                    }
                    terminal.sendText(`echo "[WEB2EXE] Compilation successful! Locating build folder (win32)..."`);
                    try {
                        const items = fs.readdirSync(targetDir);
                        const builtFolder = items.find(item => {
                            const itemPath = path.join(targetDir, item);
                            return fs.statSync(itemPath).isDirectory() && item.toLowerCase().includes('win32');
                        });
                        if (!builtFolder) {
                            terminal.sendText(`echo "Error: win32 folder not found!"`);
                            return message.reply(`❌ *Error:* Failed to locate exe folder. Current directory contents:\n${items.join(', ')}`);
                        }
                        const builtFolderPath = path.join(targetDir, builtFolder);
                        const zipPath = path.join(targetDir, `${safeAppName}.zip`);
                        message.reply(`✅ *Compilation Complete!*\n⏳ Currently compressing folder (ZIP) in htdocs\\${safeAppName}...`);
                        const zipCmd = `powershell -command "Compress-Archive -Path '${builtFolderPath}' -DestinationPath '${zipPath}' -Force"`;
                        cp.exec(zipCmd, { cwd: targetDir }, (zipErr) => {
                            if (zipErr) {
                                terminal.sendText(`echo "Error: Failed to compress to ZIP!"`);
                                return message.reply(`❌ *ZIP Error:*\n${zipErr.message}`);
                            }
                            terminal.sendText(`echo "[WEB2EXE] ZIP created successfully. Processing delivery..."`);
                            setTimeout(async () => {
                                if (!fs.existsSync(zipPath)) {
                                    return message.reply(`❌ *Error:* ZIP file not found after compression.`);
                                }
                                const stats = fs.statSync(zipPath);
                                const fileSizeInMB = stats.size / (1024 * 1024);
                                const ip = getNetworkIP();
                                const downloadUrl = `http://${ip}/${safeAppName}/${safeAppName}.zip`;
                                if (fileSizeInMB > 65) {
                                    terminal.sendText(`echo "File is too large (${fileSizeInMB.toFixed(2)} MB). Sending Download Link only."`);
                                    return message.reply(`✅ *App Complete & Successfully Zipped!*\n\n⚠️ *Info:* File size is too large to send directly via WhatsApp (*${fileSizeInMB.toFixed(2)} MB*).\n\n👇 *Please download the application directly from your local server (Fastest):*\n🌐 ${downloadUrl}\n\n_Ensure your Phone and Laptop are on the same WiFi network, then open the link above._`);
                                }
                                try {
                                    terminal.sendText(`echo "Uploading to WhatsApp (Size: ${fileSizeInMB.toFixed(2)} MB)..."`);
                                    const media = MessageMedia.fromFilePath(zipPath);
                                    await waClientInstance.sendMessage(message.from, media, {
                                        sendMediaAsDocument: true,
                                        caption: `💻 *Desktop App (.exe) Complete!*\n🌐 Web URL: ${url}\n📁 App Name: ${safeAppName}\n📦 File Size: ${fileSizeInMB.toFixed(2)} MB\n\n⬇️ *Alternative Download Link (Via XAMPP Server):*\n${downloadUrl}`
                                    });
                                    if (typeof sendLogToPanel === 'function') {
                                        sendLogToPanel(`[WEB2EXE] Successfully sent ZIP file to WA.`, 'log-success');
                                    }
                                    terminal.sendText(`echo "[WEB2EXE] ZIP file successfully delivered to WhatsApp!"`);
                                    setTimeout(() => terminal.dispose(), 5000);
                                }
                                catch (sendErr) {
                                    console.error("WA Send Error:", sendErr);
                                    terminal.sendText(`echo "WhatsApp Error: Upload failed. Redirecting to Alternative Link."`);
                                    message.reply(`✅ *Compilation Successful, but WhatsApp rejected the file.*\n(System memory full / WA size limit)\n📦 File Size: ${fileSizeInMB.toFixed(2)} MB\n\n👇 *Don't worry, please download the application directly from your server:*\n🌐 ${downloadUrl}`);
                                }
                            }, 2500);
                        });
                    }
                    catch (systemErr) {
                        console.error("System Error:", systemErr);
                        message.reply(`❌ *System Error (File Processing):*\n${systemErr.message}`);
                    }
                });
            }
            // ================= DATABASE SHELL =================
            else if (cmd.startsWith('!query ')) {
                const queryText = message.body.substring(7);
                const mysqlExe = path.join(XAMPP_DIR, 'mysql', 'bin', 'mysql.exe');
                if (!fs.existsSync(mysqlExe))
                    return message.reply('❌ *Error:* mysql.exe not found.');
                const safeQuery = queryText.replace(/"/g, '\\"');
                cp.exec(`"${mysqlExe}" -u root -e "${safeQuery}"`, (err, stdout, stderr) => {
                    if (err || stderr)
                        message.reply(`❌ *Query Error:*\n${stderr || err.message}`);
                    else {
                        const resText = stdout.trim();
                        message.reply(resText ? `📊 *Result:*\n\`\`\`\n${resText}\n\`\`\`` : `✅ *Success.*`);
                    }
                });
            }
            else if (cmd.startsWith('!db ')) {
                const args = message.body.substring(4).trim();
                const firstSpaceIndex = args.indexOf(' ');
                if (firstSpaceIndex === -1)
                    return message.reply('❌ *Invalid Format:*\n!db <db_name> <query>');
                const dbName = args.substring(0, firstSpaceIndex).trim();
                const queryText = message.body.substring(firstSpaceIndex + 1).trim();
                const mysqlExe = path.join(XAMPP_DIR, 'mysql', 'bin', 'mysql.exe');
                if (!fs.existsSync(mysqlExe))
                    return message.reply('❌ *Error:* mysql.exe not found.');
                const safeQuery = queryText.replace(/"/g, '\\"');
                cp.execFile(mysqlExe, ['-u', 'root', dbName, '-e', safeQuery], (err, stdout, stderr) => {
                    if (err || stderr)
                        message.reply(`❌ *Query Error [${dbName}]:*\n${stderr || err.message}`);
                    else {
                        const resText = stdout.trim();
                        message.reply(resText ? `📊 *Table [${dbName}]:*\n\`\`\`\n${resText}\n\`\`\`` : `✅ *Success.*`);
                    }
                });
            }
            else if (cmd === '!status') {
                const helpMsg = `✅ *System Bot Active!*\n\n*System Monitor:*\n▫️ !system _(Check Laptop RAM & CPU)_\n▫️ !preview _(Start Live Laptop Screen on Web)_\n▫️ !stop preview _(Stop Live Screen)_\n\n*Server & Mobile Preview:*\n▫️ !start php <folder>\n▫️ !stop php\n▫️ !start laravel <folder>\n▫️ !stop laravel\n▫️ !start python <folder>\n▫️ !stop python\n\n*Directory (Htdocs):*\n▫️ !htdocs _(View htdocs folder contents)_\n\n*Flutter Applications:*\n▫️ !start flutter <folder>\n▫️ !stop flutter\n▫️ !build flutter <folder> _(Compile APK)_\n\n*Desktop App Compiler:*\n▫️ !web2exe <url> <app_name> _(Convert Link to EXE)_\n\n*Ngrok Tunneling:*\n▫️ !start ngrok <port>\n▫️ !stop ngrok\n\n*Vercel Deploy (Cloud):*\n▫️ !setvercel <API_KEY>\n▫️ !deploy <htdocs_folder> _(Auto-detect framework)_\n\n*XAMPP Modules:*\n▫️ !start apache / !stop apache\n▫️ !start mariadb / !stop mariadb\n\n*SQL Database:*\n▫️ !query <global_sql_command>\n▫️ !db <db_name> <query>\n\n*Main System:*\n▫️ !cleanup`;
                message.reply(helpMsg);
            }
        }
    });
    waClientInstance.initialize().catch(err => {
        sendLogToPanel('[WA BOT ERROR] Initialization Failed / Connection Refused.', 'log-error');
        isWaInitializing = false;
        waClientInstance = null;
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'wa_status', status: 'disconnected' });
    });
}
// ===================================================================
function openWSLTerminal() {
    sendLogToPanel('> Opening Windows Subsystem for Linux (WSL) terminal...', 'log-info');
    const terminal = vscode.window.createTerminal("WSL Shell");
    terminal.show();
    terminal.sendText('wsl');
    sendLogToPanel('[WSL] Linux Terminal Successfully Opened.', 'log-success');
}
function websiteServer() {
    sendLogToPanel('> Opening Website Server ./web/web.js...', 'log-info');
    const terminal = vscode.window.createTerminal("Websel");
    terminal.show();
    terminal.sendText('cd web');
    terminal.sendText('node web.js');
    sendLogToPanel('[WSL] Website Server Terminal Successfully Opened.', 'log-success');
}
function runNetstatCommand() {
    sendLogToPanel('> Running Netstat Scan...', 'log-info');
    const terminal = vscode.window.createTerminal("Network Scanner (Netstat)");
    terminal.show();
    terminal.sendText('netstat -ano | findstr LISTENING');
    sendLogToPanel('[NETSTAT] Check Status in VS Code Terminal.', 'log-success');
}
async function startNgrokCommand() {
    const port = await vscode.window.showInputBox({ prompt: 'Enter Port to forward via Ngrok (E.g: 8000, 3000, 8080)' });
    if (!port)
        return;
    sendLogToPanel(`> Starting Ngrok Tunnel on Port: ${port}`, 'log-info');
    const terminal = vscode.window.createTerminal({ name: `Ngrok: ${port}` });
    terminal.show();
    terminal.sendText(`ngrok http ${port}`);
    activeTerminals['ngrok'] = terminal;
    sendLogToPanel(`[NGROK] Successfully launched in VS Code Terminal. Check public URL there.`, 'log-success');
    if (currentPanel)
        currentPanel.webview.postMessage({ command: 'status', service: 'ngrok', status: 'running' });
}
async function startPhpServerCommand() {
    const options = {
        canSelectMany: false,
        openLabel: 'Select Web Folder (PHP Native)',
        canSelectFiles: false,
        canSelectFolders: true
    };
    const fileUri = await vscode.window.showOpenDialog(options);
    if (fileUri && fileUri[0]) {
        const folderPath = fileUri[0].fsPath;
        sendLogToPanel(`> Starting PHP Public Server at: ${folderPath}`, 'log-info');
        const terminal = vscode.window.createTerminal({ name: "PHP Public Server", cwd: folderPath });
        terminal.show();
        terminal.sendText('php -S 0.0.0.0:8081');
        activeTerminals['phpserver'] = terminal;
        sendLogToPanel(`[PHP SERVER] Successfully launched in VS Code Terminal.`, 'log-success');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'status', service: 'phpserver', status: 'running' });
        setTimeout(() => {
            vscode.env.openExternal(vscode.Uri.parse('http://127.0.0.1:8081'));
        }, 2000);
    }
}
async function startLaravelCommand() {
    const options = {
        canSelectMany: false,
        openLabel: 'Select Laravel Project Folder',
        canSelectFiles: false,
        canSelectFolders: true
    };
    const fileUri = await vscode.window.showOpenDialog(options);
    if (fileUri && fileUri[0]) {
        const laravelPath = fileUri[0].fsPath;
        if (!fs.existsSync(path.join(laravelPath, 'artisan'))) {
            vscode.window.showErrorMessage('artisan file not found.');
            sendLogToPanel(`ERROR: Directory ${laravelPath} is not a Laravel project.`, 'log-error');
            return;
        }
        sendLogToPanel(`> Running Laravel to: ${laravelPath}`, 'log-info');
        const terminal = vscode.window.createTerminal({ name: "Laravel Server", cwd: laravelPath });
        terminal.show();
        terminal.sendText('php artisan serve --host=0.0.0.0 --port=8000');
        activeTerminals['laravel'] = terminal;
        sendLogToPanel(`[LARAVEL] Artisan serve Successfully Opened.`, 'log-success');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'status', service: 'laravel', status: 'running' });
        setTimeout(() => {
            vscode.env.openExternal(vscode.Uri.parse('http://127.0.0.1:8000'));
        }, 2000);
    }
}
async function startNodeCommand() {
    const options = {
        canSelectMany: false,
        openLabel: 'Select Node.js Project Folder',
        canSelectFiles: false,
        canSelectFolders: true
    };
    const fileUri = await vscode.window.showOpenDialog(options);
    if (fileUri && fileUri[0]) {
        const folderPath = fileUri[0].fsPath;
        sendLogToPanel(`> Starting Node.js Server at: ${folderPath}`, 'log-info');
        const terminal = vscode.window.createTerminal({ name: "Node.js Server", cwd: folderPath });
        terminal.show();
        const hasServerJs = fs.existsSync(path.join(folderPath, 'server.js'));
        const envInject = os.platform() === 'win32' ? '$env:HOST="0.0.0.0"; $env:PORT="3000"; ' : 'HOST=0.0.0.0 PORT=3000 ';
        if (hasServerJs) {
            terminal.sendText(`${envInject}node server.js`);
        }
        else {
            terminal.sendText(`${envInject}npm start || node index.js`);
        }
        activeTerminals['node'] = terminal;
        sendLogToPanel(`[NODE] Successfully launched in VS Code Terminal.`, 'log-success');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'status', service: 'node', status: 'running' });
        setTimeout(() => {
            vscode.env.openExternal(vscode.Uri.parse('http://127.0.0.1:3000'));
        }, 2000);
    }
}
async function startPythonCommand() {
    const options = {
        canSelectMany: false,
        openLabel: 'Select Python Web Folder',
        canSelectFiles: false,
        canSelectFolders: true
    };
    const fileUri = await vscode.window.showOpenDialog(options);
    if (fileUri && fileUri[0]) {
        const folderPath = fileUri[0].fsPath;
        sendLogToPanel(`> Starting Python HTTP Server at: ${folderPath}`, 'log-info');
        const terminal = vscode.window.createTerminal({ name: "Python Server", cwd: folderPath });
        terminal.show();
        terminal.sendText('python -m http.server 8082');
        activeTerminals['python'] = terminal;
        sendLogToPanel(`[PYTHON] Successfully launched in VS Code Terminal.`, 'log-success');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'status', service: 'python', status: 'running' });
        setTimeout(() => {
            vscode.env.openExternal(vscode.Uri.parse('http://127.0.0.1:8082'));
        }, 2000);
    }
}
function getEmulatorPath() {
    const possiblePaths = [
        process.env.ANDROID_HOME ? path.join(process.env.ANDROID_HOME, 'emulator', 'emulator.exe') : null,
        process.env.ANDROID_SDK_ROOT ? path.join(process.env.ANDROID_SDK_ROOT, 'emulator', 'emulator.exe') : null,
        path.join(os.homedir(), 'AppData', 'Local', 'Android', 'Sdk', 'emulator', 'emulator.exe'),
        path.join(os.homedir(), 'AppData', 'Local', 'Android', 'Sdk', 'tools', 'emulator.exe'),
        'C:\\Android\\Sdk\\emulator\\emulator.exe'
    ].filter(p => p && fs.existsSync(p));
    return possiblePaths.length > 0 ? possiblePaths[0] : 'emulator';
}
function handleGetAvds(panel) {
    const emuPath = getEmulatorPath();
    cp.exec(`"${emuPath}" -list-avds`, { windowsHide: true }, (err, stdout) => {
        if (err) {
            cp.exec(`emulator -list-avds`, { windowsHide: true }, (err2, stdout2) => {
                if (err2) {
                    vscode.window.showErrorMessage("Android Emulator not found. Ensure Android SDK is installed and path is correct.");
                    if (panel)
                        panel.webview.postMessage({ command: 'avdList', avds: [] });
                    return;
                }
                processAvdList(stdout2, panel);
            });
            return;
        }
        processAvdList(stdout, panel);
    });
}
function processAvdList(stdout, panel) {
    const avds = stdout.split('\n').map(a => a.trim()).filter(a => a && !a.startsWith('INFO'));
    if (panel)
        panel.webview.postMessage({ command: 'avdList', avds });
}
function startAvd(avdName) {
    const emuPath = getEmulatorPath();
    sendLogToPanel(`> Starting Emulator: ${avdName}...`, 'log-info');
    const child = cp.spawn(`"${emuPath}"`, ['-avd', avdName], {
        shell: true,
        detached: true,
        windowsHide: true,
        stdio: 'ignore'
    });
    child.unref();
    sendLogToPanel(`[ANDROID] Emulator ${avdName} is running...`, 'log-success');
}
function stopAvd() {
    sendLogToPanel(`> Stopping all Android Emulator instances...`, 'log-info');
    cp.exec('taskkill /F /IM qemu-system-x86_64.exe /IM qemu-system-i386.exe /IM emulator.exe /IM emulator64-x86.exe', { windowsHide: true }, (err) => {
        sendLogToPanel(`[ANDROID] Emulators successfully force stopped.`, 'log-success');
    });
}
// ====================================================================================
async function createLaravelProject() {
    const folderUri = await vscode.window.showOpenDialog({ canSelectFolders: true, canSelectFiles: false, openLabel: 'Select Folder for Project' });
    if (!folderUri || !folderUri[0])
        return;
    const projectName = await vscode.window.showInputBox({ prompt: 'Enter New Laravel Project Name (E.g: my_project)' });
    if (!projectName)
        return;
    const terminal = vscode.window.createTerminal({ name: `Create Laravel: ${projectName}`, cwd: folderUri[0].fsPath });
    terminal.show();
    terminal.sendText(`composer create-project laravel/laravel ${projectName}`);
    sendLogToPanel(`> [LARAVEL] Starting project creation: ${projectName}`, 'log-info');
}
async function createFlutterProject() {
    const folderUri = await vscode.window.showOpenDialog({ canSelectFolders: true, canSelectFiles: false, openLabel: 'Select Folder for Project' });
    if (!folderUri || !folderUri[0])
        return;
    const projectName = await vscode.window.showInputBox({ prompt: 'Enter New Flutter Project Name (all_lowercase)' });
    if (!projectName)
        return;
    const terminal = vscode.window.createTerminal({ name: `Create Flutter: ${projectName}`, cwd: folderUri[0].fsPath });
    terminal.show();
    terminal.sendText(`flutter create ${projectName}`);
    sendLogToPanel(`> [FLUTTER] Starting project creation: ${projectName}`, 'log-info');
}
async function runFlutterProject() {
    const folderUri = await vscode.window.showOpenDialog({ canSelectFolders: true, canSelectFiles: false, openLabel: 'Select Flutter Project Folder to run' });
    if (!folderUri || !folderUri[0])
        return;
    const terminal = vscode.window.createTerminal({ name: `Flutter Run`, cwd: folderUri[0].fsPath });
    terminal.show();
    terminal.sendText(`flutter run`);
    activeTerminals['flutter'] = terminal;
    sendLogToPanel(`> [FLUTTER] Running Flutter Application...`, 'log-info');
    if (currentPanel)
        currentPanel.webview.postMessage({ command: 'status', service: 'flutter', status: 'running' });
}
async function createNodeProject() {
    const folderUri = await vscode.window.showOpenDialog({ canSelectFolders: true, canSelectFiles: false, openLabel: 'Select Folder for Node.js Project' });
    if (!folderUri || !folderUri[0])
        return;
    const projectName = await vscode.window.showInputBox({ prompt: 'Enter New Node.js Project Name' });
    if (!projectName)
        return;
    const projectPath = path.join(folderUri[0].fsPath, projectName);
    fs.mkdirSync(projectPath, { recursive: true });
    const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XAMPP Meta Node.js</title>
    <h1>🚀 Hello Node.js!</h1>
</html>`;
    fs.writeFileSync(path.join(projectPath, 'index.html'), htmlContent);
    const serverJsContent = `const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;
app.use(express.static(__dirname));
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});
app.listen(PORT, '0.0.0.0', () => {
    console.log('✅ Node.js server running at http://localhost:' + PORT);
});`;
    fs.writeFileSync(path.join(projectPath, 'server.js'), serverJsContent);
    const terminal = vscode.window.createTerminal({ name: `Node: ${projectName}`, cwd: projectPath });
    terminal.show();
    terminal.sendText(`npm init -y`);
    terminal.sendText(`npm install express`);
    terminal.sendText(`node server.js`);
    activeTerminals['node'] = terminal;
    sendLogToPanel(`> [NODE] Project ${projectName} created. Installing Express...`, 'log-info');
    if (currentPanel)
        currentPanel.webview.postMessage({ command: 'status', service: 'node', status: 'running' });
    setTimeout(() => {
        vscode.env.openExternal(vscode.Uri.parse('http://127.0.0.1:3000'));
    }, 8000);
}
async function createPythonProject() {
    const folderUri = await vscode.window.showOpenDialog({ canSelectFolders: true, canSelectFiles: false, openLabel: 'Select Folder for Python Project' });
    if (!folderUri || !folderUri[0])
        return;
    const projectName = await vscode.window.showInputBox({ prompt: 'Enter New Python Project Name' });
    if (!projectName)
        return;
    const projectPath = path.join(folderUri[0].fsPath, projectName);
    fs.mkdirSync(projectPath, { recursive: true });
    const terminal = vscode.window.createTerminal({ name: `Create Python: ${projectName}`, cwd: projectPath });
    terminal.show();
    terminal.sendText(`python -m venv venv`);
    terminal.sendText(`echo print("Hello XAMPP Meta Python!") > main.py`);
    sendLogToPanel(`> [PYTHON] Project ${projectName} (with venv) successfully created.`, 'log-info');
}
// ====================================================================================
function openAdminPanel(service) {
    let url = '';
    const ip = '127.0.0.1';
    if (service === 'apache')
        url = `http://${ip}/`;
    else if (service === 'mysql')
        url = `http://${ip}/phpmyadmin/`;
    else if (service === 'tomcat')
        url = `http://${ip}:8080/`;
    else if (service === 'laravel')
        url = 'http://127.0.0.1:8000';
    else if (service === 'phpserver')
        url = 'http://127.0.0.1:8081';
    else if (service === 'node')
        url = 'http://127.0.0.1:3000';
    else if (service === 'python')
        url = 'http://127.0.0.1:8082';
    else if (service === 'filezilla') {
        const fzAdminPath = path.join(XAMPP_DIR, 'FileZillaFTP', 'FileZilla Server Interface.exe');
        if (fs.existsSync(fzAdminPath))
            cp.exec(`"${fzAdminPath}"`);
        else
            vscode.window.showErrorMessage('FileZilla Admin Interface (EXE) not found.');
        return;
    }
    else if (service === 'mercury') {
        vscode.window.showInformationMessage('Mercury Admin is accessed directly from the running Mercury Desktop application window.');
        return;
    }
    if (url)
        vscode.env.openExternal(vscode.Uri.parse(url));
}
function openConfigFile(service) {
    let configPath = '';
    switch (service) {
        case 'apache':
            configPath = path.join(XAMPP_DIR, 'apache', 'conf', 'httpd.conf');
            break;
        case 'mysql':
            configPath = path.join(XAMPP_DIR, 'mysql', 'bin', 'my.ini');
            break;
        case 'filezilla':
            configPath = path.join(XAMPP_DIR, 'FileZillaFTP', 'FileZilla Server.xml');
            break;
        case 'mercury':
            configPath = path.join(XAMPP_DIR, 'MercuryMail', 'MERCURY.INI');
            break;
        case 'tomcat':
            configPath = path.join(XAMPP_DIR, 'tomcat', 'conf', 'server.xml');
            break;
    }
    openFileInEditor(configPath);
}
function openLogFile(service) {
    let logPath = '';
    switch (service) {
        case 'apache':
            logPath = path.join(XAMPP_DIR, 'apache', 'logs', 'error.log');
            break;
        case 'mysql':
            const dataDir = path.join(XAMPP_DIR, 'mysql', 'data');
            logPath = path.join(dataDir, 'mysql_error.log');
            if (fs.existsSync(dataDir)) {
                const files = fs.readdirSync(dataDir);
                const errFile = files.find(f => f.endsWith('.err'));
                if (errFile)
                    logPath = path.join(dataDir, errFile);
            }
            break;
        case 'filezilla':
            logPath = path.join(XAMPP_DIR, 'FileZillaFTP', 'Logs', 'FileZilla Server.log');
            break;
        case 'mercury':
            logPath = path.join(XAMPP_DIR, 'MercuryMail', 'Logs', 'CORE.LOG');
            break;
        case 'tomcat':
            logPath = path.join(XAMPP_DIR, 'tomcat', 'logs', 'catalina.out');
            break;
    }
    openFileInEditor(logPath);
}
function openFileInEditor(filePath) {
    if (filePath && fs.existsSync(filePath)) {
        vscode.workspace.openTextDocument(filePath).then(doc => vscode.window.showTextDocument(doc));
    }
    else {
        vscode.window.showErrorMessage(`File Not Found: ${filePath || 'Empty path'}`);
    }
}
function openMariaDBShell() {
    const mysqlBinDir = path.join(XAMPP_DIR, 'mysql', 'bin');
    const mysqlExePath = path.join(mysqlBinDir, 'mysql.exe');
    if (!fs.existsSync(mysqlExePath)) {
        vscode.window.showErrorMessage(`File mysql.exe not found in ${mysqlBinDir}.`);
        return;
    }
    const terminal = vscode.window.createTerminal("MariaDB SQL Shell");
    terminal.show();
    terminal.sendText(`cd "${mysqlBinDir}"`);
    terminal.sendText(`.\\mysql.exe -u root`);
}
function fixXamppBugs() {
    sendLogToPanel('> Terminating all XAMPP module processes...', 'log-info');
    const killCommand = 'taskkill /F /IM httpd.exe & taskkill /F /IM mysqld.exe & taskkill /F /IM FileZillaServer.exe & taskkill /F /IM filezillaserver.exe & taskkill /F /IM mercury.exe & taskkill /F /IM java.exe & taskkill /F /IM ngrok.exe';
    cp.exec(killCommand, { windowsHide: true }, (error, stdout, stderr) => {
        sendLogToPanel('Cleaning Successfully. Background sterilized.', 'log-success');
        if (currentPanel) {
            ['apache', 'mysql', 'filezilla', 'mercury', 'tomcat', 'ngrok'].forEach(service => {
                currentPanel.webview.postMessage({ command: 'status', service: service, status: 'stopped' });
            });
        }
    });
}
function runXamppCommand(service, action) {
    if (action === 'stop') {
        let processNames = [];
        if (service === 'apache')
            processNames = ['httpd.exe'];
        else if (service === 'mysql')
            processNames = ['mysqld.exe'];
        else if (service === 'filezilla')
            processNames = ['FileZillaServer.exe', 'filezillaserver.exe'];
        else if (service === 'mercury')
            processNames = ['mercury.exe'];
        else if (service === 'tomcat')
            processNames = ['java.exe', 'tomcat9.exe'];
        sendLogToPanel(`> Force stopping ${service.toUpperCase()}...`, 'log-info');
        const killCmd = processNames.map(p => `taskkill /F /IM ${p}`).join(' & ');
        cp.exec(killCmd, { windowsHide: true }, (error, stdout, stderr) => {
            if (error && !stdout.includes("SUCCESS")) {
                sendLogToPanel(`Processes for ${service} are not running or failed to stop.`, 'log-error');
            }
            else {
                sendLogToPanel(`[${service.toUpperCase()}] Force stop successful.`, 'log-success');
            }
            if (currentPanel)
                currentPanel.webview.postMessage({ command: 'status', service: service, status: 'stopped' });
        });
        return;
    }
    let batFile = `${service}_start.bat`;
    if (service === 'tomcat')
        batFile = 'catalina_start.bat';
    const execPath = path.join(XAMPP_DIR, batFile);
    if (!fs.existsSync(execPath)) {
        sendLogToPanel(`ERROR: File ${batFile} not found!`, 'log-error');
        return;
    }
    sendLogToPanel(`> Executing: ${batFile}...`, 'log-info');
    const processInstance = cp.exec(`"${execPath}"`, { windowsHide: true });
    processInstance.stdout?.on('data', (data) => {
        const text = data.toString().trim();
        if (text)
            sendLogToPanel(text, 'log-info');
    });
    processInstance.stderr?.on('data', (data) => {
        const text = data.toString().trim();
        if (text)
            sendLogToPanel(text, 'log-error');
    });
    processInstance.on('close', (code) => {
        sendLogToPanel(`[${service.toUpperCase()}] Start Process Successfully.`, 'log-success');
        if (currentPanel)
            currentPanel.webview.postMessage({ command: 'status', service: service, status: 'running' });
    });
}
function createCliTerminal() {
    if (cliTerminal) {
        cliTerminal.show();
        return;
    }
    cliWriteEmitter = new vscode.EventEmitter();
    let cliBuffer = '';
    cliTerminal = vscode.window.createTerminal({
        name: 'Meta Panel CLI',
        pty: {
            onDidWrite: cliWriteEmitter.event,
            open: () => {
                cliWriteEmitter.fire('\x1b[1;36m Meta Panel Server CLI Terminal \x1b[0m\r\n');
                cliWriteEmitter.fire('\x1b[1;36m 80 111 119 101 114 102 117 108 108 32 77 101 116 97 32 80 97 110 101 108 \x1b[0m\r\n');
                cliWriteEmitter.fire('meta-panel> ');
            },
            close: () => {
                cliTerminal = null;
                cliWriteEmitter = null;
            },
            handleInput: (data) => {
                for (let i = 0; i < data.length; i++) {
                    const char = data[i];
                    if (char === '\r') {
                        cliWriteEmitter.fire('\r\n');
                        handleCLICommand(cliBuffer.trim());
                        cliBuffer = '';
                        cliWriteEmitter.fire('meta-panel> ');
                    }
                    else if (char === '\x7f' || char === '\x08') {
                        if (cliBuffer.length > 0) {
                            cliBuffer = cliBuffer.slice(0, -1);
                            cliWriteEmitter.fire('\b \b');
                        }
                    }
                    else {
                        if (char.charCodeAt(0) >= 32 || char === '\t') {
                            cliBuffer += char;
                            cliWriteEmitter.fire(char);
                        }
                    }
                }
            }
        }
    });
    cliTerminal.show();
}
function handleCLICommand(cmd) {
    if (!cliWriteEmitter)
        return;
    const lowerCmd = cmd.toLowerCase().trim();
    if (lowerCmd === 'start apache') {
        cliWriteEmitter.fire('Starting Apache service...\r\n');
        runXamppCommand('apache', 'start');
    }
    else if (lowerCmd === 'stop apache') {
        cliWriteEmitter.fire('Stopping Apache service...\r\n');
        runXamppCommand('apache', 'stop');
    }
    else if (lowerCmd === 'start mariadb') {
        cliWriteEmitter.fire('Starting MariaDB (MySQL) service...\r\n');
        runXamppCommand('mysql', 'start');
    }
    else if (lowerCmd === 'stop mariadb') {
        cliWriteEmitter.fire('Stopping MariaDB (MySQL) service...\r\n');
        runXamppCommand('mysql', 'stop');
    }
    else if (lowerCmd === 'open panel') {
        cliWriteEmitter.fire('Opening phpMyAdmin panel in default browser...\r\n');
        const ip = getNetworkIP() || '127.0.0.1';
        cliWriteEmitter.fire(`phpMyAdmin Link: \x1b[1;34mhttp://${ip}/phpmyadmin/\x1b[0m\r\n`);
        openAdminPanel('mysql');
    }
    else if (lowerCmd === 'help') {
        cliWriteEmitter.fire('Commands: start apache, stop apache, start mariadb, stop mariadb, open panel\r\n');
    }
    else if (lowerCmd === '') {
        // Do nothing
    }
    else {
        cliWriteEmitter.fire(`Command not recognized: "${cmd}". Type "help" for a list of commands.\r\n`);
    }
}
function deactivate() {
    if (micProcess) {
        micProcess.kill();
        micProcess = null;
    }
}
module.exports = {
    activate,
    deactivate
};
// ======================= Content HTML =======================
function getWebviewContent(iconUri, musicUri, dwibaktiUri, pungkasUri, fujihadiUri, splashUri) {
    const config = vscode.workspace.getConfiguration('xampp');
    const showSplashScreen = config.get('showSplashScreen', true);
    const imgTag = iconUri ? `<img src="${iconUri}" alt="X" width="32" height="32" style="object-fit: contain;">` : `<div style="width:32px;height:32px;background:#fff;border-radius:4px;color:#f37021;display:flex;align-items:center;justify-content:center;font-weight:bold;">X</div>`;
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XAMPP Meta Panel</title>
    <style>
        /* Developer Profile Styles */
        .developer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-top: 10px;
        }
        .developer-card {
            background: #1e1e1e;
            border: 1px solid #3c4043;
            border-radius: 8px;
            padding: 12px 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .developer-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent);
        }
        .developer-img {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 8px;
            border: 2px solid #3c4043;
            background-color: #252526;
        }
        .developer-card:hover .developer-img {
            border-color: var(--accent);
        }
        .developer-name {
            font-size: 12px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 2px;
        }
        .developer-role {
            font-size: 10px;
            color: var(--accent);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Splash Screen Styles */
        .splash-container {
            position: fixed;
            inset: 0;
            background-color: #121212;
            z-index: 100000;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 1;
            transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.3s;
        }
        .splash-container.fade-out {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        .splash-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            text-align: center;
            animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .splash-logo {
            width: 140px;
            height: 140px;
            object-fit: contain;
            filter: drop-shadow(0 0 25px rgba(243, 112, 33, 0.5));
            animation: pulseGlow 2s infinite ease-in-out;
        }
        .splash-title {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: linear-gradient(45deg, #f37021, #ff9f43);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 10px;
            font-family: var(--font-family);
        }
        .splash-loader {
            display: none;
        }
        @keyframes scaleUp {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        @keyframes pulseGlow {
            0%, 100% { filter: drop-shadow(0 0 15px rgba(243, 112, 33, 0.3)); transform: scale(1); }
            50% { filter: drop-shadow(0 0 35px rgba(243, 112, 33, 0.7)); transform: scale(1.05); }
        }
        @keyframes loadProgress {
            0% { left: -100%; }
            100% { left: 0; }
        }

        :root {
            --bg-color: #1e1e1e; --panel-bg: #252526; --text-primary: #cccccc; --text-secondary: #808080;
            --border-color: #3e3e42; --btn-bg: #333333; --btn-hover: #404040; --btn-active: #0e639c;
            --btn-active-text: #ffffff; --danger: #d16969; --success: #6A9955;
            --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; --accent: #f37021;
            
            --class-bg: #2f3640; --class-border: #00a8ff; --class-text: #f5f6fa;
            --net-bg: #1e272e;
        }

        body, html { margin: 0; padding: 0; min-height: 100vh; width: 100%; font-family: var(--font-family); background-color: var(--bg-color); color: var(--text-primary); box-sizing: border-box; overflow-y: auto; overflow-x: hidden; }
        .container { padding: 24px; width: 100%; min-height: 100vh; display: flex; flex-direction: column; gap: 20px; box-sizing: border-box; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 16px; flex-shrink: 0; flex-wrap: wrap; gap: 10px;}
        .header-title { display: flex; align-items: center; gap: 12px; position: relative;}
        .logo { background: var(--accent); padding: 6px; border-radius: 6px; display: flex; }
        .header h2 { margin: 0; font-size: 22px; font-weight: 600; color: #ffffff; }

        /* Google Grid & Cards Styling */
        .grid-section {
            margin-bottom: 20px;
        }
        .grid-section-title {
            font-size: 15px;
            font-weight: 500;
            letter-spacing: 0.25px;
            color: #e8eaed;
            margin-top: 10px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #3c4043;
            padding-bottom: 8px;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        @media (max-width: 1024px) {
            .services-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 680px) {
            .services-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background-color: #202124;
            border: 1px solid #3c4043;
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            transition: border-color 0.15s, box-shadow 0.15s;
            position: relative;
        }
        .card:hover {
            border-color: #8ab4f8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 4px 12px rgba(0,0,0,0.25);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
            font-weight: 500;
            color: #e8eaed;
        }
        .card-title svg {
            flex-shrink: 0;
        }
        .card-status {
            display: flex;
            align-items: center;
        }

        /* Status Chip with CSS content toggling */
        .status-chip {
            display: inline-flex;
            align-items: center;
            font-size: 11px;
            font-weight: 500;
            padding: 3px 8px;
            border-radius: 12px;
            gap: 6px;
            background-color: rgba(217, 48, 37, 0.1);
            color: #f28b82;
            border: 1px solid rgba(217, 48, 37, 0.2);
            transition: all 0.2s ease;
        }
        .status-chip.running {
            background-color: rgba(30, 142, 62, 0.1);
            color: #81c995;
            border: 1px solid rgba(30, 142, 62, 0.2);
        }
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #f28b82;
            transition: all 0.2s ease;
        }
        .status-chip.running .status-dot {
            background-color: #81c995;
        }
        .status-chip::after {
            content: 'Stopped';
        }
        .status-chip.running::after {
            content: 'Running';
        }

        .card-stats {
            display: flex;
            gap: 12px;
            background-color: #282a2d;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
            font-family: 'Roboto Mono', Consolas, monospace;
            border: 1px solid #3c4043;
        }
        .stat-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .stat-label {
            font-size: 9px;
            color: #9aa0a6;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stat-value {
            color: #e8eaed;
            font-weight: 500;
        }

        .card-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: auto;
        }
        .card-actions button {
            flex: 1;
            min-width: 60px;
            padding: 6px 10px;
            font-size: 12px;
            justify-content: center;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        /* Buttons & Toolbar styling */
        button {
            font-family: inherit;
            padding: 6px 12px;
            border: 1px solid #5f6368;
            background-color: transparent;
            color: #e8eaed;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: background-color 0.15s, border-color 0.15s, color 0.15s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        button:hover {
            background-color: rgba(255, 255, 255, 0.04);
            border-color: #8ab4f8;
        }
        button.start-btn {
            background-color: #303134;
            border-color: #8ab4f8;
            color: #8ab4f8;
        }
        button.start-btn:hover {
            background-color: rgba(138, 180, 248, 0.08);
        }
        button.running {
            background-color: rgba(217, 48, 37, 0.1) !important;
            border-color: #f28b82 !important;
            color: #f28b82 !important;
        }
        button.running:hover {
            background-color: rgba(217, 48, 37, 0.2) !important;
        }
        button.tool-btn {
            background-color: transparent;
            border: 1px solid #5f6368;
        }
        button.tool-btn:hover {
            background-color: rgba(255, 255, 255, 0.04);
            border-color: #8ab4f8;
        }

        /* Toolbar dropdown styling */
        .toolbar {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        .dropdown-menu {
            position: relative;
            display: inline-block;
        }
        
        .dropdown-trigger {
            font-size: 13px;
            padding: 6px 12px;
            font-weight: 500;
            border-color: #3c4043;
            color: #e8eaed;
        }
        
        .dropdown-content {
            display: none;
            position: absolute;
            right: 0;
            top: 100%;
            margin-top: 6px;
            background-color: #202124;
            min-width: 200px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
            z-index: 1000;
            border: 1px solid #3c4043;
            border-radius: 8px;
            padding: 4px 0;
            overflow: hidden;
        }
        
        .dropdown-content.show {
            display: block;
            animation: dropdownFadeIn 0.15s ease-out;
        }
        
        .dropdown-content button, .dropdown-content a {
            box-sizing: border-box;
            width: 100%;
            background: transparent;
            border: none;
            color: #e8eaed;
            padding: 10px 16px;
            font-size: 13px;
            text-align: left;
            cursor: pointer;
            display: block;
            border-radius: 0;
            transition: background-color 0.15s;
            text-decoration: none;
        }
        
        .dropdown-content button:hover, .dropdown-content a:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        @keyframes dropdownFadeIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .sql-manager { display: flex; flex-direction: column; gap: 12px; background-color: var(--panel-bg); padding: 16px; border-radius: 6px; border: 1px solid var(--border-color); flex-grow: 1; min-height: 400px; resize: vertical; overflow: auto; }
        .sql-header { display: flex; justify-content: space-between; align-items: center; }
        .sql-header h3 { margin: 0; font-size: 16px; color: #ffffff; font-weight: 600; }
        .drop-zone { border: 2px dashed var(--border-color); border-radius: 6px; padding: 30px; text-align: center; color: var(--text-secondary); transition: 0.3s; cursor: pointer; background: var(--bg-color); height: 100%; display: flex; align-items: center; justify-content: center; min-height: 200px; }
        .drop-zone.dragover { border-color: var(--btn-active); background-color: rgba(14, 99, 156, 0.1); color: var(--btn-active); }
        .editor-container { display: none; flex-direction: column; height: 100%; border: 1px solid var(--border-color); border-radius: 6px; overflow: hidden; min-height: 300px; }
        .editor-toolbar { display: flex; justify-content: space-between; background: var(--bg-color); padding: 8px 12px; border-bottom: 1px solid var(--border-color); align-items: center; flex-wrap: wrap; gap: 10px; }
        .editor-title { font-size: 13px; font-family: Consolas, monospace; color: var(--success); }
        textarea#sql-editor { flex-grow: 1; width: 100%; padding: 12px; background: #1e1e1e; color: #d4d4d4; font-family: Consolas, 'Courier New', monospace; font-size: 14px; border: none; outline: none; resize: none; box-sizing: border-box; min-height: 200px; }
        
        #diagram-view { display: none; position: relative; flex-grow: 1; border-radius: 0 0 6px 6px; overflow: hidden; background: var(--net-bg); background-image: radial-gradient(#4a4a4a 1px, transparent 1px); background-size: 20px 20px; min-height: 300px; }
        svg#diagram-lines { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
        
        .uml-class { position: absolute; width: 200px; background: var(--class-bg); border: 2px solid var(--class-border); border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: grab; z-index: 10; display: flex; flex-direction: column; overflow: hidden; color: var(--class-text); }
        .uml-class:active { cursor: grabbing; box-shadow: 0 6px 15px rgba(0,168,255,0.4); border-color: #4cd137; }
        .uml-header { background: var(--class-border); color: #fff; text-align: center; font-weight: bold; padding: 8px; font-size: 14px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
        .uml-attrs, .uml-methods { padding: 8px; font-family: Consolas, monospace; font-size: 12px; line-height: 1.5; }
        .uml-attrs { border-bottom: 1px solid #353b48; color: #dcdde1; }
        .uml-method-item { cursor: pointer; border-radius: 4px; padding: 4px 6px; transition: 0.2s; background: #353b48; margin-bottom: 4px; border-left: 3px solid transparent; }
        .uml-method-item:hover { background: #4cd137; color: #1e272e; font-weight: bold; border-left-color: #fff; }
        
        .logs { background: #1e1e1e; border: 1px solid var(--border-color); border-radius: 6px; height: 120px; flex-shrink: 0; overflow-y: auto; padding: 12px; font-family: Consolas, monospace; font-size: 12px; line-height: 1.5; }
        .log-time { color: var(--text-secondary); margin-right: 8px; }
        .log-info { color: var(--text-primary); }
        .log-success { color: var(--success); }
        .log-error { color: var(--danger); }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-color); }
        ::-webkit-scrollbar-thumb { background: #424242; border-radius: 4px; }

        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; justify-content: center; align-items: center; }
        .modal-content { background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; width: 80%; max-width: 600px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(0,0,0,0.5); position: relative; }
        .modal-header { font-size: 18px; font-weight: 600; color: #fff; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        .modal-close { position: absolute; top: 15px; right: 20px; cursor: pointer; color: var(--danger); font-size: 20px; font-weight: bold; background: none; border: none; }
        .modal-close:hover { color: #ff6b6b; }
        video { width: 100%; border-radius: 6px; outline: none; background: #000; }
        .help-list { font-size: 14px; line-height: 1.6; }
        .help-list li { margin-bottom: 8px; }
        
        #wa-qr-container { display: none; text-align: center; padding: 15px; background: #ffffff; border-radius: 8px; border: 2px solid #25d366; margin-bottom: 15px;}
    </style>
</head>
<body>
    <!-- Splash Screen Overlay -->
    ${showSplashScreen ? `
    <div id="splash-screen" class="splash-container">
        <div class="splash-content">
            <img class="splash-logo" src="${splashUri}" alt="Logo Splash Screen">
            <div class="splash-title">XAMPP Meta Panel</div>
        </div>
    </div>
    ` : ''}

    <audio id="bg-music" src="${musicUri}" loop></audio>

    <div class="container">
        <div class="header">
            <div class="header-title">
                <div class="logo">${imgTag}</div>
                <h2>XAMPP Meta Panel</h2>
            </div>
            <div class="toolbar">
                <button class="tool-btn" id="btn-wa-status" style="color: var(--danger); border-color: var(--danger); font-weight: bold;" onclick="postCmd('startWABot')">WA: Offline 🔴</button>
                <div class="dropdown-menu">
                    <button class="tool-btn dropdown-trigger" onclick="toggleDropdown(event)">⋮ Tools</button>
                    <div class="dropdown-content" id="my-dropdown">
                        <button style="color: #ffffff; font-weight: bold;" onclick="postCmd('allowMobile')">Fix Mobile 403</button>
                        <button style="color: #ffffff;" id="btn-music" onclick="toggleMusic()">Play Music</button>
                        <button style="color: #ffffff;" onclick="postCmd('refresh')">Refresh</button>
                        <button style="color: #ffffff; font-weight: bold;" id="btn-dropdown-mic" onclick="toggleMic()">AlisaAI</button>
                        <button style="color: #ffffff;" id="btn-toggle-tts" onclick="toggleTTS()">TTS: Enabled 🔊</button>
                        <button style="color: #ffffff;" id="btn-toggle-splash" onclick="toggleSplashScreenSetting()">Splash: Enabled</button>
                        <button style="color: #ffffff;" onclick="openVideoModal()">Video Track</button>
                        <button style="color: #ffffff;" onclick="openHelpModal()">Help Info</button>
                        <button style="color: #ffffff;" onclick="postCmd('openWSL')">WSL Terminal</button>
                        <button style="color: #ffffff;" onclick="postCmd('websiteServer')">Websl Server</button>
                        <button style="color: #ffffff;" onclick="postCmd('runNetstat')">Test Netstat</button>
                        <button style="color: var(--danger); font-weight: bold;" onclick="postCmd('fixBugs')">🛠 Force Cleanup</button>
                        <a href = "https://xampp-meta-panel-api-key.vercel.app/"><button style="color: #ffffff;" >API KEY</button></a>
                        <a href = "https://xampp-meta-panel.vercel.app/"><button style="color: #ffffff;" >Web Office</button></a>
                        <a href = "https://meta-panel-server-room.vercel.app/"><button style="color: #ffffff;" >Server EMU</button></a>
                    </div>
                </div>
            </div>
        </div>

        <div id="wa-qr-container">
            <h3 style="color: #075e54; margin: 0 0 10px 0;">📱 Scan QR for WhatsApp Bot</h3>
            <img id="wa-qr-img" src="" alt="QR Code" width="250" height="250">
            <p style="color: #333; font-size: 14px; margin: 10px 0 0 0;">Session will be permanently saved. Click <b>WA: Offline 🔴</b> if disconnected.</p>
        </div>

        <div style="flex-shrink: 0; display: flex; flex-direction: column; gap: 24px;">
            <!-- SECTION 1: WEB EXTENSIONS -->
            <div class="grid-section">
                <div class="grid-section-title">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.04-.42 1.99-1.07 2.75z"/></svg>
                    Web Development Extensions Meta Panel
                </div>
                <div class="services-grid">
                    <!-- LARAVEL -->
                    <div class="card" style="border-top: 3px solid #ff2d20;">
                        <div class="card-header">
                            <div class="card-title" style="color: #ff2d20;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#ff2d20"><path d="M22.016 9.48c-1.396-1.077-4.103-3.033-5.275-3.86-1.507-1.066-2.906-1.89-4.327-1.89-1.42 0-2.82.824-4.326 1.89-1.173.827-3.88 2.783-5.275 3.86-2.52 1.942-2.73 2.128-2.73 3.655 0 2.227 1.487 3.518 3.522 3.518 1.15 0 2.08-.66 2.62-1.285.54-.626 2.05-2.54 3.65-4.485 1.55-1.886 2.062-2.316 2.538-2.316.477 0 .99.43 2.54 2.316 1.6 1.945 3.11 3.86 3.65 4.485.54.625 1.47 1.285 2.62 1.285 2.035 0 3.522-1.29 3.522-3.518 0-1.527-.21-1.713-2.73-3.655z"></path></svg>
                                Laravel
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-laravel"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="laravel-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="laravel-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-laravel" onclick="toggleLaravel()" style="background-color: rgba(255, 45, 32, 0.1); border-color: #ff2d20; color: #ff2d20;">Run Serve</button>
                            <button class="tool-btn" onclick="postCmd('createLaravelProject')">➕ Create</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'laravel')">Browser</button>
                        </div>
                    </div>

                    <!-- FLUTTER -->
                    <div class="card" style="border-top: 3px solid #02569B;">
                        <div class="card-header">
                            <div class="card-title" style="color: #45D1FD;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#45D1FD"><path d="M14.314 0L2.3 12 6 15.7 21.684.013h-7.357zm.014 11.072L7.857 17.53l3.67 3.67 7.296-7.295-4.494-2.833zM21.684 24h-7.357l-5.32-5.32 4.495-2.832L21.684 24z"></path></svg>
                                Flutter
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-flutter"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="flutter-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="flutter-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-flutter" onclick="toggleFlutter()" style="background-color: rgba(2, 86, 155, 0.1); border-color: #02569B; color: #45D1FD;">Run App</button>
                            <button class="tool-btn" onclick="postCmd('createFlutterProject')">➕ Create</button>
                        </div>
                    </div>

                    <!-- NODE.JS -->
                    <div class="card" style="border-top: 3px solid #68A063;">
                        <div class="card-header">
                            <div class="card-title" style="color: #68A063;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#68A063"><path d="M11.874 0L1.75 5.83v11.66L11.874 24l10.126-5.83V5.83zm6.657 15.65l-6.657 3.82-6.657-3.82v-7.65l6.657-3.82 6.657 3.82v7.65z"></path></svg>
                                Node.js
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-node"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="node-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="node-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-node" onclick="toggleNode()" style="background-color: rgba(104, 160, 99, 0.1); border-color: #68A063; color: #68A063;">Start Server</button>
                            <button class="tool-btn" onclick="postCmd('createNodeProject')">➕ Create</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'node')">Browser</button>
                        </div>
                    </div>

                    <!-- PYTHON -->
                    <div class="card" style="border-top: 3px solid #3776AB;">
                        <div class="card-header">
                            <div class="card-title" style="color: #3776AB;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#FFD43B"><path d="M12.01 1.776c-2.887 0-5.18.232-6.618.68-1.527.476-2.023 1.258-2.023 2.502v4.544h8.847v1.17H3.454c-.66 0-1.223.513-1.223 1.156v6.33c0 .643.562 1.155 1.222 1.155h1.968v-3.79c0-1.637.74-3.155 1.95-4.143 1.144-.932 2.63-1.424 4.142-1.424h5.45c.66 0 1.222-.513 1.222-1.156v-4.54c0-.643-.562-1.154-1.222-1.154h-2.14V1.826c0-.644-.56-1.156-1.22-1.156zm-2.455 1.94c.548 0 .993.435.993.97 0 .536-.445.97-.993.97-.547 0-.993-.434-.993-.97 0-.535.446-.97.993-.97zm10.988 5.485c-.66 0-1.222.513-1.222 1.155v4.542c0 .642.56 1.154 1.22 1.154h2.14v1.28c0 .644.56 1.156 1.222 1.156h-2.132v1.278c0 .644-.56 1.156-1.22 1.156H11.51c-2.887 0-5.18-.23-6.617-.68-1.528-.474-2.024-1.256-2.024-2.502v-4.54h8.847v-1.17H2.868c-.66 0-1.22.512-1.22 1.155v6.33c0 .64.56 1.154 1.22 1.154h8.557v-1.28c0-.642.56-1.154 1.22-1.154h2.13v-1.28c0-.642.562-1.155 1.222-1.155h-2.142V9.2h2.142c.66 0 1.22-.514 1.22-1.156v-6.33c0-.643-.56-1.155-1.22-1.155h-1.968v3.79c0 1.638-.74 3.155-1.95 4.143-1.144.93-2.63 1.423-4.14 1.423h-5.45c-.662 0-1.223.514-1.223 1.156zM14.465 19.3c.548 0 .993.435.993.97 0 .536-.445.97-.993.97-.547 0-.993-.434-.993-.97 0-.535.446-.97.993-.97z"></path></svg>
                                Python
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-python"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="python-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="python-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-python" onclick="togglePython()" style="background-color: rgba(55, 118, 171, 0.1); border-color: #3776AB; color: #3776AB;">Start Server</button>
                            <button class="tool-btn" onclick="postCmd('createPythonProject')">➕ Create</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'python')">Browser</button>
                        </div>
                    </div>

                    <!-- NGROK -->
                    <div class="card" style="border-top: 3px solid #6a51d9;">
                        <div class="card-header">
                            <div class="card-title" style="color: #6a51d9;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#6a51d9"><path d="M16.99 3.01A10 10 0 1012 22a10 10 0 004.99-18.99zM12 20a8 8 0 110-16 8 8 0 010 16z"></path></svg>
                                Ngrok
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-ngrok"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="ngrok-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="ngrok-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-ngrok" onclick="toggleNgrok()" style="background-color: rgba(106, 81, 217, 0.1); border-color: #6a51d9; color: #6a51d9;">Start Tunnel</button>
                        </div>
                    </div>

                    <!-- ANDROID EMULATOR -->
                    <div class="card" style="border-top: 3px solid #3DDC84;">
                        <div class="card-header">
                            <div class="card-title" style="color: #3DDC84;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#3DDC84"><path d="M17.523 15.34c-.604 0-1.096-.484-1.096-1.08s.492-1.08 1.096-1.08c.605 0 1.098.484 1.098 1.08s-.493 1.08-1.098 1.08zm-11.04 0c-.604 0-1.096-.484-1.096-1.08s.492-1.08 1.096-1.08c.605 0 1.098.484 1.098 1.08s-.493 1.08-1.098 1.08zm11.396-5.45c.01-.132.016-.264.016-.396 0-3.35-2.733-6.066-6.082-6.066-3.35 0-6.083 2.716-6.083 6.066 0 .132.006.264.015.396h12.134zM12.013 0c4.32 0 7.824 3.477 7.824 7.766v1.127H4.188V7.766C4.188 3.477 7.692 0 12.013 0zm5.176 1.488l1.196-2.07a.406.406 0 0 0-.147-.557.417.417 0 0 0-.563.146l-1.22 2.11C15.013.435 13.565 0 12.013 0c-1.55 0-3 .435-4.444 1.116L6.35-.995a.418.418 0 0 0-.563-.146.406.406 0 0 0-.147.557l1.196 2.07C3.125 3.328 1 6.136 1 9.475v7.262c0 2.22 1.815 4.024 4.048 4.024h13.93c2.233 0 4.048-1.803 4.048-4.024V9.475c0-3.34-2.125-6.148-5.837-7.987z"></path></svg>
                                Android
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-android"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="android-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="android-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-android" onclick="openAndroidModal()" style="background-color: rgba(61, 220, 132, 0.1); border-color: #3DDC84; color: #3DDC84;">Open Manager</button>
                            <button class="tool-btn" style="color: var(--danger); border-color: var(--danger);" onclick="postCmd('stopAvd')">Force Stop</button>
                        </div>
                    </div>

                    <!-- PHP PUBLIC -->
                    <div class="card" style="border-top: 3px solid #777BB4;">
                        <div class="card-header">
                            <div class="card-title" style="color: #777BB4;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#777BB4"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.12 11.23h-2.1v2.18h-1.55v-2.18H8.84v-1.39l3.58-5.32h1.61v5.27h2.1v1.44zm-3.65-1.44V8.52h-.03L9.67 11.8h2.8z"></path></svg>
                                PHP Public
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-phpserver"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="phpserver-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="phpserver-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-phpserver" onclick="togglePhpServer()" style="background-color: rgba(119, 123, 180, 0.1); border-color: #777BB4; color: #777BB4;">Run Serve</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'phpserver')">Browser</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SECTION 2: CORE SERVICES -->
            <div class="grid-section">
                <div class="grid-section-title">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
                    XAMPP Core Services
                </div>
                <div class="services-grid">
                    <!-- APACHE -->
                    <div class="card" style="border-top: 3px solid #d16969;">
                        <div class="card-header">
                            <div class="card-title" style="color: #d16969;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#d16969"><path d="M19 15v3H5v-3h14m1-2H4c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h16c.55 0 1-.45 1-1v-4c0-.55-.45-1-1-1zm-1-7v3H5V6h14m1-2H4c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h16c.55 0 1-.45 1-1V5c0-.55-.45-1-1-1z"/></svg>
                                Apache
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-apache"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="apache-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="apache-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-apache" onclick="toggleService('apache')" style="background-color: rgba(209, 105, 105, 0.1); border-color: #d16969; color: #d16969;">Start</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'apache')">Admin</button>
                            <button class="tool-btn" onclick="postCmd('openConfig', 'apache')">Config</button>
                            <button class="tool-btn" onclick="postCmd('openLog', 'apache')">Logs</button>
                        </div>
                    </div>

                    <!-- MARIADB -->
                    <div class="card" style="border-top: 3px solid #00a8ff;">
                        <div class="card-header">
                            <div class="card-title" style="color: #00a8ff;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#00a8ff"><path d="M12 2C7.58 2 4 3.79 4 6v12c0 2.21 3.58 4 8 4s8-1.79 8-4V6c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.33 6 2s-2.13 2-6 2-6-.67-6-2 2.13-2 6-2zm0 16c-3.87 0-6-1.33-6-2v-2.24c1.46.78 3.59 1.24 6 1.24s4.54-.46 6-1.24V18c0 .67-2.13 2-6 2zm0-4.5c-3.87 0-6-1.33-6-2v-2.24c1.46.78 3.59 1.24 6 1.24s4.54-.46 6-1.24V13c0 .67-2.13 2-6 2z"/></svg>
                                MariaDB
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-mysql"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="mysql-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="mysql-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-mysql" onclick="toggleService('mysql')" style="background-color: rgba(0, 168, 255, 0.1); border-color: #00a8ff; color: #00a8ff;">Start</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'mysql')">Admin</button>
                            <button class="tool-btn" onclick="postCmd('openConfig', 'mysql')">Config</button>
                            <button class="tool-btn" onclick="postCmd('openLog', 'mysql')">Logs</button>
                            <button class="tool-btn" onclick="postCmd('openShell', 'mysql')">>_ Shell</button>
                        </div>
                    </div>

                    <!-- FILEZILLA -->
                    <div class="card" style="border-top: 3px solid #e67e22;">
                        <div class="card-header">
                            <div class="card-title" style="color: #e67e22;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#e67e22"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95C8.08 7.14 9.94 6 12 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11c1.56.1 2.78 1.41 2.78 2.96 0 1.65-1.35 3-3 3z"/></svg>
                                FileZilla
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-filezilla"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="filezilla-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="filezilla-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-filezilla" onclick="toggleService('filezilla')" style="background-color: rgba(230, 126, 34, 0.1); border-color: #e67e22; color: #e67e22;">Start</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'filezilla')">Admin</button>
                            <button class="tool-btn" onclick="postCmd('openConfig', 'filezilla')">Config</button>
                            <button class="tool-btn" onclick="postCmd('openLog', 'filezilla')">Logs</button>
                        </div>
                    </div>

                    <!-- MERCURY -->
                    <div class="card" style="border-top: 3px solid #9b59b6;">
                        <div class="card-header">
                            <div class="card-title" style="color: #9b59b6;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#9b59b6"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                                Mercury
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-mercury"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="mercury-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="mercury-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-mercury" onclick="toggleService('mercury')" style="background-color: rgba(155, 89, 182, 0.1); border-color: #9b59b6; color: #9b59b6;">Start</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'mercury')">Admin</button>
                            <button class="tool-btn" onclick="postCmd('openConfig', 'mercury')">Config</button>
                            <button class="tool-btn" onclick="postCmd('openLog', 'mercury')">Logs</button>
                        </div>
                    </div>

                    <!-- TOMCAT -->
                    <div class="card" style="border-top: 3px solid #f1c40f;">
                        <div class="card-header">
                            <div class="card-title" style="color: #f1c40f;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="#f1c40f"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-6h2v6zm0-8h-2V7h2v4z"/></svg>
                                Tomcat
                            </div>
                            <div class="card-status">
                                <span class="status-chip stopped" id="icon-tomcat"><span class="status-dot"></span></span>
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-label">PID</span>
                                <span class="stat-value" id="tomcat-pid">-</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Port</span>
                                <span class="stat-value" id="tomcat-port">-</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="start-btn" id="btn-tomcat" onclick="toggleService('tomcat')" style="background-color: rgba(241, 196, 15, 0.1); border-color: #f1c40f; color: #f1c40f;">Start</button>
                            <button class="tool-btn" onclick="postCmd('openAdmin', 'tomcat')">Admin</button>
                            <button class="tool-btn" onclick="postCmd('openConfig', 'tomcat')">Config</button>
                            <button class="tool-btn" onclick="postCmd('openLog', 'tomcat')">Logs</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="sql-manager">
            <div class="sql-header">
                <div style="display: flex; gap: 10px; align-items: center;">
                    <h3 style="color: #00a8ff;">Network Topology Simulator (via SQL)</h3>
                </div>
            </div>
            <div class="drop-zone" id="drop-zone" onclick="document.getElementById('file-input').click()">
                <p>Drag & Drop your .sql database file here.<br><small style="color: #00a8ff;">System will detect Tables and Foreign Keys as Cisco Topology (Nodes & Cables)</small></p>
                <input type="file" id="file-input" accept=".sql" style="display: none;">
            </div>
            
            <div class="editor-container" id="editor-container">
                <div class="editor-toolbar">
                    <span class="editor-title" id="file-name">query.sql</span>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button class="tool-btn" id="btn-loop" style="display: none; color: #4cd137; border-color: #4cd137;" onclick="toggleLoopAnimation()">📡 Auto Ping/Traffic</button>
                        <button class="tool-btn" id="btn-toggle-view" style="color: #f1c40f; border-color: #f1c40f;" onclick="toggleViewMode()">📊 Run Network Simulator</button>
                        <button class="tool-btn" onclick="closeEditor()">✖ Close</button>
                    </div>
                </div>
                
                <textarea id="sql-editor" spellcheck="false"></textarea>
                
                <div id="diagram-view">
                    <svg id="diagram-lines">
                        <defs>
                            <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                              <path d="M 0 0 L 10 5 L 0 10 z" fill="#00a8ff" />
                            </marker>
                        </defs>
                    </svg>
                    <div id="nodes-container"></div>
                </div>
            </div>
        </div>

        <div class="logs" id="log-window">
            <div><span class="log-time">[System]</span> <span class="log-info">Panel Ready. If Phone gets Forbidden (403), click "🌐 Fix Mobile 403" then Restart Apache.</span></div>
        </div>
    </div>

    <!-- MODALS -->
    
    <!-- Modal Android -->
    <div id="modal-android" class="modal-overlay">
        <div class="modal-content">
            <button class="modal-close" onclick="closeAndroidModal()">✖</button>
            <div class="modal-header">Android Studio Emulator Manager</div>
            <p style="font-size: 13px; color: var(--text-secondary); margin-bottom: 15px;">Automatically detects AVD from Android SDK and Windows Environment.</p>
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <button class="start-btn" onclick="postCmd('getAvds')">Refresh List</button>
                <button class="tool-btn" style="color: var(--danger); border-color: var(--danger);" onclick="postCmd('stopAvd')">⏹ Force Stop All</button>
            </div>
            <div id="avd-list" style="display: flex; flex-direction: column; gap: 8px; max-height: 300px; overflow-y: auto;">
                <span style="color:var(--text-secondary)">Loading AVDs...</span>
            </div>
        </div>
    </div>

    <!-- Modal Video -->
    <div id="modal-video" class="modal-overlay">
        <div class="modal-content">
            <button class="modal-close" onclick="closeVideoModal()">✖</button>
            <div class="modal-header">Video Track</div>

            <iframe 
                id="my-video"
                width="100%" 
                height="400"
                src="https://drive.google.com/file/d/1eLMIazoDioccAmORp1LIN2S_CzrlnV0_/preview"
                title="Video Track"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>

        </div>
    </div>

    <!-- Modal Help -->
    <div id="modal-help" class="modal-overlay">
        <div class="modal-content">
            <button class="modal-close" onclick="closeHelpModal()">✖</button>
            <div class="modal-header">Information User</div>
            <ul class="help-list">
            <li><img src ="https://github.com/Royhtml/Xampp-Meta-Panel/raw/main/resources/icon.png?raw=true" width="32" height="32" style="object-fit: contain; float: left; margin-right: 8px;" /> XAMPP Meta Panel</li>
                <li><b>Device Indicator:</b>
                    Click the "WA: Offline 🔴" button in the toolbar to automatically restart the connection without needing to scan QR if the laptop was just restarted.
                </li>
                <li><b>Laptop System Monitor (New):</b>
                    <ul>
                        <li>Type <code>!system</code> in WhatsApp to check your laptop CPU, remaining RAM, and Uptime.</li>
                        <li>Type <code>!preview</code> in WhatsApp to start an ultra-smooth fullscreen live feed of your laptop to your phone.</li>
                        <li>Type <code>!stop preview</code> to stop the live screen broadcast.</li>
                    </ul>
                </li>
                <li><b>WhatsApp Vercel Deploy:</b>
                    <ul>
                        <li>Set API: <code>!setvercel &lt;YOUR_VERCEL_API_KEY&gt;</code></li>
                        <li>Send <code>!deploy &lt;folder_name&gt;</code> bot will respond directly from the folder inside your htdocs directory.</li>
                    </ul>
                </li>
                <li><b>Xampp Server:</b>
                    <ul>
                        <li>Type <code>!start apache</code></li>
                        <li>Type <code>!stop apache</code></li>
                        <li>Type <code>!start mariadb</code></li>
                        <li>Type <code>!stop mariadb</code></li>
                    </ul>
                </li>
                <li><b>Alisa Mic:</b>
                    <ul>
                        <li>Start Apche Mic ("Alisa Start Apache")</li>
                        <li>Stop Apche Mic ("Alisa Stop Apache")</li>
                        <li>Start MariaDB Mic ("Alisa Start MariaDB")</li>
                        <li>Stop MariaDB Mic ("Alisa Stop MariaDB")</li>
                        <li>Open Panel ("Alisa Open Panel")</li>
                    </ul>
                </li>
                <li><b>WhatsApp Server Backend (Htdocs Folder):</b>
                    <ul>
                        <li>Type <code>!htdocs</code> to view all files/folders in htdocs</li>
                        <li>Type <code>!start php &lt;folder&gt;</code> / <code>!stop php</code></li>
                        <li>Type <code>!start laravel &lt;folder&gt;</code> / <code>!stop laravel</code></li>
                        <li>Type <code>!start flutter &lt;folder&gt;</code> / <code>!stop flutter</code></li>
                        <li>Type <code>!build flutter &lt;folder&gt;</code> to <b>automatically Compile APK. If >80MB, sends you a local server link.</b></li>
                        <li>Type <code>!start python &lt;folder&gt;</code> / <code>!stop python</code></li>
                    </ul>
                </li>
                <li><b>Desktop App Compiler (Nativefier):</b>
                    <ul>
                        <li>Type <code>!web2exe &lt;url&gt; &lt;app_name&gt;</code>. Website will automatically be converted to <code>.exe</code>, compressed into ZIP, and sent to WA while opening a *live* Terminal.</li>
                    </ul>
                </li>
                <li><b>Ngrok Tunneling (Public URL):</b>
                    <ul>
                        <li>Via Panel: Click 'Start Tunnel' in the Ngrok section</li>
                        <li>Via WhatsApp: Type <code>!start ngrok &lt;port&gt;</code> / <code>!stop ngrok</code></li>
                    </ul>
                </li>
                <li><b>MySQL Database via WhatsApp:</b>
                    <ul>
                        <li>Type <code>!query &lt;global_sql_command&gt;</code> to run SQL queries directly from WhatsApp</li>
                        <li>Type <code>!db &lt;db_name&gt; &lt;query&gt;</code> to run SQL scripts automatically</li>
                    </ul>
                </li>
                <li><b>Refresh Panel:</b>
                    <ul>
                        <li>Automatic Panel Refresh</li>
                    </ul>   
                </li>
                <li><b>Clean Xampp :</b>
                <ul>
                <li>Type !cleanup to Automatically remove all XAMPP services and eliminate shutdown bugs</li>
                <li>Panel is automatically clean from any Viruses/Bugs</li>
                </ul>
                </li>
                <li><b>Tim Pengembang & Ideator:</b>
                    <div class="developer-grid">
                        <div class="developer-card">
                            <img class="developer-img" src="${dwibaktiUri}" alt="Dwi Bakti">
                            <div class="developer-name">Dwi Bakti N Dev/Roy</div>
                            <div class="developer-role">Developer</div>
                        </div>
                        <div class="developer-card">
                            <img class="developer-img" src="${pungkasUri}" alt="Pungkas Budiono">
                            <div class="developer-name">Pungkas Budiono</div>
                            <div class="developer-role">Ideator</div>
                        </div>
                        <div class="developer-card">
                            <img class="developer-img" src="${fujihadiUri}" alt="Fuji Hadi Hartanto">
                            <div class="developer-name">Fuji Hadi Hartanto</div>
                            <div class="developer-role">Ideator</div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <style>
    .modal-overlay{
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.75);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    padding: 15px;
}

.modal-overlay.show{
    display: flex;
}
.modal-content{
    background: #111;
    color: white;
    width: 95%;
    max-width: 500px;     
    max-height: 80vh;    
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

.modal-header{
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    background: #1e1e1e;
    border-bottom: 1px solid #333;
}

.modal-close{
    position: absolute;
    margin-top: 10px;
    margin-left: 10px;
    background: red;
    color: white;
    border: none;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    cursor: pointer;
    font-size: 16px;
}


.help-list{
    padding: 15px;
    margin: 0;
    overflow-y: auto;   
    max-height: 65vh;
}

.help-list li{
    margin-bottom: 10px;
    line-height: 1.5;
}

#my-video{
    width: 100%;
    max-height: 65vh;
    background: black;
}
    </style>

    <script>
        const vscode = acquireVsCodeApi();

        window.addEventListener('load', () => {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.getVoices();
            }
            vscode.postMessage({ command: 'panelReady' });
            setTimeout(() => {
                const splash = document.getElementById('splash-screen');
                if (splash) {
                    splash.classList.add('fade-out');
                }
            }, 700);
        });

        const bgMusic = document.getElementById('bg-music');
        const btnMusic = document.getElementById('btn-music');
        
        function toggleMusic() {
            if (bgMusic.paused) {
                bgMusic.play();
                btnMusic.innerText = 'Pause Music';
                btnMusic.style.color = '#e74c3c';
                btnMusic.style.borderColor = '#e74c3c';
            } else {
                bgMusic.pause();
                btnMusic.innerText = 'Play Music';
                btnMusic.style.color = '#9b59b6';
                btnMusic.style.borderColor = '#9b59b6';
            }
        }

        let currentEnableTTS = true;
        let currentShowSplashScreen = true;

        function updateConfigUI(enableTTS, showSplashScreen) {
            currentEnableTTS = enableTTS;
            currentShowSplashScreen = showSplashScreen;
            
            const btnTts = document.getElementById('btn-toggle-tts');
            if (btnTts) {
                btnTts.innerText = enableTTS ? 'TTS: Enabled 🔊' : 'TTS: Disabled 🔇';
                btnTts.style.color = enableTTS ? '#2ecc71' : '#e74c3c';
            }
            
            const btnSplash = document.getElementById('btn-toggle-splash');
            if (btnSplash) {
                btnSplash.innerText = showSplashScreen ? 'Splash: Enabled' : 'Splash: Disabled';
                btnSplash.style.color = showSplashScreen ? '#2ecc71' : '#e74c3c';
            }
        }

        function toggleTTS() {
            vscode.postMessage({ command: 'updateConfig', key: 'enableTTS', value: !currentEnableTTS });
        }

        function toggleSplashScreenSetting() {
            vscode.postMessage({ command: 'updateConfig', key: 'showSplashScreen', value: !currentShowSplashScreen });
        }

        let recognition = null;
        let isMicActive = false;

        function speakAlisa(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                const voices = window.speechSynthesis.getVoices();
                let selectedVoice = voices.find(v => v.lang.toLowerCase().includes('ja') || v.name.toLowerCase().includes('japanese') || v.name.toLowerCase().includes('nanami') || v.name.toLowerCase().includes('haruka') || v.name.toLowerCase().includes('ayumi') || v.name.toLowerCase().includes('midori') || v.name.toLowerCase().includes('keiko'));
                if (!selectedVoice) {
                    selectedVoice = voices.find(v => v.name.toLowerCase().includes('zira') || v.name.toLowerCase().includes('hazel') || v.name.toLowerCase().includes('susan') || v.name.toLowerCase().includes('female') || v.lang.toLowerCase().startsWith('en'));
                }
                if (selectedVoice) {
                    utterance.voice = selectedVoice;
                }
                utterance.pitch = 1.35;
                utterance.rate = 0.85;
                window.speechSynthesis.speak(utterance);
            }
        }

        function toggleServiceByName(service, targetAction) {
            const btn = document.getElementById('btn-' + service);
            if (!btn) return;
            const isRunning = btn.classList.contains('running');

            if (targetAction === 'start' && !isRunning) {
                toggleService(service);
            } else if (targetAction === 'stop' && isRunning) {
                toggleService(service);
            }
        }

        function toggleMic() {
            vscode.postMessage({ command: 'toggleGlobalMic' });
        }

        function toggleDropdown(event) {
            event.stopPropagation();
            const dropdown = document.getElementById('my-dropdown');
            dropdown.classList.toggle('show');
        }

        window.addEventListener('click', function(event) {
            const dropdown = document.getElementById('my-dropdown');
            if (dropdown && dropdown.classList.contains('show') && !event.target.closest('.dropdown-menu')) {
                dropdown.classList.remove('show');
            }
        });

        const modalVideo = document.getElementById('modal-video');
        const myVideo = document.getElementById('my-video');
        function openVideoModal() { modalVideo.style.display = 'flex'; }
        function closeVideoModal() { modalVideo.style.display = 'none'; myVideo.pause(); }

        const modalHelp = document.getElementById('modal-help');
        function openHelpModal() { modalHelp.style.display = 'flex'; }
        function closeHelpModal() { modalHelp.style.display = 'none'; }
        
        function openAndroidModal() { 
            document.getElementById('modal-android').style.display = 'flex'; 
            postCmd('getAvds'); 
        }
        function closeAndroidModal() { document.getElementById('modal-android').style.display = 'none'; }

        function addLog(message, type = 'log-info') {
            const logWindow = document.getElementById('log-window');
            const time = new Date().toLocaleTimeString('en-GB');
            const lines = message.split('\\n').filter(line => line.trim() !== '');
            lines.forEach(line => {
                logWindow.innerHTML += \`<div><span class="log-time">[\${time}]</span> <span class="\${type}">\${line}</span></div>\`;
            });
            logWindow.scrollTop = logWindow.scrollHeight;
        }

        function postCmd(cmd, service) { vscode.postMessage({ command: cmd, service: service }); }

        function toggleLaravel() {
            const btn = document.getElementById('btn-laravel');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'laravel' });
                addLog('Stopping Laravel server...');
            } else {
                postCmd('startLaravel', 'laravel');
            }
        }

        function togglePhpServer() {
            const btn = document.getElementById('btn-phpserver');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'phpserver' });
                addLog('Stopping PHP server...');
            } else {
                postCmd('startPhpServer', 'phpserver');
            }
        }

        function toggleNode() {
            const btn = document.getElementById('btn-node');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'node' });
                addLog('Stopping Node.js server...');
            } else {
                postCmd('startNode', 'node');
            }
        }

        function togglePython() {
            const btn = document.getElementById('btn-python');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'python' });
                addLog('Stopping Python server...');
            } else {
                postCmd('startPython', 'python');
            }
        }
        
        function toggleFlutter() {
            const btn = document.getElementById('btn-flutter');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'flutter' });
                addLog('Stopping Flutter Application...');
            } else {
                postCmd('runFlutterProject', 'flutter');
            }
        }

        function toggleNgrok() {
            const btn = document.getElementById('btn-ngrok');
            if (btn.classList.contains('running')) {
                vscode.postMessage({ command: 'stopService', service: 'ngrok' });
                addLog('Stopping Ngrok...');
            } else {
                postCmd('startNgrok', 'ngrok');
            }
        }

        function getServicePorts(service) {
            switch(service) {
                case 'apache': return '80, 443';
                case 'mysql': return '3306';
                case 'filezilla': return '21, 14147';
                case 'mercury': return '25, 79, 105...';
                case 'tomcat': return '8080, 8005';
                case 'laravel': return '8000';
                case 'phpserver': return '8081';
                case 'flutter': return '8080';
                case 'node': return '3000';
                case 'python': return '8082';
                case 'ngrok': return 'Forwarding';
                default: return '-';
            }
        }

        function toggleService(service) {
            const btn = document.getElementById('btn-' + service);
            const isRunning = btn.innerText === 'Stop';

            if (isRunning) {
                vscode.postMessage({ command: 'stopService', service: service });
            } else {
                btn.innerText = 'Stop'; btn.classList.add('running');
                document.getElementById('icon-' + service).classList.remove('stopped');
                document.getElementById('icon-' + service).classList.add('running');
                
                document.getElementById(service + '-pid').innerText = Math.floor(Math.random() * 10000);
                document.getElementById(service + '-port').innerText = getServicePorts(service);
                vscode.postMessage({ command: 'startService', service: service });
            }
        }

        function setStatus(service, status) {
            const btn = document.getElementById('btn-' + service);
            const icon = document.getElementById('icon-' + service);
            if (status === 'stopped') {
                if (service === 'laravel' || service === 'phpserver') btn.innerText = 'Run Serve';
                else if (service === 'node' || service === 'python') btn.innerText = 'Start Server';
                else if (service === 'flutter') btn.innerText = 'Run App';
                else if (service === 'ngrok') btn.innerText = 'Start Tunnel';
                else if (service === 'android') return; 
                else btn.innerText = 'Start';
                
                if(btn) btn.classList.remove('running');
                if (icon) { icon.classList.remove('running'); icon.classList.add('stopped'); }
                
                if (document.getElementById(service + '-pid')) document.getElementById(service + '-pid').innerText = '-';
                if (document.getElementById(service + '-port')) document.getElementById(service + '-port').innerText = '-';
            } else if (status === 'running') {
                if(btn) { btn.innerText = 'Stop'; btn.classList.add('running'); }
                if (icon) { icon.classList.remove('stopped'); icon.classList.add('running'); }
                
                if (document.getElementById(service + '-pid')) document.getElementById(service + '-pid').innerText = Math.floor(Math.random() * 10000) + ' (OS)';
                if (document.getElementById(service + '-port')) document.getElementById(service + '-port').innerText = getServicePorts(service);
            }
        }

        window.addEventListener('message', event => {
            const msg = event.data;
            if (msg.command === 'log') {
                addLog(msg.text, msg.type);
            }
            else if (msg.command === 'status') {
                setStatus(msg.service, msg.status);
            }
            else if (msg.command === 'globalMicStatus') {
                isMicActive = msg.active;
                const btnMic = document.getElementById('btn-mic');
                const btnDropdownMic = document.getElementById('btn-dropdown-mic');
                if (isMicActive) {
                    if (btnMic) {
                        btnMic.innerHTML = 'Alisa: On';
                        btnMic.style.color = '#2ecc71';
                        btnMic.style.borderColor = '#2ecc71';
                    }
                    if (btnDropdownMic) {
                        btnDropdownMic.innerHTML = 'Alisa: On';
                        btnDropdownMic.style.color = '#2ecc71';
                    }
                    addLog("> Alisa Voice Assistant Active (Global). Speak 'alisa start apache', 'alisa stop apache', etc.", "log-info");
                } else {
                    if (btnMic) {
                        btnMic.innerHTML = 'Alisa Off';
                        btnMic.style.color = '#1abc9c';
                        btnMic.style.borderColor = '#1abc9c';
                    }
                    if (btnDropdownMic) {
                        btnDropdownMic.innerHTML = 'Alisa Off';
                        btnDropdownMic.style.color = '#1abc9c';
                    }
                    addLog("> Alisa Voice Assistant Deactivated.", "log-info");
                }
            }
            else if (msg.command === 'showQR') {
                document.getElementById('wa-qr-container').style.display = 'block';
                document.getElementById('wa-qr-img').src = msg.qrUrl;
            }
            else if (msg.command === 'hideQR') {
                document.getElementById('wa-qr-container').style.display = 'none';
                document.getElementById('wa-qr-img').src = '';
            }
            else if (msg.command === 'wa_status') {
                const btnWa = document.getElementById('btn-wa-status');
                if (msg.status === 'connected') {
                    btnWa.innerHTML = 'WA: ' + msg.number + ' 🟢';
                    btnWa.style.color = '#2ecc71';
                    btnWa.style.borderColor = '#2ecc71';
                } else if (msg.status === 'disconnected') {
                    btnWa.innerHTML = 'WA: Offline 🔴';
                    btnWa.style.color = '#e74c3c';
                    btnWa.style.borderColor = '#e74c3c';
                } else if (msg.status === 'loading') {
                    btnWa.innerHTML = 'WA: Connecting... ⏳';
                    btnWa.style.color = '#f1c40f';
                    btnWa.style.borderColor = '#f1c40f';
                }
            }
            else if (msg.command === 'avdList') {
                const listDiv = document.getElementById('avd-list');
                listDiv.innerHTML = '';
                if (msg.avds.length === 0) {
                    listDiv.innerHTML = '<span style="color:var(--text-secondary)">No AVDs detected on your OS.</span>';
                } else {
                    msg.avds.forEach(avd => {
                        listDiv.innerHTML += \`
                            <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-color); padding: 10px; border-radius: 4px; border: 1px solid var(--border-color);">
                                <span style="font-weight: 600;">📱 \${avd}</span>
                                <button class="start-btn" onclick="postCmd('startAvd', '\${avd}')" style="color: white;">Start</button>
                            </div>
                        \`;
                    });
                }
            }
            else if (msg.command === 'syncConfig') {
                updateConfigUI(msg.enableTTS, msg.showSplashScreen);
            }
        });

        // ==========================================
        // NETWORK TOPOLOGY SIMULATOR (SQL TO CISCO)
        // ==========================================
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');
        const editorContainer = document.getElementById('editor-container');
        const sqlEditor = document.getElementById('sql-editor');
        const diagramView = document.getElementById('diagram-view');
        const fileNameDisplay = document.getElementById('file-name');
        const btnToggleView = document.getElementById('btn-toggle-view');
        const btnLoop = document.getElementById('btn-loop');
        
        let isDiagramMode = false;
        
        let classesData = [
            { id: 'Router_Core', x: 200, y: 30, attrs: ['+ IP: 192.168.1.1', '+ MAC: AA:BB:CC', '+ Port: Gigabit0/0'], methods: ['📡 Ping Packet', '📦 Send Traffic'] },
            { id: 'Switch_Dist', x: 200, y: 220, attrs: ['+ IP: Layer 2', '+ MAC: DD:EE:FF', '+ VLAN: 10'], methods: ['📡 Ping Packet', '🔄 Broadcast ARP'] },
            { id: 'PC_Client', x: 20, y: 400, attrs: ['+ IP: 192.168.1.10', '+ Gateway: 192.168.1.1', '+ Status: Online'], methods: ['📡 Ping Packet', '📦 Request Data'] },
            { id: 'Server_DB', x: 380, y: 400, attrs: ['+ IP: 192.168.1.100', '+ Gateway: 192.168.1.1', '+ Service: MySQL'], methods: ['📡 Ping Packet', '🔄 Sync Config'] }
        ];
        let relations = [
            { from: 'Router_Core', to: 'Switch_Dist' },
            { from: 'Switch_Dist', to: 'PC_Client' },
            { from: 'Switch_Dist', to: 'Server_DB' }
        ];

        function parseSQL(sql) {
            let tables = [];
            let rels = [];
            
            sql = sql.replace(/\\/\\*[\\s\\S]*?\\*\\/|--.*$/gm, '');

            let tableBlocks = sql.split(/CREATE\\s+TABLE/i);
            tableBlocks.shift(); 

            let x = 40, y = 40;
            tableBlocks.forEach(block => {
                let tableNameMatch = block.match(/(?:IF\\s+NOT\\s+EXISTS\\s+)?[\\x60'"]?(\\w+)[\\x60'"]?\\s*\\(/i);
                if(!tableNameMatch) return;
                let tName = tableNameMatch[1];

                let colMatches = block.matchAll(/^\\s*[\\x60'"]?(\\w+)[\\x60'"]?\\s+([A-Za-z0-9_]+)/gm);
                let attrs = [];
                for(let m of colMatches) {
                    let colName = m[1]; let type = m[2];
                    if(!['PRIMARY','KEY','CONSTRAINT','FOREIGN'].includes(colName.toUpperCase())) {
                        attrs.push('+ ' + colName + ': ' + type);
                    }
                }

                let fkMatches = block.matchAll(/FOREIGN\\s+KEY[^\\)]*\\)\\s*REFERENCES\\s*[\\x60'"]?(\\w+)[\\x60'"]?/gi);
                for(let f of fkMatches) {
                    rels.push({ from: tName, to: f[1] });
                }

                tables.push({
                    id: tName,
                    x: x, y: y,
                    attrs: attrs.slice(0, 5),
                    methods: ['📡 Ping (ICMP)', '📦 Send Data (TCP)', '🔄 Sync Update']
                });

                x += 240;
                if(x > 600) { x = 40; y += 220; }
            });

            return { tables, relations: rels };
        }

        function loadSqlFile(file) {
            if (!file.name.endsWith('.sql')) {
                addLog('Error: Please upload a file with .sql format', 'log-error'); return;
            }
            const reader = new FileReader();
            reader.onload = (e) => {
                const sqlText = e.target.result;
                fileNameDisplay.innerText = file.name;
                sqlEditor.value = sqlText;
                
                const parsed = parseSQL(sqlText);
                if(parsed.tables.length > 0) {
                    classesData = parsed.tables;
                    relations = parsed.relations;
                    addLog(\`> Successfully detected \${parsed.tables.length} table entities.\`, 'log-success');
                }

                dropZone.style.display = 'none';
                editorContainer.style.display = 'flex';
                
                isDiagramMode = false;
                sqlEditor.style.display = 'block';
                diagramView.style.display = 'none';
                btnToggleView.innerText = 'Run Network Simulator';
                btnLoop.style.display = 'none'; 
                if(isLooping) toggleLoopAnimation(); 
                
                initDiagramData(); 
            };
            reader.readAsText(file);
        }

        fileInput.addEventListener('change', e => { if (e.target.files.length > 0) loadSqlFile(e.target.files[0]); });
        dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
        dropZone.addEventListener('drop', e => {
            e.preventDefault(); dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) loadSqlFile(e.dataTransfer.files[0]);
        });

        function closeEditor() {
            editorContainer.style.display = 'none'; dropZone.style.display = 'flex';
            sqlEditor.value = ''; fileInput.value = '';
            if(isLooping) toggleLoopAnimation();
        }

        function toggleViewMode() {
            isDiagramMode = !isDiagramMode;
            if(isDiagramMode) {
                sqlEditor.style.display = 'none';
                diagramView.style.display = 'block';
                btnToggleView.innerText = 'View Sql File';
                btnLoop.style.display = 'inline-block';
                drawLines(); 
                addLog("> Network Topology Simulator Active.", "log-success");
            } else {
                sqlEditor.style.display = 'block';
                diagramView.style.display = 'none';
                btnToggleView.innerText = 'Run Network Simulator';
                btnLoop.style.display = 'none'; 
                if(isLooping) toggleLoopAnimation(); 
            }
        }

        let isLooping = false;
        let loopTimeout = null;

        function toggleLoopAnimation() {
            isLooping = !isLooping;
            if (isLooping) {
                btnLoop.innerText = '⏹ Stop Traffic';
                btnLoop.style.color = 'var(--danger)';
                btnLoop.style.borderColor = 'var(--danger)';
                addLog('> Auto Network Traffic Activated', 'log-info');
                runRandomAnimation();
            } else {
                btnLoop.innerText = '📡 Auto Ping/Traffic';
                btnLoop.style.color = '#4cd137';
                btnLoop.style.borderColor = '#4cd137';
                addLog('> Auto Network Traffic Stopped', 'log-info');
                clearTimeout(loopTimeout);
            }
        }

        function runRandomAnimation() {
            if (!isLooping || !isDiagramMode) return;
            const classesWithMethods = classesData.filter(c => c.methods && c.methods.length > 0);
            if(classesWithMethods.length === 0) return;

            const randomClass = classesWithMethods[Math.floor(Math.random() * classesWithMethods.length)];
            const randomMethod = randomClass.methods[Math.floor(Math.random() * randomClass.methods.length)];

            triggerPacket(randomClass.id, randomMethod);
            loopTimeout = setTimeout(runRandomAnimation, 2000);
        }

        const container = document.getElementById('nodes-container');
        const svgLines = document.getElementById('diagram-lines');
        let draggedNode = null;
        let startX, startY, initialX, initialY;

        function initDiagramData() {
            container.innerHTML = '';
            classesData.forEach(cls => {
                const el = document.createElement('div');
                el.className = 'uml-class'; el.id = 'node-' + cls.id;
                el.style.left = cls.x + 'px'; el.style.top = cls.y + 'px';
                
                let attrsHTML = (cls.attrs || []).map(a => \`<div>\${a}</div>\`).join('');
                let methodsHTML = (cls.methods || []).map(m => \`<div class="uml-method-item" onclick="triggerPacket('\${cls.id}', '\${m}')">\${m}</div>\`).join('');
                
                el.innerHTML = \`<div class="uml-header">\${cls.id}</div><div class="uml-attrs">\${attrsHTML || '&nbsp;'}</div><div class="uml-methods">\${methodsHTML || '&nbsp;'}</div>\`;
                el.addEventListener('mousedown', e => {
                    draggedNode = el; startX = e.clientX; startY = e.clientY;
                    initialX = el.offsetLeft; initialY = el.offsetTop;
                    el.style.zIndex = 100;
                });
                container.appendChild(el);
            });
            drawLines();
        }

        document.addEventListener('mousemove', e => {
            if (!draggedNode) return;
            const dx = e.clientX - startX; const dy = e.clientY - startY;
            draggedNode.style.left = (initialX + dx) + 'px';
            draggedNode.style.top = (initialY + dy) + 'px';
            requestAnimationFrame(drawLines);
        });

        document.addEventListener('mouseup', () => {
            if (draggedNode) { draggedNode.style.zIndex = 10; draggedNode = null; }
        });

        function drawLines() {
            svgLines.innerHTML = \`<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#00a8ff" /></marker></defs>\`;
            relations.forEach(rel => {
                const elFrom = document.getElementById('node-' + rel.from);
                const elTo = document.getElementById('node-' + rel.to);
                if(!elFrom || !elTo) return;

                const fromX = elFrom.offsetLeft + (elFrom.offsetWidth / 2);
                const fromY = elFrom.offsetTop + (elFrom.offsetHeight / 2);
                const toX = elTo.offsetLeft + (elTo.offsetWidth / 2);
                const toY = elTo.offsetTop + (elTo.offsetHeight / 2);

                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', fromX); line.setAttribute('y1', fromY);
                line.setAttribute('x2', toX); line.setAttribute('y2', toY);
                line.setAttribute('stroke', '#00a8ff'); line.setAttribute('stroke-width', '2');
                line.setAttribute('stroke-dasharray', '5,5');
                line.setAttribute('marker-end', 'url(#arrow)');
                svgLines.appendChild(line);
            });
        }

        function triggerPacket(sourceId, actionName) {
            let connectedRels = relations.filter(r => r.from === sourceId || r.to === sourceId);
            let targetId = '';
            
            if (connectedRels.length > 0) {
                let rel = connectedRels[Math.floor(Math.random() * connectedRels.length)];
                targetId = (rel.from === sourceId) ? rel.to : rel.from;
            } else {
                let otherNodes = classesData.filter(c => c.id !== sourceId);
                if(otherNodes.length > 0) targetId = otherNodes[Math.floor(Math.random() * otherNodes.length)].id;
            }

            if (targetId && targetId !== sourceId) {
                let color = actionName.includes('Ping') ? '#4cd137' : (actionName.includes('Data') ? '#00a8ff' : '#f1c40f');
                animateNetworkPacket(sourceId, targetId, actionName, color);
            }
        }

        function animateNetworkPacket(fromId, toId, actionName, color) {
            const elFrom = document.getElementById('node-' + fromId);
            const elTo = document.getElementById('node-' + toId);
            if(!elFrom || !elTo) return;

            const fromX = elFrom.offsetLeft + (elFrom.offsetWidth / 2);
            const fromY = elFrom.offsetTop + (elFrom.offsetHeight / 2);
            const toX = elTo.offsetLeft + (elTo.offsetWidth / 2);
            const toY = elTo.offsetTop + (elTo.offsetHeight / 2);

            const particle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            particle.setAttribute('r', '8'); particle.setAttribute('fill', color);
            particle.setAttribute('filter', 'drop-shadow(0px 0px 4px ' + color + ')');
            svgLines.appendChild(particle);

            elFrom.style.borderColor = color; elFrom.style.boxShadow = '0 0 10px ' + color;
            let start = null; const duration = 1200; 

            function step(timestamp) {
                if (!start) start = timestamp;
                const progress = (timestamp - start) / duration;
                
                if (progress < 1) {
                    particle.setAttribute('cx', fromX + (toX - fromX) * progress);
                    particle.setAttribute('cy', fromY + (toY - fromY) * progress);
                    window.requestAnimationFrame(step);
                } else {
                    particle.remove();
                    elFrom.style.borderColor = 'var(--class-border)'; elFrom.style.boxShadow = 'none';
                    elTo.style.borderColor = color; elTo.style.boxShadow = '0 0 15px ' + color;
                    setTimeout(() => { 
                        if(elTo) { elTo.style.boxShadow = ''; elTo.style.borderColor = 'var(--class-border)'; }
                    }, 500);
                }
            }
            window.requestAnimationFrame(step);
        }

        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(drawLines, 100);
        });
    </script>
</body>
</html>`;
}
//# sourceMappingURL=extension.js.map