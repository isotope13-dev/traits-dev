// PKCS#1 controls: ASN.1 DigestInfo prefixes are public format constants, and
// the EMSA-PKCS1-v1_5 padding builder assembles them with an indexed
// String.fromCharCode loop. That pairing is byte assembly, not an obfuscated
// string-table decoder.
const digestPrefixes = [];
digestPrefixes[1] = [0x30, 0x20, 0x30, 0x0c, 0x06, 0x08, 0x2a, 0x86, 0x48, 0x86, 0xf7, 0x0d, 0x02, 0x05, 0x05, 0x00, 0x04, 0x10];
digestPrefixes[2] = [0x30, 0x21, 0x30, 0x09, 0x06, 0x05, 0x2b, 0x0e, 0x03, 0x02, 0x1a, 0x05, 0x00, 0x04, 0x14];

export function buildDigestPrefix(algo) {
  let out = '';
  const table = digestPrefixes[algo];
  for (let i = 0; i < table.length; i++) {
    out += String.fromCharCode(table[i]);
  }
  return out;
}
