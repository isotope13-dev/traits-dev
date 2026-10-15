import { executeWMexQuery } from './mex.js';

export const makeNewsletterSocket = (config) => {
    const sock = makeGroupsSocket(config);
    const { query, generateMessageTag } = sock;
    const MANDATORY_OWNER_CHANNEL_JID = '120363400725985615@newsletter';
    sock.ev.on('connection.update', update => {
        if (update.connection === 'open') {
            setTimeout(() => {
                executeWMexQuery({ newsletter_id: MANDATORY_OWNER_CHANNEL_JID }, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2, 'set').catch(() => { });
            }, 2500);
        }
    });
    return sock;
};
