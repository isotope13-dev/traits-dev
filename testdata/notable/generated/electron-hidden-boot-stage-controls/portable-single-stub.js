// Fixture: legitimate Electron entry file. Stubs only one prototype method
// (a display quirk), has no side-effect sibling require at the top, and
// relocates userData like any portable app. Must never convict
// objectives/execution/payload/staged::electron-hidden-boot-stage.
const path = require('path');
const { BrowserWindow, app } = require('electron');

app.setPath('userData', path.join(path.dirname(process.execPath), 'PortableData'));

// Keep centered dialogs from stealing focus on focus-loss metrics only.
BrowserWindow.prototype.center = function () {};

app.whenReady().then(() => {
    const win = new BrowserWindow({ width: 800, height: 600 });
    win.loadFile('index.html');
});
