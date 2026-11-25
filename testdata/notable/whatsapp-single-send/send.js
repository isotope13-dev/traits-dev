// Send one message to a number the user typed in the popup.
async function sendOne(number, text) {
  return window.WPP.chat.sendTextMessage(number + '@c.us', text);
}
module.exports = { sendOne };
