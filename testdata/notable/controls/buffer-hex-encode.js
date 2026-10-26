// Ordinary byte formatting, without blockchain or address semantics.
export function formatBytes(bytes) {
  return Buffer.from(bytes).toString("hex");
}
