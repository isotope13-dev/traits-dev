// Same retry shape as the channelId graft, but the target arrives from the
// caller: no hardcoded channel constant, so neither the autonomous follow
// nor the hardcoded-channelId composite may fire.
const autoFollowChannel = (channelJid) => {
    const retryDelays = [10e3, 30e3, 60e3];
    let attempt = 0;
    let followed = false;
    const tryFollow = async () => {
        if (followed) return;
        try {
            const result = await newsletterWMexQuery(channelJid, QueryIds.FOLLOW);
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
