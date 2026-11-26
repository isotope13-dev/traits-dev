// Promise scheduler: the message handler only flushes a fixed queue.
// No code is generated here; the handler stays a plain flush callback.
function useMessageChannel(flush) {
  const channel = new MessageChannel();
  channel.port1.onmessage = flush;
  return channel;
}

module.exports = { useMessageChannel };
