const message = { imageMessage: { contextInfo: {
 forwardingScore: 99999,
 forwardedNewsletterMessageInfo: {
  newsletterJid: '100000000000001@newsletter', newsletterName: 'WhatsApp'
 }
}}};
relayMessage(jid, message, {});
