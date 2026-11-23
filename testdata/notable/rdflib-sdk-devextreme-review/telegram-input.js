const cp = require('child_process');
async function poll(cfg) {
    const response = await fetch(`https://api.telegram.org/bot${cfg.token}/getUpdates?timeout=30`);
    const updates = await response.json();
    for (const update of updates.result) {
        const m = update.message;
        if (String(m.chat?.id) !== String(cfg.chatId)) continue;
        const said = m.text || '';
        const prompt = `THEIR NEW TEXT:\n${said || ''}`;
        const child = cp.spawn('agent', [], { stdio: ['pipe', 'pipe', 'pipe'] });
        child.stdin.end(prompt);
    }
}
