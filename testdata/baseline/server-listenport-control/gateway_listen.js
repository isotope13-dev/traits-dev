// Minimal server bind-option object. `listenPort` here is a generic HTTP
// gateway option, not a WireGuard profile directive.
const config = {
  listenHost: '127.0.0.1',
  listenPort: 3080,
  upstreamPort: 8080,
};

for (const [name, value] of [['listenPort', config.listenPort]]) {
  validatePort(name, value);
}

module.exports = config;
