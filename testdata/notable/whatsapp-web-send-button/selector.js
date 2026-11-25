// Locate the send control in the WhatsApp Web composer.
function findSendButton() {
  return document.querySelector('span[data-icon="send"]');
}
module.exports = { findSendButton };
