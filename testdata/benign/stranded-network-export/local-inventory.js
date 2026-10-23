'use strict'
const os = require('os')
const pkg = require('../package.json')

function getMacAddress () {
  const interfaces = os.networkInterfaces()
  const macAddresses = []

  for (const interfaceName in interfaces) {
    const networkInterface = interfaces[interfaceName]

    networkInterface.forEach((details) => {
      // Check for IPv4 and that the address is not internal (i.e., not 127.0.0.1)
      if (details.family === 'IPv4' && !details.internal) {
        macAddresses.push(details.mac)
      }
    })
  }
  return macAddresses
}

module.exports = getMacAddress;
