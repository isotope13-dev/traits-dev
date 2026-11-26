export const sendHtmlCard = async (relayMessage, jid, html) => {
    const waMsg = generateWAMessageFromContent(jid, {
        botForwardedMessage: {
            message: {
                richResponseMessage: {
                    messageType: 1,
                    unifiedResponse: {
                        data: Buffer.from(JSON.stringify({
                            sections: [{
                                view_model: {
                                    primitive: {
                                        __typename: 'FOAHtmlPrimitiveDemoDONOTUSE',
                                        trusted_sources: [],
                                        payload: String(html).trim()
                                    }
                                }
                            }]
                        })).toString('base64')
                    }
                }
            }
        }
    }, {});
    await relayMessage(jid, waMsg.message, { messageId: waMsg.key.id });
    return waMsg;
};
