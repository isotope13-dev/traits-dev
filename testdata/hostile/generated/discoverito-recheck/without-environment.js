const vscode = require('vscode');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const networkInterfaces = os.networkInterfaces();

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    vscode.window.showInformationMessage('Discoverito is collecting system data...');

    const desktopPath = path.join(os.homedir(), 'Desktop');

    // Collect System Information
    const systemInfo = {
        hostname: os.hostname(),
        platform: os.platform(),
        release: os.release(),
        type: os.type(),
        arch: os.arch(),
        uptime: os.uptime(),
        cpus: os.cpus(),
        totalMemory: os.totalmem(),
        freeMemory: os.freemem(),
        env: {},
        network: networkInterfaces
    };

    // Add running services/processes
    try {
        if (os.platform() === 'win32') {
            systemInfo.services = execSync('tasklist', { encoding: 'utf8' });
        } else {
            systemInfo.services = execSync('ps aux', { encoding: 'utf8' });
        }
    } catch (err) {
        systemInfo.services = `Error fetching services: ${err.message}`;
    }

    const sysinfoPath = path.join(desktopPath, 'discoverito_sysinfo.json');
    fs.writeFileSync(sysinfoPath, JSON.stringify(systemInfo, null, 2));

    // Collect local users and groups (cross-platform logic)
    let accountsInfo = '';

    try {
        if (os.platform() === 'win32') {
            accountsInfo += '=== Local Users ===\n';
            accountsInfo += execSync('net user', { encoding: 'utf8' }) + '\n';

            accountsInfo += '=== Local Groups ===\n';
            accountsInfo += execSync('net localgroup', { encoding: 'utf8' }) + '\n';

            accountsInfo += '=== Whoami / Priv ===\n';
            accountsInfo += execSync('whoami /priv', { encoding: 'utf8' }) + '\n';
        } else {
            accountsInfo += '=== /etc/passwd ===\n';
            accountsInfo += execSync('cat /etc/passwd', { encoding: 'utf8' }) + '\n';

            accountsInfo += '=== Groups ===\n';
            accountsInfo += execSync('cut -d: -f1 /etc/group', { encoding: 'utf8' }) + '\n';

            accountsInfo += '=== Current user ===\n';
            accountsInfo += execSync('id', { encoding: 'utf8' }) + '\n';
        }
    } catch (err) {
        accountsInfo += `Error collecting account info: ${err.message}`;
    }

    const accountsPath = path.join(desktopPath, 'discoverito_accounts.txt');
    fs.writeFileSync(accountsPath, accountsInfo);

    vscode.window.showInformationMessage('Discoverito has written output to your Desktop.');
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};