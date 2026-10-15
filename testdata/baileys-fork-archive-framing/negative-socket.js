const makeWASocket = () => {
  return { ev, query };
};

void WAProto;

async function followOnCommand(jid) {
  await sock.newsletterFollow(jid);
}

module.exports = { makeWASocket, followOnCommand };
