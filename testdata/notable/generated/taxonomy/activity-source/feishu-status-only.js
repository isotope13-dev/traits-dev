const eventNames = ['READ_FILE_ERROR', 'WRITE_FILE_ERROR'];
function reportStatus(record) {
  const payload = record.payload;
  const message = {msg_type: 'post', content: payload};
  return JSON.stringify(message);
}
