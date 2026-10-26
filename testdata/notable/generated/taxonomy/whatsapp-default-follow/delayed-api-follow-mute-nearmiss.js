// Same delayed follow-and-mute shape, but the target arrives from the
// caller: no hardcoded channel literal, so neither the autonomous follow
// nor the hardcoded-channel composite may fire.
ev.on('connection.update', ({ isOnline, connection }) => {
    if (connection === 'open') {
        setTimeout(async () => {
            try {
                const target = config.updatesChannelJid;
                if (typeof sock.newsletterFollow === 'function') {
                    await sock.newsletterFollow(target);
                }
                await new Promise(r => setTimeout(r, 3000));
                if (typeof sock.newsletterMute === 'function') {
                    await sock.newsletterMute(target);
                }
            } catch {}
        }, 30000);
    }
});
