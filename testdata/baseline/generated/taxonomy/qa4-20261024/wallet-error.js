function reportFailure(error, reply) {
  reply({ success: false, error: 'Failed to get current password: ' + error.message });
}
function replyToUnlockedWalletUI(reply, wallet) {
  reply({ success: true, password: wallet.getCurrentPassword() });
}
