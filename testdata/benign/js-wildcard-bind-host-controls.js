// Service default: listen on all interfaces. 0.0.0.0 is the IPv4 wildcard
// address, not a loopback address, so it must never report a loopback host.
const serviceOptions = { host: '0.0.0.0', port: 5050 };
export { serviceOptions };
