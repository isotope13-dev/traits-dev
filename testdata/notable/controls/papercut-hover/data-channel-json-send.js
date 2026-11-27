function sendChat(channel, message) {
  channel.send(JSON.stringify({message}));
}
