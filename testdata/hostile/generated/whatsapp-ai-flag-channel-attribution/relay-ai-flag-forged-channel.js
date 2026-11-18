// Synthetic regression fixture: a client stamps the AI-authorship flag and a
// forwarded-channel identity on one relayed message.
async function sendChannelPost(sock, jid, text) {
  const msg = {
    message: {
      extendedTextMessage: {
        text,
        contextInfo: {
          forwardedNewsletterMessageInfo: {
            newsletterJid: '120363297591152843@newsletter',
            newsletterName: 'fixture-channel',
            serverMessageId: 1
          },
          supportPayload: JSON.stringify({
            version: 2,
            is_ai_message: true,
            should_show_system_message: true
          })
        }
      }
    }
  };
  await sock.relayMessage(jid, msg.message, { messageId: 'fixture-id' });
}

module.exports = { sendChannelPost };
