async function sendUserApprovedTransaction(wallet, connection, transaction) {
  const signed = await wallet.signTransaction(transaction);
  return connection.sendRawTransaction(signed.serialize());
}

console.log(wallet.publicKey.toBase58());
