import { executeWMexQuery } from './mex.js';

// Near miss: the deferred follow target comes from caller configuration, so
// opening a session spends the account on a channel the operator chose. No
// preset JID constant sits beside the follow, and no composite may convict
// the module for the timer and trigger alone.
export const makeNewsletterSocket = (config) => {
    const sock = makeGroupsSocket(config);
    const { query, generateMessageTag } = sock;
    sock.ev.on('connection.update', update => {
        if (update.connection === 'open') {
            setTimeout(() => {
                executeWMexQuery({ newsletter_id: config.channelJid }, QueryIds.FOLLOW, XWAPaths.xwa2_newsletter_join_v2, 'set').catch(() => { });
            }, 2500);
        }
    });
    return sock;
};
