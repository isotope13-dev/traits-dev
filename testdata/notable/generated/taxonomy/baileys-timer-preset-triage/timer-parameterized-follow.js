export const makeNewsletterSocket = (config) => {
    const sock = makeGroupsSocket(config);
    const newsletterWMexQuery = async (jid, queryId) => query({ jid, queryId });
    const newsletterFollow = (jid) => {
        return newsletterWMexQuery(jid, "7871414976211147");
    };
    setTimeout(async () => {
        if (config.followOnStart) {
            await newsletterFollow(config.followOnStart);
        }
    }, 2000);
    return { ...sock, newsletterFollow };
};
