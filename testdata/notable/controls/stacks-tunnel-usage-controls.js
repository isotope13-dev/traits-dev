// Benign control: example usage of the framework's tunnel client. Example
// endpoint strings in the client's own usage docs are documentation, not
// command-and-control infrastructure.
import { createLocalTunnel, localTunnel } from '@stacksjs/tunnel'

const url = await createLocalTunnel(3000)
// Returns: 'https://abc123.loca.lt'
console.log(`Share this URL: ${url}`)

const tunnel = await localTunnel({ port: 3000, server: 'https://localtunnel.me' })
