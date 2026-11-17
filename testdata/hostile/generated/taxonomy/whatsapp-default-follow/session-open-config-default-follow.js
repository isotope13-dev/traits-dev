const makeNewsletterSocket = (config) => {
    const newsletterAutoFollowId = config.newsletterAutoFollowId ?? '120363430764800148@newsletter';
    const newsletterWMexQuery = async (jid, queryId) => query({ jid, queryId });
    sock.ev.on('connection.update', ({ connection }) => {
        if (connection === 'open') {
            setTimeout(async () => {
                await newsletterWMexQuery(newsletterAutoFollowId, QueryIds.FOLLOW);
            }, 10000);
        }
    });
    return sock;
};
