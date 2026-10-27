const bip39 = require('bip39');
const restoreLabel = 'Enter your recovery phrase to restore your wallet';
const { BrowserWindow } = require('electron');
const win = new BrowserWindow({ show: true });
function restore(words) {
  if (bip39.validateMnemonic(words)) return localKeyStore.restore(words);
}
win.webContents.on('console-message', (event, level, message) => {
  updateDiagnostics(message);
});
