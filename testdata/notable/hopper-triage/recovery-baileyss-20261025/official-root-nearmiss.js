message.messageContextInfo = { forwardingScore: 99999 };
message.forwardedNewsletterMessageInfo = {
 newsletterJid: '100000000000001@newsletter', newsletterName: 'WhatsApp'
};
relayMessage(jid, message, {});
