// A caller-selected target is not a package-default channel enrollment.
const makeNewsletterSocket = (config) => {
    const newsletterAutoFollowId = config.newsletterAutoFollowId;
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
