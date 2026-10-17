const escaped0 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped1 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped2 = "\x70\x61\x79\x6c\x6f\x61\x64";
const escaped3 = "\x70\x61\x79\x6c\x6f\x61\x64";
const encoded = "\x70\x61\x79\x6c\x6f\x61\x64\x20\x74\x65\x78\x74";
function decode(codes) {
  const chars = [];
  for (let i = 0; i < codes.length; i++) chars.push(String.fromCharCode(codes[i]));
  return chars.join("");
}
