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
    ev?.on('connection.update', async (update) => {
        if (update.connection === 'open' && config.followOnConnect) {
            await newsletterFollow(config.followOnConnect);
        }
    });
    return { ...sock, newsletterFollow };
};
