const ws = new WebSocketClient(endpoint, config);
const sendAsync = promisify(ws.send);
const key = Curve.generateKeyPair();
crypto.generateKeyPairSync('rsa', {modulusLength:2048});
aesEncryptCTR(plaintext, key, iv);
