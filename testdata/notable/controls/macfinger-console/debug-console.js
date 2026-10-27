const { BrowserWindow } = require('electron');
const win = new BrowserWindow({ show: false });
win.webContents.on('console-message', (event, level, message) => {
  const data = JSON.parse(message);
  if (data.seed) renderPreview(data.seed);
});
console.log('preview:' + JSON.stringify({ seed: 1234 }));
