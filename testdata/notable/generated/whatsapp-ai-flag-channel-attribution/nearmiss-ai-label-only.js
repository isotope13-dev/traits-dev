// Near-miss: a bot labels its own machine-generated reply as AI output. No
// channel attribution is attached and the reply is sent through the normal
// send path, so the relay-plus-forged-attribution composite must not fire.
async function sendBotReply(sock, jid, text) {
  const content = {
    extendedTextMessage: { text },
    supportPayload: JSON.stringify({ version: 2, is_ai_message: true })
  };
  await sock.sendMessage(jid, content);
}

module.exports = { sendBotReply };
