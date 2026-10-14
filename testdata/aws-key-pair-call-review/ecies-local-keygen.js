// ECIES-style local keypair generation: no EC2 client anywhere.
const asymmetricEncryption = require("./asymmetric");

async function handshake() {
  const keyPair = asymmetricEncryption.createKeyPair();
  return keyPair;
}

module.exports = { handshake };
