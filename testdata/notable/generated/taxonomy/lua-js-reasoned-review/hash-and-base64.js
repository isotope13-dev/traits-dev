async function aeskey(input) {
  const digest = await sha256(input);
  return subtle.importKey('raw', digest, {name: 'AES-GCM'}, false, ['encrypt', 'decrypt']);
}
function decode(input) { return Buffer.from(input, "base64").toString('utf8'); }
