const bytes = new Uint8Array([1,2,3]);
const text = new TextDecoder().decode(bytes.map(x => x ^ 0x87));
console.log(text);
