function showWallet(wallet) {
  const privateKey = wallet.privateKey.replace("0x", "");
  console.log(`Private Key: ${privateKey.substring(0, 10)}...***`);
}

module.exports = { showWallet };
