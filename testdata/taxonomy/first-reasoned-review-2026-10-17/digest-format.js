const escaped0 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped1 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped2 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped3 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escapedLabel = "\x64\x69\x67\x65\x73\x74\x20\x66\x6f\x72\x6d\x61\x74";
const K = [0x428a2f98,0x71374491,0xb5c0fbcf];
function formatDigest(bytes) {
  return bytes.map(b => String.fromCharCode(97 + b % 26)).join("");
}
