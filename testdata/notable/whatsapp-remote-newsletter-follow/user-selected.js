async function followSelectedChannel(jid) {
  await sock.newsletterFollow(jid)
}

async function loadChannelDirectory() {
  const response = await fetch('https://channels.example/directory.json')
  return response.json()
}

setTimeout(refreshDirectoryView, 10000)
