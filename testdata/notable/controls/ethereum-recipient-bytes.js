// Offline recipient-address conversion; no lookup, transmission, or execution.
export function recipientBytes(transaction) {
  return Buffer.from(transaction.to.slice(2), "hex");
}
