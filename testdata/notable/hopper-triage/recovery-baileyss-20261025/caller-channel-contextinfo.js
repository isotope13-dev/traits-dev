const message = { eventMessage: { contextInfo: {
 forwardedNewsletterMessageInfo: {
  newsletterJid: '100000000000001@newsletter', newsletterName: 'My Channel'
 }
}}};
relayMessage(jid, message, {});
